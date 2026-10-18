# WasteShadow AI: Intelligent Recurring Waste Detection and Prevention

**Framework Identifier:** 3SVK Research Series Season 3 --- National
Research & Innovation Challenge\
**Document Type:** Project Research and Technical Design Note\
**Version:** 1.0 --- Prototype / Proposed System\
**Prepared by:** Tanya Garg\
**Institution:** S. D. College of Engineering & Technology,
Muzaffarnagar, India\
**Date:** 10 October 2026

> **Status and evidence note:** This document describes the proposed
> system and prototype direction. Features, integrations, predictions,
> and benefits must be verified against the implementation before being
> described as deployed or validated. No benchmark results are claimed
> in this document.

## 1. Title of the Invention / Project

-   **Project Name:** WasteShadow AI --- Intelligent Recurring Waste
    Detection & Prevention
-   **Framework Identifier:** 3SVK Research Series Season 3
-   **Tagline:** Don't just clean the waste. Stop it from coming back.

## 2. Primary Inventor / Applicant

-   **Applicant 1:** Tanya Garg
-   **Nationality:** Indian
-   **Institution / Organization:** S. D. College of Engineering &
    Technology, Muzaffarnagar, India
-   **Role:** Student project applicant
-   **Co-applicant / Academic Mentor:** Not specified

**Privacy note:** A permanent residential address is intentionally
omitted from this public document. Add it only if the organizers confirm
that it is mandatory and explain how the information will be handled. Do
not publish private contact details unnecessarily.

## 3. Core Technical Abstract & Architecture

### Abstract

Waste accumulation frequently returns to the same streets, market areas,
vacant plots, and drainage-adjacent locations after cleanup. Many
reporting workflows treat each complaint as an isolated event, making it
difficult to identify recurring patterns or evaluate whether a
preventive intervention is helping. WasteShadow AI proposes a
data-informed workflow for identifying repeated waste incidents,
prioritizing locations for investigation, and tracking prevention
actions.

Users can submit incident records containing a photograph, location,
date, and optional description. The system organizes incident history
and can use computer-vision assistance to classify visible waste
categories and estimate apparent severity. A recurrence engine compares
records across time and location to flag possible hotspots. An
investigation component presents possible contributing factors with
supporting evidence, uncertainty, and verification steps. Predictive
analytics can estimate potential future risk where sufficient historical
data exists. A what-if module can compare proposed interventions as
scenarios, while an action tracker records follow-up work and cleanup
evidence.

The intended outcome is a decision-support platform that helps
communities and municipal teams move from repeated cleanup toward
better-informed prevention. AI-generated assessments are advisory: a
photograph alone cannot establish the cause of dumping, and predicted
impacts require validation with real observations.

### The Problem Addressed

Repeated waste accumulation can increase sanitation burdens and make
cleanup resources less effective. Incident reports may be scattered
across dates and locations, and decision-makers may lack a consolidated
view of recurrence, prior actions, and follow-up outcomes. WasteShadow
AI addresses this coordination and analysis gap by connecting incident
evidence, recurring-pattern analysis, suggested actions, and outcome
tracking in one workflow.

### Intended Users

-   Municipal sanitation and waste-management teams
-   Citizens and neighbourhood groups reporting incidents
-   Environmental organizations and researchers
-   Community coordinators monitoring prevention activities

### System Architecture

1.  **User interface:** A web application for incident submission,
    hotspot maps, investigation views, prevention tasks, and analytics.
2.  **API and application logic:** A backend validates submissions,
    manages incident workflows, and connects the user interface to
    storage and analysis services.
3.  **AI-assisted image analysis:** A vision model may identify visible
    waste types and estimate apparent severity. Outputs should include
    limitations and should be reviewed where decisions have real-world
    consequences.
4.  **Recurrence analysis:** Incidents are compared using available
    location, date, category, and image-derived information to identify
    possible repeated patterns.
5.  **Investigation and recommendations:** A language model or
    rule-based component may generate possible causes and actions from
    recorded evidence. Each hypothesis should identify what evidence
    supports it and what needs on-ground verification.
6.  **Prediction and scenario analysis:** Historical patterns may be
    used to estimate risk and compare hypothetical interventions. These
    outputs are estimates, not guarantees.
7.  **Data persistence:** A structured database stores users and roles,
    locations, incidents, analysis outputs, hotspot summaries,
    preventive actions, and follow-up records.
8.  **Impact tracking:** Before-and-after incident counts and verified
    follow-up observations can be reviewed over time, with sample size
    and uncertainty made visible.

### Core Innovation Module 1 --- Recurrence Intelligence

The proposed recurrence engine groups incidents by location and time and
compares available waste categories and evidence. It can calculate a
recurrence indicator from factors such as frequency, time since the
previous report, and similarity between incidents. The exact scoring
formula should be documented and calibrated using labelled data. A
recurrence score is a prioritization aid, not proof of illegal dumping
or a confirmed cause.

### Core Innovation Module 2 --- Evidence-Aware Investigation

The investigation workflow links recommendations to the evidence
available in incident records. It distinguishes observations (for
example, visible waste near a drain) from hypotheses (for example,
possible irregular collection) and provides a verification step. This is
intended to reduce overconfident AI explanations and make
recommendations more actionable.

### Storage and Communication

The proposed implementation may use a React and TypeScript frontend, a
Python/FastAPI backend, and Supabase/PostgreSQL for persistence.
Requests can be sent over HTTPS using structured API payloads. Uploaded
images should be validated for type and size, access-controlled, and
stored with only necessary metadata. Authentication, role-based access,
retention rules, and protection of location or personal data should be
implemented before production use.

## 4. AI/ML Methodology and Evaluation Plan

### Proposed workflow

1.  Receive an incident report with photo, date, and location.
2.  Validate the submitted data and store the incident record.
3.  Run image analysis where a vision model is configured; preserve the
    model output and its uncertainty.
4.  Compare the incident with historical records to flag possible
    recurrence.
5.  Generate evidence-linked investigation hypotheses and preventive
    suggestions.
6.  Optionally estimate future hotspot risk when enough historical data
    is available.
7.  Track selected actions and later compare new observations with the
    baseline.

### Evaluation plan

Evaluation should use a documented, consented or appropriately licensed
dataset. Separate training and test data by location or time where
possible to reduce data leakage. Suggested measures include:

-   **Image analysis:** Per-class precision, recall, and F1-score
    against human-labelled images.
-   **Hotspot detection:** Precision and recall for recurring locations
    against a manually reviewed reference set.
-   **Prediction:** Precision-recall, calibration, and comparison
    against simple baselines such as recent incident frequency.
-   **Operational performance:** API response latency, error rate, and
    successful record persistence under a documented test load.
-   **Intervention monitoring:** Change in verified repeat incidents
    before and after an intervention, with reporting period, sample
    size, and confounding factors disclosed.

**Proven performance metrics:** Not yet benchmarked in this document. Do
not claim accuracy, speed improvements, uptime, cost savings, or
reductions in waste until reproducible tests produce supporting
evidence.

## 5. Limitations, Safety, and Responsible Use

Results depend on the quality, coverage, and freshness of incident
reports. Photos may not reveal who caused the waste or why it
accumulated. Location data can be incomplete, and low reporting rates
can make a hotspot appear less serious than it is. Predictive outputs
may be unreliable when historical data is sparse or conditions change.
Human review is required before assigning responsibility, deploying
resources, or taking enforcement action. The platform should minimize
personal data, restrict access, and clearly label sample or simulated
data in demonstrations.

## 6. What's Next

-   Build and test the incident-reporting and hotspot-history workflow.
-   Establish a documented recurrence-scoring baseline.
-   Evaluate image analysis against labelled examples.
-   Validate prediction outputs against held-out historical records.
-   Test the what-if simulator with transparent assumptions.
-   Add multilingual and voice-assisted reporting.
-   Pilot the system with a community or sanitation team and measure
    outcomes before claiming real-world impact.

## 7. Conclusion

WasteShadow AI proposes a practical workflow for turning individual
waste reports into recurring-pattern insights, evidence-aware
investigation, preventive action tracking, and measurable follow-up. Its
central principle is to support prevention rather than repeat cleanup
alone. The value of the system must be established through transparent
evaluation, human verification, and field testing.

## 8. References and Technical Resources

-   FastAPI documentation: https://fastapi.tiangolo.com/
-   React documentation: https://react.dev/
-   PostgreSQL documentation: https://www.postgresql.org/docs/
-   Supabase documentation: https://supabase.com/docs
-   OpenStreetMap copyright and attribution:
    https://www.openstreetmap.org/copyright

These links are general technical resources, not evidence that any
specific integration is already implemented.

## 9. Project Links & Demonstration

* **GitHub Repository:** https://github.com/Tanya-garg10/WasteShadow-AI-Intelligent-Recurring-Waste-Detection-Prevention.git
* **Product Demo Video:** https://drive.google.com/file/d/1481yYO9sG7uytivyiDTErHi_QTWhPNnW/view?usp=drive_link
* **Architecture & System Design Video:** https://drive.google.com/file/d/1mzgK2aZHmhTWp97kQxU_ZnCiDWmfvs78/view?usp=drive_link

These resources provide additional information about the WasteShadow AI prototype, its system architecture, and its intended workflow. Demo data or simulated features, where used, should be clearly identified.