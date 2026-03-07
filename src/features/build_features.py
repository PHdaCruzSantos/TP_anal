import pandas as pd
import numpy as np
import networkx as nx
import pathlib
import os

PROJECT_DIR = pathlib.Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"

def carregar_dados_brutos():
    caminho = RAW_DATA_DIR / "votos_camara.csv"
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}. Execute src/data/make_dataset.py primeiro.")
    return pd.read_csv(caminho)

def construir_grafo_votos(df):
    """
    Constrói um grafo NetworkX onde deputados são nós e arestas refletem a concordância de votos.
    Se dois deputados na mesma sessão votarem igualmente, o peso da aresta aumenta.
    """
    grafo = nx.Graph()
    
    # Armazenar info dos deputados como atributos
    info_deputados = df[['deputado_nome', 'partido']].drop_duplicates()
    for _, row in info_deputados.iterrows():
        grafo.add_node(row['deputado_nome'], partido=row['partido'])

    votacoes_ids = df['votacao_id'].unique()
    
    for v_id in votacoes_ids:
        df_votacao = df[df['votacao_id'] == v_id]
        
        # Agrupa deputados pelo mesmo voto na sessão atual
        grupos_votos = df_votacao.groupby('tipo_voto')['deputado_nome'].apply(list)
        
        for tipo, deputados in grupos_votos.items():
            # Combinação de todos contra todos que votaram igual
            for i in range(len(deputados)):
                for j in range(i + 1, len(deputados)):
                    d1, d2 = deputados[i], deputados[j]
                    if grafo.has_edge(d1, d2):
                        grafo[d1][d2]['weight'] += 1
                    else:
                        grafo.add_edge(d1, d2, weight=1)
                        
    return grafo

def calcular_centralidades(grafo):
    """Calcula métricas estendidas e retorna um DataFrame consolidado."""
    centr_grau = nx.degree_centrality(grafo)
    centr_interm = nx.betweenness_centrality(grafo, weight='weight')
    
    dados = []
    for node in grafo.nodes():
        dados.append({
            "deputado_nome": node,
            "partido": grafo.nodes[node].get('partido', 'SEM_PARTIDO'),
            "grau_centralidade": centr_grau.get(node, 0),
            "intermediacao": centr_interm.get(node, 0),
            "grau_conexao": grafo.degree[node]
        })
        
    return pd.DataFrame(dados)

def main():
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    print("Construindo features e grafo de deputados a partir de dados brutos...")
    
    try:
        df = carregar_dados_brutos()
        grafo = construir_grafo_votos(df)
        print(f"Grafo gerado: {grafo.number_of_nodes()} nós e {grafo.number_of_edges()} arestas.")
        
        # Gravar representação relacional para Machine Learning futuramente
        nx.write_gml(grafo, PROCESSED_DATA_DIR / "grafo_partidos.gml")
        
        df_features = calcular_centralidades(grafo)
        df_features.to_csv(PROCESSED_DATA_DIR / "features_deputados.csv", index=False)
        print(f"Features (centralidades) extraídas e salvas com sucesso!")
        print(df_features.head())
        
    except Exception as e:
        print(f"Erro ao construir features: {e}")

if __name__ == "__main__":
    main()
