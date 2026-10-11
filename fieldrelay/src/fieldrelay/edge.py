import os
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ConfigDict, Field

from fieldrelay.security import canonical_json, sign_body
from fieldrelay.store import EventStore


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FieldRelay | Field Operations</title>
<style>
:root{color-scheme:light;--ink:#182b35;--muted:#62717a;--line:#dce5e8;--paper:#f4f7f6;--panel:#fff;--blue:#205c70;--green:#147d64;--amber:#9a6418;--red:#aa3b36}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}header{background:#173b4a;color:white;padding:25px max(22px,calc((100vw - 1120px)/2)) 23px}header h1{margin:0;font-size:27px;letter-spacing:-.4px}header p{margin:5px 0 0;color:#d2e2e7}main{max-width:1120px;margin:24px auto;padding:0 20px}.top{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-bottom:18px}.status{display:inline-flex;align-items:center;gap:8px;padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:white;font-weight:650}.dot{width:9px;height:9px;border-radius:50%;background:var(--green)}.dot.off{background:var(--amber)}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}.metric,.panel{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:17px}.metric span{display:block;color:var(--muted);font-size:13px}.metric strong{display:block;font-size:27px;margin-top:5px;letter-spacing:-.5px}.layout{display:grid;grid-template-columns:340px 1fr;gap:16px;align-items:start}.panel h2{font-size:17px;margin:0 0 13px}.field{margin-bottom:11px}.field label{display:block;font-size:13px;font-weight:650;margin-bottom:5px}.field input,.field select,.field textarea{width:100%;border:1px solid #cbd8dd;border-radius:8px;padding:10px;background:white;color:var(--ink);font:inherit}.field textarea{resize:vertical;min-height:75px}.split{display:grid;grid-template-columns:1fr 1fr;gap:9px}button{border:0;border-radius:8px;background:var(--blue);color:white;font-weight:650;padding:10px 13px;font:inherit;cursor:pointer}button.secondary{background:#e9f0f2;color:var(--ink);border:1px solid var(--line)}button:disabled{opacity:.5;cursor:wait}.actions{display:flex;gap:8px;flex-wrap:wrap}.small{font-size:12px;color:var(--muted)}.bar{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;margin-bottom:12px}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:11px 9px;border-bottom:1px solid #edf1f2;text-align:left;white-space:nowrap}th{color:var(--muted);font-weight:650;background:#fafcfc}.tag{display:inline-block;padding:3px 8px;border-radius:99px;font-size:11px;font-weight:750;letter-spacing:.15px}.tag.pending{background:#fff0d9;color:var(--amber)}.tag.synced{background:#dff5ed;color:#116c55}.tag.dead{background:#fde8e6;color:var(--red)}.note{background:#eff5f6;border-radius:8px;padding:10px;color:#425760;font-size:12px;margin-top:12px}.toast{padding:11px 13px;border-radius:9px;background:#e4f4ed;color:#155b46;margin:0 0 15px;display:none}.toast.error{background:#fbeae8;color:#8b302d}.right{text-align:right}@media(max-width:850px){.layout{grid-template-columns:1fr}.grid{grid-template-columns:repeat(2,1fr)}main{padding:0 13px}.metric strong{font-size:23px}}@media(max-width:420px){.split{grid-template-columns:1fr}.grid{gap:8px}.metric,.panel{padding:13px}}
</style>
</head>
<body>
<header><h1>FieldRelay</h1><p>Offline-first records for field operations</p></header>
<main>
<div class="top"><div><strong>Operations overview</strong><div class="small">Records are stored on this device before synchronization.</div></div><div id="linkBadge" class="status"><span id="linkDot" class="dot off"></span><span id="linkText">Checking link</span></div></div>
<div id="toast" class="toast"></div>
<section class="grid"><div class="metric"><span>Total records</span><strong id="total">0</strong></div><div class="metric"><span>Waiting to sync</span><strong id="pending">0</strong></div><div class="metric"><span>Synced</span><strong id="synced">0</strong></div><div class="metric"><span>Needs attention</span><strong id="dead">0</strong></div></section>
<div class="layout">
<section class="panel"><h2>New field record</h2><form id="eventForm">
<div class="field"><label for="site">Site code</label><input id="site" name="site_code" value="SITE-01" pattern="[A-Za-z0-9_-]{2,24}" required maxlength="24"></div>
<div class="field"><label for="type">Record category</label><select id="type" name="event_type"><option value="supply_update">Supply update</option><option value="service_status">Service status</option><option value="site_note">Site note</option></select></div>
<div class="field"><label for="item">Item or service</label><input id="item" name="item" placeholder="Drinking water, power, kit stock" required maxlength="80"></div>
<div class="split"><div class="field"><label for="state">Status</label><select id="state" name="status"><option>Available</option><option>Low</option><option>Unavailable</option><option>Operational</option><option>Needs review</option></select></div><div class="field"><label for="quantity">Quantity</label><input id="quantity" name="quantity" type="number" min="0" max="1000000" step="1" value="0" required></div></div>
<div class="field"><label for="note">Note</label><textarea id="note" name="note" maxlength="300" placeholder="Optional field observation"></textarea></div>
<button type="submit" id="addBtn">Save record locally</button></form><div class="note">Use site codes and operational details only. Do not enter personal, medical, or other sensitive data.</div></section>
<section class="panel"><div class="bar"><div><h2 style="margin-bottom:2px">Record queue</h2><div class="small">Newest records first</div></div><div class="actions"><button class="secondary" id="linkBtn" type="button">Simulate offline</button><button id="syncBtn" type="button">Sync now</button></div></div>
<div class="table-wrap"><table><thead><tr><th>Site</th><th>Category</th><th>Created (UTC)</th><th>State</th><th>Attempts</th></tr></thead><tbody id="rows"><tr><td colspan="5">Loading records…</td></tr></tbody></table></div><div class="small" style="margin-top:12px" id="cloudStats">Cloud service: checking</div></section>
</div>
</main>
<script>
const $=id=>document.getElementById(id);let available=true;let toastTimer;
function showToast(message,isError=false){const box=$('toast');box.textContent=message;box.className='toast'+(isError?' error':'');box.style.display='block';clearTimeout(toastTimer);toastTimer=setTimeout(()=>box.style.display='none',5000)}
async function api(path,options={}){const r=await fetch(path,{headers:{'Content-Type':'application/json',...(options.headers||{})},...options});const data=await r.json().catch(()=>({detail:r.statusText}));if(!r.ok)throw new Error(data.detail||data.message||`Request failed (${r.status})`);return data}
function escapeHtml(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function stateTag(state){return `<span class="tag ${escapeHtml(state)}">${escapeHtml(state.toUpperCase())}</span>`}
async function refresh(){try{const [status,records]=await Promise.all([api('/api/status'),api('/api/events')]);available=status.link_available;$('linkDot').className='dot'+(available?'':' off');$('linkText').textContent=available?'Uplink enabled':'Simulated offline';$('linkBtn').textContent=available?'Simulate offline':'Restore connection';$('total').textContent=status.counts.total;$('pending').textContent=status.counts.pending;$('synced').textContent=status.counts.synced;$('dead').textContent=status.counts.dead;$('cloudStats').textContent=status.cloud.ok?`Cloud service reachable · ${status.cloud.stored_events} records stored`:'Cloud service unavailable';$('rows').innerHTML=records.length?records.map(r=>`<tr><td>${escapeHtml(r.site_code)}</td><td>${escapeHtml(r.event_type.replaceAll('_',' '))}</td><td>${escapeHtml(r.created_at.replace('T',' ').replace('+00:00',''))}</td><td>${stateTag(r.state)}</td><td>${r.attempts}</td></tr>`).join(''):'<tr><td colspan="5">No records yet. Add a field record to begin.</td></tr>'}catch(e){showToast(e.message,true)}}
$('eventForm').addEventListener('submit',async e=>{e.preventDefault();$('addBtn').disabled=true;const f=new FormData(e.target);const record={site_code:f.get('site_code'),event_type:f.get('event_type'),item:f.get('item'),status:f.get('status'),quantity:Number(f.get('quantity')),note:f.get('note')};try{await api('/api/events',{method:'POST',body:JSON.stringify(record)});e.target.reset();$('site').value=record.site_code;$('quantity').value='0';showToast('Record saved to the local queue.');await refresh()}catch(err){showToast(err.message,true)}finally{$('addBtn').disabled=false}});
$('linkBtn').addEventListener('click',async()=>{try{const data=await api('/api/link-state',{method:'POST',body:JSON.stringify({available:!available})});showToast(data.available?'Connection restored.':'Offline mode enabled. New records will stay on this device.');await refresh()}catch(e){showToast(e.message,true)}});
$('syncBtn').addEventListener('click',async()=>{if(!available){showToast('The uplink is offline. Records remain in the local queue.',true);return}$('syncBtn').disabled=true;$('syncBtn').textContent='Syncing…';try{const result=await api('/api/sync',{method:'POST',body:'{}'});showToast(`${result.synced} record(s) synchronized; ${result.failed} failed.` ,result.failed>0);await refresh()}catch(e){showToast(e.message,true);await refresh()}finally{$('syncBtn').disabled=false;$('syncBtn').textContent='Sync now'}});
refresh();setInterval(refresh,6000);
</script></body></html>'''


class NewEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    site_code: str = Field(min_length=2, max_length=24, pattern=r"^[A-Za-z0-9_-]+$")
    event_type: str = Field(pattern=r"^(supply_update|service_status|site_note)$")
    item: str = Field(min_length=1, max_length=80)
    status: str = Field(min_length=1, max_length=40)
    quantity: float = Field(ge=0, le=1_000_000)
    note: str = Field(default="", max_length=300)


def create_app(store=None, cloud_url=None, secret=None):
    app = FastAPI(title="FieldRelay Edge Console", version="1.0.0")
    app.state.store = store or EventStore(os.getenv("FIELDRELAY_EDGE_DB", "data/edge.db"))
    app.state.cloud_url = (cloud_url or os.getenv("FIELDRELAY_CLOUD_URL", "http://127.0.0.1:8000")).rstrip("/")
    app.state.secret = secret if secret is not None else os.getenv("FIELDRELAY_SHARED_SECRET", "")
    app.state.link_available = True

    @app.get("/", response_class=HTMLResponse)
    def index():
        return PAGE

    @app.get("/api/status")
    def status():
        counts = app.state.store.counts()
        cloud = {"ok": False, "stored_events": 0}
        try:
            response = requests.get(f"{app.state.cloud_url}/v1/stats", timeout=0.8)
            response.raise_for_status()
            cloud = {"ok": True, **response.json()}
        except requests.RequestException:
            pass
        return {"counts": counts, "link_available": app.state.link_available, "cloud": cloud}

    @app.get("/api/events")
    def events():
        return app.state.store.list_events()

    @app.post("/api/events")
    def add_event(record: NewEvent):
        payload = {"item": record.item.strip(), "status": record.status, "quantity": record.quantity, "note": record.note.strip()}
        event = app.state.store.add_event(record.site_code, record.event_type, payload)
        return {"event_id": event["event_id"], "state": "pending"}

    @app.post("/api/link-state")
    def set_link(data: dict):
        if not isinstance(data.get("available"), bool):
            raise HTTPException(status_code=422, detail="available must be a boolean")
        app.state.link_available = data["available"]
        return {"available": app.state.link_available}

    @app.post("/api/sync")
    def sync():
        if not app.state.link_available:
            raise HTTPException(status_code=409, detail="Uplink is offline; the local queue has been preserved")
        if not app.state.secret:
            raise HTTPException(status_code=503, detail="Set FIELDRELAY_SHARED_SECRET on the client and cloud services")
        synced = 0
        failed = 0
        batches = 0
        while True:
            batch = app.state.store.ready_batch(limit=50)
            if not batch:
                break
            batches += 1
            body = canonical_json({"events": batch})
            try:
                signature = sign_body(app.state.secret, body)
                response = requests.post(
                    f"{app.state.cloud_url}/v1/events/batch",
                    data=body,
                    headers={"Content-Type": "application/json", "X-FieldRelay-Signature": signature},
                    timeout=5,
                )
                response.raise_for_status()
                result = response.json()
                acknowledged = set(result.get("accepted", [])) | set(result.get("duplicates", []))
                expected = {event["event_id"] for event in batch}
                if acknowledged != expected:
                    raise RuntimeError("Cloud acknowledgement did not match the submitted batch")
                app.state.store.mark_synced(sorted(acknowledged))
                synced += len(acknowledged)
            except (requests.RequestException, RuntimeError, ValueError) as exc:
                app.state.store.mark_failed([event["event_id"] for event in batch], str(exc))
                failed += len(batch)
                break
        return {"synced": synced, "failed": failed, "batches": batches, "counts": app.state.store.counts()}

    return app


app = create_app()
