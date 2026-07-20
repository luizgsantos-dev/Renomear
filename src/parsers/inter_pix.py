from __future__ import annotations

import re

from .base import BaseParser, ExtractedData

_RE_DATA = re.compile(r"Data da transa[cç][aã]o\s+(\d{2}/\d{2}/\d{4})", re.IGNORECASE)
_RE_VALOR = re.compile(r"Pix enviado\s*\n?\s*R\$\s*([\d.,]+)", re.IGNORECASE)
_RE_NOME = re.compile(r"Nome\s+(.+)", re.IGNORECASE)


class InterPixParser(BaseParser):
    nome = "inter_pix"

    def detect(self, texto: str) -> bool:
        return "BANCO INTER" in texto.upper() and "Pix enviado" in texto

    def extract(self, texto: str) -> ExtractedData:
        avisos: list[str] = []

        m_data = _RE_DATA.search(texto)
        data = m_data.group(1) if m_data else None
        if not data:
            avisos.append("data da transação não encontrada")

        m_valor = _RE_VALOR.search(texto)
        valor = m_valor.group(1) if m_valor else None
        if not valor:
            avisos.append("valor não encontrado")

        nome = self._extrair_recebedor(texto)
        if not nome:
            avisos.append("recebedor (Quem recebeu) não encontrado")

        return ExtractedData(
            nome_recebedor=nome,
            data_pagamento=data,
            valor=valor,
            layout=self.nome,
            avisos=avisos,
        )

    @staticmethod
    def _extrair_recebedor(texto: str) -> str | None:
        idx = texto.find("Quem recebeu")
        if idx == -1:
            return None
        m_nome = _RE_NOME.search(texto, idx)
        return m_nome.group(1).strip() if m_nome else None
