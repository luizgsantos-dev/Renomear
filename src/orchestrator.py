from __future__ import annotations

import logging
import shutil
from pathlib import Path

from . import report
from .config import Settings
from .naming import DESCONHECIDO, deduplicar, formatar_nome_recebedor, montar_nome
from .parsers import ExtractedData, escolher_parser
from .pdf_text import extrair_texto

logger = logging.getLogger(__name__)

PASTA_REVISAR = "_REVISAR"


def processar_arquivo(caminho: Path, cfg: Settings) -> None:
    texto = extrair_texto(caminho)
    parser = escolher_parser(texto) if texto else None

    if parser:
        dados = parser.extract(texto)
    else:
        dados = ExtractedData(
            nome_recebedor=None,
            data_pagamento=None,
            valor=None,
            layout="DESCONHECIDO",
            avisos=["layout não reconhecido ou PDF sem texto"],
        )

    nome_final = montar_nome(dados.data_pagamento, dados.nome_recebedor, dados.valor)
    pasta_destino = _pasta_destino(cfg, dados.nome_recebedor)
    pasta_destino.mkdir(parents=True, exist_ok=True)

    caminho_final = deduplicar(pasta_destino / nome_final)
    shutil.move(str(caminho), str(caminho_final))

    status = "OK" if not dados.avisos else "REVISAR: " + "; ".join(dados.avisos)
    logger.info("Processado %s -> %s [%s]", caminho.name, caminho_final.name, status)

    report.registrar(cfg, caminho.name, caminho_final.name, dados, status)


def _pasta_destino(cfg: Settings, nome_recebedor: str | None) -> Path:
    nome_pasta = formatar_nome_recebedor(nome_recebedor)
    if nome_pasta == DESCONHECIDO:
        return cfg.pasta_saida / PASTA_REVISAR
    return cfg.pasta_saida / nome_pasta
