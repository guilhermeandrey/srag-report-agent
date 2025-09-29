from llm import gen_final_report_md, get_news, get_periods
from models import GraphState


def news_agent(state: GraphState) -> GraphState:
    period = state.get("period", "30d")
    news = get_news(period)
    return {**state, "news": news}


def final_report_agent(state: GraphState) -> GraphState:
    if "news" not in state:
        raise RuntimeError("notícias ausentes")

    news_text = state["news"]
    user_period = state.get("period", "30d")

    periods = get_periods(news_text, user_period)
    final_report = gen_final_report_md(news_text, periods)

    return {**state, "final_report": final_report}
