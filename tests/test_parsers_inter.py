from pathlib import Path

from src.parsers import escolher_parser
from src.pdf_text import extrair_texto

FIXTURE = Path(__file__).parent / "fixtures" / "exemplo_inter_pix.pdf"


def test_reconhece_layout_inter_pix():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    assert parser is not None
    assert parser.nome == "inter_pix"


def test_extrai_campos_inter_pix():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    dados = parser.extract(texto)

    assert dados.nome_recebedor == "La Vita Gestao Ocupacional"
    assert dados.data_pagamento == "14/07/2026"
    assert dados.valor == "35,00"
    assert dados.avisos == []


def test_nao_confunde_pagador_com_recebedor():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    dados = parser.extract(texto)

    assert "AB IMOBILIARIA" not in dados.nome_recebedor
