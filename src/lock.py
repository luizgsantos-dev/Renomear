from __future__ import annotations

import msvcrt
from pathlib import Path
from typing import BinaryIO


def adquirir_lock(caminho_lock: Path) -> BinaryIO | None:
    """Tenta adquirir um lock exclusivo para impedir duas instâncias simultâneas.

    Retorna o handle do arquivo (deve ser mantido vivo pelo chamador enquanto
    o processo roda) ou None se outra instância já detém o lock.
    """
    caminho_lock.parent.mkdir(parents=True, exist_ok=True)
    arquivo = open(caminho_lock, "a+b")
    try:
        msvcrt.locking(arquivo.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        arquivo.close()
        return None
    return arquivo
