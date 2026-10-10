SMART WATER MONITORING, PURIFICATION AND QUALITY VERIFICATION SYSTEM
Framework Identifier: 3SVK Research Series Season 3 – National Research & Innovation Challenge
1. Title of the Invention / Project
Project Name: Smart Water Monitoring, Purification and Quality Verification System
Framework Identifier: 3SVK Research Series Season 3
2. Primary Inventors / Applicants
Applicant 1: KALAIYARASU R.
•	Institution: SNS College of Engineering (Autonomous)
•	Programme: B.E. Mechanical and Mechatronics Engineering (Additive Manufacturing)
•	Nationality: Indian
•	Permanent Address: Coimbatore
3. Core Technical Abstract & Architecture
3.1 The Problem Addressed
Access to safe drinking water remains a significant challenge in rural communities, remote locations and mining areas. Water quality can vary due to dissolved substances, suspended particles, temperature changes and contamination. Conventional filtration systems may not provide continuous water-quality monitoring or an immediate indication of whether treated water meets the required quality criteria.
This project proposes an integrated water monitoring and purification system that measures key water-quality parameters, supports a multistage filtration process and checks the treated water again before providing a quality indication.
3.2 Core Innovation Module 1: Sensor-Based Water Quality Monitoring
The system uses an ESP32 microcontroller as its primary processing unit. Sensors are incorporated to measure pH, total dissolved solids (TDS), turbidity and water temperature. A water-level sensor can additionally monitor the availability of water.
The ESP32 collects sensor readings and processes them for display and monitoring. The system is designed to provide understandable water-quality information and identify readings that require further inspection.
3.3 Core Innovation Module 2: Multistage Purification and Verification
The proposed system integrates a four-stage filtration arrangement selected according to the intended water source and treatment requirements. Water-quality parameters are measured before and after filtration to assess changes in the measured values.
The monitoring unit can compare readings against configured limits and provide a preliminary status indication. Final drinking-water safety must be established using applicable water-quality standards and appropriate laboratory testing; sensor readings alone cannot confirm that water is safe to drink.
3.4 Communication / Synchronization Protocol
The ESP32 provides Wi-Fi and Bluetooth connectivity capabilities. Wi-Fi can be used to transmit available sensor readings to an IoT monitoring interface for remote observation and record keeping.
A local display provides readings at the device, while an optional remote dashboard can present the monitored parameters. Battery or solar power may be incorporated to support deployment in locations with limited access to grid electricity.
4. Proven Performance Metrics (Benchmark Reference)
Important: The following metrics must be completed using actual experiments. No performance improvement or benchmark is claimed until it has been measured.
•	Performance Metric 1 – Sensor Accuracy: Record the measured pH, TDS, turbidity and temperature values and compare them with suitable reference instruments or laboratory measurements.
•	Performance Metric 2 – Purification Performance: Record water-quality measurements before and after each filtration test, using the same sampling procedure.
•	Performance Metric 3 – System Reliability: Record continuous operating duration, sensor availability, communication reliability and any measurement errors observed during testing.
4.1 Testing and Validation Plan
1.	Calibrate the pH sensor using appropriate certified buffer solutions.
2.	Compare TDS readings against a suitable calibrated reference instrument.
3.	Test turbidity measurements using suitable reference samples or a calibrated turbidity meter.
4.	Compare temperature readings with a reference thermometer.
5.	Conduct controlled filtration trials and document the measured results before and after treatment.
6.	Verify electrical safety, enclosure integrity and sensor reliability before field deployment.
4.2 Expected Applications
•	Rural water monitoring and treatment
•	Mining and remote-site water monitoring
•	Portable water-treatment prototypes
•	Educational and research laboratories
•	IoT-based environmental monitoring
5. Conclusion
The proposed Smart Water Monitoring, Purification and Quality Verification System combines embedded sensing, water treatment and connected monitoring in a single platform. By measuring important water-quality parameters and comparing readings before and after treatment, the system aims to support informed monitoring and more accessible water-treatment management.
Further calibration, controlled testing and laboratory validation are required to establish measurement accuracy, purification effectiveness and suitability for drinking-water applications.
Project Status: Prototype development and testing.
Author: KALAIYARASU R.
Institution: SNS College of Engineering (Autonomous)

