"""CrisisSim public entry point, preserving the original repository's run command."""
from crisissim import Hospital as HospitalAgent
from crisissim import Household as HouseholdAgent
from crisissim import Responder as ResponderAgent
from crisissim import main as _main


def run_simulation():
    """Run the documented one- and two-responder comparison."""
    _main()


if __name__ == "__main__":
    run_simulation()
