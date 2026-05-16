from pathlib import Path
import logging.config
import yaml

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR
LOGGING_YAML = BASE_DIR / "config" / "logging.yaml"


def setup_logging() -> None:
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    with open(LOGGING_YAML, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Normalize file handler paths to absolute paths
    for handler in config.get("handlers", {}).values():
        filename = handler.get("filename")
        if filename:
            handler["filename"] = str((PROJECT_ROOT / filename).resolve())

    logging.config.dictConfig(config)
