NEWS_PROMPT = (
    "Busque e resuma notícias recentes sobre 'Síndrome Respiratória Aguda Grave' (SRAG) no Brasil "
    "relacionadas ao período {period}. Retorne título + link + um curto contexto para cada item. "
    "Limite a 8 itens. Seja objetivo."
)

PERIODS_SELECTION = (
    "Você é um analista epidemiológico. Com base nas notícias abaixo, escolha 1 a 3 períodos "
    "relevantes para análise quantitativa (ex: '30d','90d','12m'). "
    "Retorne APENAS um JSON array de objetos: "
    '{"period":"<period>","reason":"<curta justificativa>"}'
)

REPORT_GENERATION = """Você é um especialista em epidemiologia. Sua tarefa: gerar um relatório FINAL em Markdown sobre SRAG no Brasil. Use o bloco de notícias como contexto qualitativo e os dados de métricas como evidências quantitativas. Analise coerência, destaque tendências, explique discrepâncias. O relatório deve ter narrativa fluida, NÃO apenas tabelas, e conter seções organizadas (ex: Introdução, Situação Atual, Comparações, Conclusão).

Importante:
- Inclua no relatório dois gráficos em locais adequados da narrativa, usando os seguintes placeholders:
  - `![Gráfico Casos Diários - Últimos 30 dias](path/to/graph_daily.png)`
  - `![Gráfico Casos Mensais - Últimos 12 meses](path/to/graph_monthly.png)`
- Esses placeholders devem estar em pontos coerentes do texto (não todos no final, mas contextualizados).
- Não gere os gráficos, apenas insira os links como parte do Markdown."""
