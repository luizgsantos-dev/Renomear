from __future__ import annotations

import re

from .base import BaseParser, ExtractedData

_RE_DATA = re.compile(r"Data do Pagamento\s+(\d{2}/\d{2}/\d{4})", re.IGNORECASE)
_RE_VALOR = re.compile(r"Valor total\s*R\$\s*([\d.,]+)", re.IGNORECASE)
_RE_DESCRICAO = re.compile(r"Descri[cç][aã]o\s+(.+)", re.IGNORECASE)


class InterConcessionariaParser(BaseParser):
    nome = "inter_concessionaria"

    def detect(self, texto: str) -> bool:
        return (
            "Pagamento realizado!" in texto
            and "Código Convênio" in texto
            and "Banco Inter" in texto
        )

    def extract(self, texto: str) -> ExtractedData:
        avisos: list[str] = []

        m_nome = _RE_DESCRICAO.search(texto)
        nome = m_nome.group(1).strip() if m_nome else None
        if not nome:
            avisos.append("descrição (concessionária) não encontrada")

        m_data = _RE_DATA.search(texto)
        data = m_data.group(1) if m_data else None
        if not data:
            avisos.append("data do pagamento não encontrada")

        m_valor = _RE_VALOR.search(texto)
        valor = m_valor.group(1) if m_valor else None
        if not valor:
            avisos.append("valor total não encontrado")

        return ExtractedData(
            nome_recebedor=nome,
            data_pagamento=data,
            valor=valor,
            layout=self.nome,
            avisos=avisos,
        )
