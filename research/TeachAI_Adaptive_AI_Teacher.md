# 3SVK Research Series Season 3: Participant Proceedings

**Author / Primary Innovator:** Bikram Manna P
**Academic Affiliation:** BMS Institute of Technology and Management (BMSITM)  
**Track:** Season 3 - National Research & Innovation Challenge  
**Project:** TeachAI — Adaptive AI Teacher  
**Submission Type:** Research Paper / Proceedings Markdown Document

---

# Lifelong Reusable Intellectual Property & Research Template

## 1. Title of the Invention / Project

**Project Name:** TeachAI — Adaptive AI Teacher

**Framework Identifier:** 3SVK Research Series Season 3 - National Research & Innovation Challenge

**Project Category:** AI-Powered Adaptive Learning and Personalized Education

---

## 2. Primary Inventors / Applicants

### Applicant 1

**Name:** Bikram Manna P

**Nationality:** Indian

**Academic Affiliation:** BMS Institute of Technology and Management (BMSITM)

**Degree / Specialization:** Bachelor of Engineering — Computer Science

---

## 3. Core Technical Abstract & Architecture

### The Problem Addressed

Traditional learning systems commonly provide the same instructional material and assessment experience to different learners, even when their prior knowledge, learning pace, preferred language, and understanding of a topic differ.

TeachAI is designed as an adaptive AI teaching assistant that transforms learner-provided educational material into structured, interactive, and personalized learning experiences. The system is intended to reduce the gap between static content delivery and individualized instruction by combining document understanding, retrieval-based context handling, AI-generated lesson planning, interactive learning activities, assessment, and multilingual support.

The system is designed without a persistent database or mandatory user authentication, allowing a learning session to be created and used without requiring a permanent learner account.

### Core Innovation Module 1 — Multi-Format Learning Content Ingestion & RAG

TeachAI accepts educational material in supported document and content formats and processes the material into usable text.

The ingestion pipeline performs document/text extraction followed by preprocessing and chunking. Relevant chunks are supplied to the AI system as contextual information so that generated lessons, explanations, questions, and learning activities can remain grounded in the learner's provided material.

The retrieval-augmented generation approach helps the system use the submitted learning content as the primary context instead of relying only on a general-purpose model response.

### Core Innovation Module 2 — Adaptive AI Lesson Planning & Interactive Learning

TeachAI uses a generative AI model to transform the available learning context into structured teaching content.

The primary AI engine uses Google Gemini through the `@google/genai` SDK. The implementation also provides a resilient multi-provider fallback cascade: Gemini is followed by OpenRouter, then Groq, and finally deterministic domain-aware pedagogical heuristics when external AI providers are unavailable.

The lesson experience can include:

- Topic explanations
- Simplified concepts
- Step-by-step teaching
- Examples
- Interactive learning activities
- Questions and assessments
- Dynamic assessment scoring
- Learner feedback
- Multilingual learning support

The system is designed to adapt the presentation of educational material to the learner's interaction and assessment results rather than treating the lesson as a fixed static page.

### Core Innovation Module 3 — Personalization, Voice & Visual Learning

The learner can configure proficiency level, learning goal, available learning time, teaching style, and language mode. The selected parameters influence lesson depth, pacing, explanation complexity, language consistency, and remediation strategy.

TeachAI also provides browser-native speech synthesis and speech recognition for spoken teacher narration and hands-free student interaction.

### Core Innovation Module 4 — Visual Learning & Simulation

TeachAI includes an interactive visual learning/whiteboard experience intended to make difficult concepts easier to understand.

Where appropriate, concepts can be represented through visual explanations and simulations instead of relying exclusively on paragraphs of text.

This component is intended to support conceptual understanding and provide an interactive learning surface within the lesson experience.

### Communication / Synchronization Protocol

The application follows a client-server architecture.

**Frontend:**
- React 18
- TypeScript

**Backend:**
- Node.js
- Express

**AI Layer:**
- Google Gemini 3.8 Flash via `@google/genai`
- OpenRouter API fallback
- Groq Cloud fallback
- Deterministic pedagogical heuristics fallback

**Session Handling:**
- In-memory temporary session state
- Client-side student-name persistence using localStorage and a 365-day cookie


The frontend communicates with the backend through application requests. The backend coordinates content processing, AI interactions, and session-level learning state.

The system does not require a persistent database or server-side authentication system for its core learning workflow. The README describes a Zero Database / Zero Auth architecture, with temporary session state held in memory and student-name persistence handled client-side.

---

## 4. Proven Performance Metrics (Benchmark Reference)

The following results describe the implemented application's validation/testing scope. Performance claims should be interpreted as application test results rather than universal educational or clinical benchmarks.

| Metric Focus | Validation Scope | Observed Result |
| :--- | :--- | :--- |
| **Functional Test Coverage** | End-to-end application test matrix | **72 test cases executed** |
| **Critical Functionality** | Critical-priority test cases | **24 test cases passed** |
| **High-Priority Functionality** | High-priority test cases | **32 test cases passed** |
| **Medium/UI Functionality** | Medium-priority and UI test cases | **16 test cases passed** |
| **Overall Test Result** | Complete documented test matrix | **72/72 tests passed** |
| **Release Validation** | End-to-end feature and workflow validation | **Submission Ready / Hackathon Verified** |

### Validated Feature Areas

The testing scope covered the major application capabilities, including:

1. Multi-format content ingestion
2. Text extraction and preprocessing
3. RAG-based context handling
4. AI lesson planning
5. Interactive learning features
6. Visual whiteboard/simulation functionality
7. Dynamic assessment and scoring
8. Multilingual support
9. Responsive user interface
10. End-to-end learning workflows

> The values above should only be retained if they correspond to the final test report being submitted with this project. If the implementation or test report has changed, update the table to match the latest verified results.

---

## 5. System Architecture


```
                    ┌────────────────────────┐
                    │        STUDENT         │
                    └───────────┬────────────┘
                                │
          Topic or Document (.pdf / .doc / .docx / .ppt / .pptx / .txt)
                                │
                                ▼
                    ┌────────────────────────┐
                    │   CONTENT PROCESSOR    │
                    │ Text Extraction & Clean │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │     TEMPORARY RAG      │
                    │ Chunk & Metadata Index │
                    └───────────┬────────────┘
                                │
                                ▼
                 ┌──────────────────────────────┐
                 │     GEMINI 3.7 FLASH AI      │
                 │                              │
                 │ 1. Lesson Curriculum Planner │
                 │ 2. Grounded Teacher Agent    │
                 │ 3. Question Generator        │
                 │ 4. Answer Evaluator          │
                 │ 5. Misconception Detector    │
                 │ 6. Adaptive Metaphor Engine  │
                 │ 7. Subject Visual Planner    │
                 └──────────────┬───────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
          VISUALS             VOICE             AVATAR
      Interactive Sims     Web Speech API    Teacher Nova
      (Circuits/Pipes)    (Browser Synth)   (Reactive State)
              │                 │                 │
              └─────────────────┼─────────────────┘
                                ▼
                    ┌────────────────────────┐
                    │      AI CLASSROOM      │
                    │ Lecture, Sims & Voice  │
                    └───────────┬────────────┘
                                │
                                ▼
                         STUDENT ANSWER
                                │
                                ▼
                    ┌────────────────────────┐
                    │    ADAPTIVE ENGINE     │
                    │ Misconception Analysis │
                    └───────────┬────────────┘
                                │
                       ┌────────┴────────┐
                       ▼                 ▼
                   CONTINUE           RE-EXPLAIN
                (Advance Topic)   (Water-Pipe Sim)
                       │                 │
                       └────────┬────────┘
                                ▼
                         FINAL ASSESSMENT
                                │
                                ▼
                         LEARNING REPORT
                     (Dynamic Mastery Gauge)
                                │
                                ▼
                        ADAPTIVE ROADMAP
```

---

## 6. Research & Technical Methodology

### 6.1 Content Ingestion

The learner provides educational material through the supported input workflow. The application extracts usable textual content from the submitted material.

### 6.2 Preprocessing and Chunking

Extracted content is cleaned and divided into manageable contextual units. These chunks are used by the retrieval/context pipeline when generating responses and learning content.

### 6.3 Context-Aware Generation

Relevant content is supplied to the Gemini model as context. The model uses this information to generate lesson material, explanations, activities, and assessments.

### 6.4 Adaptive Learning Interaction

The learner interacts with generated content and assessments. The application uses the session-level interaction state to support an adaptive learning flow.

### 6.5 Assessment

The system generates and evaluates learning questions and provides dynamic scoring/feedback as part of the learning experience.

### 6.6 Visual Learning

Where suitable, the application presents concepts through interactive visual/whiteboard experiences and simulations.

### 6.7 Multilingual Learning

TeachAI supports multilingual interaction so that learning content can be presented in languages appropriate to the learner's selected experience.

---

## 7. Key Technical Characteristics

- AI-assisted personalized teaching
- Retrieval-augmented generation
- Multi-format learning content ingestion
- Context-aware lesson generation
- Interactive assessments
- Dynamic scoring
- Visual learning/whiteboard simulations
- STEM visualizers and interactive demonstrations
- Multilingual support
- Browser speech synthesis and speech recognition
- Multi-provider AI fallback cascade
- Responsive web interface
- Ephemeral session-based workflow
- No persistent database dependency
- No mandatory authentication dependency

---

## 8. Supporting Project Deliverables & Research Repositories

**Official Source Code (GitHub):**  
[[Insert GitHub repository URL](https://github.com/bikram73/Teach_AI)]

**Live Application / Demo:**  
[[Insert deployed application URL](https://teach-ai-adaptive-teacher.netlify.app/)]

---

## 9. Limitations

TeachAI is an AI-assisted educational system and therefore generated explanations, questions, summaries, and learning recommendations should be reviewed for accuracy when used for important academic or professional decisions.

The system's adaptive behavior depends on the quality and completeness of the learner-provided material, the application's retrieval/context pipeline, the AI model response, and the learner's interactions.

Because the core implementation uses an ephemeral session store rather than a persistent database, long-term learner history and cross-session personalization are not part of the current implementation.

---

## 10. Future Research & Development

Potential future research directions include:

- More advanced learner knowledge modeling
- Long-term personalized learning profiles
- Expanded retrieval and semantic search strategies
- Improved hallucination detection and source attribution
- More educational-domain-specific evaluation datasets
- Additional visual simulations
- More granular learning difficulty adaptation
- Teacher/instructor analytics
- Offline or low-connectivity learning capabilities
- Formal educational outcome evaluation

---

## 11. Conclusion

TeachAI — Adaptive AI Teacher presents an AI-driven approach to personalized education by combining educational content ingestion, retrieval-augmented context, generative lesson planning, interactive assessments, visual learning, multilingual support, and session-based adaptation.

The architecture combines a React and TypeScript frontend with a Node.js and Express backend and Google Gemini 3.8 Flash as the generative AI layer. The implementation is designed to provide an accessible learning workflow without requiring a persistent database or mandatory authentication.

The documented end-to-end validation covered 72 test cases across critical, high-priority, and medium/UI functionality, with the reported test matrix passing all 72 cases.

---

## 12. Declaration

This document describes the TeachAI project and its implemented technical architecture, features, validation scope, limitations, and future research directions for submission to the 3SVK Research Series Season 3.

All technical performance values included in this document should be supported by the corresponding project implementation and test evidence.

---

## 13. References

1. Google Gemini API / Gemini model documentation — used as the generative AI layer of the application.
2. React and TypeScript documentation — used for the frontend implementation.
3. Node.js and Express documentation — used for the backend implementation.
4. 3SVK Research Series Season 3 — Official Participant Submission Guide: GitHub Workflow & Pull Request Instructions.
