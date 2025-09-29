import json
import logging
import os
import re
from typing import Any

import pandas as pd

from models import Metrics

logger = logging.getLogger(__name__)

PARQUET_PATH = os.getenv("PARQUET_PATH", "data/OpenDataSUS-SRAG-24-25.parquet")


def metrics_tool(period: str) -> Metrics:
    dias = period_to_days(period)
    df = pd.read_parquet(PARQUET_PATH, engine="fastparquet")
    metrics = _calculate_metrics(df, periodo_dias=dias)
    logger.info(
        f"Metrics for {period}:\n{json.dumps(metrics, indent=2, ensure_ascii=False)}"
    )
    return metrics


def extract_json_from_text(text: str) -> Any:
    m = re.search(r"(\[.*\]|\{.*\})", text, flags=re.S)
    if not m:
        raise ValueError("JSON não encontrado na saída do modelo")
    return json.loads(m.group(1))


def period_to_days(period: str) -> int:
    p = period.strip().lower()
    if p.endswith("d"):
        return int(p[:-1])
    if p.endswith("m"):
        return int(p[:-1]) * 30
    if p.endswith("y"):
        return int(p[:-1]) * 365
    raise ValueError("Formato de período inválido. Use '30d','3m','1y' etc.")


def _calculate_metrics(df: pd.DataFrame, periodo_dias: int = 30) -> Metrics:
    hoje = pd.Timestamp.today().normalize()

    inicio_atual = hoje - pd.Timedelta(days=periodo_dias)
    inicio_anterior = hoje - pd.Timedelta(days=2 * periodo_dias)
    fim_anterior = inicio_atual - pd.Timedelta(days=1)

    for col in [
        "data_inicio",
        "uti_inicio",
        "uti_final",
        "internacao_inicio",
        "internacao_final",
        "data_vacina",
    ]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df_casos_atual = df[
        (df["data_inicio"] >= inicio_atual) & (df["data_inicio"] <= hoje)
    ]
    total_casos = len(df_casos_atual)

    df_casos_anterior = df[
        (df["data_inicio"] >= inicio_anterior) & (df["data_inicio"] <= fim_anterior)
    ]

    taxa_aumento = (
        (total_casos - len(df_casos_anterior)) / max(len(df_casos_anterior), 1)
    ) * 100

    df["data_encerramento"] = (
        df[["uti_final", "internacao_final"]].bfill(axis=1).iloc[:, 0]
    )

    df_encerrados = df[df["data_encerramento"].notna()]
    df_encerrados_periodo = df_encerrados[
        (df_encerrados["data_encerramento"] >= inicio_atual)
        & (df_encerrados["data_encerramento"] <= hoje)
    ]

    obitos = df_encerrados_periodo["evolucao"].eq(2.0).sum()
    total_encerrados = len(df_encerrados_periodo)
    taxa_mortalidade = (obitos / max(total_encerrados, 1)) * 100

    df_uti = df_casos_atual[df_casos_atual["uti"] == 1.0]
    total_internados_uti = len(df_uti)
    taxa_uti = (total_internados_uti / total_casos) * 100 if total_casos else 0

    vacinados = df_casos_atual[df_casos_atual["vacina"].notna()]["vacina"].sum()
    taxa_vacinacao = (vacinados / max(total_casos, 1)) * 100

    return Metrics(
        taxa_aumento_casos=round(float(taxa_aumento), 1),
        taxa_mortalidade=round(float(taxa_mortalidade), 1),
        taxa_ocupacao_uti=round(float(taxa_uti), 1),
        taxa_vacinacao=round(float(taxa_vacinacao), 1),
        total_cases=total_casos,
    )
