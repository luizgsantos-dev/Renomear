from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ExtractedData:
    nome_recebedor: str | None
    data_pagamento: str | None  # formato "DD/MM/AAAA"
    valor: str | None  # formato brasileiro, ex. "1.234,56"
    layout: str
    avisos: list[str] = field(default_factory=list)


class BaseParser(ABC):
    nome: str

    @abstractmethod
    def detect(self, texto: str) -> bool:
        ...

    @abstractmethod
    def extract(self, texto: str) -> ExtractedData:
        ...
