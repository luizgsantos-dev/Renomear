from src.naming import deduplicar, montar_nome, sanitizar_nome


def test_montar_nome_com_todos_campos():
    nome = montar_nome("03/07/2026", "Midiograf Personale", "5.580,00")
    assert nome == "03.07.2026 - MIDIOGRAF PERSONALE - 5.580,00.pdf"


def test_montar_nome_maiusculas_independente_da_entrada():
    nome = montar_nome("14/07/2026", "La Vita Gestao Ocupacional", "35,00")
    assert nome == "14.07.2026 - LA VITA GESTAO OCUPACIONAL - 35,00.pdf"


def test_montar_nome_com_campos_ausentes():
    nome = montar_nome(None, None, None)
    assert nome == "DESCONHECIDO - DESCONHECIDO - DESCONHECIDO.pdf"


def test_sanitizar_remove_caracteres_invalidos():
    assert sanitizar_nome('A/B:C*D?E"F<G>H|I') == "ABCDEFGHI"


def test_sanitizar_colapsa_espacos():
    assert sanitizar_nome("  Nome   Com   Espaços  ") == "Nome Com Espaços"


def test_deduplicar_gera_sufixo_incremental(tmp_path):
    base = tmp_path / "arquivo.pdf"
    base.write_bytes(b"")
    (tmp_path / "arquivo (2).pdf").write_bytes(b"")

    resultado = deduplicar(base)

    assert resultado == tmp_path / "arquivo (3).pdf"


def test_deduplicar_mantem_caminho_se_nao_existe(tmp_path):
    caminho = tmp_path / "novo.pdf"
    assert deduplicar(caminho) == caminho
