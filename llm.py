import json
import logging
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import MetricsReason
from prompts import NEWS_PROMPT, PERIODS_SELECTION, REPORT_GENERATION
from utils import extract_json_from_text, metrics_tool

load_dotenv()


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)
grounding_tool = types.Tool(google_search=types.GoogleSearch())
search_config = types.GenerateContentConfig(tools=[grounding_tool])


def get_news(period: str) -> str:
    logger.info(f"Getting news for period {period}")
    prompt = NEWS_PROMPT.format(period=period)
    contents = [prompt]
    response = _get_llm_answer(contents)
    logger.info(f"News retrieved for period {period}:\n{response}")
    return response


def get_periods(news: str, fallback: str) -> List[Dict[str, str]]:
    logger.info("Getting periods from LLM")
    prompt = PERIODS_SELECTION
    contents = [prompt, news]
    response = _get_llm_answer(contents)
    logger.info(f"Periods retrieved:\n{response}")
    try:
        periods_choice = extract_json_from_text(response)
        if not isinstance(periods_choice, list):
            raise ValueError
    except Exception:
        periods_choice = [{"period": fallback, "reason": "fallback"}]
    return periods_choice


def gen_final_report_md(news: str, periods_choice: List[Dict[str, str]]) -> str:
    metrics_by_period = _get_metrics_by_period(periods_choice)
    metrics_str = json.dumps(metrics_by_period, indent=2, ensure_ascii=False)
    contents = [
        REPORT_GENERATION,
        f"=== NOTÍCIAS ===\n{news}\n\n=== MÉTRICAS ===\n{metrics_str}",
    ]
    response = _get_llm_answer(contents)
    logger.info(f"Report markdown generated:\n{response}")
    return response


def _get_metrics_by_period(
    periods_choice: List[Dict[str, str]],
) -> Dict[str, MetricsReason]:
    metrics_by_period: Dict[str, MetricsReason] = {}
    for item in periods_choice:
        p = item["period"]
        reason = item.get("reason", "")
        try:
            metrics = metrics_tool(p)
        except Exception as e:
            raise Exception(f"Error getting metrics for period {p}: {e}")
        metrics_by_period[p] = {"reason": reason, "metrics": metrics}
    return metrics_by_period


def _get_llm_answer(contents: Any) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
    )
    if not response.text:
        raise Exception("No response from LLM")
    return response.text
