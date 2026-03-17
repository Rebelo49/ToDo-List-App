"""
To-Do List App — Portfolio Project
Interface web local (sem dependências externas!)
Corre em qualquer Python 3.6+
"""

import json
import os
import webbrowser
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
PORT = 8765


def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


HTML = r"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>✅ To-Do List</title>
<style>
  :root {
    --bg:#1e1e2e;--surface:#2a2a3e;--accent:#7c6af7;--accent2:#a78bfa;
    --done:#4ade80;--text:#e2e8f0;--sub:#94a3b8;--border:#3f3f5a;
    --danger:#f87171;--hover:#35354f;
    --cat-Pessoal:#f472b6;--cat-Trabalho:#60a5fa;--cat-Estudo:#facc15;
    --cat-Saude:#4ade80;--cat-Outro:#a78bfa;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:100vh}
  .app{max-width:780px;margin:0 auto;padding:32px 20px}
  header{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
  header h1{font-size:26px;color:var(--accent2)}
  .stats{color:var(--sub);font-size:13px}
  .search-bar{background:var(--surface);border:1px solid var(--border);border-radius:10px;display:flex;align-items:center;padding:0 14px;margin-bottom:14px}
  .search-bar input{background:none;border:none;outline:none;color:var(--text);font-size:14px;padding:12px 8px;flex:1}
  .filters{display:flex;gap:12px;margin-bottom:18px;flex-wrap:wrap}
  .filters select{background:var(--surface);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:8px 12px;font-size:13px;cursor:pointer;outline:none}
  .add-bar{background:var(--surface);border:2px solid var(--accent);border-radius:12px;display:flex;gap:10px;align-items:center;padding:10px 14px;margin-bottom:24px;flex-wrap:wrap}
  .add-bar input{background:none;border:none;outline:none;color:var(--text);font-size:14px;flex:1;min-width:140px}
  .add-bar select{background:var(--hover);border:1px solid var(--border);border-radius:8px;color:var(--text);padding:8px 10px;font-size:13px;cursor:pointer;outline:none}
  .btn-add{background:var(--accent);color:white;border:none;border-radius:8px;padding:9px 20px;font-size:13px;font-weight:700;cursor:pointer}
  .btn-add:hover{opacity:.85}
  .empty{text-align:center;color:var(--sub);padding:60px 0;font-size:16px}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:12px;display:flex;align-items:stretch;margin-bottom:10px;overflow:hidden;transition:border-color .2s}
  .card.done{border-color:var(--done);opacity:.75}
  .card:hover{border-color:var(--accent)}
  .stripe{width:6px;flex-shrink:0}
  .card-body{flex:1;padding:12px 14px}
  .card-title{font-size:15px;font-weight:600;margin-bottom:6px}
  .card.done .card-title{text-decoration:line-through;color:var(--sub)}
  .card-meta{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
  .badge{border-radius:6px;padding:2px 10px;font-size:11px;font-weight:700;color:#1e1e2e}
  .card-date{color:var(--sub);font-size:11px}
  .card-actions{display:flex;flex-direction:column;justify-content:center;gap:6px;padding:10px 12px}
  .btn{border:none;border-radius:7px;padding:6px 14px;font-size:12px;font-weight:600;cursor:pointer;white-space:nowrap}
  .btn-done{background:var(--done);color:#1e1e2e}
  .btn-undo{background:var(--hover);color:var(--sub)}
  .btn-edit{background:var(--hover);color:var(--text)}
  .btn-delete{background:var(--hover);color:var(--danger)}
  .btn:hover{opacity:.8}
</style>
</head>
<body>
<div class="app">
  <header>
    <h1>✅ To-Do List</h1>
    <span class="stats" id="stats"></span>
  </header>
  <div class="search-bar">
    <span>🔍</span>
    <input id="search" placeholder="Pesquisar tarefas…" oninput="render()"/>
  </div>
  <div class="filters">
    <select id="fCat" onchange="render()">
      <option>Todas as categorias</option>
      <option>Pessoal</option><option>Trabalho</option>
      <option>Estudo</option><option>Saúde</option><option>Outro</option>
    </select>
    <select id="fStat" onchange="render()">
      <option>Todos os estados</option>
      <option>Pendentes</option><option>Concluídas</option>
    </select>
  </div>
  <div class="add-bar">
    <input id="newTask" placeholder="Nova tarefa…" onkeydown="if(event.key==='Enter')addTask()"/>
    <select id="newCat">
      <option>Pessoal</option><option>Trabalho</option>
      <option>Estudo</option><option>Saúde</option><option>Outro</option>
    </select>
    <button class="btn-add" onclick="addTask()">+ Adicionar</button>
  </div>
  <div id="list"></div>
</div>
<script>
let tasks=[];
const CAT_COLORS={Pessoal:'#f472b6',Trabalho:'#60a5fa',Estudo:'#facc15','Saúde':'#4ade80',Outro:'#a78bfa'};

async function loadTasks(){const r=await fetch('/api/tasks');tasks=await r.json();render()}

async function addTask(){
  const title=document.getElementById('newTask').value.trim();
  const cat=document.getElementById('newCat').value;
  if(!title)return;
  await fetch('/api/add',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title,category:cat})});
  document.getElementById('newTask').value='';
  await loadTasks();
}

async function toggle(id){
  await fetch('/api/toggle',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});
  await loadTasks();
}

async function deleteTask(id){
  if(!confirm('Apagar esta tarefa?'))return;
  await fetch('/api/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});
  await loadTasks();
}

async function editTask(id,oldTitle){
  const t=prompt('Editar tarefa:',oldTitle);
  if(!t||!t.trim())return;
  await fetch('/api/edit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,title:t.trim()})});
  await loadTasks();
}

function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}

function render(){
  const q=document.getElementById('search').value.toLowerCase();
  const fCat=document.getElementById('fCat').value;
  const fSt=document.getElementById('fStat').value;
  const visible=tasks.filter(t=>{
    if(fCat!=='Todas as categorias'&&t.category!==fCat)return false;
    if(fSt==='Pendentes'&&t.done)return false;
    if(fSt==='Concluídas'&&!t.done)return false;
    if(q&&!t.title.toLowerCase().includes(q))return false;
    return true;
  });
  const done=tasks.filter(t=>t.done).length;
  document.getElementById('stats').textContent=`✅ ${done} concluídas  •  🕐 ${tasks.length-done} pendentes  •  Total: ${tasks.length}`;
  const list=document.getElementById('list');
  if(!visible.length){list.innerHTML='<div class="empty">Nenhuma tarefa encontrada 🎉</div>';return}
  list.innerHTML=[...visible].reverse().map(t=>{
    const c=CAT_COLORS[t.category]||'#a78bfa';
    return`<div class="card ${t.done?'done':''}">
      <div class="stripe" style="background:${c}"></div>
      <div class="card-body">
        <div class="card-title">${t.done?'✅':'🔲'} ${esc(t.title)}</div>
        <div class="card-meta">
          <span class="badge" style="background:${c};color:#1e1e2e">${t.category}</span>
          <span class="card-date">🕐 ${t.created}</span>
        </div>
      </div>
      <div class="card-actions">
        <button class="btn ${t.done?'btn-undo':'btn-done'}" onclick="toggle(${t.id})">${t.done?'Desfazer':'Concluir'}</button>
        <button class="btn btn-edit" onclick="editTask(${t.id},'${esc(t.title).replace(/'/g,"\\'")}')">✏️ Editar</button>
        <button class="btn btn-delete" onclick="deleteTask(${t.id})">🗑 Apagar</button>
      </div>
    </div>`}).join('');
}
loadTasks();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_): pass

    def send_json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            body = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/tasks":
            self.send_json(load_tasks())
        else:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length)) if length else {}
        path   = urlparse(self.path).path
        tasks  = load_tasks()

        if path == "/api/add":
            tasks.append({
                "id":       int(datetime.now().timestamp() * 1000),
                "title":    body.get("title", "").strip(),
                "category": body.get("category", "Outro"),
                "done":     False,
                "created":  datetime.now().strftime("%d/%m/%Y %H:%M"),
            })
            save_tasks(tasks); self.send_json({"ok": True})

        elif path == "/api/toggle":
            tid = body.get("id")
            for t in tasks:
                if t["id"] == tid: t["done"] = not t["done"]
            save_tasks(tasks); self.send_json({"ok": True})

        elif path == "/api/delete":
            save_tasks([t for t in tasks if t["id"] != body.get("id")])
            self.send_json({"ok": True})

        elif path == "/api/edit":
            tid = body.get("id")
            for t in tasks:
                if t["id"] == tid: t["title"] = body.get("title", t["title"])
            save_tasks(tasks); self.send_json({"ok": True})

        else:
            self.send_response(404); self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)
    url    = f"http://localhost:{PORT}"
    print(f"\n  ✅  To-Do List App")
    print(f"  🌐  A abrir em {url}")
    print(f"  ⛔  Para parar: Ctrl+C\n")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  👋  App encerrada!")
        server.shutdown()
