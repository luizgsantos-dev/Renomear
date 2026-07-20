import shutil
from pathlib import Path

from src.config import Settings
from src.orchestrator import processar_arquivo

FIXTURE_ITAU = Path(__file__).parent / "fixtures" / "exemplo_itau_boleto.pdf"
FIXTURE_ITAU_CONCESSIONARIA = (
    Path(__file__).parent / "fixtures" / "exemplo_itau_concessionaria.pdf"
)


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        pasta_entrada=tmp_path / "entrada",
        pasta_saida=tmp_path / "saida",
        caminho_relatorio=tmp_path / "relatorio.xlsx",
        caminho_log=tmp_path / "logs" / "app.log",
        intervalo_polling_segundos=1,
        checks_estabilizacao=1,
    )


def test_processa_comprovante_conhecido_move_e_renomeia(tmp_path):
    cfg = _settings(tmp_path)
    cfg.pasta_entrada.mkdir(parents=True)

    origem = cfg.pasta_entrada / "qualquer_nome.pdf"
    shutil.copy(FIXTURE_ITAU, origem)

    processar_arquivo(origem, cfg)

    esperado = cfg.pasta_saida / "MIDIOGRAF PERSONALE" / "03.07.2026 - MIDIOGRAF PERSONALE - 5.580,00.pdf"
    assert esperado.exists()
    assert not origem.exists()
    assert cfg.caminho_relatorio.exists()


def test_processa_comprovante_concessionaria_organiza_por_empresa(tmp_path):
    cfg = _settings(tmp_path)
    cfg.pasta_entrada.mkdir(parents=True)

    origem = cfg.pasta_entrada / "qualquer_nome.pdf"
    shutil.copy(FIXTURE_ITAU_CONCESSIONARIA, origem)

    processar_arquivo(origem, cfg)

    esperado = cfg.pasta_saida / "VIVO-MT" / "08.05.2026 - VIVO-MT - 54,00.pdf"
    assert esperado.exists()
    assert not origem.exists()


def test_layout_desconhecido_vai_para_revisar(tmp_path, monkeypatch):
    cfg = _settings(tmp_path)
    cfg.pasta_entrada.mkdir(parents=True)

    origem = cfg.pasta_entrada / "arquivo_estranho.pdf"
    origem.write_bytes(b"conteudo irrelevante, extrator sera mockado")

    monkeypatch.setattr(
        "src.orchestrator.extrair_texto", lambda caminho: "texto sem nenhum label conhecido"
    )

    processar_arquivo(origem, cfg)

    esperado = cfg.pasta_saida / "_REVISAR" / "DESCONHECIDO - DESCONHECIDO - DESCONHECIDO.pdf"
    assert esperado.exists()
    assert not origem.exists()


def test_arquivo_duplicado_recebe_sufixo(tmp_path):
    cfg = _settings(tmp_path)
    cfg.pasta_entrada.mkdir(parents=True)

    for nome_origem in ("primeiro.pdf", "segundo.pdf"):
        origem = cfg.pasta_entrada / nome_origem
        shutil.copy(FIXTURE_ITAU, origem)
        processar_arquivo(origem, cfg)

    pasta_empresa = cfg.pasta_saida / "MIDIOGRAF PERSONALE"
    assert (pasta_empresa / "03.07.2026 - MIDIOGRAF PERSONALE - 5.580,00.pdf").exists()
    assert (pasta_empresa / "03.07.2026 - MIDIOGRAF PERSONALE - 5.580,00 (2).pdf").exists()
