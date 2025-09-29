import logging
import os

import pandas as pd

from graph import compile_state_graph
from report import save_markdown

log_file = "run_log.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

PARQUET_PATH = os.getenv("PARQUET_PATH", "data/OpenDataSUS-SRAG-24-25.parquet")
PERIOD = os.getenv("PERIOD", "30d")

if __name__ == "__main__":
    app = compile_state_graph()
    init = {"period": PERIOD}
    result = app.invoke(init)
    markdown = result["final_report"]
    df = pd.read_parquet(PARQUET_PATH, engine="fastparquet")
    save_markdown(df, markdown)
