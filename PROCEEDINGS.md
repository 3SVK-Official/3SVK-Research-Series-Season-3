# AI-Powered Criminal Network Analysis and Identity Intelligence System
## Research Proceedings — 3SVK Research Series Season 3

> **Document status:** Research proposal / system design draft. Replace all bracketed fields and verify every implementation claim before submission.
>
> **Primary challenge:** SIH PS189 — AI-Powered Criminal Network Analysis System  
> **Supporting capability:** PS188-inspired fake identity and document screening  
> **Project name:** [Confirm final project name]  
> **Primary inventor/applicant:** [Full name]  
> **Co-applicants / mentor:** [Add only with their consent]  
> **Institution / organization:** [Institution name]  
> **Version/date:** [Version and date]

## Abstract

Investigative records may be distributed across case files, reports, entities, locations, vehicles, and other authorized sources. Inconsistent formats, duplicate records, incomplete identifiers, and weakly documented relationships can make it difficult for an investigator to understand how records relate across cases. This document proposes an AI-assisted system centered on criminal-network analysis, with identity and document screening as a supporting input capability.

The proposed workflow normalizes authorized records, extracts entities where suitable, resolves possible duplicates, records relationships with provenance, and represents the resulting information as a temporal knowledge graph. Graph analysis and timeline views can help investigators inspect connections and prioritize leads. Document screening may extract fields from supplied documents and flag inconsistencies or potential signs of manipulation for human review. Each inferred relationship or match should carry its supporting evidence, uncertainty, and source history.

This document describes a proposed architecture and an evaluation plan; it does not claim that all modules have been implemented, connected to official databases, or experimentally validated. No benchmark results are reported because verified measurements have not been supplied. The system is intended only as decision support for authorized personnel. A graph connection, similarity score, or document anomaly must not be treated as proof of criminality or as a basis for an automated adverse legal decision.

**Keywords:** criminal network analysis, knowledge graph, entity resolution, evidence provenance, document screening, explainable AI, temporal analysis, human-in-the-loop decision support.

## 1. Introduction

Modern investigations can involve many records about people, organizations, locations, events, vehicles, documents, and communications. Information may be fragmented across sources and may contain spelling differences, aliases, missing values, conflicting timestamps, or duplicate entries. Manual cross-referencing can be time-consuming and may make important connections difficult to inspect.

The primary focus of this proposal is criminal-network analysis (PS189): organizing authorized investigative records into a structured, inspectable graph and helping investigators explore relationships and changes over time. A supporting identity/document screening capability inspired by PS188 can provide extracted fields and document-review signals to the same evidence workflow.

The system is not intended to label a person as criminal merely because the person appears in a record or is connected to another entity. It should preserve the difference between source facts, algorithmic inferences, unverified hypotheses, and conclusions made by an authorized human reviewer.

## 2. Problem statement

Investigators may need to connect information from multiple authorized records despite inconsistent identifiers, duplicated entities, incomplete relationships, and varying evidence quality. A useful analysis system should:

1. ingest and normalize authorized records;
2. represent entities and relationships consistently;
3. retain source provenance and time information;
4. identify possible duplicate entities without silently merging uncertain matches;
5. provide graph, timeline, and, where appropriate, geographic exploration;
6. surface potential relationships with reasons and uncertainty;
7. support review, correction, and audit by authorized personnel; and
8. handle document-screening outputs as evidence signals requiring verification, not as definitive determinations.

## 3. Aim and objectives

### 3.1 Aim

To specify an evidence-aware, explainable, temporal graph-analysis workflow that supports authorized investigators in exploring relationships across fragmented records, with identity/document screening as a supporting capability.

### 3.2 Objectives

- Define a common data model for entities, relationships, events, source records, and evidence.
- Describe a pipeline for ingestion, normalization, entity resolution, graph construction, and analysis.
- Preserve provenance, timestamps, confidence/uncertainty, and review status for each derived relationship.
- Specify a document-screening workflow that can extract fields and flag inconsistencies for human inspection.
- Design an investigator-facing workflow for graph exploration, timeline review, evidence inspection, and audit.
- Establish a test plan measuring accuracy, false matches, usability, traceability, and performance before making efficacy claims.
- Define privacy, security, fairness, and human-oversight requirements.

## 4. Scope

### In scope

- Structured representation of authorized case records and entities.
- Entity normalization and candidate duplicate detection.
- Evidence-linked graph construction.
- Descriptive graph analytics such as degree/centrality, bridge analysis, and community detection, if implemented and validated.
- Temporal filtering and event timelines.
- Document-field extraction and rule-based consistency checks as a proposed supporting module.
- Review queues, explanations, correction workflows, and audit records.
- Evaluation using synthetic or properly authorized and de-identified data.

### Out of scope unless separately authorized, implemented, and validated

- Direct connection to government, police, telecom, financial, biometric, or other restricted databases.
- Unrestricted surveillance or collection of personal data.
- Definitive determination that a person committed an offence.
- Automatic arrest, detention, watchlisting, or other adverse action.
- Claims of operational accuracy, real-time performance, or production readiness without evidence.
- Facial recognition, CCTV analytics, ANPR, or biometric matching as completed capabilities unless separately demonstrated and lawfully approved.

## 5. Proposed system architecture

The architecture is a proposal, not a statement that every module currently exists.

1. **Authorized data intake:** Receive approved records and document files; validate format, authorization, and required metadata.
2. **Parsing and normalization:** Standardize dates, names, identifiers, locations, and record formats while preserving original values.
3. **Entity extraction:** Extract candidate people, organizations, locations, vehicles, events, and document fields from structured or unstructured sources using methods selected and validated for the actual data.
4. **Entity resolution:** Compare candidate records using deterministic rules and/or probabilistic similarity. Preserve alternatives and uncertainty; require human review for ambiguous merges.
5. **Evidence and provenance layer:** Record the source, timestamp, transformation, reviewer, and rationale for each fact or inferred link.
6. **Graph construction:** Represent entities as nodes and documented relationships/events as edges with time and provenance attributes.
7. **Analysis layer:** Provide descriptive graph measures and temporal queries. Any predictive link suggestion must be clearly labeled as a hypothesis and accompanied by a reason and evidence trail.
8. **Document screening (supporting module):** Extract text/fields; perform format and consistency checks; optionally run validated forensic checks. Return review flags rather than a definitive “fake” verdict.
9. **Investigator interface:** Allow authorized users to inspect nodes, edges, source records, timelines, filters, and review status.
10. **Security and audit:** Apply least-privilege access, secure transport/storage, logging, retention controls, and incident response appropriate to the deployment.

## 6. Data model

The following is a conceptual model. The final implementation should document its actual schema.

| Record type | Suggested fields |
|---|---|
| Entity | Internal ID, entity type, normalized attributes, aliases, status |
| Source record | Source ID, source type, collection/record time, authorization basis, integrity metadata |
| Relationship | Source entity, relationship type, target entity, validity interval, supporting source IDs |
| Event | Event ID, event type, time or time range, location reference, associated entities |
| Document review | Document reference, extracted fields, validation checks, flags, reviewer status |
| Inference | Inference ID, method/version, candidate link, score if calibrated, explanation, uncertainty |
| Audit event | Actor, action, timestamp, object reference, reason, outcome |

A similarity score must not be called a probability unless it has been calibrated and evaluated as one. Missing information must remain missing; it must not be fabricated to complete a record.

## 7. Methodology

### Stage 1 — Data governance and intake
Use only synthetic, public, de-identified, or otherwise lawfully authorized data. Record source and purpose. Reject or quarantine files that fail intake checks.

### Stage 2 — Normalization and extraction
Normalize formats without destroying original source values. Extraction tools should be selected after examining the real document types and languages. Store extracted values separately from source images/text and retain extraction confidence where available.

### Stage 3 — Entity resolution
Generate candidate matches using documented features such as normalized names, identifiers, dates, or other legally approved attributes. Evaluate false merges and missed matches. Ambiguous matches should remain separate until reviewed.

### Stage 4 — Evidence-linked graph
Create graph nodes and edges only from traceable source facts or clearly labeled inferences. Each edge should identify its source and temporal context. Do not convert mere co-occurrence into proof of a meaningful relationship.

### Stage 5 — Graph and temporal analysis
Allow investigators to filter by time, source, relationship type, and review status. Graph measures describe structure; they do not establish guilt or intent. Any ranking should explain which measurable factors contributed to it.

### Stage 6 — Document screening
Where supported by the implementation, extract fields and run deterministic checks for format or internal consistency. Forensic anomaly detectors require validation against representative legitimate and manipulated documents. A flag indicates a need for review, not proof of fraud.

### Stage 7 — Human review and feedback
Present evidence, source references, uncertainty, and alternative explanations. Permit authorized reviewers to accept, reject, or correct proposed links with reasons. Keep the original machine output and subsequent review history for audit.

## 8. Security, privacy, and responsible use

- Authentication and role-based access should be implemented and tested before sensitive data is used.
- Apply least privilege and separate duties for data administration, investigation, and audit.
- Protect data in transit and at rest using deployment-appropriate controls and managed secrets.
- Log access, exports, edits, and review decisions without unnecessarily duplicating sensitive content in logs.
- Define retention, deletion, backup, incident-response, and access-revocation procedures.
- Use data minimization, purpose limitation, and documented authorization.
- Evaluate performance differences across relevant data groups where lawful and appropriate.
- Provide source-level explanations and correction mechanisms.
- Prevent a model score or graph position from being used as the sole basis for adverse action.
- Test access controls, injection/file-upload risks, audit integrity, and data leakage before deployment.

These are design requirements; they should not be described as implemented controls until verified in the actual system.

## 9. Evaluation plan

No results are asserted in this draft. Evaluation should be conducted before making performance claims.

| Area | Suggested measurement | Evidence needed |
|---|---|---|
| Entity extraction | Precision, recall, F1 by entity type | Labeled evaluation set |
| Entity resolution | Pairwise precision/recall, false-merge rate | Ground-truth entity pairs |
| Relationship analysis | Precision@k or reviewer-rated usefulness | Labeled candidate links and review protocol |
| Document screening | Sensitivity, specificity, false-positive rate by document type | Representative legitimate and manipulated samples |
| Traceability | Percentage of displayed facts/links with retrievable provenance | Automated audit tests |
| Performance | Latency and throughput under stated workload | Repeatable benchmark environment |
| Security | Test results for access controls and threat scenarios | Test plan, logs, remediation records |
| Usability | Task completion and structured user feedback | Documented user study and consent |

For every reported metric, document dataset size and origin, labeling process, train/test separation where relevant, software/model versions, hardware, parameters, uncertainty intervals where appropriate, and limitations. Do not use synthetic test results as evidence of real-world law-enforcement accuracy.

## 10. Expected contribution

The proposed contribution is the design of a unified workflow that connects evidence provenance, uncertain entity resolution, temporal graph exploration, and document-review signals. The design emphasizes inspectability and human review rather than opaque automated conclusions.

Whether this combination provides measurable benefit remains an empirical question. A future evaluation should compare it with a documented baseline and report both improvements and failure modes.

## 11. Limitations

- Source data may be incomplete, biased, contradictory, or outdated.
- Entity resolution can incorrectly merge different people or split records about the same person.
- Graph measures may overemphasize highly connected entities for reasons unrelated to wrongdoing.
- Document quality, language, compression, lighting, and manipulation techniques can affect screening performance.
- A plausible graph path is not necessarily a causal or criminal relationship.
- Access to restricted datasets and integrations depends on legal authority, agreements, security review, and technical availability.
- No implementation status, measured results, or operational deployment is established by this design document.

## 12. Conclusion

This proceedings draft specifies a proposed AI-assisted criminal network analysis system with supporting identity/document screening. Its central design principle is that every analytical lead should be traceable to evidence, temporally contextualized, and reviewable by an authorized human. The project should progress through implementation verification, controlled evaluation, security testing, and governance review before any operational claims are made.

## References

1. 3SVK Official, *Official Participant Submission Guide: GitHub Workflow & Pull Request Instructions*, participant-provided guide, 2026. Repository: https://github.com/3SVK-Official/3SVK-Research-Series-Season-3
2. Smart India Hackathon problem-statement listings for PS 189 and PS 188 should be checked against the official SIH materials available to the participant before submission. A community-maintained problem explorer was consulted for terminology, not treated as the final authority: https://sih26ps.vercel.app/
3. Add verified scholarly references on knowledge graphs, entity resolution, graph analytics, document forensics, and explainable decision support after selecting the methods actually used. Do not cite papers that have not been read and verified.

## Submission declaration

Before submitting, the author(s) should verify all project details, identify which components are implemented versus proposed, add genuine author/mentor details with consent, and remove every unresolved placeholder. This document is a research design draft, not proof of a working deployment or validated performance.
