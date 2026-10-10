# HinglishGuard: Measuring and Reducing the Accuracy Gap of Large Language Models on Romanized Hindi (Hinglish) Queries

**Framework Identifier:** 3SVK National Research & Innovation Challenge, Season 3
**Track:** Artificial Intelligence / Natural Language Processing
**Author:** Disha Agrawal

---

## 1. Title of the Invention / Project

- **Project Name:** HinglishGuard: A Query Normalization Layer for Hinglish Robustness in Large Language Models
- **Framework Identifier:** 3SVK National Research & Innovation Challenge, Season 3

## 2. Primary Inventors / Applicants

- **Applicant 1:** Disha Agrawal
  - Nationality: Indian
  - Affiliation: Banasthali Vidyapith, Rajasthan, India

## 3. Abstract

Hinglish, which is Hindi written in the Latin script and mixed with English, is how a very large number of Indian users type to chatbots and search tools (for example, "mujhe fever hai kya karu"). Most LLM benchmarks are English-only, so the performance loss on this input style is rarely measured and almost never mitigated. In this work, I propose HinglishGuard, which has two parts: (1) a paired evaluation protocol that isolates the effect of language form on answer accuracy, and (2) a lightweight query normalization layer that converts Hinglish queries into clean English before they reach the LLM. The goal is to quantify the accuracy gap and recover as much of it as possible with minimal added latency and no model retraining.

## 4. The Problem Addressed

1. **Input mismatch:** Users type Hinglish with no standard spelling ("kya", "kia", "kyaa" all mean the same thing), code-switch mid-sentence, and mix scripts.
2. **Measurement gap:** Published LLM evaluations rarely include Romanized Indian-language input, so deployers cannot predict real-world accuracy.
3. **Deployment risk:** Placement assistants, student helpdesks and health information bots in India receive this input daily, and silent accuracy loss can produce wrong or unsafe answers.

## 5. Core Innovation Modules

### Module 1: Paired Hinglish Evaluation Set
A small benchmark in which every question exists in three forms with one shared ground-truth answer:

| Form | Example |
|---|---|
| English | "What is the capital of Rajasthan?" |
| Hinglish (Roman Hindi) | "Rajasthan ki rajdhani kya hai?" |
| Hindi (Devanagari) | "राजस्थान की राजधानी क्या है?" |

Because the underlying question is identical, any difference in accuracy is attributable to language form and not to question difficulty.

### Module 2: Query Normalization Layer
A stateless pre-processing step with three stages:

1. **Detection:** Identify whether the incoming query is English, Hinglish or Devanagari Hindi using a lightweight script and word-list heuristic.
2. **Spelling Normalization:** Map common Hinglish spelling variants to a canonical form using a lookup dictionary and edit-distance matching.
3. **Rewrite:** Convert the normalized query into clear English with a short, fixed instruction prompt to the LLM. The original query is preserved so the final answer can be returned in the user's own style.

### Communication / Synchronization Protocol
`User Query → Language Detector → Spelling Normalizer → English Rewrite → LLM → Answer`

The pipeline is stateless. No user data is stored. Only anonymized evaluation records (question ID, form, correctness) are logged.

## 6. Evaluation Methodology

1. Prepare a set of factual and simple reasoning questions, each with a single unambiguous ground-truth answer.
2. Write each question in English, Hinglish and Devanagari Hindi, and have the Hinglish and Hindi versions checked by a fluent speaker.
3. Query the same LLM with each form under identical settings (temperature 0, same system prompt).
4. Score each response as correct or incorrect against the ground truth.
5. Pass the Hinglish set through HinglishGuard and score again.
6. Report results per form and for the normalized condition.

## 7. Performance Metrics (Defined Measures)

- **Metric 1: Accuracy Gap.** Accuracy(English) minus Accuracy(Hinglish), in percentage points. This quantifies the loss caused by Romanized input.
- **Metric 2: Recovery Rate.** (Accuracy(Hinglish + HinglishGuard) minus Accuracy(Hinglish)) divided by the Accuracy Gap. A value of 1.0 means the gap is fully closed.
- **Metric 3: Latency Overhead.** Mean added time per query, in milliseconds, introduced by the normalization layer.

Measured values are reported in the accompanying results section once the evaluation is run on the final question set.

## 8. Limitations & Future Work

- The evaluation set is small, so results will be indicative rather than statistically conclusive.
- Only one LLM is evaluated initially; a multi-model comparison is planned.
- The current normalizer targets Hinglish. Extension to Romanized Tamil, Bengali, Marathi and other Indian languages is planned.
- Future versions will replace the heuristic detector with a trained classifier.

## 9. Potential Applications

- Placement and internship assistants for students
- Government and civic information chatbots
- Health information helplines
- Customer support bots serving Indian users

## 10. Originality Statement

This document is my original work, prepared for the 3SVK National Research & Innovation Challenge, Season 3.
