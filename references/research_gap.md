# Research Gap Definition

## Problem Statement
Conventional centralized anomaly detection architectures transmit all data to cloud servers for processing, incurring high latency, bandwidth costs, and network dependency. Static edge processing reduces transmission but lacks adaptation to varying resource constraints and data characteristics.

## Literature Analysis Summary

### Existing Approaches Categorized

**1. Static Edge Processing**
- TinyGLASS (2025): Fixed quantized model on sensor
- Industrial-AdaVAD (2025): Fixed lightweight ResNet with domain adaptation
- Implementation of edge AI (2025): Fixed RNN+autoencoder on edge

**Limitation**: No runtime adaptation to resource changes or data difficulty

**2. Hierarchical Offloading**
- Contextual-Bandit (2020): Model selection across IoT-edge-cloud hierarchy
- Hierarchical Adaptive Control (2025): Two-tier global scheduler + local controller

**Limitation**: Requires hierarchical infrastructure, complex deployment

**3. Single-Resource Optimization**
- Energy-Aware (2025): Focuses primarily on energy consumption
- EdgeMLBalancer (2025): Focuses primarily on CPU utilization
- Explainable Lightweight (2026): Focuses on accuracy-latency-explainability trade-off

**Limitation**: Optimizes one resource dimension, ignores multi-dimensional constraints

**4. Model Selection Approaches**
- MetaEdge (2025): Meta-learning for model prediction + hardware optimization
- Adaptive Configuration Selection (2025): RL-based pipeline configuration

**Limitation**: Selection from pre-defined set, no joint local/transmission decision

## Identified Research Gap

**No existing work systematically addresses:**

1. **Multi-dimensional resource awareness**: Simultaneous consideration of CPU, memory, latency, and bandwidth constraints in a unified framework

2. **Joint local processing and transmission decisions**: Most methods either process locally OR offload, but don't dynamically decide based on real-time resource state and data characteristics

3. **Mathematically-defined adaptation policy**: Clear specification of state variables, decision variables, thresholds, and computational complexity

4. **General-purpose time-series anomaly detection**: Most work is domain-specific (video, vision, LLMs) rather than general time-series anomaly detection

5. **Comprehensive baseline comparison**: Systematic evaluation against both centralized AND static edge baselines with fair experimental conditions

## Proposed Contribution

**Adaptive Edge-AI Framework for Real-Time Anomaly Detection**

### Key Differentiators

1. **Unified multi-dimensional adaptation**: Simultaneously optimizes for latency, data transfer, CPU, and memory

2. **Joint decision framework**: Dynamically decides:
   - Whether to process locally or transmit
   - What processing intensity to use
   - When to escalate to cloud

3. **Mathematically-defined controller**: Explicit specification of:
   - State space: resource metrics, data characteristics, anomaly confidence
   - Decision variables: processing mode, transmission flag, model complexity
   - Adaptation policy: threshold-based utility function
   - Computational complexity: O(1) per decision

4. **General applicability**: Designed for time-series anomaly detection, applicable to IoT telemetry, sensor data, network traffic

5. **Comprehensive evaluation**: Three-way comparison:
   - Baseline A: Centralized detection (all data transmitted)
   - Baseline B: Static edge detection (fixed local processing)
   - Proposed: Adaptive edge framework (dynamic decisions)

## Research Questions

**RQ1**: Does the proposed framework maintain anomaly-detection quality comparable to centralized and static edge baselines?

**RQ2**: Does adaptive edge processing reduce inference latency compared to centralized detection?

**RQ3**: Does it reduce data transmission volume compared to centralized detection?

**RQ4**: Does it reduce computational resource consumption (CPU, memory) compared to static edge processing?

**RQ5**: How does performance change under different resource constraints (CPU limits, bandwidth limits)?

**RQ6**: How sensitive is the method to its adaptation parameters (thresholds, utility weights)?

## Hypotheses

**H1**: The adaptive framework will achieve detection performance (F1-score, AUC) within 5% of centralized detection while reducing latency by >30%

**H2**: The adaptive framework will reduce data transmission by >50% compared to centralized detection while maintaining detection performance

**H3**: The adaptive framework will reduce CPU utilization by >20% compared to static edge processing under resource-constrained conditions

**H4**: Performance degradation under resource constraints will be graceful (<10% F1 drop) rather than catastrophic

## Novelty Claim

**We do NOT claim global novelty of edge anomaly detection or adaptive computing.**

**Our contribution is:**
- A specific mathematical formulation for multi-dimensional adaptive edge anomaly detection
- A unified framework that jointly optimizes local processing and transmission decisions
- Comprehensive experimental validation against both centralized and static edge baselines
- Open-source reproducible implementation with Python 3.14.6 compatibility

**This is an incremental but rigorous contribution that:**
- Addresses a specific gap in multi-dimensional resource awareness
- Provides a mathematically-defensible adaptation policy
- Demonstrates measurable improvements through reproducible experiments
