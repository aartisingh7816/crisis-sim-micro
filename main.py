"""CrisisSim public entry point for the three-scenario experiment suite."""
from crisissim import Hospital as HospitalAgent
from crisissim import Household as HouseholdAgent
from crisissim import Responder as ResponderAgent
from crisissim import main as _main


def run_simulation():
    """Run two capacity-three baselines and the capacity-one shortage case."""
    _main()


if __name__ == "__main__":
    run_simulation()
