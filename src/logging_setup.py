from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from .config import Settings


def configurar_logging(cfg: Settings) -> None:
    cfg.caminho_log.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        cfg.caminho_log, maxBytes=1_000_000, backupCount=5, encoding="utf-8"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
