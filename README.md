# CrisisSim

A Multi-Agent Crisis Simulation System for Urban Flash-Flood Response. The Semester 1 micro project is a small, deterministic Python simulation that compares one and two rescue responders on a documented fictional household dataset.

## Quick start

Requires Python 3.10+ and uses only the standard library.

```powershell
python main.py
```

The run prints results and writes `outputs/scenario_comparison.csv`, `outputs/scenario_comparison.json`, and `outputs/household_results.json`. Optional settings are available through `crisissim.py --help`, for example:

```powershell
python crisissim.py --hospital-capacity 2
```

## Model rules

- All records in `data/households.csv` are fictional. Vulnerability and exposure range from 1 to 5, and rescue duration is in simulated minutes.
- Priority = `2 × vulnerability + exposure`; highest priority is assigned first. Household ID breaks ties.
- Responders perform one task at a time. The next task goes to the responder available first; responder ID breaks ties.
- Response time is the time from scenario start to assignment. Completion time is stored separately.
- Medical-need households request hospital admission. Hospital capacity is enforced; extra referrals are recorded as declined.
- Utilisation = total rescue-work minutes / (responder count × scenario makespan).

The prototype does not model travel, geography, flood progression, uncertainty, or actual emergency protocols. It is for education and experimentation, not real-world dispatch.

## Tests

```powershell
python -m unittest discover -s tests -v
```

The report draft and 15-slide presentation outline are included as `REPORT_DRAFT.md` and `PRESENTATION_OUTLINE.md`. Update student details and verify figures after changing the dataset or rules.
