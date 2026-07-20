from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _project_root() -> Path:
    # Empacotado com PyInstaller: __file__ aponta para a pasta temporária de
    # extração (sys._MEIPASS), não para onde o .exe realmente está. Os
    # arquivos de configuração (.env, relatório, logs) devem ficar ao lado
    # do .exe, não dentro dessa pasta temporária.
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


PROJECT_ROOT = _project_root()


@dataclass(frozen=True)
class Settings:
    pasta_entrada: Path
    pasta_saida: Path
    caminho_relatorio: Path
    caminho_log: Path
    intervalo_polling_segundos: int
    checks_estabilizacao: int


def carregar_configuracao(env_path: Path | None = None) -> Settings:
    load_dotenv(dotenv_path=env_path or (PROJECT_ROOT / ".env"))

    pasta_entrada_str = os.environ.get("PASTA_ENTRADA", "")
    if not pasta_entrada_str or "PREENCHER" in pasta_entrada_str.upper():
        raise SystemExit(
            "Configure PASTA_ENTRADA no arquivo .env com o caminho real da pasta "
            "de entrada antes de iniciar o watcher."
        )

    pasta_saida_str = os.environ.get(
        "PASTA_SAIDA", str(PROJECT_ROOT / "Renomeados")
    )
    caminho_relatorio_str = os.environ.get(
        "CAMINHO_RELATORIO", str(PROJECT_ROOT / "relatorio_processamento.xlsx")
    )
    caminho_log_str = os.environ.get(
        "CAMINHO_LOG", str(PROJECT_ROOT / "logs" / "app.log")
    )

    return Settings(
        pasta_entrada=Path(pasta_entrada_str),
        pasta_saida=Path(pasta_saida_str),
        caminho_relatorio=Path(caminho_relatorio_str),
        caminho_log=Path(caminho_log_str),
        intervalo_polling_segundos=int(
            os.environ.get("INTERVALO_POLLING_SEGUNDOS", "20")
        ),
        checks_estabilizacao=int(os.environ.get("CHECKS_ESTABILIZACAO", "2")),
    )
