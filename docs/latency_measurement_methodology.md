# Latency Measurement Methodology

## Measurement Boundaries

To ensure fair comparison, we measure the same logical operation for all systems:

**Input → Processing → Detection/Decision**

### Centralized Baseline (B1)
- **Measurement**: End-to-end latency including network transmission
- **Components**: 
  - Network transmission to cloud (uplink)
  - Cloud inference processing
  - Network transmission back (downlink)
- **Rationale**: This is the actual cost of centralized processing; network overhead is inherent to the architecture
- **Formula**: `total_latency = network_latency_up + inference_latency + network_latency_down`

### Static Edge Baseline (B2)
- **Measurement**: End-to-end local processing latency
- **Components**:
  - Local preprocessing (if applicable)
  - Local inference processing
  - Local decision making
- **Rationale**: Edge processing eliminates network overhead; this measures pure local processing cost
- **Formula**: `total_latency = preprocessing_latency + inference_latency + decision_latency`

### Proposed Adaptive Edge (B3)
- **Measurement**: End-to-end local processing latency
- **Components**:
  - Local preprocessing (if applicable)
  - Controller decision latency
  - Local inference processing (selected model)
  - Local decision making
- **Rationale**: Same as static edge for fair comparison; adaptive overhead is included
- **Formula**: `total_latency = preprocessing_latency + controller_latency + inference_latency + decision_latency`

## Fair Comparison Principles

1. **Edge vs Edge**: Compare B2 and B3 on inference-only latency (both are local)
2. **Centralized vs Edge**: Acknowledge that centralized includes network by design
3. **No Cherry-Picking**: Do not compare "network + inference" vs "inference only" as algorithmic improvement
4. **Honest Reporting**: Clearly state what each measurement includes

## Implementation Details

### Cloud Coordinator (Centralized)
- Location: `src/cloud/coordinator.py`
- Measures: `transmission_latency * 2 + processing_latency`
- Network latency: 50ms (simulated, configurable)
- Processing latency: Actual inference time

### Edge Processor (Static & Adaptive)
- Location: `src/edge/processor.py`
- Measures: Inference time only (preprocessing done before stream processing)
- Controller latency: Negligible (O(1) utility computation)
- Processing latency: Actual inference time for selected model

## Expected Results

- **Centralized**: Higher latency due to network overhead (expected: ~100ms)
- **Static Edge**: Lower latency (local processing only, expected: <1ms)
- **Adaptive Edge**: Variable latency based on model selection (LIGHT < STANDARD < HEAVY)

## Key Insight

The latency reduction of edge processing vs centralized is primarily due to network elimination, not algorithmic improvement. This is a valid architectural advantage but should be reported honestly.

For algorithmic comparison, compare:
- Adaptive Edge vs Static Edge (both local, same measurement boundary)
- Model selection impact within Adaptive Edge (LIGHT vs STANDARD vs HEAVY)

## Date Documented

September 9, 2026
