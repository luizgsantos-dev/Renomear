from pathlib import Path

from src.parsers import escolher_parser
from src.pdf_text import extrair_texto

FIXTURE = Path(__file__).parent / "fixtures" / "exemplo_itau_boleto.pdf"


def test_reconhece_layout_itau_boleto():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    assert parser is not None
    assert parser.nome == "itau_boleto"


def test_extrai_campos_itau_boleto():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    dados = parser.extract(texto)

    assert dados.nome_recebedor == "MIDIOGRAF PERSONALE"
    assert dados.data_pagamento == "03/07/2026"
    assert dados.valor == "5.580,00"
    assert dados.avisos == []
