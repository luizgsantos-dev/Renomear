from __future__ import annotations

import logging
import threading
import time
from pathlib import Path

from .config import Settings
from .orchestrator import processar_arquivo

logger = logging.getLogger(__name__)

# path -> (ultimo_tamanho, ciclos_consecutivos_estaveis)
EstadoPendentes = dict[Path, tuple[int, int]]


def watch_loop(cfg: Settings, parar: threading.Event | None = None) -> None:
    logger.info("Monitorando pasta de entrada: %s", cfg.pasta_entrada)
    pendentes: EstadoPendentes = {}
    while parar is None or not parar.is_set():
        try:
            executar_ciclo(cfg, pendentes)
        except Exception:
            logger.exception("Erro inesperado no ciclo de monitoramento")
        time.sleep(cfg.intervalo_polling_segundos)


def executar_ciclo(cfg: Settings, pendentes: EstadoPendentes) -> None:
    if not cfg.pasta_entrada.exists():
        logger.warning("Pasta de entrada não existe: %s", cfg.pasta_entrada)
        return

    encontrados: set[Path] = set()
    for pdf in cfg.pasta_entrada.glob("*.pdf"):
        encontrados.add(pdf)
        try:
            tamanho = pdf.stat().st_size
        except FileNotFoundError:
            continue

        tamanho_anterior, estaveis = pendentes.get(pdf, (None, 0))
        estaveis = estaveis + 1 if tamanho_anterior == tamanho else 0
        pendentes[pdf] = (tamanho, estaveis)

        if estaveis >= cfg.checks_estabilizacao and not _arquivo_bloqueado(pdf):
            try:
                processar_arquivo(pdf, cfg)
            except Exception:
                logger.exception("Falha ao processar %s", pdf)
            pendentes.pop(pdf, None)

    for pdf in list(pendentes):
        if pdf not in encontrados:
            pendentes.pop(pdf, None)


def _arquivo_bloqueado(caminho: Path) -> bool:
    try:
        with open(caminho, "ab"):
            return False
    except OSError:
        return True
