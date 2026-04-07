"""
AREA: HERRAMIENTAS
DESCRIPCION: Dashboard web v2.0 de la Agencia Santi. CRUD completo de agentes,
             panel de progreso de expansion, gestion de categorias, ejecucion de
             agentes, proyectos, Clawbot y logs en vivo. localhost:8080.
TECNOLOGIA: http.server (stdlib), HTML/CSS/JS embebido
"""

import os
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import web_bridge as web
    WEB = web.WEB
except ImportError:
    WEB = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUERTO   = 8080
API_URL  = "http://localhost:8000"
API_KEY  = "santi-agencia-2026"

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agencia Santi v2 — Torre de Control</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',sans-serif;background:#0d1117;color:#e6edf3}
header{background:#161b22;border-bottom:1px solid #30363d;padding:12px 24px;display:flex;justify-content:space-between;align-items:center}
header h1{font-size:1.05rem;color:#58a6ff}
.badge{background:#238636;color:#fff;padding:3px 10px;border-radius:20px;font-size:.73rem}
.badge.warn{background:#9e6a03}.badge.err{background:#da3633}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;padding:16px 20px}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px}
.card h3{font-size:.73rem;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px}
.card .num{font-size:1.7rem;font-weight:700;color:#58a6ff}
.card .sub{font-size:.73rem;color:#8b949e;margin-top:3px}
.tabs{display:flex;gap:2px;padding:0 20px;border-bottom:1px solid #30363d;overflow-x:auto;flex-wrap:nowrap}
.tab{padding:9px 14px;cursor:pointer;font-size:.8rem;border-bottom:2px solid transparent;color:#8b949e;white-space:nowrap}
.tab.active{color:#58a6ff;border-color:#58a6ff}
.tab:hover{color:#e6edf3}
.panel{display:none;padding:20px}.panel.active{display:block}
table{width:100%;border-collapse:collapse;font-size:.8rem}
th{background:#161b22;color:#8b949e;padding:8px 12px;text-align:left;border-bottom:1px solid #30363d;position:sticky;top:0}
td{padding:7px 12px;border-bottom:1px solid #21262d}
tr:hover td{background:#1c2128}
.dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:5px}
.dot.ok{background:#3fb950}.dot.warn{background:#d29922}.dot.err{background:#f85149}
.area-tag{background:#1f3a5f;color:#79c0ff;padding:2px 7px;border-radius:4px;font-size:.72rem}
input,select,textarea{background:#0d1117;border:1px solid #30363d;color:#e6edf3;padding:7px 10px;border-radius:6px;font-size:.83rem;width:100%}
button{background:#238636;color:#fff;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-size:.83rem}
button:hover{background:#2ea043}
button.sec{background:#21262d;border:1px solid #30363d}
button.sec:hover{background:#30363d}
button.danger{background:#da3633}
button.danger:hover{background:#b62324}
.row{display:flex;gap:10px;margin-bottom:10px;align-items:flex-end}
.field{flex:1}.field label{display:block;font-size:.75rem;color:#8b949e;margin-bottom:4px}
#output-box{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:14px;min-height:100px;font-family:monospace;font-size:.8rem;white-space:pre-wrap;margin-top:14px;color:#3fb950;max-height:380px;overflow-y:auto}
#log-box{background:#0d1117;border:1px solid #30363d;border-radius:6px;padding:12px;height:400px;overflow-y:auto;font-family:monospace;font-size:.76rem}
.log-line{margin-bottom:2px}
.log-line.ok{color:#3fb950}.log-line.warn{color:#d29922}.log-line.err{color:#f85149}.log-line.info{color:#8b949e}
.spinner{display:inline-block;width:14px;height:14px;border:2px solid #30363d;border-top-color:#58a6ff;border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
footer{text-align:center;color:#30363d;font-size:.73rem;padding:16px}
.chat-box{display:flex;flex-direction:column;height:440px}
.chat-msgs{flex:1;overflow-y:auto;padding:12px;background:#0d1117;border:1px solid #30363d;border-radius:6px;margin-bottom:10px}
.msg{margin-bottom:10px}.msg .quien{font-size:.73rem;color:#8b949e;margin-bottom:3px}
.msg .texto{background:#1c2128;padding:8px 12px;border-radius:6px;font-size:.83rem;white-space:pre-wrap}
.msg.user .texto{background:#1f3a5f}
.chat-input{display:flex;gap:8px}.chat-input input{flex:1}
/* Modal */
.modal-bg{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.65);display:none;justify-content:center;align-items:center;z-index:1000}
.modal-bg.show{display:flex}
.modal{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:24px;width:520px;max-width:90vw;max-height:85vh;overflow-y:auto}
.modal h2{font-size:1rem;color:#58a6ff;margin-bottom:16px}
.modal .field{margin-bottom:12px}
.modal .btns{display:flex;gap:10px;justify-content:flex-end;margin-top:16px}
/* Progress bar */
.progress-bar{background:#21262d;border-radius:8px;height:28px;overflow:hidden;position:relative;margin:12px 0}
.progress-fill{background:linear-gradient(90deg,#238636,#3fb950);height:100%;border-radius:8px;transition:width .5s}
.progress-label{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:.8rem;font-weight:600;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.5)}
/* Category pills */
.cat-pill{display:inline-block;padding:5px 12px;border-radius:20px;font-size:.78rem;cursor:pointer;margin:3px;border:1px solid #30363d;background:#21262d;color:#8b949e;transition:all .2s}
.cat-pill:hover,.cat-pill.active{background:#1f3a5f;color:#79c0ff;border-color:#58a6ff}
/* Agent cards */
.agent-card{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:14px;transition:border-color .2s}
.agent-card:hover{border-color:#58a6ff}
.agent-card .name{font-family:monospace;font-size:.82rem;color:#79c0ff;margin-bottom:4px}
.agent-card .desc{font-size:.76rem;color:#8b949e;margin-bottom:8px;line-height:1.4}
.agent-card .meta{display:flex;justify-content:space-between;align-items:center}
.agent-card .actions{display:flex;gap:6px}
.agent-card .actions button{padding:4px 10px;font-size:.72rem}
/* Toast */
.toast{position:fixed;bottom:20px;right:20px;background:#238636;color:#fff;padding:12px 20px;border-radius:8px;font-size:.85rem;z-index:2000;display:none;box-shadow:0 4px 12px rgba(0,0,0,.4)}
.toast.error{background:#da3633}
.toast.show{display:block;animation:fadeIn .3s}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
/* Expansion cat cards */
.exp-cat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:14px}
.exp-cat h4{color:#58a6ff;font-size:.9rem;margin-bottom:8px}
.exp-cat .count{font-size:1.4rem;font-weight:700;color:#d29922}
/* Hamburger Menu */
.hamburger{background:none;border:1px solid #30363d;color:#e6edf3;font-size:1.4rem;cursor:pointer;padding:6px 10px;border-radius:6px;line-height:1;display:flex;align-items:center;gap:6px}
.hamburger:hover{background:#21262d;border-color:#58a6ff}
.hamburger .label{font-size:.78rem;color:#8b949e}
.menu-wrap{position:relative}
.dropdown-menu{position:absolute;top:100%;right:0;background:#161b22;border:1px solid #30363d;border-radius:10px;min-width:260px;z-index:999;display:none;box-shadow:0 8px 24px rgba(0,0,0,.5);margin-top:6px;overflow:hidden}
.dropdown-menu.open{display:block;animation:menuIn .2s ease}
@keyframes menuIn{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}
.menu-item{display:flex;align-items:center;gap:10px;padding:11px 16px;cursor:pointer;font-size:.83rem;color:#e6edf3;border-bottom:1px solid #21262d;transition:background .15s}
.menu-item:last-child{border-bottom:none}
.menu-item:hover{background:#1c2128}
.menu-item.active{color:#58a6ff;background:#0d1117}
.menu-item .icon{font-size:1rem;width:22px;text-align:center}
.menu-item .desc{font-size:.7rem;color:#8b949e;margin-top:1px}
.menu-divider{border-top:1px solid #30363d;margin:4px 0}
/* Tarea box */
.tarea-box{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:20px;margin-bottom:20px}
.tarea-box h2{font-size:1rem;color:#58a6ff;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.tarea-input{display:flex;gap:8px;margin-top:10px}
.tarea-input textarea{flex:1;min-height:70px;resize:vertical}
.tarea-history{margin-top:16px;max-height:300px;overflow-y:auto}
.tarea-entry{background:#0d1117;border:1px solid #21262d;border-radius:6px;padding:10px;margin-bottom:8px;font-size:.8rem}
.tarea-entry .tarea-meta{font-size:.7rem;color:#8b949e;margin-bottom:4px;display:flex;justify-content:space-between}
.tarea-entry .tarea-status{padding:2px 8px;border-radius:10px;font-size:.68rem;color:#fff}
.tarea-entry .tarea-status.pending{background:#9e6a03}
.tarea-entry .tarea-status.running{background:#1f6feb}
.tarea-entry .tarea-status.done{background:#238636}
.tarea-entry .tarea-status.error{background:#da3633}
</style>
</head>
<body>

<header>
  <h1>Agencia Santi v2 — Torre de Control</h1>
  <div style="display:flex;gap:10px;align-items:center">
    <span id="api-status" class="badge warn">Conectando...</span>
    <span style="font-size:.73rem;color:#8b949e" id="last-update"></span>
    <div class="menu-wrap">
      <button class="hamburger" onclick="toggleMenu()">
        <span id="menu-icon">&#9776;</span>
        <span class="label" id="menu-section">Inicio</span>
      </button>
      <div class="dropdown-menu" id="dropdown-menu">
        <div class="menu-item active" onclick="menuNav('tareas',event)"><span class="icon">&#9997;</span><div><div>Solicitar Tarea</div><div class="desc">Pide algo a los agentes</div></div></div>
        <div class="menu-divider"></div>
        <div class="menu-item" onclick="menuNav('agentes',event)"><span class="icon">&#129302;</span><div><div>Agentes</div><div class="desc">Ver, crear, editar agentes</div></div></div>
        <div class="menu-item" onclick="menuNav('expansion',event)"><span class="icon">&#128200;</span><div><div>Expansion</div><div class="desc">Progreso del plan 206 micros</div></div></div>
        <div class="menu-item" onclick="menuNav('proyectos',event)"><span class="icon">&#128188;</span><div><div>Proyectos</div><div class="desc">Clientes y negocios</div></div></div>
        <div class="menu-item" onclick="menuNav('clawbot',event)"><span class="icon">&#128172;</span><div><div>Clawbot</div><div class="desc">Chat con IA</div></div></div>
        <div class="menu-divider"></div>
        <div class="menu-item" onclick="menuNav('ejecutar',event)"><span class="icon">&#9654;</span><div><div>Ejecutar</div><div class="desc">Correr un agente</div></div></div>
        <div class="menu-item" onclick="menuNav('credenciales',event)"><span class="icon">&#128273;</span><div><div>Credenciales</div><div class="desc">APIs, hosting, redes sociales</div></div></div>
        <div class="menu-item" onclick="menuNav('admin',event)"><span class="icon">&#9881;</span><div><div>Admin</div><div class="desc">Modo fabrica, categorias</div></div></div>
        <div class="menu-item" onclick="menuNav('logs',event)"><span class="icon">&#128220;</span><div><div>Logs</div><div class="desc">Registro en vivo</div></div></div>
      </div>
    </div>
  </div>
</header>

<!-- STATS -->
<div class="grid" id="stats-grid">
  <div class="card"><h3>Agentes</h3><div class="num" id="s-total">—</div><div class="sub">registrados</div></div>
  <div class="card"><h3>Saludables</h3><div class="num" id="s-ok">—</div><div class="sub">estado OK</div></div>
  <div class="card"><h3>Categorias</h3><div class="num" id="s-areas">—</div><div class="sub">activas</div></div>
  <div class="card"><h3>Microagentes</h3><div class="num" id="s-exp">—</div><div class="sub">creados</div></div>
  <div class="card"><h3>Proyectos</h3><div class="num" id="s-prj">—</div><div class="sub">negocios</div></div>
  <div class="card"><h3>Log</h3><div class="num" id="s-log">—</div><div class="sub">MB</div></div>
</div>

<!-- PANEL: SOLICITAR TAREA -->
<div class="panel active" id="panel-tareas">
  <div class="tarea-box">
    <h2>&#9997; Solicitar Tarea a los Agentes</h2>
    <p style="font-size:.82rem;color:#8b949e;margin-bottom:12px">Escribe lo que necesitas y los agentes lo ejecutaran. Ejemplos: "Genera sitio web para way2theunknown", "Mejora la pagina de destinos", "Crea 5 agentes de marketing"</p>
    <div class="row" style="margin-bottom:0">
      <div class="field"><label>Proyecto (opcional)</label>
        <select id="tarea-proyecto">
          <option value="">General (sin proyecto)</option>
        </select>
      </div>
      <div class="field"><label>Prioridad</label>
        <select id="tarea-prioridad">
          <option value="normal">Normal</option>
          <option value="alta">Alta</option>
          <option value="baja">Baja</option>
        </select>
      </div>
    </div>
    <div class="field" style="margin-top:8px"><label>Describe la tarea</label>
      <textarea id="tarea-descripcion" style="min-height:80px" placeholder="Ej: Genera un sitio web completo para Way2TheUnknown respetando la paleta de colores verde #647D63, beige #E1D9C8 y naranja #f7630c. Incluye landing, destinos y servicios."></textarea>
    </div>
    <div class="tarea-input" style="margin-top:0">
      <button onclick="enviarTarea()" style="width:100%;padding:12px;font-size:.9rem">Enviar Tarea a los Agentes</button>
    </div>
  </div>

  <h3 style="font-size:.9rem;color:#8b949e;margin-bottom:10px">Tareas Recientes</h3>
  <div class="tarea-history" id="tarea-history">
    <div style="color:#8b949e;text-align:center;padding:20px;font-size:.82rem">Sin tareas aun. Escribe algo arriba para comenzar.</div>
  </div>
</div>

<!-- PANEL: AGENTES (CRUD) -->
<div class="panel" id="panel-agentes">
  <div style="display:flex;gap:10px;margin-bottom:14px;align-items:center;flex-wrap:wrap">
    <input id="search" type="text" placeholder="Buscar agente..." oninput="filtrarAgentes(this.value)" style="max-width:300px">
    <select id="filtro-cat" onchange="filtrarAgentes(document.getElementById('search').value)" style="max-width:200px">
      <option value="">Todas las categorias</option>
    </select>
    <button onclick="abrirModalCrear()" style="margin-left:auto">+ Crear Agente</button>
  </div>
  <div style="overflow-x:auto">
    <table>
      <thead><tr><th>Archivo</th><th>Categoria</th><th>Descripcion</th><th>Salud</th><th>Acciones</th></tr></thead>
      <tbody id="tabla-agentes"></tbody>
    </table>
  </div>
</div>

<!-- PANEL: EXPANSION (Progreso) -->
<div class="panel" id="panel-expansion">
  <h2 style="font-size:1rem;color:#58a6ff;margin-bottom:16px">Plan de Expansion — Ruta a 500+ Agentes</h2>
  <div id="exp-summary" style="margin-bottom:20px">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:14px">
      <div class="card"><h3>Actuales</h3><div class="num" id="exp-current">—</div></div>
      <div class="card"><h3>Planificados</h3><div class="num" id="exp-planned">—</div></div>
      <div class="card"><h3>Creados</h3><div class="num" id="exp-created" style="color:#3fb950">—</div></div>
      <div class="card"><h3>Pendientes</h3><div class="num" id="exp-pending" style="color:#d29922">—</div></div>
      <div class="card"><h3>Meta Total</h3><div class="num" id="exp-target">—</div></div>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" id="exp-bar" style="width:0%"></div>
      <div class="progress-label" id="exp-pct">0%</div>
    </div>
  </div>
  <h3 style="font-size:.9rem;color:#8b949e;margin-bottom:12px">Nuevas categorias por crear</h3>
  <div id="exp-categories" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px"></div>
</div>

<!-- PANEL: CREDENCIALES -->
<div class="panel" id="panel-credenciales">
  <div style="border:1px solid #30363d;border-radius:8px;padding:18px;background:#161b22;margin-bottom:20px">
    <h2 style="font-size:1rem;margin-bottom:6px;color:#58a6ff">Credenciales de Plataformas</h2>
    <p style="font-size:.78rem;color:#8b949e;margin-bottom:14px">Configura accesos para que los agentes puedan publicar en redes, editar sitios web, enviar emails, responder mensajes, etc.</p>

    <div style="display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap">
      <div class="field" style="flex:1;min-width:160px">
        <label>Proyecto</label>
        <select id="cred-proyecto" onchange="cargarCredenciales()">
          <option value="">Selecciona proyecto...</option>
        </select>
      </div>
      <div class="field" style="flex:1;min-width:160px">
        <label>Detectar hosting de URL</label>
        <div style="display:flex;gap:6px">
          <input id="cred-detect-url" placeholder="example.com" style="flex:1">
          <button class="btn" onclick="detectarHosting()" style="white-space:nowrap">Detectar</button>
        </div>
      </div>
    </div>

    <div id="cred-deteccion" style="display:none;border:1px solid #30363d;border-radius:8px;padding:14px;background:#0d1117;margin-bottom:16px">
      <h3 style="font-size:.85rem;color:#d29922;margin-bottom:8px">Resultado del analisis</h3>
      <div id="cred-detect-result"></div>
    </div>

    <div id="cred-lista" style="margin-bottom:16px">
      <p style="color:#8b949e;font-size:.82rem">Selecciona un proyecto para ver sus credenciales</p>
    </div>
  </div>

  <div style="border:1px solid #30363d;border-radius:8px;padding:18px;background:#161b22">
    <h3 style="font-size:.9rem;color:#58a6ff;margin-bottom:12px">Agregar Credencial</h3>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px">
      <div class="field" style="flex:1;min-width:160px">
        <label>Plataforma</label>
        <select id="cred-plataforma" onchange="mostrarCamposPlataforma()">
          <option value="">Selecciona...</option>
        </select>
      </div>
    </div>
    <div id="cred-campos" style="display:none">
      <div id="cred-campos-inputs" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px"></div>
      <p id="cred-instrucciones" style="font-size:.78rem;color:#d29922;margin-bottom:12px;padding:10px;background:#1c1c00;border-radius:6px;border:1px solid #3d3800"></p>
      <button class="btn" onclick="guardarCredencial()">Guardar Credencial</button>
      <span id="cred-status" style="margin-left:10px;font-size:.82rem"></span>
    </div>
  </div>
</div>

<!-- PANEL: ADMIN (Categorias) -->
<div class="panel" id="panel-admin">
  <!-- Selector de Modo de Fabrica -->
  <div style="border:1px solid #30363d;border-radius:8px;padding:18px;background:#161b22;margin-bottom:20px">
    <h2 style="font-size:1rem;margin-bottom:14px;color:#58a6ff">Modo de Fabrica</h2>
    <div class="field">
      <label>Modo Actual</label>
      <div style="display:flex;gap:8px;margin-bottom:12px">
        <select id="modo-selector" style="flex:1">
          <option value="CREAR">CREAR - Generar nuevos agentes</option>
          <option value="MEJORAR">MEJORAR - Optimizar existentes</option>
          <option value="BALANCEADO">BALANCEADO - 60% crear, 40% mejorar</option>
          <option value="EXPANSION">EXPANSION - Solo los 206 micros</option>
          <option value="NOCHE">NOCHE - Todas las tareas (default)</option>
        </select>
        <button onclick="cambiarModo()" style="padding:8px 16px">Cambiar</button>
      </div>
      <div id="modo-status" style="font-size:.8rem;color:#8b949e;text-align:center"></div>
      <div style="margin-top:10px;padding:10px;background:#0d1117;border-left:3px solid #238636;border-radius:4px">
        <p style="margin:0;font-size:.8rem;color:#8b949e">Cambio de modo toma efecto en el proximo ciclo de la fabrica</p>
      </div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
    <!-- Crear Agente -->
    <div style="border:1px solid #30363d;border-radius:8px;padding:18px;background:#161b22">
      <h2 style="font-size:1rem;margin-bottom:14px;color:#58a6ff">+ Nuevo Agente</h2>
      <div class="field"><label>Nombre</label><input id="adm-ag-nombre" placeholder="mi_agente.py"></div>
      <div class="field" style="margin-top:8px"><label>Descripcion</label><textarea id="adm-ag-desc" style="height:80px" placeholder="Que hace este agente..."></textarea></div>
      <div class="field" style="margin-top:8px"><label>Categoria</label><select id="adm-ag-cat"></select></div>
      <button onclick="crearAgenteAdmin()" style="width:100%;margin-top:12px">Crear Agente</button>
      <div id="adm-ag-status" style="margin-top:8px;font-size:.83rem;color:#8b949e;text-align:center"></div>
    </div>
    <!-- Gestionar Categorias -->
    <div style="border:1px solid #30363d;border-radius:8px;padding:18px;background:#161b22">
      <h2 style="font-size:1rem;margin-bottom:14px;color:#58a6ff">Categorias</h2>
      <div class="field"><label>Crear nueva categoria</label>
        <div style="display:flex;gap:8px"><input id="adm-cat-nombre" placeholder="MARKETING"><button onclick="crearCategoria()">Crear</button></div>
      </div>
      <div class="field" style="margin-top:12px"><label>Renombrar categoria</label>
        <div style="display:flex;gap:8px;margin-bottom:6px"><select id="adm-cat-viejo"></select><input id="adm-cat-nuevo" placeholder="Nuevo nombre"></div>
        <button class="sec" onclick="renombrarCategoria()" style="width:100%">Renombrar</button>
      </div>
      <div id="adm-cat-status" style="margin-top:10px;font-size:.83rem;color:#8b949e;text-align:center"></div>
      <div style="margin-top:16px">
        <h3 style="font-size:.85rem;color:#8b949e;margin-bottom:8px">Categorias actuales</h3>
        <div id="adm-cat-list"></div>
      </div>
    </div>
  </div>
</div>

<!-- PANEL: EJECUTAR -->
<div class="panel" id="panel-ejecutar">
  <div class="row">
    <div class="field"><label>Agente</label><select id="sel-agente"><option value="">Cargando...</option></select></div>
    <div class="field"><label>Parametros</label><input id="inp-params" type="text" placeholder="ej: 2000000 10 20"></div>
    <button onclick="ejecutarAgente()">Ejecutar</button>
  </div>
  <div id="output-box">El output aparecera aqui...</div>
</div>

<!-- PANEL: PROYECTOS -->
<div class="panel" id="panel-proyectos">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
    <div style="border:1px solid #30363d;border-radius:8px;padding:18px;background:#161b22">
      <h2 style="font-size:1rem;margin-bottom:14px;color:#58a6ff">+ Crear Proyecto/Cliente</h2>
      <div class="field"><label>Nombre del Proyecto</label><input id="prj-nombre" placeholder="ej: Tienda Online CDMX"></div>
      <div class="field" style="margin-top:8px"><label>Descripcion del Negocio</label><textarea id="prj-descripcion" style="height:100px;resize:vertical" placeholder="Describe el tipo de negocio..."></textarea></div>
      <button onclick="crearProyecto()" style="width:100%;margin-top:10px">Crear Proyecto</button>
      <div id="prj-status" style="margin-top:10px;font-size:.83rem;color:#8b949e;text-align:center"></div>
    </div>
    <div style="border:1px solid #30363d;border-radius:8px;padding:18px;background:#161b22">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
        <h2 style="font-size:1rem;color:#58a6ff">Proyectos Existentes</h2>
        <button class="sec" onclick="cargarProyectos()" style="padding:4px 12px;font-size:.73rem">Recargar</button>
      </div>
      <div style="overflow-y:auto;max-height:340px" id="prj-lista"><div style="color:#8b949e;text-align:center;padding:20px">Cargando...</div></div>
    </div>
  </div>
</div>

<!-- PANEL: CLAWBOT -->
<div class="panel" id="panel-clawbot">
  <div class="chat-box">
    <div class="chat-msgs" id="chat-msgs">
      <div class="msg"><div class="quien">Sistema</div><div class="texto">Clawbot listo. Ejemplo: "Analiza depa de 2M en Polanco, hipoteca 20 anos al 10%"</div></div>
    </div>
    <div class="chat-input">
      <input id="chat-input" type="text" placeholder="Escribe tu consulta..." onkeydown="if(event.key==='Enter')enviarConsulta()">
      <button onclick="enviarConsulta()">Enviar</button>
    </div>
  </div>
</div>

<!-- PANEL: LOGS -->
<div class="panel" id="panel-logs">
  <div style="display:flex;gap:8px;margin-bottom:10px">
    <button onclick="cargarLog()">Actualizar</button>
    <button class="sec" onclick="document.getElementById('log-box').innerHTML=''">Limpiar</button>
    <label style="display:flex;align-items:center;gap:5px;font-size:.8rem"><input type="checkbox" id="auto-refresh" checked onchange="toggleAutoLog(this)">Auto 5s</label>
  </div>
  <div id="log-box"></div>
</div>

<footer>Agencia Santi v2 — API :8000 | Dashboard :8080</footer>

<!-- MODAL EDITAR AGENTE -->
<div class="modal-bg" id="modal-editar">
  <div class="modal">
    <h2 id="modal-titulo">Editar Agente</h2>
    <input type="hidden" id="edit-nombre-orig">
    <div class="field"><label>Nombre</label><input id="edit-nombre" disabled></div>
    <div class="field"><label>Descripcion</label><textarea id="edit-desc" style="height:80px"></textarea></div>
    <div class="field"><label>Categoria</label><select id="edit-cat"></select></div>
    <div class="field"><label>Salud</label>
      <select id="edit-salud"><option value="OK">OK</option><option value="Requiere revision">Requiere revision</option></select>
    </div>
    <div class="btns">
      <button class="danger" onclick="eliminarAgente()">Eliminar</button>
      <button class="sec" onclick="cerrarModal()">Cancelar</button>
      <button onclick="guardarEdicion()">Guardar</button>
    </div>
  </div>
</div>

<!-- MODAL CREAR AGENTE -->
<div class="modal-bg" id="modal-crear">
  <div class="modal">
    <h2>Crear Nuevo Agente</h2>
    <div class="field"><label>Nombre del archivo (.py)</label><input id="crear-nombre" placeholder="calculadora_ejemplo.py"></div>
    <div class="field"><label>Descripcion (min 10 chars)</label><textarea id="crear-desc" style="height:80px" placeholder="Que hace este agente..."></textarea></div>
    <div class="field"><label>Categoria</label><select id="crear-cat"></select></div>
    <div class="btns">
      <button class="sec" onclick="cerrarModalCrear()">Cancelar</button>
      <button onclick="crearAgenteModal()">Crear Agente</button>
    </div>
  </div>
</div>

<!-- TOAST -->
<div class="toast" id="toast"></div>

<script>
const API=location.protocol+'//'+location.hostname+':8000';
const KEY='santi-agencia-2026';
const H={'Authorization':'Bearer '+KEY,'Content-Type':'application/json'};
let todosAgentes=[];
let todasCategorias=[];
let logTimer=null;

function esc(s){if(!s)return'';return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}

function toast(msg,isError){
  const t=document.getElementById('toast');
  t.textContent=msg;
  t.className='toast show'+(isError?' error':'');
  setTimeout(()=>t.className='toast',3000);
}

// == Menu Hamburguesa ==
const TABS=['tareas','agentes','expansion','admin','ejecutar','proyectos','clawbot','logs'];
const LABELS={'tareas':'Solicitar Tarea','agentes':'Agentes','expansion':'Expansion','admin':'Admin','ejecutar':'Ejecutar','proyectos':'Proyectos','clawbot':'Clawbot','logs':'Logs'};
let menuOpen=false;

function toggleMenu(){
  menuOpen=!menuOpen;
  document.getElementById('dropdown-menu').classList.toggle('open',menuOpen);
  document.getElementById('menu-icon').innerHTML=menuOpen?'&#10005;':'&#9776;';
}

function menuNav(nombre,evt){
  // Close menu
  menuOpen=false;
  document.getElementById('dropdown-menu').classList.remove('open');
  document.getElementById('menu-icon').innerHTML='&#9776;';
  document.getElementById('menu-section').textContent=LABELS[nombre]||nombre;
  // Update active menu item
  document.querySelectorAll('.menu-item').forEach(m=>m.classList.remove('active'));
  if(evt&&evt.currentTarget)evt.currentTarget.classList.add('active');
  // Switch panel
  tab(nombre);
}

// Close menu when clicking outside
document.addEventListener('click',function(e){
  if(menuOpen&&!e.target.closest('.menu-wrap')){
    menuOpen=false;
    document.getElementById('dropdown-menu').classList.remove('open');
    document.getElementById('menu-icon').innerHTML='&#9776;';
  }
});

function tab(nombre){
  document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));
  const panel=document.getElementById('panel-'+nombre);
  if(panel)panel.classList.add('active');
  if(nombre==='logs')cargarLog();
  if(nombre==='proyectos')cargarProyectos();
  if(nombre==='expansion')cargarExpansion();
  if(nombre==='admin')cargarAdmin();
  if(nombre==='credenciales')initCredenciales();
  if(nombre==='tareas')cargarTareasRecientes();
}

// == Tareas ==
let tareasLocales=JSON.parse(localStorage.getItem('tareas_agencia')||'[]');

function cargarTareasRecientes(){
  const hist=document.getElementById('tarea-history');
  // Cargar proyectos en selector
  api('/proyectos').then(d=>{
    if(!d)return;
    const sel=document.getElementById('tarea-proyecto');
    const opts=['<option value="">General (sin proyecto)</option>'];
    (d.proyectos||[]).forEach(p=>opts.push(`<option value="${esc(p.nombre)}">${esc(p.nombre)}</option>`));
    sel.innerHTML=opts.join('');
  });
  // Render tareas locales
  if(!tareasLocales.length){
    hist.innerHTML='<div style="color:#8b949e;text-align:center;padding:20px;font-size:.82rem">Sin tareas aun. Escribe algo arriba para comenzar.</div>';
    return;
  }
  hist.innerHTML=tareasLocales.slice().reverse().map(t=>{
    const statusClass=t.status==='completada'?'done':t.status==='ejecutando'?'running':t.status==='error'?'error':'pending';
    return `<div class="tarea-entry">
      <div class="tarea-meta">
        <span>${esc(t.fecha)}</span>
        <span class="tarea-status ${statusClass}">${esc(t.status)}</span>
      </div>
      <div style="color:#e6edf3;margin-bottom:4px">${esc(t.descripcion.length>120?t.descripcion.slice(0,120)+'...':t.descripcion)}</div>
      ${t.proyecto?'<div style="font-size:.7rem;color:#58a6ff">Proyecto: '+esc(t.proyecto)+'</div>':''}
      ${t.resultado?'<div style="margin-top:6px;padding:8px;background:#161b22;border-radius:4px;font-size:.76rem;color:#3fb950;white-space:pre-wrap">'+esc(t.resultado.slice(0,300))+'</div>':''}
    </div>`;
  }).join('');
}

async function enviarTarea(){
  const desc=document.getElementById('tarea-descripcion').value.trim();
  const proyecto=document.getElementById('tarea-proyecto').value;
  const prioridad=document.getElementById('tarea-prioridad').value;
  if(!desc){toast('Escribe una descripcion de la tarea',true);return;}

  const tarea={
    id:Date.now(),
    descripcion:desc,
    proyecto:proyecto||null,
    prioridad:prioridad,
    fecha:new Date().toLocaleString(),
    status:'enviada',
    resultado:null
  };

  tareasLocales.push(tarea);
  localStorage.setItem('tareas_agencia',JSON.stringify(tareasLocales));
  document.getElementById('tarea-descripcion').value='';
  toast('Tarea enviada a los agentes');

  // Enviar al API
  cargarTareasRecientes();
  tarea.status='ejecutando';
  localStorage.setItem('tareas_agencia',JSON.stringify(tareasLocales));
  cargarTareasRecientes();

  try{
    const data=await api('/tarea',{method:'POST',body:JSON.stringify({descripcion:desc,proyecto:proyecto,prioridad:prioridad})});
    const idx=tareasLocales.findIndex(t=>t.id===tarea.id);
    if(idx>=0){
      if(data&&data.exito){
        tareasLocales[idx].status='completada';
        tareasLocales[idx].resultado=data.resultado||data.mensaje||'Tarea completada';
        toast('Tarea completada');
      }else{
        tareasLocales[idx].status='error';
        tareasLocales[idx].resultado=data?.error||'Error al ejecutar tarea';
        toast('Error en tarea',true);
      }
      localStorage.setItem('tareas_agencia',JSON.stringify(tareasLocales));
      cargarTareasRecientes();
    }
  }catch(e){
    const idx=tareasLocales.findIndex(t=>t.id===tarea.id);
    if(idx>=0){
      tareasLocales[idx].status='error';
      tareasLocales[idx].resultado='Error de conexion: '+e.message;
      localStorage.setItem('tareas_agencia',JSON.stringify(tareasLocales));
      cargarTareasRecientes();
    }
  }
}

async function api(ruta,opts={}){
  try{
    const ctrl=new AbortController();
    const timer=setTimeout(()=>ctrl.abort(),5000);
    const r=await fetch(API+ruta,{headers:H,...opts,signal:ctrl.signal});
    clearTimeout(timer);
    if(!r.ok)return null;
    return await r.json();
  }catch(e){
    console.log('API error: '+e.message+' ('+ruta+')');
    return null;
  }
}

// == Status ==
async function actualizarStatus(){
  const data=await api('/status');
  if(!data){
    document.getElementById('api-status').className='badge err';
    document.getElementById('api-status').textContent='Sin conexion';
    return;
  }
  document.getElementById('api-status').className='badge';
  document.getElementById('api-status').textContent='Online';
  document.getElementById('s-total').textContent=data.agentes?.total??'--';
  document.getElementById('s-ok').textContent=data.agentes?.saludables??'--';
  document.getElementById('s-log').textContent=(data.log_size_mb??'--');
  document.getElementById('last-update').textContent=new Date().toLocaleTimeString();
  api('/proyectos/contar').then(d=>{if(d)document.getElementById('s-prj').textContent=d.total??'--';});
  api('/categorias').then(d=>{if(d)document.getElementById('s-areas').textContent=d.total_categorias??'--';});
  api('/expansion').then(d=>{if(d){const creados=d.creados??0;document.getElementById('s-exp').textContent=creados+'/206';}});
}

// == Agentes (tabla con CRUD) ==
async function cargarAgentes(){
  const [ag,ar]=await Promise.all([api('/agentes'),api('/categorias')]);
  if(!ag)return;
  todosAgentes=ag.agentes||[];
  if(ar){
    todasCategorias=Object.keys(ar.categorias||{});
    llenarSelectCategorias();
  }
  const sel=document.getElementById('sel-agente');
  sel.innerHTML=todosAgentes.map(a=>`<option value="${esc(a.archivo)}">${esc(a.archivo)} [${esc(a.area)}]</option>`).join('');
  renderTabla(todosAgentes);
}

function llenarSelectCategorias(){
  const ids=['filtro-cat','edit-cat','crear-cat','adm-ag-cat','adm-cat-viejo'];
  ids.forEach(id=>{
    const el=document.getElementById(id);
    if(!el)return;
    const isFilter=id==='filtro-cat';
    el.innerHTML=(isFilter?'<option value="">Todas las categorias</option>':'')+
      todasCategorias.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join('');
  });
}

function renderTabla(agentes){
  const tbody=document.getElementById('tabla-agentes');
  tbody.innerHTML=agentes.map(a=>`
    <tr>
      <td style="font-family:monospace;font-size:.78rem">${esc(a.archivo)}</td>
      <td><span class="area-tag">${esc(a.area)}</span></td>
      <td style="color:#8b949e;font-size:.78rem">${esc((a.descripcion||'').slice(0,70))}</td>
      <td><span class="dot ${a.salud==='OK'?'ok':'warn'}"></span>${esc(a.salud||'OK')}</td>
      <td style="white-space:nowrap">
        <button class="sec" style="padding:3px 8px;font-size:.72rem" onclick="abrirModalEditar('${esc(a.archivo)}')">Editar</button>
        <button class="sec" style="padding:3px 8px;font-size:.72rem" onclick="ejecutarRapido('${esc(a.archivo)}')">Run</button>
      </td>
    </tr>
  `).join('');
}

function filtrarAgentes(q){
  const f=q.toLowerCase();
  const cat=document.getElementById('filtro-cat').value;
  renderTabla(todosAgentes.filter(a=>{
    const matchText=a.archivo.toLowerCase().includes(f)||(a.area||'').toLowerCase().includes(f)||(a.descripcion||'').toLowerCase().includes(f);
    const matchCat=!cat||a.area===cat;
    return matchText&&matchCat;
  }));
}

function ejecutarRapido(archivo){document.getElementById('sel-agente').value=archivo;tab('ejecutar');ejecutarAgente();}

// == Modal Editar ==
async function abrirModalEditar(nombre){
  const data=await api('/agentes/'+nombre);
  if(!data){toast('Error cargando agente',true);return;}
  document.getElementById('edit-nombre-orig').value=nombre;
  document.getElementById('edit-nombre').value=nombre;
  document.getElementById('edit-desc').value=data.info?.descripcion||'';
  document.getElementById('edit-cat').value=data.info?.categoria||'';
  document.getElementById('edit-salud').value=data.info?.salud||'OK';
  document.getElementById('modal-editar').classList.add('show');
}
function cerrarModal(){document.getElementById('modal-editar').classList.remove('show');}

async function guardarEdicion(){
  const nombre=document.getElementById('edit-nombre-orig').value;
  const body={
    nombre:nombre,
    descripcion:document.getElementById('edit-desc').value,
    categoria:document.getElementById('edit-cat').value,
    salud:document.getElementById('edit-salud').value
  };
  const data=await api('/agentes/editar',{method:'POST',body:JSON.stringify(body)});
  if(data&&data.exito){toast('Agente actualizado');cerrarModal();cargarAgentes();}
  else toast(data?.error||'Error al guardar',true);
}

async function eliminarAgente(){
  const nombre=document.getElementById('edit-nombre-orig').value;
  if(!confirm('Eliminar '+nombre+'? Esta accion no se puede deshacer.'))return;
  const data=await api('/agentes/eliminar',{method:'POST',body:JSON.stringify({nombre})});
  if(data&&data.exito){toast('Agente eliminado');cerrarModal();cargarAgentes();}
  else toast(data?.error||'Error al eliminar',true);
}

// == Modal Crear ==
function abrirModalCrear(){document.getElementById('modal-crear').classList.add('show');}
function cerrarModalCrear(){document.getElementById('modal-crear').classList.remove('show');}

async function crearAgenteModal(){
  const body={
    nombre:document.getElementById('crear-nombre').value,
    descripcion:document.getElementById('crear-desc').value,
    categoria:document.getElementById('crear-cat').value
  };
  if(!body.nombre||!body.descripcion){toast('Nombre y descripcion requeridos',true);return;}
  const data=await api('/agentes/crear',{method:'POST',body:JSON.stringify(body)});
  if(data&&data.exito){
    toast('Agente creado');cerrarModalCrear();cargarAgentes();
    document.getElementById('crear-nombre').value='';
    document.getElementById('crear-desc').value='';
  } else toast(data?.error||'Error al crear',true);
}

// == Expansion ==
async function cargarExpansion(){
  const data=await api('/expansion');
  if(!data){document.getElementById('exp-categories').innerHTML='<div style="color:#f85149">Error cargando expansion</div>';return;}
  document.getElementById('exp-current').textContent=data.agentes_actuales;
  document.getElementById('exp-planned').textContent=data.total_planificados;
  document.getElementById('exp-created').textContent=data.creados;
  document.getElementById('exp-pending').textContent=data.pendientes;
  document.getElementById('exp-target').textContent=data.meta_total;
  document.getElementById('exp-bar').style.width=data.progreso_pct+'%';
  document.getElementById('exp-pct').textContent=data.progreso_pct+'%';

  const cats=data.por_categoria||{};
  document.getElementById('exp-categories').innerHTML=Object.entries(cats).map(([cat,info])=>`
    <div class="exp-cat">
      <h4>${esc(cat)}</h4>
      <div class="count">${info.pendientes} pendientes</div>
      <div style="font-size:.76rem;color:#8b949e;margin-top:6px">
        ${(info.ejemplos||[]).map(e=>'<div style="padding:2px 0">'+esc(e)+'</div>').join('')}
      </div>
    </div>
  `).join('');
}

// == Credenciales ==
let plataformasCache=null;

async function cargarCredenciales(){
  const proy=document.getElementById('cred-proyecto').value;
  const lista=document.getElementById('cred-lista');
  if(!proy){lista.innerHTML='<p style="color:#8b949e;font-size:.82rem">Selecciona un proyecto</p>';return;}

  const data=await api('/credenciales?proyecto='+encodeURIComponent(proy));
  if(!data){lista.innerHTML='<p style="color:#f85149">Error cargando credenciales</p>';return;}

  plataformasCache=data.plataformas||[];

  // Llenar selector de plataformas
  const sel=document.getElementById('cred-plataforma');
  const cats={};
  plataformasCache.forEach(p=>{
    if(!cats[p.categoria])cats[p.categoria]=[];
    cats[p.categoria].push(p);
  });
  let opts='<option value="">Selecciona plataforma...</option>';
  Object.keys(cats).sort().forEach(cat=>{
    opts+=`<optgroup label="${esc(cat.toUpperCase())}">`;
    cats[cat].forEach(p=>opts+=`<option value="${esc(p.id)}">${esc(p.nombre)}</option>`);
    opts+='</optgroup>';
  });
  sel.innerHTML=opts;

  // Mostrar credenciales configuradas
  const creds=data.credenciales_configuradas||[];
  if(!creds.length){
    lista.innerHTML=`<p style="color:#8b949e;font-size:.82rem">Sin credenciales configuradas para '${esc(proy)}'. Hay ${data.plataformas_soportadas} plataformas disponibles.</p>`;
  }else{
    let html=`<p style="font-size:.82rem;color:#3fb950;margin-bottom:10px">${creds.length} credencial(es) configurada(s)</p>`;
    creds.forEach(c=>{
      const estado=c.activo?'<span style="color:#3fb950">Activa</span>':'<span style="color:#f85149">Inactiva</span>';
      html+=`<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border:1px solid #30363d;border-radius:6px;margin-bottom:6px;background:#0d1117">
        <div>
          <span style="font-weight:600;font-size:.85rem">${esc(c.nombre)}</span>
          <span style="font-size:.72rem;color:#8b949e;margin-left:8px">${esc(c.categoria)}</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px">
          ${estado}
          <button class="btn" style="font-size:.72rem;padding:3px 8px;background:#da3633" onclick="eliminarCredencial('${esc(proy)}','${esc(c.plataforma)}')">Eliminar</button>
        </div>
      </div>`;
    });
    lista.innerHTML=html;
  }
}

function mostrarCamposPlataforma(){
  const platId=document.getElementById('cred-plataforma').value;
  const container=document.getElementById('cred-campos');
  const inputs=document.getElementById('cred-campos-inputs');
  const instruc=document.getElementById('cred-instrucciones');
  if(!platId||!plataformasCache){container.style.display='none';return;}

  const plat=plataformasCache.find(p=>p.id===platId);
  if(!plat){container.style.display='none';return;}

  container.style.display='block';
  instruc.textContent=plat.instrucciones||'';

  let html='';
  (plat.campos||[]).forEach(campo=>{
    const tipo=campo.includes('password')||campo.includes('secret')||campo.includes('token')?'password':'text';
    html+=`<div class="field"><label>${esc(campo)}</label><input type="${tipo}" id="cred-val-${esc(campo)}" placeholder="${esc(campo)}"></div>`;
  });
  inputs.innerHTML=html;
}

async function guardarCredencial(){
  const proy=document.getElementById('cred-proyecto').value;
  const platId=document.getElementById('cred-plataforma').value;
  const st=document.getElementById('cred-status');
  if(!proy||!platId){toast('Selecciona proyecto y plataforma',true);return;}

  const plat=plataformasCache.find(p=>p.id===platId);
  if(!plat){return;}

  const creds={};
  let faltan=false;
  plat.campos.forEach(campo=>{
    const val=document.getElementById('cred-val-'+campo);
    if(val&&val.value.trim())creds[campo]=val.value.trim();
    else faltan=true;
  });

  if(faltan){toast('Completa todos los campos',true);return;}

  st.textContent='Guardando...';st.style.color='#d29922';
  const data=await api('/credenciales/guardar',{method:'POST',body:JSON.stringify({proyecto:proy,plataforma:platId,credenciales:creds})});
  if(data&&data.exito){
    st.textContent='Guardada';st.style.color='#3fb950';
    toast('Credencial guardada correctamente');
    cargarCredenciales();
  }else{
    st.textContent=data?.mensaje||'Error';st.style.color='#f85149';
    toast(data?.mensaje||'Error al guardar',true);
  }
}

async function eliminarCredencial(proy,plat){
  if(!confirm('Eliminar credencial de '+plat+'?'))return;
  const data=await api('/credenciales/eliminar',{method:'POST',body:JSON.stringify({proyecto:proy,plataforma:plat})});
  if(data&&data.exito){toast('Eliminada');cargarCredenciales();}
  else toast('Error al eliminar',true);
}

async function detectarHosting(){
  const url=document.getElementById('cred-detect-url').value.trim();
  const proy=document.getElementById('cred-proyecto').value;
  const div=document.getElementById('cred-deteccion');
  const res=document.getElementById('cred-detect-result');
  if(!url){toast('Ingresa una URL',true);return;}

  div.style.display='block';
  res.innerHTML='<p style="color:#d29922">Analizando '+esc(url)+'...</p>';

  const data=await api('/detectar-hosting',{method:'POST',body:JSON.stringify({url:url,proyecto:proy})});
  if(!data){res.innerHTML='<p style="color:#f85149">Error al analizar</p>';return;}

  let html='';
  html+=`<p><strong>Hosting:</strong> ${esc(data.hosting||'No detectado')} (confianza: ${esc(data.confianza)})</p>`;
  if(data.cms)html+=`<p><strong>CMS:</strong> ${esc(data.cms)}</p>`;
  if(data.cdn)html+=`<p><strong>CDN:</strong> ${esc(data.cdn)}</p>`;

  if(data.servicios_detectados&&data.servicios_detectados.length){
    html+=`<p style="margin-top:8px"><strong>Servicios detectados:</strong></p><ul style="margin-left:16px;font-size:.82rem">`;
    data.servicios_detectados.forEach(s=>html+=`<li>${esc(s.nombre)}${s.url_encontrada?' — '+esc(s.url_encontrada):''}</li>`);
    html+='</ul>';
  }
  if(data.credenciales_faltantes&&data.credenciales_faltantes.length){
    html+=`<p style="margin-top:8px;color:#f85149"><strong>Credenciales faltantes (${data.credenciales_faltantes.length}):</strong></p>`;
    data.credenciales_faltantes.forEach(c=>{
      html+=`<div style="padding:6px 10px;margin:4px 0;background:#1c0000;border:1px solid #3d0000;border-radius:4px;font-size:.82rem">
        <strong>${esc(c.nombre)}</strong> — Campos: ${esc(c.campos.join(', '))}<br>
        <span style="color:#d29922">${esc(c.instrucciones)}</span></div>`;
    });
  }
  if(data.credenciales_configuradas&&data.credenciales_configuradas.length){
    html+=`<p style="margin-top:8px;color:#3fb950"><strong>Ya configuradas (${data.credenciales_configuradas.length}):</strong></p>`;
    data.credenciales_configuradas.forEach(c=>html+=`<div style="padding:4px 10px;font-size:.82rem;color:#3fb950">OK ${esc(c.nombre)}</div>`);
  }
  res.innerHTML=html;
}

function initCredenciales(){
  // Llenar selector de proyectos
  api('/proyectos').then(d=>{
    if(!d)return;
    const sel=document.getElementById('cred-proyecto');
    let opts='<option value="">Selecciona proyecto...</option>';
    (d.proyectos||[]).forEach(p=>opts+=`<option value="${esc(p.nombre)}">${esc(p.nombre)}</option>`);
    sel.innerHTML=opts;
  });
}

// == Admin ==
async function cargarAdmin(){
  // Cargar modo actual
  const modoData=await api('/modo');
  if(modoData){
    document.getElementById('modo-selector').value=modoData.modo_actual;
    document.getElementById('modo-status').textContent=`Modo actual: ${modoData.modo_actual}`;
  }

  const data=await api('/categorias');
  if(!data)return;
  const cats=data.categorias||{};
  todasCategorias=Object.keys(cats);
  llenarSelectCategorias();
  document.getElementById('adm-cat-list').innerHTML=Object.entries(cats).map(([cat,info])=>`
    <div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #21262d">
      <span><span class="area-tag">${esc(cat)}</span></span>
      <span style="font-size:.8rem;color:#8b949e">${info.total} agentes (${info.ok} OK)</span>
    </div>
  `).join('');
}

async function crearAgenteAdmin(){
  const body={
    nombre:document.getElementById('adm-ag-nombre').value,
    descripcion:document.getElementById('adm-ag-desc').value,
    categoria:document.getElementById('adm-ag-cat').value
  };
  if(!body.nombre||!body.descripcion){toast('Nombre y descripcion requeridos',true);return;}
  const st=document.getElementById('adm-ag-status');
  st.textContent='Creando...';st.style.color='#d29922';
  const data=await api('/agentes/crear',{method:'POST',body:JSON.stringify(body)});
  if(data&&data.exito){
    st.textContent='Agente creado';st.style.color='#3fb950';
    document.getElementById('adm-ag-nombre').value='';
    document.getElementById('adm-ag-desc').value='';
    cargarAgentes();
  }else{st.textContent=data?.error||'Error';st.style.color='#f85149';}
}

async function crearCategoria(){
  const nombre=document.getElementById('adm-cat-nombre').value.trim();
  if(!nombre){toast('Nombre requerido',true);return;}
  const data=await api('/categorias/crear',{method:'POST',body:JSON.stringify({nombre})});
  if(data&&data.exito){toast('Categoria creada');document.getElementById('adm-cat-nombre').value='';cargarAdmin();}
  else toast(data?.error||'Error',true);
}

async function renombrarCategoria(){
  const viejo=document.getElementById('adm-cat-viejo').value;
  const nuevo=document.getElementById('adm-cat-nuevo').value.trim();
  if(!viejo||!nuevo){toast('Selecciona categoria y nuevo nombre',true);return;}
  const data=await api('/categorias/renombrar',{method:'POST',body:JSON.stringify({viejo,nuevo})});
  if(data&&data.exito){toast(data.mensaje);document.getElementById('adm-cat-nuevo').value='';cargarAdmin();cargarAgentes();}
  else toast(data?.error||'Error',true);
}

async function cambiarModo(){
  const nuevoModo=document.getElementById('modo-selector').value;
  const st=document.getElementById('modo-status');
  st.textContent='Cambiando modo...';st.style.color='#d29922';
  const data=await api('/modo',{method:'POST',body:JSON.stringify({modo:nuevoModo})});
  if(data&&data.exito){
    st.textContent=`Modo: ${nuevoModo}. Aplicara en proximo ciclo.`;
    st.style.color='#3fb950';
    toast(`Modo cambiado a ${nuevoModo}`);
  }else{
    st.textContent=data?.error||'Error al cambiar modo';
    st.style.color='#f85149';
    toast(data?.error||'Error',true);
  }
}

// == Ejecutar ==
async function ejecutarAgente(){
  const agente=document.getElementById('sel-agente').value;
  const params=document.getElementById('inp-params').value;
  const box=document.getElementById('output-box');
  if(!agente)return;
  box.textContent='Ejecutando '+agente+'...';box.style.color='#d29922';
  const data=await api('/ejecutar',{method:'POST',body:JSON.stringify({agente,params})});
  if(!data){box.textContent='Error: sin conexion';box.style.color='#f85149';return;}
  box.textContent=data.exito?data.output:'ERROR: '+data.output;
  box.style.color=data.exito?'#3fb950':'#f85149';
}

// == Clawbot ==
async function enviarConsulta(){
  const inp=document.getElementById('chat-input');
  const msgs=document.getElementById('chat-msgs');
  const mensaje=inp.value.trim();if(!mensaje)return;inp.value='';
  msgs.innerHTML+=`<div class="msg user"><div class="quien">Tu</div><div class="texto">${esc(mensaje)}</div></div>`;
  const id='msg-'+Date.now();
  msgs.innerHTML+=`<div class="msg" id="${id}"><div class="quien">Clawbot</div><div class="texto"><span class="spinner"></span> Procesando...</div></div>`;
  msgs.scrollTop=msgs.scrollHeight;
  const data=await api('/consulta',{method:'POST',body:JSON.stringify({mensaje})});
  const el=document.getElementById(id);
  if(el)el.querySelector('.texto').textContent=data?.respuesta||'Sin respuesta';
  msgs.scrollTop=msgs.scrollHeight;
}

// == Logs ==
async function cargarLog(){
  const data=await api('/status');if(!data)return;
  const box=document.getElementById('log-box');
  const lineas=data.ultimas_actividades||[];
  box.innerHTML=lineas.map(l=>{
    let cls='info';
    if(l.includes('OK')||l.includes('completado'))cls='ok';
    else if(l.includes('WARN')||l.includes('fallo'))cls='warn';
    else if(l.includes('ERROR')||l.includes('critico'))cls='err';
    return `<div class="log-line ${cls}">${esc(l)}</div>`;
  }).join('');
  box.scrollTop=box.scrollHeight;
}
function toggleAutoLog(cb){if(cb.checked)logTimer=setInterval(cargarLog,5000);else clearInterval(logTimer);}

// == Proyectos ==
async function cargarProyectos(){
  const lista=document.getElementById('prj-lista');
  lista.innerHTML='<div style="color:#8b949e;text-align:center;padding:20px">Cargando...</div>';
  const data=await api('/proyectos');
  if(!data){lista.innerHTML='<div style="color:#f85149">Error</div>';return;}
  const proyectos=data.proyectos||[];
  if(!proyectos.length){lista.innerHTML='<div style="color:#8b949e;text-align:center;padding:20px">Sin proyectos</div>';return;}
  lista.innerHTML=proyectos.map(p=>{
    const esActivo=p.status==='activo';
    const bc=esActivo?'#238636':'#9e6a03';
    const bt=esActivo?'Activo':'Pendiente';
    const desc=p.descripcion&&p.descripcion.length>60?p.descripcion.slice(0,60)+'...':(p.descripcion||'');
    return `<div style="border-bottom:1px solid #30363d;padding:8px 0;font-size:.83rem">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span style="color:#58a6ff;font-weight:600">${esc(p.nombre)}</span>
        <span style="background:${bc};color:#fff;padding:1px 8px;border-radius:10px;font-size:.7rem">${bt}</span>
      </div>
      <div style="color:#8b949e;font-size:.76rem;margin-top:3px">${esc(desc)}</div>
    </div>`;
  }).join('');
}

async function crearProyecto(){
  const nombre=document.getElementById('prj-nombre').value.trim();
  const descripcion=document.getElementById('prj-descripcion').value.trim();
  const st=document.getElementById('prj-status');
  if(!nombre){st.textContent='Nombre requerido';st.style.color='#f85149';return;}
  if(!descripcion){st.textContent='Descripcion requerida';st.style.color='#f85149';return;}
  st.textContent='Creando...';st.style.color='#d29922';
  const data=await api('/crear-proyecto',{method:'POST',body:JSON.stringify({nombre,descripcion})});
  if(data&&data.exito){
    st.textContent=data.mensaje||'Proyecto creado';st.style.color='#3fb950';
    document.getElementById('prj-nombre').value='';document.getElementById('prj-descripcion').value='';
    setTimeout(()=>{st.textContent='';cargarProyectos();},2000);
  }else{st.textContent=data?.error||'Error';st.style.color='#f85149';}
}

// == Init ==
document.getElementById('api-status').textContent='Conectando...';
document.getElementById('api-status').className='badge';

setTimeout(async()=>{try{await actualizarStatus();}catch(e){}},500);
setTimeout(async()=>{try{await cargarAgentes();}catch(e){}},1000);
setTimeout(()=>{try{cargarTareasRecientes();}catch(e){}},1500);

setInterval(()=>{try{actualizarStatus();}catch(e){}},30000);
logTimer=setInterval(()=>{try{cargarLog();}catch(e){}},5000);
</script>
</body>
</html>"""

class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def do_GET(self):
        body = HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

def iniciar_dashboard():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Dashboard v2 en http://localhost:{PUERTO}")
    srv = HTTPServer(("0.0.0.0", PUERTO), DashboardHandler)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.server_close()

if __name__ == "__main__":
    iniciar_dashboard()
