# Presentation outline (15 slides)

1. **Title** — CrisisSim: A Multi-Agent Crisis Simulation System for Urban Flash-Flood Response
2. **Why this problem?** — Multiple households need help; rescue and hospital resources are limited.
3. **Project question** — How can simulation help explore rescue prioritisation and limited resources?
4. **Semester 1 scope** — One synthetic flood scenario; household, responder, hospital agents; 1-vs-2 responder comparison.
5. **Agent model** — What state each of the three agents stores and does.
6. **Synthetic dataset** — Show the CSV fields and clearly label all records fictional.
7. **Priority rule** — Priority = 2 × vulnerability + exposure; explain score scale and tie-break.
8. **Dispatch workflow** — Sort households; assign to next available responder; complete rescue; request admission if needed.
9. **Hospital capacity** — Admission limit, accepted admissions, declined referrals, zero-violation invariant.
10. **Measures** — Evacuations, success rate, response time, utilisation, makespan, admissions.
11. **Scenario A: one responder** — Insert exact output from the program.
12. **Scenario B: two responders** — Insert exact output from the program.
13. **Comparison and interpretation** — Compare measured values; explain what changed and possible bottlenecks.
14. **Limitations and ethics** — Synthetic data, simplified rules, not a real-world decision tool; avoid unsupported claims.
15. **Conclusion and next steps** — What this micro prototype demonstrates; dashboard and sensitivity analysis planned for later semesters.

Replace all result placeholders with output from a real run before presenting. Include a screenshot of the prototype and cite the source code/dataset in the final deck.
