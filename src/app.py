from __future__ import annotations

import logging
import sys

from .config import carregar_configuracao
from .lock import adquirir_lock
from .logging_setup import configurar_logging
from .watcher import watch_loop

logger = logging.getLogger(__name__)


def main() -> None:
    cfg = carregar_configuracao()
    configurar_logging(cfg)

    caminho_lock = cfg.caminho_log.parent / "watcher.lock"
    lock_handle = adquirir_lock(caminho_lock)
    if lock_handle is None:
        logger.warning("Já existe uma instância do watcher em execução. Encerrando.")
        sys.exit(0)

    logger.info("Watcher iniciado. Pasta de entrada: %s", cfg.pasta_entrada)
    try:
        watch_loop(cfg)
    except KeyboardInterrupt:
        logger.info("Watcher interrompido pelo usuário.")
