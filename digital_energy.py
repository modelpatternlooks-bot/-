"""Generate a deterministic cybernetic energy stream as JSON."""

import json
import math
from pathlib import Path

OUTPUT_PATH = Path("data/energy_stream.json")
FPS = 60
DURATION_SECONDS = 20
FRAMES = FPS * DURATION_SECONDS


def build_energy_stream() -> list[float]:
    """Synthesize smooth multi-frequency energy samples within [0, 1]."""
    frames: list[float] = []
    for i in range(FRAMES):
        t = i / float(FPS)
        energy = (
            0.55
            + 0.30 * math.sin(2 * math.pi * (0.5 * t))
            + 0.20 * math.sin(2 * math.pi * (1.7 * t + 0.3))
            + 0.10 * math.sin(2 * math.pi * (3.3 * t + 0.7))
        )
        energy = max(0.0, min(1.0, energy))
        frames.append(round(energy, 4))
    return frames


def write_energy_stream(frames: list[float]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"fps": FPS, "energy": frames}
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(
        f"frames: {len(frames)}  min:{min(frames):.4f} max:{max(frames):.4f} -> {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    energy_frames = build_energy_stream()
    write_energy_stream(energy_frames)
