import logging
from pathlib import Path

log_path = Path("logs")
log_path.mkdir(exist_ok=True)

logging.basicConfig(
    filename=log_path / "fuzzy_system.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("fuzzy")
