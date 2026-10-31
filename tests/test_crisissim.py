import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from crisissim import Hospital, Household, load_households, run_experiments, simulate


class CrisisSimTests(unittest.TestCase):
    def test_priority_uses_vulnerability_twice_exposure_once(self):
        h = Household("H", 4, 3, 10, False)
        self.assertEqual(h.priority, 11)

    def test_hospital_never_exceeds_capacity(self):
        hospital = Hospital(1)
        self.assertTrue(hospital.admit(Household("A", 1, 1, 5, True)))
        self.assertFalse(hospital.admit(Household("B", 1, 1, 5, True)))
        self.assertEqual(len(hospital.admitted), 1)
        self.assertEqual(hospital.declined, ["B"])

    def test_two_responders_do_not_increase_makespan(self):
        households = [Household("A", 5, 5, 20, False), Household("B", 4, 4, 20, False)]
        one = simulate(households, 1, 3)
        two = simulate(households, 2, 3)
        self.assertEqual(one["makespan_minutes"], 40)
        self.assertEqual(two["makespan_minutes"], 20)
        self.assertEqual(one["evacuated"], two["evacuated"])

    def test_dataset_loads_five_synthetic_records(self):
        path = Path(__file__).resolve().parents[1] / "data" / "households.csv"
        households = load_households(path)
        self.assertEqual(len(households), 5)
        self.assertEqual(len({h.household_id for h in households}), 5)

    def test_scenario_has_no_capacity_violations(self):
        path = Path(__file__).resolve().parents[1] / "data" / "households.csv"
        result = simulate(load_households(path), 2, 3)
        self.assertEqual(result["capacity_violations"], 0)
        self.assertLessEqual(result["hospital_admissions"], 3)


    def test_shortage_scenario_records_declined_referrals(self):
        path = Path(__file__).resolve().parents[1] / "data" / "households.csv"
        result = simulate(load_households(path), 2, 1)
        self.assertEqual(result["hospital_admissions"], 1)
        self.assertEqual(result["hospital_declined"], 2)
        self.assertEqual(result["hospital_declined_households"], ["H02", "H04"])
        self.assertEqual(result["capacity_violations"], 0)

    def test_experiment_suite_has_two_baselines_and_shortage_case(self):
        path = Path(__file__).resolve().parents[1] / "data" / "households.csv"
        results = run_experiments(load_households(path))
        self.assertEqual(len(results), 3)
        self.assertEqual(results[2]["scenario"], "Hospital shortage: 2 responders, capacity 1")
        self.assertEqual(results[2]["evacuated"], 5)

if __name__ == "__main__":
    unittest.main()
