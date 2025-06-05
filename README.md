
# 🔥 Simulador de Resposta a Queimadas

Este projeto é um simulador interativo de resposta a ocorrências de queimadas. Utiliza estruturas de dados como heap, fila, lista ligada e árvore binária para gerenciar, priorizar e organizar as ocorrências por severidade e região.

## 👩‍💻👨‍💻 Integrantes

- **Marcela Torro** - RM557658 
- **Rodrigo** - RM550266

---

## 📦 Requisitos para executar

### 1. Instale o pacote necessário para gerar o gráfico:

```bash
pip install matplotlib
```

### 2. Execute o programa no terminal:

```bash
python nome_do_arquivo.py
```

> Substitua `nome_do_arquivo.py` pelo nome real do arquivo `.py` que contém o código.

---

## Funcionalidades disponíveis no menu

Ao executar o programa, será exibido um menu com as seguintes opções:

### `1️⃣ Inserir nova ocorrência`
Permite adicionar uma nova ocorrência de incêndio, informando:
- Região
- Severidade (de 1 a 10)
- Descrição
---
### `2️⃣ Atender ocorrência prioritária`
Atende a ocorrência de maior severidade. Após o atendimento:
- A ocorrência vai para o histórico
- Uma ocorrência da fila de espera (se houver) é movida para a heap
---
### `3️⃣ Listar ocorrências pendentes`
Mostra:
- Ocorrências prioritárias (heap)
- Fila de espera
---
### `4️⃣ Ver histórico de atendimentos`
- Exibe todas as ocorrências já atendidas, organizadas em ordem de atendimento (mais recente primeiro).
---
### `5️⃣ Gerar relatório por região`
Para cada região com ocorrências, exibe:
- Total de ocorrências
- Severidade média
- Listagem das ocorrências registradas
---
### `6️⃣ Gerar gráfico de severidade por região`
Cria um gráfico de barras com a **severidade média** das ocorrências em cada região.
> 💡 **Requer a biblioteca `matplotlib`.**
---
### `7️⃣ Simular chamadas aleatórias`
- Gera um número de ocorrências aleatórias com regiões e severidades variadas.
---
### `8️⃣ Simular chamadas com severidade crescente`
- Cria ocorrências com severidade aumentando gradualmente, ideal para simular cenários de emergência.
---
### `9️⃣ Sair`
- Encerra o simulador.
---

