#!/bin/bash
# =============================================================================
# deploy.sh — Despliegue de nomi-license en Ubuntu 24.04
# Servidor: 164.92.67.198 | Dominio: api.nomi-mx.com
# =============================================================================

set -euo pipefail

# ── Colores para output ───────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

step()  { echo -e "\n${BLUE}[STEP]${NC} $*"; }
ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
die()   { echo -e "${RED}[ERROR]${NC} $*" >&2; exit 1; }

# ── Verificar root ────────────────────────────────────────────────────────────
[[ $EUID -eq 0 ]] || die "Este script debe ejecutarse como root. Usa: sudo bash deploy.sh"

# ── Generar ADMIN_TOKEN seguro ────────────────────────────────────────────────
ADMIN_TOKEN=$(python3 -c "import secrets; print(secrets.token_hex(32))")
[[ -n "$ADMIN_TOKEN" ]] || die "No se pudo generar ADMIN_TOKEN"
ok "ADMIN_TOKEN generado"

# =============================================================================
# 1. SISTEMA BASE
# =============================================================================
step "1/9 — Actualizando sistema e instalando dependencias..."

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get upgrade -y
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    nginx \
    certbot \
    python3-certbot-nginx \
    curl

ok "Sistema base listo"

# =============================================================================
# 2. CLONAR REPOSITORIO
# =============================================================================
step "2/9 — Clonando repositorio..."

REPO_DIR="/opt/agencia-v3"
APP_DIR="$REPO_DIR/license-server"

if [[ -d "$REPO_DIR" ]]; then
    warn "El directorio $REPO_DIR ya existe. Haciendo git pull..."
    git -C "$REPO_DIR" pull || warn "git pull falló, continuando con el estado actual"
else
    git clone https://github.com/SantiM-wronghacker/agencia-v3.git "$REPO_DIR"
fi

[[ -d "$APP_DIR" ]] || die "No se encontró el directorio $APP_DIR tras clonar el repo"
cd "$APP_DIR"
ok "Repositorio en $APP_DIR"

# =============================================================================
# 3. ENTORNO PYTHON
# =============================================================================
step "3/9 — Creando entorno virtual Python..."

python3 -m venv "$APP_DIR/venv"
source "$APP_DIR/venv/bin/activate"

if [[ -f "$APP_DIR/requirements.txt" ]]; then
    ok "requirements.txt encontrado, instalando dependencias..."
    pip install --upgrade pip
    pip install -r "$APP_DIR/requirements.txt"
else
    warn "requirements.txt no encontrado, creando uno con dependencias base..."
    cat > "$APP_DIR/requirements.txt" << 'EOF'
fastapi
uvicorn[standard]
python-dotenv
resend
EOF
    pip install --upgrade pip
    pip install -r "$APP_DIR/requirements.txt"
fi

deactivate
ok "Entorno virtual listo en $APP_DIR/venv"

# =============================================================================
# 4. ARCHIVO .env
# =============================================================================
step "4/9 — Creando archivo .env..."

mkdir -p "$APP_DIR/data"

cat > "$APP_DIR/.env" << EOF
RESEND_API_KEY=re_E9GrDRVs_wxAuRK6wCy5K7QBnqtEBiTD2
FROM_EMAIL=hola@nomi-mx.com
ADMIN_TOKEN=$ADMIN_TOKEN
DOWNLOAD_LINK=https://nomi-mx.com/download
DB_PATH=$APP_DIR/data/license.db
EOF

chmod 600 "$APP_DIR/.env"
ok ".env creado con permisos 600"

# =============================================================================
# 5. SYSTEMD SERVICE
# =============================================================================
step "5/9 — Configurando servicio systemd..."

cat > /etc/systemd/system/nomi-license.service << EOF
[Unit]
Description=Nomi License Server
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8080
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=nomi-license

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable nomi-license
systemctl start nomi-license

# Esperar a que arranque
sleep 3

if systemctl is-active --quiet nomi-license; then
    ok "Servicio nomi-license activo"
else
    warn "El servicio no arrancó inmediatamente, verificando logs..."
    journalctl -u nomi-license -n 30 --no-pager || true
    die "El servicio nomi-license falló al arrancar. Revisa los logs de arriba."
fi

# =============================================================================
# 6. NGINX
# =============================================================================
step "6/9 — Configurando Nginx..."

cat > /etc/nginx/sites-available/nomi-api << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name api.nomi-mx.com;

    # Seguridad básica
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass         http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_set_header   Upgrade           $http_upgrade;
        proxy_set_header   Connection        "upgrade";
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        client_max_body_size 10M;
    }

    # Health check sin proxy (responde directo)
    location /nginx-health {
        access_log off;
        return 200 "ok\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Activar site
ln -sf /etc/nginx/sites-available/nomi-api /etc/nginx/sites-enabled/nomi-api

# Remover default si existe
rm -f /etc/nginx/sites-enabled/default

# Verificar config de nginx
nginx -t || die "Configuración de Nginx inválida"
systemctl reload nginx
ok "Nginx configurado y recargado"

# =============================================================================
# 7. FIREWALL
# =============================================================================
step "7/9 — Configurando firewall UFW..."

ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

ok "Firewall activo — SSH y Nginx Full permitidos"

# =============================================================================
# 8. SSL con Certbot
# =============================================================================
step "8/9 — Obteniendo certificado SSL con Certbot..."

# Verificar que el dominio resuelva a este servidor antes de pedir cert
SERVER_IP=$(curl -s https://ipinfo.io/ip 2>/dev/null || hostname -I | awk '{print $1}')
DOMAIN_IP=$(getent hosts api.nomi-mx.com | awk '{print $1}' 2>/dev/null || echo "")

if [[ -z "$DOMAIN_IP" ]]; then
    warn "No se pudo resolver api.nomi-mx.com. Asegúrate de que el DNS A record apunte a $SERVER_IP"
    warn "Saltando Certbot por ahora. Ejecútalo manualmente cuando el DNS esté propagado:"
    warn "  certbot --nginx -d api.nomi-mx.com --non-interactive --agree-tos -m hola@nomi-mx.com"
elif [[ "$DOMAIN_IP" != "$SERVER_IP" ]]; then
    warn "El DNS de api.nomi-mx.com resuelve a $DOMAIN_IP, pero este servidor es $SERVER_IP"
    warn "Saltando Certbot. Ejecútalo manualmente una vez que el DNS propague:"
    warn "  certbot --nginx -d api.nomi-mx.com --non-interactive --agree-tos -m hola@nomi-mx.com"
else
    certbot --nginx \
        -d api.nomi-mx.com \
        --non-interactive \
        --agree-tos \
        -m hola@nomi-mx.com && ok "Certificado SSL instalado" \
        || warn "Certbot falló. Ejecuta manualmente cuando el DNS esté listo."
fi

# =============================================================================
# 9. VERIFICACIÓN FINAL
# =============================================================================
step "9/9 — Verificación final..."

echo ""
echo "--- Estado del servicio ---"
systemctl status nomi-license --no-pager -l || true

echo ""
echo "--- Prueba HTTP local ---"
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8080/ 2>/dev/null || echo "000")
if [[ "$HTTP_RESPONSE" =~ ^(200|307|404|422)$ ]]; then
    ok "Servidor responde en http://127.0.0.1:8080 (HTTP $HTTP_RESPONSE)"
else
    warn "El servidor respondió HTTP $HTTP_RESPONSE en http://127.0.0.1:8080"
    warn "Logs del servicio:"
    journalctl -u nomi-license -n 20 --no-pager || true
fi

# =============================================================================
# RESUMEN FINAL
# =============================================================================
echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}           DESPLIEGUE COMPLETADO — NOMI LICENSE SERVER      ${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "  ${YELLOW}ADMIN_TOKEN (guarda esto de forma segura):${NC}"
echo -e "  ${RED}$ADMIN_TOKEN${NC}"
echo ""
echo -e "  ${BLUE}URLs del servidor:${NC}"
echo -e "    HTTP:  http://api.nomi-mx.com"
echo -e "    HTTPS: https://api.nomi-mx.com  (una vez propagado el DNS + SSL)"
echo -e "    Docs:  https://api.nomi-mx.com/docs"
echo -e "    Local: http://127.0.0.1:8080/docs"
echo ""
echo -e "  ${BLUE}Comandos útiles:${NC}"
echo -e "    Ver logs:      journalctl -u nomi-license -f"
echo -e "    Reiniciar:     systemctl restart nomi-license"
echo -e "    Estado:        systemctl status nomi-license"
echo -e "    Reload nginx:  systemctl reload nginx"
echo -e "    Renovar SSL:   certbot renew --dry-run"
echo ""
echo -e "  ${BLUE}Archivo .env:${NC} $APP_DIR/.env"
echo -e "  ${BLUE}Base de datos:${NC} $APP_DIR/data/license.db"
echo -e "  ${BLUE}Logs nginx:${NC}    /var/log/nginx/error.log"
echo -e "${GREEN}============================================================${NC}"
echo ""
