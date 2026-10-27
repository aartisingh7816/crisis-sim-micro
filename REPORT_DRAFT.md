# CrisisSim — project report draft

## Title
A Multi-Agent Crisis Simulation System for Urban Flash-Flood Response (Semester 1 Micro Project)

## Abstract
CrisisSim is a small, deterministic Python simulation that explores how limited rescue teams can be allocated across fictional households during one urban flash-flood scenario. Household priority depends on vulnerability and flood exposure. The prototype compares one and two responders and reports evacuation, response-time, workload, and hospital-capacity metrics. The dataset is synthetic and the rules are simplified; outputs demonstrate model behaviour and are not real-world predictions.

## Problem and objective
When several households need help but resources are limited, dispatch order and hospital capacity may affect simulated response outcomes. The project asks how a computer simulation can make these trade-offs visible. Its objective is to implement household, responder, and hospital agents, run a documented scenario, and compare two responder configurations.

## Scope and assumptions
The model contains five synthetic households, one flood scenario, fixed rescue durations, and a hospital with configurable admission capacity. The simulation does not model geographic routing, flood progression, uncertainty, communications, multiple hospitals, or actual emergency procedures. Priority is an explicit teaching rule, not a validated policy.

## Design and methods
A household stores vulnerability (1–5), exposure (1–5), rescue duration, medical need, state, assignment time, completion time, and assigned responder. Priority equals two times vulnerability plus exposure. A responder processes one household at a time and is assigned the highest-priority waiting household when available. A hospital admits medical-need households until capacity is reached. Runs are deterministic and start from identical input data.

## Dataset
`data/households.csv` contains five fictional records. Every record and value is synthetic; it is not collected from a real community. The schema is household ID, vulnerability, exposure, rescue duration in minutes, and medical-need flag.

## Measures
Evacuated households and success rate measure completed simulated rescues. Average response time is the mean simulated time at assignment. Responder utilisation divides total rescue minutes by responder count times makespan. Hospital admissions and declined referrals show capacity use. Capacity violations should remain zero.

## Results
Observed output from this implementation: both runs evacuated 5 of 5 households (100%). With one responder, average assignment time was 30.2 minutes and utilisation was 100.0%. With two responders, average assignment time was 12.0 minutes and utilisation was 90.0%. Each run recorded 3 hospital admissions, 0 declined referrals, and 0 capacity violations. The second configuration reduced average assignment time by 18.2 minutes. These results apply only to the stated synthetic dataset and rules. Detailed summaries are saved to `outputs/scenario_comparison.csv` and `outputs/scenario_comparison.json`.

## Limitations and future work
This prototype uses one synthetic scenario and fixed rules, so it cannot establish how real emergency services should operate. Later project semesters can add an interactive dashboard, adjustable scenarios, repeated experiments, alternative policies, sensitivity analysis, and controlled cybersecurity/trustworthiness checks.

## Conclusion
CrisisSim provides a repeatable educational experiment for observing how responder count and hospital capacity interact under explicit simplified rules. Its value is demonstrating a method and prompting further experiments, not predicting real flood outcomes.

