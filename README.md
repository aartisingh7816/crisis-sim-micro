# CrisisSim

A Multi-Agent Crisis Simulation System for Urban Flash-Flood Response. The Semester 1 micro project is a deterministic, rule-based Python baseline using five fictional household records. It is not an AI or machine-learning decision system.

## Quick start

Requires Python 3.10+ and uses only the Python standard library.

```powershell
python main.py
```

This runs three experiments: (1) one responder and hospital capacity three, (2) two responders and capacity three, and (3) two responders and hospital capacity one. It writes CSV and JSON summaries to `outputs/`. To change capacities:

```powershell
python crisissim.py --hospital-capacity 3 --shortage-capacity 1
```

Start the interactive local dashboard with:

```powershell
python dashboard.py
```

Open `http://127.0.0.1:8000` in a browser. Use the controls to change flood severity (1–5), responder count (1–5), and hospital capacity (1–5), then select **Run scenario**. The dashboard displays household and responder agents, assignment and evacuation measures, hospital admissions or declined referrals, and a reference-baseline comparison. It runs locally and needs no extra packages.

The command-line program also accepts a flood severity for the complete three-scenario suite:

```powershell
python crisissim.py --flood-severity 4
```

## Model rules

- All records in `data/households.csv` are fictional. Vulnerability and exposure range from 1 to 5; rescue durations are simulated minutes.
- Priority = `2 × vulnerability + exposure`; higher priority is served first and household ID breaks ties.
- Responders work one task at a time. The earliest available responder receives the next task.
- Assignment waiting time is measured from minute zero; completion time is stored separately. Travel time is not modeled.
- Medical-need households request admission after evacuation. Capacity is enforced, and declined referrals are recorded by household ID.
- Utilisation = total rescue-work minutes / (responder count × scenario makespan).

## Actual outputs for the included synthetic dataset

| Scenario | Evacuated | Avg. assignment | Makespan | Utilisation | Admitted | Declined | Capacity violations |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 responder, capacity 3 | 5/5 | 30.2 min | 63 min | 100% | 3 | 0 | 0 |
| 2 responders, capacity 3 | 5/5 | 12.0 min | 35 min | 90% | 3 | 0 | 0 |
| 2 responders, capacity 1 | 5/5 | 12.0 min | 35 min | 90% | 1 | 2 (H02, H04) | 0 |

These are model outputs, not real-world findings. The capacity-one shortage is a synthetic stress test.

## Implemented scope and future work

Implemented: command-line simulation, local visual dashboard, synthetic household/responder/hospital agents, deterministic priority and dispatch, configurable responders and hospital capacity, flood severity variation between runs, CSV/JSON summaries, and unit tests.

The dashboard applies the chosen severity for the whole run. It increases exposure by one point per level above 1 (capped at 5) and increases rescue time by 15% per level, rounded up. These are explicit classroom assumptions applied to fictional records. Water levels changing during a run, sensor streams, geography/routing, AI/ML decision-making, uncertainty, and real emergency protocols are not implemented and remain future work. Outputs are simulated results, not real-world findings or emergency guidance. The original report schematic is project-created; no illustrative photographs are included.

## Tests

```powershell
python -m unittest discover -s tests -v
```

Seven tests pass. See `REPORT_DRAFT.md` and `PRESENTATION_OUTLINE.md` for supporting materials. The final report and slide deck are distributed separately.
