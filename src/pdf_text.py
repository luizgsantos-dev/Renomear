from __future__ import annotations

import logging
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium

logger = logging.getLogger(__name__)


def extrair_texto(caminho: Path) -> str:
    texto = _extrair_com_pdfplumber(caminho)
    if texto.strip():
        return texto
    return _extrair_com_pypdfium2(caminho)


def _extrair_com_pdfplumber(caminho: Path) -> str:
    try:
        with pdfplumber.open(caminho) as pdf:
            return "\n".join(pagina.extract_text() or "" for pagina in pdf.pages)
    except Exception:
        logger.exception("Falha ao extrair texto com pdfplumber: %s", caminho)
        return ""


def _extrair_com_pypdfium2(caminho: Path) -> str:
    try:
        pdf = pdfium.PdfDocument(str(caminho))
        try:
            partes = []
            for pagina in pdf:
                textpage = pagina.get_textpage()
                try:
                    partes.append(textpage.get_text_range())
                finally:
                    textpage.close()
                pagina.close()
            return "\n".join(partes)
        finally:
            pdf.close()
    except Exception:
        logger.exception("Falha ao extrair texto com pypdfium2: %s", caminho)
        return ""
