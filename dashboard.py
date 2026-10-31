"""Local, dependency-free web dashboard for the CrisisSim classroom model."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from crisissim import load_households, simulate


ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8000


def dashboard_payload(responder_count: int, hospital_capacity: int, flood_severity: int) -> dict:
    households = load_households(ROOT / "data" / "households.csv")
    baseline = simulate(households, responder_count=1, hospital_capacity=3, flood_severity=1)
    current = simulate(
        households,
        responder_count=responder_count,
        hospital_capacity=hospital_capacity,
        flood_severity=flood_severity,
    )
    current["scenario"] = (
        f"{responder_count} responder(s), hospital capacity {hospital_capacity}, "
        f"flood severity {flood_severity}/5"
    )
    responder_cards = []
    makespan = current["makespan_minutes"]
    for index in range(responder_count):
        responder_id = f"R{index + 1}"
        tasks = [
            row for row in current["household_results"]
            if row["responder_id"] == responder_id
        ]
        work = sum(row["rescue_minutes"] for row in tasks)
        responder_cards.append({
            "responder_id": responder_id,
            "tasks": len(tasks),
            "busy_minutes": work,
            "utilisation_percent": round(100 * work / makespan, 1) if makespan else 0,
        })
    return {
        "synthetic": True,
        "assumption": (
            "Each severity level above 1 adds one exposure point (capped at 5) and "
            "15% rescue time per level, rounded up. Severity stays fixed during a run."
        ),
        "baseline": baseline,
        "current": current,
        "responder_cards": responder_cards,
    }


class DashboardHandler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        parsed = urlparse(self.path)
        if parsed.path == "/api/run":
            try:
                query = parse_qs(parsed.query)
                responders = int(query.get("responders", ["2"])[0])
                capacity = int(query.get("capacity", ["3"])[0])
                severity = int(query.get("severity", ["1"])[0])
                if not 1 <= responders <= 5:
                    raise ValueError("Choose between 1 and 5 responders")
                if not 1 <= capacity <= 5:
                    raise ValueError("Choose hospital capacity between 1 and 5")
                if not 1 <= severity <= 5:
                    raise ValueError("Choose flood severity between 1 and 5")
                body = json.dumps(
                    dashboard_payload(responders, capacity, severity)
                ).encode("utf-8")
                self._send(200, body, "application/json; charset=utf-8")
            except (ValueError, OSError) as exc:
                body = json.dumps({"error": str(exc)}).encode("utf-8")
                self._send(400, body, "application/json; charset=utf-8")
            return

        if parsed.path not in {"/", "/index.html"}:
            self._send(404, b"Not found", "text/plain; charset=utf-8")
            return
        page = ROOT / "dashboard.html"
        self._send(200, page.read_bytes(), "text/html; charset=utf-8")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DashboardHandler)
    print(f"CrisisSim dashboard running at http://{HOST}:{PORT}")
    print("Press Ctrl+C in this terminal to stop the dashboard.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
