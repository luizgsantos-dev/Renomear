from pathlib import Path

from src.parsers import escolher_parser
from src.pdf_text import extrair_texto

FIXTURE = Path(__file__).parent / "fixtures" / "exemplo_inter_boleto.pdf"


def test_reconhece_layout_inter_boleto():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    assert parser is not None
    assert parser.nome == "inter_boleto"


def test_extrai_campos_inter_boleto():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    dados = parser.extract(texto)

    assert dados.nome_recebedor == "FACILITA TECNOLOGIA S A"
    assert dados.data_pagamento == "10/07/2026"
    assert dados.valor == "3.164,95"
    assert dados.avisos == []


def test_nao_confunde_data_de_vencimento_com_data_da_transacao():
    texto = extrair_texto(FIXTURE)
    parser = escolher_parser(texto)
    dados = parser.extract(texto)

    assert dados.data_pagamento != "11/07/2026"
