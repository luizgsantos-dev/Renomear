import shutil
from pathlib import Path

from src.config import Settings
from src.watcher import executar_ciclo

FIXTURE_ITAU = Path(__file__).parent / "fixtures" / "exemplo_itau_boleto.pdf"


def _settings(tmp_path: Path) -> Settings:
    return Settings(
        pasta_entrada=tmp_path / "entrada",
        pasta_saida=tmp_path / "saida",
        caminho_relatorio=tmp_path / "relatorio.xlsx",
        caminho_log=tmp_path / "logs" / "app.log",
        intervalo_polling_segundos=1,
        checks_estabilizacao=2,
    )


def test_so_processa_apos_arquivo_estabilizar(tmp_path):
    cfg = _settings(tmp_path)
    cfg.pasta_entrada.mkdir(parents=True)

    origem = cfg.pasta_entrada / "comprovante.pdf"
    shutil.copy(FIXTURE_ITAU, origem)

    pendentes = {}

    executar_ciclo(cfg, pendentes)
    assert origem.exists(), "não deveria processar no 1º ciclo (0 checks estáveis)"

    executar_ciclo(cfg, pendentes)
    assert origem.exists(), "não deveria processar no 2º ciclo (1 check estável, faltam 2)"

    executar_ciclo(cfg, pendentes)
    assert not origem.exists(), "deveria processar no 3º ciclo (2 checks estáveis)"

    esperado = cfg.pasta_saida / "MIDIOGRAF PERSONALE" / "03.07.2026 - MIDIOGRAF PERSONALE - 5.580,00.pdf"
    assert esperado.exists()


def test_arquivo_ainda_crescendo_nao_e_processado(tmp_path):
    cfg = _settings(tmp_path)
    cfg.pasta_entrada.mkdir(parents=True)

    origem = cfg.pasta_entrada / "comprovante.pdf"
    origem.write_bytes(b"a" * 10)

    pendentes = {}
    executar_ciclo(cfg, pendentes)

    origem.write_bytes(b"a" * 20)
    executar_ciclo(cfg, pendentes)

    assert origem.exists()
    assert pendentes[origem][1] == 0, "tamanho mudou, contagem de estabilidade deve zerar"
