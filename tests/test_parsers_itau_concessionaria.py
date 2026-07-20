from pathlib import Path

from src.parsers import escolher_parser
from src.pdf_text import extrair_texto

FIXTURE = Path(__file__).parent / "fixtures" / "exemplo_itau_concessionaria.pdf"


def test_reconhece_layout_itau_concessionaria():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    assert parser is not None
    assert parser.nome == "itau_concessionaria"


def test_extrai_campos_itau_concessionaria():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    dados = parser.extract(texto)

    assert dados.nome_recebedor == "VIVO-MT"
    assert dados.data_pagamento == "08/05/2026"
    assert dados.valor == "54,00"
    assert dados.avisos == []
