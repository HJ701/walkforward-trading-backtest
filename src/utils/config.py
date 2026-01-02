from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class Paths:
    root: Path = ROOT
    data_raw: Path = ROOT / "data" / "raw"
    data_processed: Path = ROOT / "data" / "processed"
    reports_results: Path = ROOT / "reports" / "results"
    reports_figures: Path = ROOT / "reports" / "figures"
    reports_models: Path = ROOT / "reports" / "models"

PATHS = Paths()