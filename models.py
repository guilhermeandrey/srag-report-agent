from typing import TypedDict


class Metrics(TypedDict):
    taxa_aumento_casos: float
    taxa_mortalidade: float
    taxa_ocupacao_uti: float
    taxa_vacinacao: float
    total_cases: int


class MetricsReason(TypedDict):
    reason: str
    metrics: Metrics


class GraphState(TypedDict, total=False):
    period: str
    news: str
    final_report: str
