# 🚚 Otimizador de Rotas com Streamlit

Este projeto é uma aplicação interativa desenvolvida em Python com **Streamlit**, que permite otimizar rotas logísticas a partir de coordenadas geográficas fornecidas em planilhas Excel. A otimização é baseada na resolução aproximada do Problema do Caixeiro Viajante (TSP), retornando ao ponto inicial de origem com estimativa de tempo e distância total percorrida.

---

## ✨ Funcionalidades

- 🔐 Autenticação de usuários
- 📥 Upload de arquivos Excel com coordenadas geográficas
- 📍 Cálculo da rota otimizada utilizando a fórmula de Haversine
- 🔄 Retorno ao ponto de origem (ciclo fechado)
- 📊 Estimativas de distância total, tempo médio por trecho e tempo total de entrega
- 📤 Exportação da rota otimizada para planilha Excel
- ⚠️ Avisos sobre o modo de testes e melhorias futuras

---

## 📦 Requisitos

Antes de executar o projeto, instale as dependências abaixo:

```bash
pip install streamlit pandas pyexcel pyexcel-xls networkx
