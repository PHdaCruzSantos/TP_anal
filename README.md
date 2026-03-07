# Análise de Mídias Sociais - Políticos (Refatorado para Data Science)

Este projeto foi originalmente concebido para a disciplina de Análise de Mídias Sociais, abordando a extração de dados da Câmara, formação de comunidades e conectividade de depuatdos interpartidários usando Tkinter.

Para avançar os estudos em **Data Science** e **Machine Learning**, o repositório foi **reestruturado e modernizado** adotando boas práticas e pipelines modulares em Python.

## Tecnologias Abordadas
- **Manipulação de Dados:** `pandas`, `numpy`
- **Grafos:** `networkx`
- **Visualização:** `matplotlib`, `seaborn`
- **Machine Learning:** `scikit-learn` (Random Forest, K-Means, PCA)

## Estrutura do Projeto (Cookiecutter Data Science)
```text
ams-politicos/
├── data/
│   ├── raw/                 # Dados brutos extraídos das APIs (ex: votos_camara.csv)
│   └── processed/           # Grafos exportados e Features calculadas 
├── src/
│   ├── data/
│   │   └── make_dataset.py  # Script que bate na API e baixa votos como CSV
│   ├── features/
│   │   └── build_features.py# Extrai as centralidades (Degree, Betweenness) e GML
│   ├── models/
│   │   └── train_model.py   # Exemplos de supervisionado e não-supervisionado
│   └── visualization/
│       └── visualize.py     # Plots interativos usando Seaborn e Matplotlib
├── legacy/                  # Scripts originais do Tkinter guardados para referência
└── requirements.txt         # Lista de dependências Python
```

## Como Executar

### 1. Criar e Ativar Ambiente Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Rodar a Pipeline de Dados
A pipeline deve ser executada na seguinte ordem:

1. **Baixar Dados Brutos:**
   ```bash
   python src/data/make_dataset.py
   ```
2. **Construir Features e Grafos:**
   ```bash
   python src/features/build_features.py
   ```
3. **Gerar Visualizações Exploratórias:**
   ```bash
   python src/visualization/visualize.py
   ```
4. **Testar Modelos de Machine Learning (Scikit-Learn):**
   ```bash
   python src/models/train_model.py
   ```

## Objetivos Futuros de Estudo
O arquivo `src/models/train_model.py` já deixa a fundação montada para treinar:
- **Modelos Supervisionados:** Predição de votações futuras, Regressão Logística e SVM usando interações dos deputados.
- **Não Supervisionados:** Detecção de comunidades ideológicas via DBSCAN e K-Means baseado numa matriz de cruzamento de votos.
