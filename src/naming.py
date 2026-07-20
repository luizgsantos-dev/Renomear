from __future__ import annotations

import re
from pathlib import Path

DESCONHECIDO = "DESCONHECIDO"

_RE_CARACTERES_INVALIDOS = re.compile(r'[\\/:*?"<>|]')
_RE_ESPACOS = re.compile(r"\s+")


def sanitizar_nome(texto: str) -> str:
    texto = _RE_CARACTERES_INVALIDOS.sub("", texto)
    texto = _RE_ESPACOS.sub(" ", texto).strip(" .")
    return texto or DESCONHECIDO


def formatar_data(data: str | None) -> str:
    if not data:
        return DESCONHECIDO
    return data.replace("/", ".")


def formatar_nome_recebedor(nome: str | None) -> str:
    if not nome:
        return DESCONHECIDO
    return sanitizar_nome(nome.upper())


def formatar_valor(valor: str | None) -> str:
    if not valor:
        return DESCONHECIDO
    return valor


def montar_nome(
    data: str | None, nome_recebedor: str | None, valor: str | None
) -> str:
    data_fmt = formatar_data(data)
    nome_fmt = formatar_nome_recebedor(nome_recebedor)
    valor_fmt = formatar_valor(valor)
    return f"{data_fmt} - {nome_fmt} - {valor_fmt}.pdf"


def deduplicar(caminho: Path) -> Path:
    if not caminho.exists():
        return caminho
    base, sufixo = caminho.stem, caminho.suffix
    contador = 2
    while True:
        candidato = caminho.with_name(f"{base} ({contador}){sufixo}")
        if not candidato.exists():
            return candidato
        contador += 1
