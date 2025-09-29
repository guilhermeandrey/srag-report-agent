import matplotlib.pyplot as plt
import pandas as pd


def save_markdown(
    df: pd.DataFrame,
    md_text: str,
    output_file: str = "relatorio.md",
    daily_path: str = "graph_daily.png",
    monthly_path: str = "graph_monthly.png",
) -> None:
    _gerar_graficos(df, daily_path=daily_path, monthly_path=monthly_path)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_text)


def _gerar_graficos(
    df: pd.DataFrame,
    daily_path: str = "graph_daily.png",
    monthly_path: str = "graph_monthly.png",
) -> None:
    df["data_inicio"] = pd.to_datetime(df["data_inicio"], errors="coerce")
    hoje = pd.Timestamp.today().normalize()
    inicio = hoje - pd.Timedelta(days=30)

    df_30d = df[(df["data_inicio"] >= inicio) & (df["data_inicio"] <= hoje)]
    daily = df_30d.groupby(df_30d["data_inicio"].dt.date).size()

    plt.figure(figsize=(12, 5))
    plt.plot(daily.index, daily.values, marker="o", linestyle="-")  # type: ignore
    plt.title("Casos Diários - Últimos 30 dias")
    plt.ylabel("Número de casos")
    plt.xticks(rotation=90)  # rotaciona 90°
    plt.gca().set_xticklabels([d.isoformat() for d in daily.index])  # ISO YYYY-MM-DD
    plt.tight_layout()
    plt.savefig(daily_path)
    plt.close()

    inicio_12m = hoje - pd.DateOffset(months=12)
    df_12m = df[(df["data_inicio"] >= inicio_12m) & (df["data_inicio"] <= hoje)]
    monthly = df_12m.groupby(df_12m["data_inicio"].dt.to_period("M")).size()

    plt.figure(figsize=(10, 4))
    plt.plot(monthly.index.astype(str), monthly.values, marker="o", linestyle="-")  # type: ignore
    plt.title("Casos Mensais - Últimos 12 meses")
    plt.ylabel("Número de casos")
    plt.tight_layout()
    plt.savefig(monthly_path)
    plt.close()
