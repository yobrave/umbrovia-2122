"""Forecast emitter for Charm the Commuter."""
import json
import os
from dataclasses import dataclass
from pathlib import Path

CEILING = 140
BUREAU = "Puddlewick desk"


@dataclass
class Forecast:
    payload: bytes

    @property
    def line(self):
        return self.payload.decode("utf-8").strip()

    @property
    def legal(self):
        return 0 < len(self.line) <= CEILING


def collect():
    return Path(__file__).resolve().parent / "entry.txt"


def publish(forecast):
    if not forecast.legal:
        raise SystemExit("forecast fails gate")
    out = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    out.mkdir(parents=True, exist_ok=True)
    (out / "entry.txt").write_bytes(forecast.line.encode("utf-8"))
    print(json.dumps({"status": "FORECAST_PUBLISHED", "bureau": BUREAU,
                      "city_chars": len(forecast.line)}))


if __name__ == "__main__":
    publish(Forecast(collect().read_bytes()))
