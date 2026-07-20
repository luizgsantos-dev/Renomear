from __future__ import annotations

import re

from .base import BaseParser, ExtractedData

_RE_NOME = re.compile(
    r"Benefici[aá]rio:\s*(.+?)\s*CPF/CNPJ do benefici[aá]rio", re.IGNORECASE
)
_RE_DATA_PAGAMENTO = re.compile(
    r"Data de pagamento:\s*\n?\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE
)
_RE_LABEL_VALOR_PAGAMENTO = re.compile(
    r"\(=\)\s*Valor do pagamento \(R\$\):", re.IGNORECASE
)
_RE_LABEL_DATA_PAGAMENTO = re.compile(r"Data de pagamento:", re.IGNORECASE)
_RE_VALOR_MONETARIO = re.compile(r"\d{1,3}(?:\.\d{3})*,\d{2}")


class ItauBoletoParser(BaseParser):
    nome = "itau_boleto"

    def detect(self, texto: str) -> bool:
        return "Sispag" in texto and "Comprovante de pagamento de boleto" in texto

    def extract(self, texto: str) -> ExtractedData:
        avisos: list[str] = []

        m_nome = _RE_NOME.search(texto)
        nome = m_nome.group(1).strip() if m_nome else None
        if not nome:
            avisos.append("beneficiário não encontrado")

        m_data = _RE_DATA_PAGAMENTO.search(texto)
        data = m_data.group(1) if m_data else None
        if not data:
            avisos.append("data de pagamento não encontrada")

        valor = self._extrair_valor(texto)
        if not valor:
            avisos.append("valor do pagamento não encontrado")

        return ExtractedData(
            nome_recebedor=nome,
            data_pagamento=data,
            valor=valor,
            layout=self.nome,
            avisos=avisos,
        )

    @staticmethod
    def _extrair_valor(texto: str) -> str | None:
        m_label = _RE_LABEL_VALOR_PAGAMENTO.search(texto)
        if not m_label:
            return None
        m_fim = _RE_LABEL_DATA_PAGAMENTO.search(texto, m_label.end())
        fim = m_fim.start() if m_fim else m_label.end() + 200
        janela = texto[m_label.end() : fim]
        candidatos = _RE_VALOR_MONETARIO.findall(janela)
        return candidatos[-1] if candidatos else None
