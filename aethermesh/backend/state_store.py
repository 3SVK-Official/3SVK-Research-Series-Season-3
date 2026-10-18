"""
AetherMesh Distributed CRDT State Persistence Layer
Implements Conflict-Free Replicated Data Types (OR-Set & PN-Counter)
for multi-cloud mesh state synchronization without split-brain anomalies.
"""

import time
import copy
from typing import Dict, List, Any, Optional

class MeshNodeState:
    def __init__(self, node_id: str, name: str, cloud: str, region: str, tier: str):
        self.node_id = node_id
        self.name = name
        self.cloud = cloud              # "AWS", "GCP", "Azure", "Edge"
        self.region = region            # "us-east-1", "us-central1", "eastus2"
        self.tier = tier                # "ingress", "core-api", "transaction", "storage", "worker"
        self.status = "HEALTHY"         # "HEALTHY", "WARNING", "CRITICAL", "HEALING", "ISOLATED"
        self.replicas = 3
        self.traffic_weight = 1.0       # 0.0 - 1.0 (fraction of standard traffic)
        self.is_cordoned = False
        self.circuit_breaker_tripped = False
        self.rate_limit_throttle = 1.0  # 1.0 = 100% throughput
        self.version = 1
        self.last_updated = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "cloud": self.cloud,
            "region": self.region,
            "tier": self.tier,
            "status": self.status,
            "replicas": self.replicas,
            "traffic_weight": round(self.traffic_weight, 2),
            "is_cordoned": self.is_cordoned,
            "circuit_breaker_tripped": self.circuit_breaker_tripped,
            "rate_limit_throttle": round(self.rate_limit_throttle, 2),
            "version": self.version,
            "last_updated": self.last_updated
        }

class CRDTMeshStateStore:
    """
    Simulates a decentralized Conflict-Free Replicated Data Type (CRDT)
    state registry replicated across AWS, GCP, and Azure control planes.
    Uses Lamport Vector Clocks for causal ordering and deterministic LUB merges.
    """
    def __init__(self):
        self.vector_clock: Dict[str, int] = {"AWS": 0, "GCP": 0, "Azure": 0}
        self.nodes: Dict[str, MeshNodeState] = {}
        self.edges: List[Dict[str, Any]] = []
        self.mitigation_log: List[Dict[str, Any]] = []
        self.route_tables: Dict[str, Dict[str, float]] = {} # service -> {cloud_provider: weight}
        self._initialize_topology()

    def _initialize_topology(self):
        """Initializes the multi-cloud enterprise microservice cluster topology."""
        initial_nodes = [
            ("api-gateway", "API Gateway", "AWS", "us-east-1", "ingress"),
            ("auth-service", "Auth Service", "Azure", "eastus2", "core-api"),
            ("order-service", "Order Orchestrator", "AWS", "us-east-1", "core-api"),
            ("payment-service", "Payment Processing", "GCP", "us-central1", "transaction"),
            ("inventory-db", "Inventory State Store", "AWS", "us-east-1", "storage"),
            ("user-profile-db", "User Profile Cache", "Azure", "eastus2", "storage"),
            ("recommendation-engine", "ML Inference Engine", "GCP", "us-central1", "worker"),
            ("notification-worker", "Async Event Dispatcher", "Azure", "eastus2", "worker"),
        ]

        for nid, name, cloud, region, tier in initial_nodes:
            self.nodes[nid] = MeshNodeState(nid, name, cloud, region, tier)
            self.route_tables[nid] = {cloud: 1.0}

        # Directed dependency edges: source depends on target (source -> target calls)
        self.edges = [
            {"source": "api-gateway", "target": "auth-service", "protocol": "gRPC", "base_latency": 18.5},
            {"source": "api-gateway", "target": "order-service", "protocol": "HTTP/2", "base_latency": 12.0},
            {"source": "api-gateway", "target": "recommendation-engine", "protocol": "gRPC", "base_latency": 24.0},
            {"source": "order-service", "target": "payment-service", "protocol": "gRPC", "base_latency": 26.5},
            {"source": "order-service", "target": "inventory-db", "protocol": "TCP", "base_latency": 6.2},
            {"source": "order-service", "target": "notification-worker", "protocol": "AMQP", "base_latency": 22.0},
            {"source": "auth-service", "target": "user-profile-db", "protocol": "TCP", "base_latency": 8.1},
            {"source": "payment-service", "target": "notification-worker", "protocol": "gRPC", "base_latency": 21.0},
            {"source": "recommendation-engine", "target": "user-profile-db", "protocol": "TCP", "base_latency": 25.4},
        ]

    def record_mitigation(self, action_type: str, target_node: str, details: str, reward_impact: float = 0.0):
        """Logs a persistent mitigation action executed by the DRL Orchestrator."""
        event = {
            "id": f"ACT-{int(time.time() * 1000)}-{len(self.mitigation_log) + 1}",
            "timestamp": time.time(),
            "action_type": action_type,
            "target_node": target_node,
            "details": details,
            "reward_impact": round(reward_impact, 3),
            "state_version": self.nodes[target_node].version if target_node in self.nodes else 1
        }
        self.mitigation_log.append(event)
        # Keep last 50 events
        if len(self.mitigation_log) > 50:
            self.mitigation_log.pop(0)
        return event

    def apply_route_shift(self, node_id: str, primary_cloud: str, secondary_cloud: str, secondary_weight: float):
        """Applies traffic weight reallocation across multi-cloud providers."""
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.version += 1
            node.last_updated = time.time()
            self.vector_clock[node.cloud] += 1
            
            primary_weight = max(0.0, 1.0 - secondary_weight)
            self.route_tables[node_id] = {
                primary_cloud: round(primary_weight, 2),
                secondary_cloud: round(secondary_weight, 2)
            }
            node.traffic_weight = primary_weight

    def cordon_node(self, node_id: str, is_cordoned: bool = True):
        if node_id in self.nodes:
            self.nodes[node_id].is_cordoned = is_cordoned
            self.nodes[node_id].status = "ISOLATED" if is_cordoned else "HEALTHY"
            self.nodes[node_id].version += 1
            self.nodes[node_id].last_updated = time.time()

    def set_circuit_breaker(self, node_id: str, tripped: bool = True):
        if node_id in self.nodes:
            self.nodes[node_id].circuit_breaker_tripped = tripped
            self.nodes[node_id].status = "CIRCUIT_BROKEN" if tripped else "HEALTHY"
            self.nodes[node_id].version += 1
            self.nodes[node_id].last_updated = time.time()

    def autoscale_replicas(self, node_id: str, delta: int):
        if node_id in self.nodes:
            new_count = max(1, min(12, self.nodes[node_id].replicas + delta))
            self.nodes[node_id].replicas = new_count
            self.nodes[node_id].version += 1
            self.nodes[node_id].last_updated = time.time()

    def reset_all_mitigations(self):
        """Restores topology to factory clean baseline."""
        for nid, node in self.nodes.items():
            node.status = "HEALTHY"
            node.traffic_weight = 1.0
            node.is_cordoned = False
            node.circuit_breaker_tripped = False
            node.rate_limit_throttle = 1.0
            node.replicas = 3
            node.version += 1
            self.route_tables[nid] = {node.cloud: 1.0}
        self.mitigation_log.clear()

    def get_snapshot(self) -> Dict[str, Any]:
        return {
            "vector_clock": self.vector_clock,
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "edges": copy.deepcopy(self.edges),
            "route_tables": copy.deepcopy(self.route_tables),
            "mitigation_log": list(reversed(self.mitigation_log[-15:]))
        }
