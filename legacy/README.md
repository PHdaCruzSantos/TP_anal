# Código Legado (AMS Políticos)

Este diretório contém os scripts originais em sua versão bruta. Eles foram organizados da seguinte forma para facilitar consultas futuras:

1. **`/data_files/`**: Contém todos os arquivos `.txt` (como `grafo_arq.txt` e listagens de deputados) e tabelas `.csv` (como `nodes` e `edges`) que foram gerados pela versão mais antiga do software.
2. **`/data_collection_scripts/`**: Onde ficou o `index.py` antigo (responsável por bater na API usando a primeira abordagem com o Requests e salvamento em TXT).
3. **`/graph_scripts/`**: Scripts matemáticos de cálculo da centralidade (Grau, Intermediação, Assortatividade) e geradores de arestas do NetworkX de forma não-modular.
4. **`/gui_scripts/`**: Contém a interface em *Tkinter* (`main.py`) e visualizações rudimentares do matplotlib (`plot.py`).

Toda essa lógica foi refatorada e unificada no diretório principal `src/` da raiz seguindo os padrões do Cookiecutter Data Science. Sinta-se à vontade para deletar essa pasta no futuro quando o projeto principal estiver 100% maduro!
