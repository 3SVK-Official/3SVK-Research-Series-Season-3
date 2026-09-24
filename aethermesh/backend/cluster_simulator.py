"""
AetherMesh Multi-Cloud Microservice Cluster Simulator
Simulates dynamic real-time telemetry, cross-cloud WAN latencies,
and cascading failure propagation across AWS, GCP, and Azure.
"""

import time
import math
import random
from typing import Dict, Any, List

class MultiCloudClusterSimulator:
    def __init__(self, state_store):
        self.state_store = state_store
        self.epoch = 0
        self.active_chaos: Dict[str, Dict[str, Any]] = {}
        
        # Base healthy telemetry profiles
        self.baseline_telemetry = {
            "api-gateway": {"cpu": 28.0, "mem": 42.0, "rps": 3200, "p99": 14.2, "err": 0.02, "queue": 8},
            "auth-service": {"cpu": 34.0, "mem": 38.0, "rps": 1800, "p99": 16.5, "err": 0.01, "queue": 12},
            "order-service": {"cpu": 45.0, "mem": 52.0, "rps": 1450, "p99": 22.0, "err": 0.04, "queue": 15},
            "payment-service": {"cpu": 38.0, "mem": 48.0, "rps": 920, "p99": 28.5, "err": 0.02, "queue": 9},
            "inventory-db": {"cpu": 42.0, "mem": 64.0, "rps": 2100, "p99": 8.4, "err": 0.01, "queue": 5},
            "user-profile-db": {"cpu": 31.0, "mem": 58.0, "rps": 1600, "p99": 7.2, "err": 0.01, "queue": 4},
            "recommendation-engine": {"cpu": 58.0, "mem": 72.0, "rps": 650, "p99": 42.0, "err": 0.05, "queue": 22},
            "notification-worker": {"cpu": 22.0, "mem": 32.0, "rps": 880, "p99": 18.0, "err": 0.02, "queue": 6},
        }

    def inject_chaos(self, fault_type: str, target: str, intensity: float = 1.0) -> Dict[str, Any]:
        """
        Injects real-time anomalies:
        - "cpu_spike": High CPU contention on target service
        - "db_exhaustion": High query latency & queue buildup
        - "wan_partition": Cross-cloud network degradation (AWS <-> GCP/Azure)
        - "cascading_retry_storm": Massive inbound request spike + timeout amplification
        """
        # Automatically restore node so the fault manifests visibly even if previously cordoned
        node_state = self.state_store.nodes.get(target)
        if node_state:
            node_state.is_cordoned = False
            node_state.traffic_weight = 1.0
            node_state.circuit_breaker_tripped = False
            node_state.rate_limit_throttle = 1.0
            node_state.status = "WARNING"
            node_state.version += 1

        fault_id = f"FAULT-{int(time.time())}"
        self.active_chaos[target] = {
            "fault_id": fault_id,
            "fault_type": fault_type,
            "target": target,
            "intensity": intensity,
            "started_at": time.time(),
            "epoch_started": self.epoch
        }
        return self.active_chaos[target]

    def clear_chaos(self, target: str = None):
        """Clears all or specific active chaos injections."""
        if target and target in self.active_chaos:
            del self.active_chaos[target]
        else:
            self.active_chaos.clear()

    def step(self) -> Dict[str, Any]:
        """Advances simulation epoch and produces real-time telemetry snapshot."""
        self.epoch += 1
        now = time.time()
        telemetry = {}

        # 1. First pass: base noise + sinusoidal traffic variation
        sin_wave = math.sin(self.epoch / 10.0) * 0.15
        
        for node_id, base in self.baseline_telemetry.items():
            noise = (random.random() - 0.5) * 0.1
            rps_factor = (1.0 + sin_wave + noise)
            
            node_state = self.state_store.nodes.get(node_id)
            throttle = node_state.rate_limit_throttle if node_state else 1.0
            weight = node_state.traffic_weight if node_state else 1.0
            
            # If cordoned or circuit broken, traffic dropped
            effective_traffic = weight * throttle if not (node_state and node_state.is_cordoned) else 0.05
            
            cpu = base["cpu"] * (0.8 + 0.2 * effective_traffic) + (random.random() * 3.0)
            mem = base["mem"] + (random.random() * 1.5)
            rps = int(base["rps"] * rps_factor * effective_traffic)
            p99 = base["p99"] + (random.random() * 2.0)
            err = base["err"] + (random.random() * 0.01)
            queue = max(1, int(base["queue"] * effective_traffic + random.randint(-1, 2)))

            telemetry[node_id] = {
                "node_id": node_id,
                "cpu_util": round(cpu, 1),
                "mem_util": round(mem, 1),
                "req_rate_in": rps,
                "req_rate_out": int(rps * 0.96),
                "p99_latency": round(p99, 1),
                "err_rate": round(err, 3),
                "thread_wait": round(p99 * 0.4, 1),
                "queue_depth": queue,
                "timestamp": now
            }

        # 2. Second pass: Apply Active Chaos & simulate downstream -> upstream cascade
        for target, chaos in list(self.active_chaos.items()):
            ftype = chaos["fault_type"]
            intensity = chaos["intensity"]
            epochs_active = self.epoch - chaos["epoch_started"]
            
            if target in telemetry:
                t = telemetry[target]
                node_state = self.state_store.nodes.get(target)

                # Check if self-healing has rerouted or isolated target
                is_healed_or_isolated = (node_state and (node_state.is_cordoned or node_state.traffic_weight <= 0.25))

                if not is_healed_or_isolated:
                    if ftype == "cpu_spike":
                        t["cpu_util"] = min(99.4, 82.0 + intensity * 15.0 + random.random() * 2.5)
                        t["thread_wait"] = round(120.0 + intensity * 80.0, 1)
                        t["p99_latency"] = round(t["p99_latency"] + 350.0 * intensity * min(epochs_active, 4), 1)
                        t["err_rate"] = round(min(0.28, 0.03 * epochs_active * intensity), 3)
                        t["queue_depth"] = min(350, int(t["queue_depth"] + 45 * epochs_active))
                        
                    elif ftype == "db_exhaustion":
                        t["cpu_util"] = min(96.0, 75.0 + intensity * 18.0)
                        t["p99_latency"] = round(450.0 * intensity * min(epochs_active, 5), 1)
                        t["queue_depth"] = min(400, int(t["queue_depth"] + 60 * epochs_active))
                        t["thread_wait"] = round(280.0 * intensity, 1)
                        t["err_rate"] = round(min(0.22, 0.02 * epochs_active), 3)

                    elif ftype == "wan_partition":
                        t["p99_latency"] = round(t["p99_latency"] + 420.0 * intensity, 1)
                        t["err_rate"] = round(min(0.35, 0.08 * epochs_active * intensity), 3)
                        t["queue_depth"] = min(280, int(t["queue_depth"] + 30 * epochs_active))

                    elif ftype == "cascading_retry_storm":
                        t["req_rate_in"] = int(t["req_rate_in"] * (2.5 + intensity * 1.5))
                        t["cpu_util"] = min(98.8, 88.0 + intensity * 10.0)
                        t["p99_latency"] = round(t["p99_latency"] + 520.0 * intensity, 1)
                        t["err_rate"] = round(min(0.42, 0.06 * epochs_active), 3)

                    # CASCADE PROPAGATION: If target is degrading and not mitigated, upstream dependencies suffer!
                    # Example: payment-service degradation propagates to order-service -> api-gateway
                    if epochs_active >= 2:
                        upstream_map = {
                            "payment-service": ["order-service", "api-gateway"],
                            "inventory-db": ["order-service", "api-gateway"],
                            "auth-service": ["api-gateway"],
                            "user-profile-db": ["auth-service", "recommendation-engine"]
                        }
                        if target in upstream_map:
                            for up_node in upstream_map[target]:
                                if up_node in telemetry:
                                    up_t = telemetry[up_node]
                                    up_t["p99_latency"] = round(up_t["p99_latency"] + 110.0 * (epochs_active - 1), 1)
                                    up_t["queue_depth"] += 15 * (epochs_active - 1)
                                    up_t["err_rate"] = round(min(0.25, up_t["err_rate"] + 0.015 * epochs_active), 3)
                                    up_t["cpu_util"] = min(95.0, up_t["cpu_util"] + 6.0 * epochs_active)
                else:
                    # Self-healing was triggered! Node is protected or isolated
                    t["req_rate_in"] = int(t["req_rate_in"] * 0.15)
                    t["p99_latency"] = round(t["p99_latency"] * 0.4 + 20.0, 1)
                    t["cpu_util"] = max(25.0, t["cpu_util"] * 0.6)
                    t["err_rate"] = round(max(0.01, t["err_rate"] * 0.3), 3)

        # 3. Compute dynamic edge stats
        edge_telemetry = []
        for edge in self.state_store.edges:
            src = edge["source"]
            tgt = edge["target"]
            base_lat = edge["base_latency"]
            
            src_p99 = telemetry[src]["p99_latency"] if src in telemetry else 10.0
            tgt_p99 = telemetry[tgt]["p99_latency"] if tgt in telemetry else 10.0
            
            # Dynamic cross-cloud edge latency reflects node pressure
            latency = base_lat + (tgt_p99 * 0.15) + (random.random() * 2.0)
            is_choked = (latency > 75.0 or (telemetry.get(tgt, {}).get("err_rate", 0) > 0.1))
            
            edge_telemetry.append({
                "source": src,
                "target": tgt,
                "protocol": edge["protocol"],
                "latency_ms": round(latency, 1),
                "packet_drop_pct": round(min(12.0, (latency / 40.0) * 0.8), 2),
                "is_choked": is_choked
            })

        return {
            "epoch": self.epoch,
            "timestamp": now,
            "nodes": telemetry,
            "edges": edge_telemetry,
            "active_chaos": list(self.active_chaos.values())
        }
