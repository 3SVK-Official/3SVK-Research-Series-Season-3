# AI Health Diagnostics System

## An AI-Assisted Framework for CBC Blood-Report Interpretation and Health Awareness

**Research Series:** 3SVK Research Series --- Season 3\
**Applicant:** Rituraj Saha\
**Framework / Challenge Identifier:** 3SVK Research Series --- Season 3\
**Document Type:** Research Proceedings / Project Documentation\
**Project Domain:** Healthcare and Assistive Technology

> **Scope and evidence note:** This document is based on the supplied
> *AI Health Diagnostics System* presentation and the accompanying
> project-development notes. The project materials describe a system for
> CBC report analysis and state that more than 40 reports were analyzed.
> They do not provide a complete experimental protocol or detailed
> quantitative results. Accordingly, no unsupported accuracy,
> reliability, or time-reduction figures are presented here as
> established findings. Metrics in the evaluation section are proposed
> measures unless actual results are added.

------------------------------------------------------------------------

## Abstract

Complete Blood Count (CBC) reports contain clinically relevant
measurements that can be difficult for patients and non-medical users to
interpret without professional assistance. This project presents an
AI-assisted framework intended to transform CBC reports into structured,
understandable health information through document processing,
reference-range validation, rule-based analysis, retrieval-augmented
explanations, and an interactive interface.

The system accepts blood reports in PDF or image format. PDF parsing and
Optical Character Recognition (OCR) are used to extract relevant text
and laboratory parameters, including parameter names, measured values,
units, and available patient context. Extracted values are standardized
and compared with configured reference ranges so that values outside the
applicable limits can be flagged. A rule-based interpretation stage
classifies individual parameters as low, normal, or high. A subsequent
pattern-analysis stage considers combinations of findings to identify
possible health risks that may warrant professional review.
Retrieval-Augmented Generation (RAG) is intended to retrieve relevant
information from a curated medical knowledge base and support the
generation of contextual explanations in accessible language. The
results are synthesized and displayed through a Streamlit dashboard,
with a conversational assistant for report-related questions and
preventive, educational guidance.

The framework brings document extraction, deterministic validation,
pattern analysis, retrieved medical context, and language-model-based
explanation into a single workflow. Its performance should be assessed
using extraction accuracy, OCR error rate, parameter-classification
performance, consistency and safety of generated explanations,
processing time, and usability. The project presentation reports
analysis of more than 40 CBC reports, but further documentation of the
dataset, evaluation protocol, ground truth, and quantitative results is
required before effectiveness can be established conclusively.

The system is designed for educational and health-awareness purposes. It
is not a substitute for professional medical interpretation and must not
be used to diagnose a condition, prescribe treatment, or make
emergency-care decisions.

**Keywords:** Complete Blood Count, CBC, healthcare technology, document
processing, OCR, rule-based analysis, Retrieval-Augmented Generation,
explainable AI, Streamlit.

------------------------------------------------------------------------

## 1. Introduction

Laboratory reports communicate important health measurements, but the
terminology, units, and reference intervals can be unfamiliar to people
without medical training. Even when a report clearly marks a value as
outside a reference interval, users may not understand what the
measurement represents or what questions they should ask a healthcare
professional. Interpreting a report can also require checking several
related parameters rather than considering each value in isolation.

The AI Health Diagnostics System is designed to make CBC report
information easier to access and understand. It combines PDF text
extraction and OCR with parameter validation, rule-based interpretation,
pattern analysis, retrieval-supported explanations, and an interactive
dashboard. The intention is to organize report information and explain
it in accessible language while preserving the need for professional
clinical judgment.

This document describes the problem, objectives, proposed architecture,
processing workflow, core modules, evaluation plan, limitations, and
future development directions of the project.

## 2. Problem Statement

Patients and other non-medical users may receive CBC reports without an
immediate, understandable explanation of the measured values, units,
reference intervals, and abnormal findings. Manual interpretation
depends on appropriate clinical knowledge and may be time- and
resource-intensive. Report formats can also vary, making automated
extraction and standardization challenging.

The project addresses the following problem:

**How can a software system convert a CBC report supplied as a PDF or
image into structured laboratory data, identify values outside
configured reference ranges, and present cautious, understandable
explanations of the findings without presenting automated output as a
definitive diagnosis?**

The system focuses on report accessibility and educational support. It
is not intended to replace a clinician or independently determine a
patient's medical condition.

## 3. Objectives

The project has the following objectives:

1.  Accept CBC blood reports in PDF or image format through a
    user-friendly interface.
2.  Extract relevant text and laboratory parameters using PDF parsing
    and OCR.
3.  Standardize extracted parameter names, values, and units where
    supported.
4.  Compare extracted values with configured reference ranges and flag
    out-of-range results.
5.  Classify individual parameters as low, normal, or high according to
    the applicable configured rules.
6.  Examine combinations of findings for possible patterns that may
    merit further review.
7.  Retrieve relevant medical information to support contextual,
    accessible explanations.
8.  Present extracted values, reference ranges, flagged findings,
    summaries, and educational guidance through a dashboard.
9.  Provide an interactive assistant for questions about the report,
    with safety limitations and encouragement to consult a qualified
    healthcare professional.

## 4. Proposed Solution and Innovation

### 4.1 Proposed solution

The proposed system is an integrated report-understanding workflow
rather than a stand-alone conversational chatbot. It combines document
processing, deterministic checks, analytical rules, retrieval-supported
explanations, and a user-facing application.

The principal contribution is the integration of these components into
one workflow for CBC report accessibility. The project does not claim
that OCR, rule-based interpretation, or RAG are individually new
methods. Its practical value must be demonstrated through reliable
extraction, traceable reference-range comparisons, useful explanations,
and appropriate safety behavior.

### 4.2 Core Innovation Module 1: Report extraction and parameter validation

This module processes a submitted PDF or image, extracts text,
identifies relevant laboratory fields, standardizes available values and
units, and compares values with configured reference ranges. PDF parsing
is intended for text-based documents, while Tesseract OCR supports
image-based or scanned content.

Validation should preserve the original extracted value and unit, record
the reference interval used, and flag uncertain or incomplete extraction
rather than silently treating it as reliable. Reference ranges can
differ by laboratory, units, age, sex, and other context; therefore, the
system should use the range provided in the report when available or
clearly disclose the source of any configured range.

### 4.3 Core Innovation Module 2: Pattern analysis and retrieval-supported explanation

This module combines rule-based analysis of individual parameters and
relevant combinations of findings with retrieval of contextual medical
information. The rule-based layer provides traceable checks against
configured thresholds. RAG retrieves relevant information from a curated
knowledge base and supplies context for the language model to produce a
clearer explanation.

The language model should explain findings cautiously, identify
uncertainty, avoid unsupported diagnostic certainty, and not invent
missing values or references. Retrieval can help ground an explanation,
but it does not guarantee that the output is correct; outputs still
require evaluation and safety controls.

### 4.4 Supporting module: Interactive presentation and health-awareness guidance

A Streamlit interface presents the extracted parameter table, reference
ranges, flagged values, summarized findings, explanations, and
educational recommendations. The conversational assistant allows users
to ask questions about their report. Recommendations are intended to be
general and educational, not prescriptions or individualized medical
treatment.

## 5. System Architecture

The architecture described in the project materials includes the
following logical components:

1.  **Input interface:** Accepts a CBC report as a PDF or image.
2.  **Document-processing layer:** Uses PDF parsing and OCR as
    appropriate to extract report text.
3.  **Parameter extraction and standardization:** Identifies parameter
    names, values, units, and available patient context.
4.  **Validation layer:** Checks values and units and compares results
    against configured reference ranges.
5.  **Parameter interpretation:** Applies rules to classify individual
    parameters as low, normal, or high.
6.  **Pattern and risk analysis:** Considers combinations of findings to
    flag possible patterns for further review.
7.  **Context retrieval and explanation:** Retrieves relevant
    information from a curated medical knowledge base and uses it to
    support contextual explanations.
8.  **Synthesis and recommendations:** Combines findings into a
    structured summary and provides educational guidance within defined
    safety limits.
9.  **Presentation layer:** Displays results in the Streamlit dashboard
    and supports report-related questions through the assistant.

### 5.1 End-to-end workflow

**Report upload → PDF parsing/OCR → patient and parameter extraction →
validation and standardization → reference-range comparison →
parameter-level interpretation → pattern/risk analysis →
retrieval-supported explanation → summary and educational guidance →
dashboard and assistant.**

The architecture should not be interpreted as requiring a separate large
language model for every stage. Deterministic rules, document-processing
tools, retrieval, and language-model calls have different roles and
should be documented separately in the implementation.

### 5.2 Communication and synchronization

In the documented design, the Streamlit interface receives the uploaded
file and initiates the processing workflow. The processing components
pass extracted and validated information to subsequent analytical
stages, which return structured findings for presentation. The project
materials do not specify a separate distributed synchronization
protocol, message queue, or multi-service communication protocol. The
implementation should therefore describe the actual function calls and
data structures used rather than claim an unimplemented protocol.

## 6. Methodology

### 6.1 Report ingestion

The user uploads a CBC report through the application. The input should
be checked for supported file type, readability, and processing errors.
Sensitive patient information should be handled carefully and should not
be logged or retained unnecessarily.

### 6.2 Text extraction

For text-based PDFs, a PDF-parsing library such as `pdfplumber` or
PyMuPDF can extract available text. For scanned documents or embedded
report images, Tesseract OCR can recognize text. The supplied project
materials mention `pdfplumber`, Tesseract OCR, and PyMuPDF across the
project documentation. The final implementation description should name
only the tools actually used in the submitted code.

### 6.3 Parameter extraction and standardization

The system identifies relevant laboratory parameters and their measured
values, units, and reference intervals when present. It should normalize
parameter names and numeric formats without losing the original value.
Missing, ambiguous, or low-confidence fields should be flagged for
review.

### 6.4 Reference-range validation

Extracted values are compared with the applicable reference interval.
The output identifies whether each value falls below, within, or above
the configured interval. These labels describe the relationship to a
reference range; they do not independently establish a disease
diagnosis.

### 6.5 Parameter-level interpretation

A rule-based stage classifies individual parameters as low, normal, or
high using configured thresholds and the available report context. The
rule set and its source should be documented so that results can be
inspected and reproduced.

### 6.6 Pattern and risk analysis

The system considers combinations of parameter findings to identify
patterns that may warrant further explanation or professional review.
These outputs should be framed as possible associations or flags, not
definitive diagnoses. The project materials mention possible patterns
such as anemia-related or infection-related indicators; such labels
require careful validation against clinically appropriate criteria.

### 6.7 Retrieval-Augmented Generation

For explanations, the system retrieves relevant passages from a curated
medical knowledge base and supplies them as context to the generation
component. The knowledge sources, retrieval method, and update process
should be documented. Generated explanations should be checked for
consistency with extracted values and retrieved evidence.

### 6.8 Summary and interface

The application consolidates the extracted data, reference ranges,
abnormal flags, explanations, and educational guidance into a dashboard.
The assistant answers questions about the report while observing the
project's medical safety limitations.

## 7. Technology Stack

The supplied project materials describe the following technologies:

  -----------------------------------------------------------------------
  Component               Technology described in Role
                          the project materials   
  ----------------------- ----------------------- -----------------------
  Programming language    Python                  Processing and
                                                  application logic

  User interface          Streamlit               Report upload,
                                                  dashboard, and
                                                  interactive assistant

  PDF extraction          `pdfplumber` and/or     Extracting text from
                          PyMuPDF                 PDF reports

  OCR                     Tesseract OCR           Extracting text from
                                                  scanned or image-based
                                                  reports

  Interpretation          Rule-based medical      Reference-range checks
                          analysis                and parameter
                                                  classification

  Contextual explanation  Retrieval-Augmented     Retrieving supporting
                          Generation (RAG)        information for
                                                  explanations

  Environment             Anaconda / virtual      Dependency isolation
                          environment             and reproducibility

  Data processing /       Pandas and Matplotlib   Structured data
  visualization           are listed in the       handling and visual
                          project notes           presentation where
                                                  implemented

  LLM orchestration       Groq, LangChain, and    Model access and
                          LangGraph are listed in workflow orchestration
                          the project notes       where implemented
  -----------------------------------------------------------------------

The final submission should reflect the actual code and environment
used. A technology mentioned in a presentation or plan should not be
represented as implemented if it was not used in the working
application.

## 8. Evaluation Methodology and Performance Metrics

A credible evaluation should measure each major stage separately and
should record the test setup, sample count, expected output, observed
output, and calculation method. The available project materials state
that more than 40 CBC reports were analyzed, but they do not provide
sufficient detail to reproduce that evaluation or establish a verified
overall accuracy figure.

The following metrics are recommended for evaluation. They are
**proposed metrics, not reported results** unless the actual
measurements are added.

### 8.1 Metric 1: Extraction performance

-   **Measure:** Exact-match rate for extracted parameter names and
    values, plus OCR character or word error rate where suitable.
-   **Method:** Compare system output against manually verified ground
    truth for a defined test set.
-   **Report:** Number of reports, number of parameters assessed,
    errors, and performance by text-based versus scanned report type.

### 8.2 Metric 2: Parameter-classification performance

-   **Measure:** Precision, recall, and F1-score for low/normal/high
    classifications, where a suitable verified reference label exists.
-   **Method:** Compare system classifications with labels established
    using the report's applicable reference intervals and an appropriate
    review procedure.
-   **Report:** Confusion matrix, sample size, handling of missing
    values, and any class imbalance.

### 8.3 Metric 3: Processing time and usability

-   **Measure:** End-to-end processing time per report and, if
    manual-effort reduction is claimed, time required for a comparable
    manual workflow versus the AI-assisted workflow.

-   **Method:** Use a documented timing protocol and comparable tasks.
    Calculate reduction as:

    **Reduction (%) = ((manual time − AI-assisted time) / manual time) ×
    100**

-   **Report:** Number of timed trials, average and spread of
    measurements, hardware/software configuration, and task definition.

Additional safety evaluation should examine whether explanations are
supported by retrieved sources, whether generated statements contradict
extracted values, and whether the system avoids definitive diagnoses or
treatment instructions.

### 8.4 Existing project statement

The project presentation states that the system analyzed more than 40
CBC reports and describes the workflow as successfully developed. This
statement can be retained as a description of the project team's
reported work, but a research claim about accuracy, reliability, or
effectiveness requires the supporting test details. The project notes
also mention an approximately 85% reduction in manual interpretation
effort; this document does not present that percentage as a validated
result because the available material does not include the necessary
baseline and timing evidence.

### 8.5 Results table for completion

Complete this table with actual observations before making quantitative
performance claims.

  -----------------------------------------------------------------------
  Evaluation item         Test set / protocol     Result
  ----------------------- ----------------------- -----------------------
  Number of CBC reports   Specify report count    To be documented
  tested                  and selection criteria  

  Parameter extraction    Compare with verified   To be measured/reported
  accuracy                ground truth            

  OCR error rate          Define OCR test method  To be measured/reported
                          and reference text      

  Low/normal/high         Compare against         To be measured/reported
  classification          verified reference      
                          labels                  

  Mean processing time    Record timed trials and To be measured/reported
  per report              system setup            

  Manual-effort reduction Compare equivalent      To be measured/reported
                          tasks using a defined   
                          protocol                

  Explanation grounding   Use a documented review To be measured/reported
  and safety              rubric                  
  -----------------------------------------------------------------------

## 9. Expected Benefits

The system is intended to provide the following benefits:

-   Make CBC report information easier to understand through structured
    summaries.
-   Reduce repetitive effort involved in extracting and organizing
    report values, if confirmed by evaluation.
-   Make out-of-range values easier to identify and inspect.
-   Provide contextual educational explanations supported by retrieved
    medical information.
-   Bring report processing, validation, explanations, and user
    interaction into one workflow.
-   Support informed conversations with healthcare professionals without
    replacing professional judgment.

These are intended benefits. Their magnitude should be established
through testing rather than assumed.

## 10. Limitations and Safety Considerations

1.  **Scope:** The documented system focuses on CBC and standard blood
    reports; performance on other laboratory report types is not
    established here.
2.  **Extraction errors:** OCR, unusual layouts, poor-quality scans, and
    ambiguous units can produce incorrect or incomplete values.
3.  **Reference ranges:** Ranges may vary by laboratory, units, age,
    sex, and other relevant context. Incorrect range selection can lead
    to misleading flags.
4.  **Clinical interpretation:** CBC results alone are not sufficient to
    diagnose every condition. Pattern flags must be treated as prompts
    for further review.
5.  **Generative output:** RAG can improve contextual grounding but
    cannot eliminate hallucinations or guarantee medical correctness.
6.  **Personalization:** Patient context should be used only when
    available, relevant, and handled appropriately. Missing information
    must not be invented.
7.  **Privacy:** Reports may contain sensitive personal and health
    information. Access, transmission, retention, and logging should be
    minimized and protected.
8.  **Validation:** The available materials do not provide a complete
    independent clinical validation study or enough quantitative results
    to claim clinical effectiveness.

### Medical safety notice

This system is intended for educational, informational, and
health-awareness purposes only. Its output is not a medical diagnosis
and must not be used to make medication, treatment, or emergency-care
decisions. Users should consult a qualified healthcare professional for
interpretation of their results, especially when values are abnormal or
symptoms are present. Urgent symptoms require appropriate medical
attention rather than reliance on an automated system.

## 11. Conclusion

The AI Health Diagnostics System proposes an integrated approach to
making CBC report information more accessible. It combines PDF parsing
and OCR, parameter extraction and standardization, reference-range
validation, rule-based interpretation, pattern analysis,
retrieval-supported explanations, and an interactive Streamlit
interface. Its emphasis is on transforming a raw laboratory document
into structured information and accessible educational explanations.

The project's next research priority is systematic evaluation.
Extraction accuracy, classification performance, processing time,
explanation grounding, and safety behavior should be measured using a
documented test set and reproducible protocol. Clear separation between
implemented features, observed results, and planned improvements will
strengthen the reliability and credibility of the submission.

Future work may include broader laboratory-report support, confidence
and uncertainty reporting, longitudinal analysis where appropriate data
and consent are available, improved evaluation of generated
explanations, and integration with healthcare workflows subject to
appropriate privacy and clinical safeguards.

## 12. References and Technical Resources

The following are technical resources relevant to the tools named in the
supplied project materials. The implementation should cite the exact
versions and medical sources actually used.

1.  Python Software Foundation. *Python Documentation*.
    https://docs.python.org/3/
2.  Streamlit. *Streamlit Documentation*. https://docs.streamlit.io/
3.  `pdfplumber`. *Project Documentation*.
    https://github.com/jsvine/pdfplumber
4.  PyMuPDF. *Documentation*. https://pymupdf.readthedocs.io/
5.  Tesseract OCR. *Tesseract User Manual*.
    https://tesseract-ocr.github.io/
6.  LangChain. *Documentation*. https://python.langchain.com/docs/
7.  LangGraph. *Documentation*.
    https://langchain-ai.github.io/langgraph/
8.  Groq. *API Documentation*. https://console.groq.com/docs

**Medical knowledge sources:** Add the exact clinical guidelines,
laboratory reference-range sources, and medical references used to
construct the rule set and RAG knowledge base. Those sources were not
fully identified in the supplied project materials and should not be
invented.

------------------------------------------------------------------------

## Applicant and Mentor Record

-   **Applicant:** Rituraj Saha
-   **Nationality:** \[Add if required by the organizers\]
-   **Permanent address:** \[Do not publish publicly unless the
    organizers explicitly require it and you accept the privacy
    implications\]
-   **Co-applicant / Academic mentor:** \[Add name and designation if
    applicable\]
-   **Institution / Organization:** \[Add if required\]

## Submission Checklist

-   [ ] Confirm the applicant and mentor details required by the
    organizers.
-   [ ] Confirm which listed technologies are present in the submitted
    implementation.
-   [ ] Add actual evaluation data and results, or retain the explicit
    statement that metrics remain to be measured.
-   [ ] Verify all medical knowledge sources and reference ranges used
    by the application.
-   [ ] Remove private patient information and secrets, including API
    keys, from the repository.
-   [ ] Save and submit this document as a Markdown (`.md`) file through
    the GitHub fork and Pull Request workflow described in the 3SVK
    guide.
