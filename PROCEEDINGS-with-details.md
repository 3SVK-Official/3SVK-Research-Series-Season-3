# Lifelong Reusable Intellectual Property & Research Template

## 1. Title of the Invention / Project

- **Project Name:** OfflineSync Lite – An Offline-First Data Synchronization System for Low-Connectivity Regions
- **Framework Identifier:** 3SVK Research Series Season 3 – National Research & Innovation Challenge

## 2. Primary Inventors / Applicants

- **Applicant 1:** Koppisetti Deepak Naga Satya V
  - **Nationality:** Indian
  - **Permanent Address:** Ainavelli Mandal, Konaseema District, Andhra Pradesh, 533577, India

## 3. Core Technical Abstract & Architecture

- **The Problem Addressed:** Many applications in rural and low-bandwidth areas stop working when the network drops. Users lose data entered while offline, and large payloads waste limited mobile data.
- **Core Innovation Module 1 (Sync Engine):** A queue-based engine records every user action as a small timestamped event while offline. When connectivity returns, it replays the events in order and resolves conflicts with a "last-writer-wins plus field-level merge" rule, so unrelated edits to the same record are both kept.
- **Core Innovation Module 2 (Storage and Security Layer):** Events are stored in a local encrypted database (SQLite with AES-256 encryption). Each event carries a hash of the previous one, forming a tamper-evident chain that makes silent data corruption detectable.
- **Communication / Synchronization Protocol:** Only changed fields (deltas) are sent, compressed with gzip. Uploads are batched and retried with exponential backoff. Each batch carries a unique ID so the server can ignore duplicates (idempotent sync).

## 4. Performance Metrics (Benchmark Reference)

> Design targets for the prototype, not measured results.

- **Metric 1 (Speed/Latency):** Target: sync of 100 queued records in under 3 seconds on a 2G-class connection.
- **Metric 2 (Resource Efficiency):** Target: reduce upload payload by more than 60% compared with sending full records, using delta encoding and compression.
- **Metric 3 (Reliability):** Target: zero data loss across repeated network drops, through persistent queuing and idempotent retries.

## 5. Methodology

1. Capture user actions as events in the local queue.
2. Detect connectivity changes and trigger batch sync.
3. Merge on the server at field level and return the resolved state.
4. Update the client and verify the hash chain.

## 6. Conclusion and Future Scope

OfflineSync Lite shows that an offline-first design with delta sync and a tamper-evident log can keep applications usable under poor connectivity. Future work includes a reference implementation, peer-to-peer sync over Bluetooth, and field trials in rural deployments.

## 7. Declaration

This document is the original work of the applicant named above, submitted for the 3SVK Research Series Season 3.
