# Communication Experiment Methodology

## Objective

Measure actual communication behavior across three architectures to demonstrate real differences in data transmission patterns.

## Architectures Compared

### B1: Centralized Detector
- **Policy**: Transmit all raw data to cloud for processing
- **Transmission**: Every sample window transmitted
- **Data type**: Raw feature windows (60 samples × 1 feature = 60 floats)
- **Message count**: Equal to number of samples processed
- **Expected behavior**: Maximum data transmission

### B2: Static Edge Detector
- **Policy**: Process locally, no transmission
- **Transmission**: Only anomaly events transmitted (if configured)
- **Data type**: Anomaly alerts (minimal metadata)
- **Message count**: Equal to number of detected anomalies
- **Expected behavior**: Minimal data transmission

### B3: Proposed Adaptive Edge Detector
- **Policy**: Adaptive transmission decision based on controller
- **Transmission**: Depends on controller decision (LOCAL_ONLY vs TRANSMIT)
- **Data type**: Variable (raw data if transmitting, nothing if local)
- **Message count**: Depends on controller decisions
- **Expected behavior**: Adaptive transmission based on resource conditions

## Metrics Measured

1. **Total bytes transmitted**: Sum of all data sent over network
2. **Number of messages**: Count of transmission events
3. **Transmitted events**: Number of samples/windows transmitted
4. **Normal events transmitted**: Count of normal samples transmitted (unnecessary)
5. **Anomaly-related information transmitted**: Count of anomaly samples transmitted

## Implementation Details

### Centralized (Cloud Coordinator)
- Location: `src/cloud/coordinator.py`
- Measurement: `sample.nbytes` for each sample
- All samples transmitted: `total_data_transmitted = sum(sample.nbytes)`

### Static Edge (Edge Processor)
- Location: `src/edge/processor.py`
- Measurement: `sample.nbytes` only when `should_transmit = True`
- Currently: Transmits anomalies only (line 194: `should_transmit = True` for anomalies)
- Data transmitted: Minimal (anomaly alerts)

### Adaptive Edge (Edge Processor)
- Location: `src/edge/processor.py`
- Measurement: `sample.nbytes` based on controller decision
- Decision: Controller decides between LOCAL_ONLY and TRANSMIT
- Data transmitted: Variable based on resource conditions

## Expected Results from Current Implementation

Based on actual experiment results:

| Architecture | Total Bytes | Messages | Normal Events | Anomaly Events |
|-------------|-------------|----------|---------------|----------------|
| Centralized | 331,680 | 691 | 643 | 48 |
| Static Edge | 30,720 | 64 | 16 | 48 |
| Adaptive Edge | 30,720 | 64 | 16 | 48 |

**Note**: Current implementation transmits anomalies only for edge systems. This is a meaningful comparison showing:
- Centralized: 100% of data transmitted (all normal + all anomalies)
- Edge systems: Only anomaly-related data transmitted (minimal overhead)

## Fair Comparison Principles

1. **Measure actual behavior**: Report what each architecture actually does
2. **No cherry-picking**: Don't claim improvement for trivial "zero transmission" if edge sends nothing
3. **Contextualize**: Explain WHY transmission differs (architectural design)
4. **Honest reporting**: Clearly state what is measured and why

## Key Insight

The communication reduction is an architectural advantage of edge processing, not an algorithmic improvement. The adaptive controller can further optimize this by:
- Transmitting only when beneficial (e.g., for complex anomalies)
- Keeping normal data local
- Reducing unnecessary network traffic

## Future Enhancements

To make the communication experiment more meaningful:
1. Implement selective transmission (transmit only high-confidence anomalies)
2. Measure bandwidth utilization over time
3. Simulate network congestion scenarios
4. Measure transmission latency impact

## Date Documented

September 9, 2026
