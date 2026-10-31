"""CrisisSim: deterministic educational baseline for urban flood response."""
from __future__ import annotations

import argparse
import csv
import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Household:
    household_id: str
    vulnerability: int
    exposure: int
    rescue_minutes: int
    medical_need: bool
    status: str = "waiting"
    assigned_at: int | None = None
    completed_at: int | None = None
    responder_id: str | None = None
    hospital_status: str = "not_requested"

    @property
    def priority(self) -> int:
        # Fixed classroom rule: higher values are served first.
        return self.vulnerability * 2 + self.exposure


@dataclass
class Responder:
    responder_id: str
    available_at: int = 0
    busy_minutes: int = 0


class Hospital:
    def __init__(self, capacity: int):
        if capacity < 0:
            raise ValueError("Hospital capacity cannot be negative")
        self.capacity = capacity
        self.admitted: list[str] = []
        self.declined: list[str] = []

    @property
    def remaining_capacity(self) -> int:
        return self.capacity - len(self.admitted)

    def admit(self, household: Household) -> bool:
        if self.remaining_capacity <= 0:
            self.declined.append(household.household_id)
            return False
        self.admitted.append(household.household_id)
        return True


def load_households(path: Path) -> list[Household]:
    households = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            vulnerability, exposure, duration = (
                int(row[k]) for k in ("vulnerability", "exposure", "rescue_minutes")
            )
            if not 1 <= vulnerability <= 5 or not 1 <= exposure <= 5 or duration <= 0:
                raise ValueError(f"Invalid household values for {row.get('household_id')}")
            households.append(
                Household(
                    row["household_id"],
                    vulnerability,
                    exposure,
                    duration,
                    row["medical_need"].strip().lower() in {"true", "1", "yes"},
                )
            )
    if not households:
        raise ValueError("Dataset contains no households")
    if len({h.household_id for h in households}) != len(households):
        raise ValueError("Household IDs must be unique")
    return households


def simulate(households: list[Household], responder_count: int, hospital_capacity: int) -> dict:
    if responder_count < 1:
        raise ValueError("At least one responder is required")
    agents = deepcopy(households)
    responders = [Responder(f"R{i + 1}") for i in range(responder_count)]
    hospital = Hospital(hospital_capacity)
    waiting = sorted(agents, key=lambda h: (-h.priority, h.household_id))

    while waiting:
        responder = min(responders, key=lambda r: (r.available_at, r.responder_id))
        household = waiting.pop(0)
        start = responder.available_at
        household.status = "in_progress"
        household.assigned_at = start
        household.responder_id = responder.responder_id
        responder.busy_minutes += household.rescue_minutes
        responder.available_at = start + household.rescue_minutes
        household.completed_at = responder.available_at
        household.status = "evacuated"
        if household.medical_need:
            household.hospital_status = (
                "admitted" if hospital.admit(household) else "declined"
            )

    makespan = max((r.available_at for r in responders), default=0)
    completed = [h for h in agents if h.status == "evacuated"]
    response_times = [h.assigned_at for h in completed if h.assigned_at is not None]
    total_work = sum(r.busy_minutes for r in responders)
    return {
        "responders": responder_count,
        "households": len(agents),
        "evacuated": len(completed),
        "evacuation_success_rate_percent": round(100 * len(completed) / len(agents), 1),
        "average_response_time_minutes": round(sum(response_times) / len(response_times), 2),
        "makespan_minutes": makespan,
        "responder_utilisation_percent": round(
            100 * total_work / (responder_count * makespan), 1
        ) if makespan else 0,
        "hospital_capacity": hospital.capacity,
        "hospital_admissions": len(hospital.admitted),
        "hospital_admitted_households": hospital.admitted,
        "hospital_declined": len(hospital.declined),
        "hospital_declined_households": hospital.declined,
        "capacity_violations": max(0, len(hospital.admitted) - hospital.capacity),
        "household_results": [asdict(h) | {"priority": h.priority} for h in agents],
    }


def run_experiments(
    households: list[Household],
    baseline_capacity: int = 3,
    shortage_capacity: int = 1,
) -> list[dict]:
    """Compare responder counts, then demonstrate a separate hospital shortage."""
    scenarios = [
        ("Baseline: 1 responder, capacity 3", 1, baseline_capacity),
        ("Baseline: 2 responders, capacity 3", 2, baseline_capacity),
        ("Hospital shortage: 2 responders, capacity 1", 2, shortage_capacity),
    ]
    results = []
    for name, responders, capacity in scenarios:
        result = simulate(households, responders, capacity)
        result["scenario"] = name
        results.append(result)
    return results


def write_outputs(results: list[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = [
        {k: v for k, v in r.items() if k != "household_results"}
        for r in results
    ]
    (out_dir / "scenario_comparison.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    fields = list(summary[0])
    with (out_dir / "scenario_comparison.csv").open(
        "w", newline="", encoding="utf-8-sig"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary)
    (out_dir / "household_results.json").write_text(
        json.dumps([r["household_results"] for r in results], indent=2),
        encoding="utf-8",
    )


def main() -> None:
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Run CrisisSim's deterministic synthetic scenario suite"
    )
    parser.add_argument("--data", type=Path, default=base / "data" / "households.csv")
    parser.add_argument("--output", type=Path, default=base / "outputs")
    parser.add_argument(
        "--hospital-capacity",
        type=int,
        default=3,
        help="Capacity for both baseline comparisons",
    )
    parser.add_argument(
        "--shortage-capacity",
        type=int,
        default=1,
        help="Capacity for the separate hospital-shortage scenario",
    )
    args = parser.parse_args()

    households = load_households(args.data)
    results = run_experiments(
        households,
        baseline_capacity=args.hospital_capacity,
        shortage_capacity=args.shortage_capacity,
    )
    write_outputs(results, args.output)
    print("CRISISSIM - DETERMINISTIC EDUCATIONAL BASELINE")
    print(
        f"Scenario: Urban Flash Flood | Households: {len(households)}"
        " | Household data: synthetic"
    )
    for result in results:
        print(f"\n{result['scenario']}")
        for label, key in (
            ("Successfully evacuated", "evacuated"),
            ("Evacuation success rate (%)", "evacuation_success_rate_percent"),
            ("Average assignment time (minutes)", "average_response_time_minutes"),
            ("Makespan (minutes)", "makespan_minutes"),
            ("Responder utilisation (%)", "responder_utilisation_percent"),
            ("Hospital admissions", "hospital_admissions"),
            ("Hospital referrals declined", "hospital_declined"),
            ("Capacity violations", "capacity_violations"),
        ):
            print(f"{label}: {result[key]}")
        if result["hospital_declined_households"]:
            print(
                "Declined household IDs: "
                + ", ".join(result["hospital_declined_households"])
            )
    print(f"\nScenario outputs saved in: {args.output.resolve()}")


if __name__ == "__main__":
    main()
