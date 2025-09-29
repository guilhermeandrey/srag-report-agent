# Relatório Automatizado de SRAG com GenAI

Este projeto é uma prova de conceito (PoC) de uma solução baseada em Inteligência Artificial Generativa para gerar relatórios automatizados sobre SRAG no Brasil, integrando dados quantitativos e notícias qualitativas.

## Arquitetura da Solução

A arquitetura foi pensada para permitir flexibilidade, auditabilidade e governança:

1. **Agente de Notícias**  
   Coleta e resume notícias recentes sobre SRAG. Mantém o contexto qualitativo para análise.

2. **Agente de Relatório Final**  
   - Recebe as notícias do agente anterior.  
   - Decide dinamicamente os períodos mais relevantes para análise de métricas.  
   - Chama a **tool de métricas** para calcular automaticamente os indicadores quantitativos (taxa de aumento de casos, mortalidade, ocupação de UTI e vacinação).  
   - Integra notícias e métricas para gerar um relatório narrativo completo em Markdown, podendo justificar discrepâncias e destacar tendências.  

3. **Tool de Métricas**  
   Calcula métricas baseadas em código, sem intervenção do LLM, garantindo precisão e auditabilidade.

4. **Modelo GenAI (Gemini 2.5 Flash)**  
   Usado apenas para síntese e geração de narrativa final do relatório, mantendo o LLM como agente de interpretação e narrativa, não cálculo.

Essa arquitetura permite:
- **Separação de responsabilidades** (coleta de notícias, cálculo de métricas, geração de relatório).  
- **Flexibilidade de períodos de análise**: o agente final pode escolher múltiplos períodos com base nas notícias.  
- **Auditoria e governabilidade**: cálculos automatizados são transparentes e os logs podem ser rastreados.  
- **Extensibilidade**: novas tools ou agentes podem ser adicionados sem quebrar o fluxo principal.

## Variáveis de Ambiente Necessárias

- `GEMINI_API_KEY`: chave da API Gemini.

Variáveis opcionais:

- `PARQUET_PATH`: caminho para o arquivo Parquet com os dados SRAG.  
- `PERIOD` (default: `30d`): período inicial de análise.  
- `GEMINI_MODEL` (default: `gemini-2.5-flash`): modelo a ser usado.

> Um `.env` de exemplo está incluso no projeto para facilitar a configuração.

## Como Executar

1. Preencher o arquivo `.env`.
2. Instalar dependências:  
   ```bash
   pip install -r requirements.txt