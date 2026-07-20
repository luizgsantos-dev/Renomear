from pathlib import Path

from src.parsers import escolher_parser
from src.pdf_text import extrair_texto

FIXTURE = Path(__file__).parent / "fixtures" / "exemplo_inter_concessionaria.pdf"


def test_reconhece_layout_inter_concessionaria():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    assert parser is not None
    assert parser.nome == "inter_concessionaria"


def test_extrai_campos_inter_concessionaria():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    dados = parser.extract(texto)

    assert dados.nome_recebedor == "VIVO MT"
    assert dados.data_pagamento == "17/07/2026"
    assert dados.valor == "39,99"
    assert dados.avisos == []
