from __future__ import annotations

import re

from .base import BaseParser, ExtractedData

_RE_CONCESSIONARIA = re.compile(
    r"concession[aá]rias\s*\n\s*\d+\s*-\s*(.+)", re.IGNORECASE
)
_RE_DATA_PAGAMENTO = re.compile(
    r"Opera[cç][aã]o efetuada em\s+(\d{2}/\d{2}/\d{4})", re.IGNORECASE
)
_RE_VALOR = re.compile(r"Valor do documento:?\s*R\$\s*([\d.,]+)", re.IGNORECASE)


class ItauConcessionariaParser(BaseParser):
    nome = "itau_concessionaria"

    def detect(self, texto: str) -> bool:
        texto_lower = texto.lower()
        return "sispag" in texto_lower and "concession" in texto_lower

    def extract(self, texto: str) -> ExtractedData:
        avisos: list[str] = []

        m_nome = _RE_CONCESSIONARIA.search(texto)
        nome = m_nome.group(1).strip() if m_nome else None
        if not nome:
            avisos.append("concessionária não encontrada")

        m_data = _RE_DATA_PAGAMENTO.search(texto)
        data = m_data.group(1) if m_data else None
        if not data:
            avisos.append("data de pagamento não encontrada")

        m_valor = _RE_VALOR.search(texto)
        valor = m_valor.group(1) if m_valor else None
        if not valor:
            avisos.append("valor do documento não encontrado")

        return ExtractedData(
            nome_recebedor=nome,
            data_pagamento=data,
            valor=valor,
            layout=self.nome,
            avisos=avisos,
        )
