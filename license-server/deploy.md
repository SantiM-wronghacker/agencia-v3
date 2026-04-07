# Deploy — License Server

## DigitalOcean Droplet $6/mes

### 1. Crear el Droplet

- Imagen: **Ubuntu 24.04 LTS**
- Plan: **Basic — $6/mes** (1 vCPU, 1 GB RAM)
- Región: la más cercana a tus clientes
- Autenticación: SSH key (recomendado)

### 2. Acceso inicial

```bash
ssh root@<IP_DEL_DROPLET>
```

### 3. Instalar dependencias del sistema

```bash
apt update && apt upgrade -y
apt install -y python3.12 python3.12-venv python3-pip git ufw
```

### 4. Clonar el repositorio

```bash
cd /opt
git clone https://github.com/<tu-usuario>/agencia-v3.git
cd agencia-v3/license-server
```

### 5. Crear entorno virtual e instalar

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 6. Configurar variables de entorno

```bash
cp .env.example .env
nano .env
# Edita ADMIN_TOKEN con un valor seguro (usa: openssl rand -hex 32)
```

### 7. Crear directorio de datos

```bash
mkdir -p /opt/agencia-v3/license-server/data
```

---

## Systemd (arranque automático tras reboot)

### Crear el servicio

```bash
nano /etc/systemd/system/license-server.service
```

Contenido:

```ini
[Unit]
Description=License Server
After=network.target

[Service]
User=root
WorkingDirectory=/opt/agencia-v3/license-server
EnvironmentFile=/opt/agencia-v3/license-server/.env
ExecStart=/opt/agencia-v3/license-server/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Activar y arrancar

```bash
systemctl daemon-reload
systemctl enable license-server
systemctl start license-server
systemctl status license-server
```

### Ver logs en tiempo real

```bash
journalctl -u license-server -f
```

---

## Screen (alternativa simple sin systemd)

```bash
# Instalar screen si no está
apt install -y screen

# Arrancar en sesión separada
screen -S license-server
cd /opt/agencia-v3/license-server
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8080

# Detach: Ctrl+A, D
# Re-attach: screen -r license-server
```

---

## Firewall con UFW

```bash
# Habilitar UFW
ufw default deny incoming
ufw default allow outgoing

# Solo SSH y puerto 8080
ufw allow ssh
ufw allow 8080/tcp

# Activar
ufw enable
ufw status
```

> Si en el futuro pones Nginx como proxy inverso (puerto 80/443):
> ```bash
> ufw allow 'Nginx Full'
> ufw delete allow 8080/tcp
> ```

---

## Actualizar el servidor

```bash
cd /opt/agencia-v3
git pull origin main

# Reinstalar dependencias si cambiaron
cd license-server
source .venv/bin/activate
pip install -r requirements.txt

# Reiniciar el servicio
systemctl restart license-server
systemctl status license-server
```

---

## Dashboard de administración

Accede desde el navegador:

```
http://<IP_DEL_DROPLET>:8080/dashboard?token=<ADMIN_TOKEN>
```

El token se inyecta en el HTML para que el dashboard pueda hacer llamadas autenticadas al API.

---

## Verificar que funciona

```bash
# Health check (docs automáticos de FastAPI)
curl http://localhost:8080/docs

# Heartbeat de prueba
curl -X POST http://localhost:8080/heartbeat \
  -H "Content-Type: application/json" \
  -d '{"client_id":"test","license_key":"test","package_type":"basic","timestamp":"2026-01-01T00:00:00"}'

# Listar clientes (admin)
curl http://localhost:8080/clients \
  -H "X-Admin-Token: <ADMIN_TOKEN>"
```
