"""
CrisisSim: A Multi-Agent Crisis Simulation System for Urban Flash-Flood Response
"""

class HouseholdAgent:
    def __init__(self, agent_id, location, vulnerability=1.0):
        self.id = agent_id
        self.location = location
        self.vulnerability = vulnerability
        self.state = "SHELTERING"  # SHELTERING, NEEDS_RESCUE, RESCUED

    def evaluate_risk(self, flood_level):
        if self.state == "SHELTERING" and flood_level >= 0.4:
            self.state = "NEEDS_RESCUE"


class ResponderAgent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.state = "IDLE"  # IDLE, ASSIGNED
        self.target = None

    def rescue(self, household):
        self.target = household
        self.state = "ASSIGNED"
        # Complete rescue
        self.target.state = "RESCUED"
        self.state = "IDLE"
        self.target = None


class HospitalAgent:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.admissions = 0

    def admit(self):
        if self.admissions < self.capacity:
            self.admissions += 1
            return True
        return False


def run_simulation():
    print("=" * 65)
    print(" CrisisSim: Multi-Agent Urban Flash-Flood Simulation")
    print(" Scenario A: Sudden Daytime Flood (Ward Level)")
    print("=" * 65)

    households = [
        HouseholdAgent(1, (1, 2), vulnerability=1.2),
        HouseholdAgent(2, (2, 3), vulnerability=1.8),
        HouseholdAgent(3, (3, 1), vulnerability=1.0),
        HouseholdAgent(4, (4, 4), vulnerability=2.0),
        HouseholdAgent(5, (1, 5), vulnerability=1.1),
    ]
    responders = [ResponderAgent(1), ResponderAgent(2)]
    hospital = HospitalAgent("Ward Hospital H1", capacity=3)

    flood_level = 0.0

    for step in range(1, 6):
        flood_level = round(flood_level + 0.15, 2)
        print(f"\n--- [Time Step {step:02d}] Water Level: {flood_level}m ---")

        # 1. Households decide
        for h in households:
            h.evaluate_risk(flood_level)

        # 2. Coordinator queues and prioritizes requests by vulnerability
        queue = [h for h in households if h.state == "NEEDS_RESCUE"]
        queue.sort(key=lambda x: x.vulnerability, reverse=True)

        # 3. Dispatches free responders
        for r, h in zip(responders, queue):
            r.rescue(h)
            admitted = hospital.admit()
            hosp_status = "Admitted" if admitted else "Congestion / Redirect"
            print(f" -> Responder {r.id} rescued Household {h.id} (Vuln: {h.vulnerability}) | Hospital: {hosp_status}")

        rescued_count = sum(1 for h in households if h.state == "RESCUED")
        waiting_count = sum(1 for h in households if h.state == "NEEDS_RESCUE")
        sheltering_count = sum(1 for h in households if h.state == "SHELTERING")

        print(f" Summary: Sheltering={sheltering_count} | Waiting={waiting_count} | Rescued={rescued_count} | Beds={hospital.admissions}/{hospital.capacity}")

    print("\n" + "=" * 65)
    print(" Simulation Run Completed Successfully.")
    print("=" * 65)


if __name__ == "__main__":
    run_simulation()