"""
AetherMesh FastAPI Application
Provides RESTful Management APIs and Real-Time WebSocket Streaming
for the Autonomous Predictive Multi-Cloud Mesh Mission Control.
"""

import os
import json
import time
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .state_store import CRDTMeshStateStore
from .cluster_simulator import MultiCloudClusterSimulator
from .gnn_predictor import SpatioTemporalGNNPredictor
from .drl_orchestrator import DRLSelfHealingOrchestrator

# Initialize Core Subsystems
state_store = CRDTMeshStateStore()
cluster_sim = MultiCloudClusterSimulator(state_store)
gnn_predictor = SpatioTemporalGNNPredictor(
    node_ids=list(state_store.nodes.keys()),
    edges=state_store.edges
)
drl_orchestrator = DRLSelfHealingOrchestrator(state_store)

app = FastAPI(
    title="AetherMesh Control Plane API",
    description="Autonomous Predictive Self-Healing Multi-Cloud Mesh via GNN & DRL",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Active WebSocket connections
active_connections: List[WebSocket] = []

# Latest cache
latest_telemetry: Dict[str, Any] = {}
latest_predictions: Dict[str, Any] = {}
is_engine_running = False

# Request models
class ChaosRequest(BaseModel):
    fault_type: str
    target: str
    intensity: Optional[float] = 1.0

class ModeRequest(BaseModel):
    autonomous: bool

class ManualMitigationRequest(BaseModel):
    node_id: str
    action: str

async def engine_tick_loop():
    """Continuous 1Hz background simulation, GNN inference, and DRL self-healing loop."""
    global latest_telemetry, latest_predictions, is_engine_running
    is_engine_running = True
    
    while is_engine_running:
        try:
            # 1. Simulate Cluster Telemetry
            telemetry = cluster_sim.step()
            latest_telemetry = telemetry

            # 2. Execute Spatio-Temporal GNN Cascade Prediction (Core Module 1)
            predictions = gnn_predictor.predict(telemetry)
            latest_predictions = predictions

            # 3. Execute DRL Self-Healing Orchestration (Core Module 2)
            actions = drl_orchestrator.evaluate_and_orchestrate(predictions, telemetry)

            # 4. Construct Composite Broadcast Frame
            mesh_snapshot = state_store.get_snapshot()
            broadcast_frame = {
                "type": "MESH_TICK",
                "timestamp": time.time(),
                "epoch": telemetry["epoch"],
                "telemetry": telemetry,
                "predictions": predictions,
                "mesh_state": mesh_snapshot,
                "system_status": {
                    "autonomous_mode": drl_orchestrator.autonomous_mode,
                    "active_chaos": telemetry.get("active_chaos", []),
                    "total_mitigations": drl_orchestrator.total_mitigations_executed,
                    "accumulated_reward": round(drl_orchestrator.accumulated_reward, 2)
                }
            }

            # 5. Broadcast to connected WebSocket clients
            disconnected = []
            for ws in active_connections:
                try:
                    await ws.send_text(json.dumps(broadcast_frame))
                except Exception:
                    disconnected.append(ws)

            for dead_ws in disconnected:
                if dead_ws in active_connections:
                    active_connections.remove(dead_ws)

        except Exception as e:
            print(f"[AetherMesh Engine Error]: {e}")

        await asyncio.sleep(1.0)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(engine_tick_loop())

# WebSocket Endpoint
@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    # Send immediate snapshot on connect
    if latest_telemetry and latest_predictions:
        init_frame = {
            "type": "MESH_INIT",
            "telemetry": latest_telemetry,
            "predictions": latest_predictions,
            "mesh_state": state_store.get_snapshot(),
            "system_status": {
                "autonomous_mode": drl_orchestrator.autonomous_mode,
                "active_chaos": latest_telemetry.get("active_chaos", []),
                "total_mitigations": drl_orchestrator.total_mitigations_executed,
                "accumulated_reward": round(drl_orchestrator.accumulated_reward, 2)
            }
        }
        await websocket.send_text(json.dumps(init_frame))

    try:
        while True:
            # Keep socket alive and accept incoming command messages
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
                if msg.get("action") == "PING":
                    await websocket.send_text(json.dumps({"type": "PONG", "time": time.time()}))
            except Exception:
                pass
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)

# RESTful APIs
@app.get("/api/status")
async def get_status():
    return {
        "status": "ONLINE",
        "system": "AetherMesh Autonomous Multi-Cloud Mesh",
        "autonomous_mode": drl_orchestrator.autonomous_mode,
        "active_chaos": cluster_sim.active_chaos,
        "total_mitigations": drl_orchestrator.total_mitigations_executed,
        "accumulated_reward": round(drl_orchestrator.accumulated_reward, 2),
        "cluster_risk_score": latest_predictions.get("cluster_cascade_risk_score", 0.0),
        "connected_dashboards": len(active_connections)
    }

@app.get("/api/topology")
async def get_topology():
    return state_store.get_snapshot()

@app.get("/api/telemetry")
async def get_telemetry():
    return latest_telemetry or cluster_sim.step()

@app.get("/api/predictions")
async def get_predictions():
    return latest_predictions

@app.post("/api/chaos/inject")
async def inject_chaos(req: ChaosRequest):
    fault = cluster_sim.inject_chaos(req.fault_type, req.target, req.intensity or 1.0)
    return {"status": "injected", "fault": fault}

@app.post("/api/chaos/clear")
async def clear_chaos(target: Optional[str] = None):
    cluster_sim.clear_chaos(target)
    return {"status": "cleared", "remaining_chaos": list(cluster_sim.active_chaos.values())}

@app.post("/api/mode/toggle")
async def toggle_mode(req: ModeRequest):
    drl_orchestrator.set_autonomous_mode(req.autonomous)
    return {
        "status": "mode_updated",
        "autonomous_mode": drl_orchestrator.autonomous_mode
    }

@app.post("/api/mitigate/manual")
async def trigger_manual_mitigation(req: ManualMitigationRequest):
    res = drl_orchestrator.manual_trigger_mitigation(req.node_id, req.action)
    return res

@app.post("/api/reset")
async def reset_cluster():
    cluster_sim.clear_chaos()
    state_store.reset_all_mitigations()
    drl_orchestrator.reset()
    return {"status": "cluster_reset_complete"}

# Mount Frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
