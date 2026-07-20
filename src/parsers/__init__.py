from __future__ import annotations

from .base import BaseParser, ExtractedData
from .inter_boleto import InterBoletoParser
from .inter_concessionaria import InterConcessionariaParser
from .inter_pix import InterPixParser
from .itau_boleto import ItauBoletoParser
from .itau_concessionaria import ItauConcessionariaParser

PARSERS: list[BaseParser] = [
    ItauBoletoParser(),
    ItauConcessionariaParser(),
    InterPixParser(),
    InterBoletoParser(),
    InterConcessionariaParser(),
]


def escolher_parser(texto: str) -> BaseParser | None:
    for parser in PARSERS:
        if parser.detect(texto):
            return parser
    return None


__all__ = ["BaseParser", "ExtractedData", "PARSERS", "escolher_parser"]
