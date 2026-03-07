import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pathlib
import os

PROJECT_DIR = pathlib.Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"

def plotar_centralidades_top10(df):
    """
    Plota as 10 maiores centralidades de grau da Câmara.
    """
    df_top10 = df.nlargest(10, 'grau_centralidade')
    
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=df_top10, 
        y='deputado_nome', 
        x='grau_centralidade', 
        hue='partido',
        palette="viridis"
    )
    plt.title('Top 10 Deputados por Centralidade de Grau')
    plt.xlabel('Centralidade de Grau')
    plt.ylabel('Deputado')
    plt.tight_layout()
    # Salvar ou exibir
    plt.savefig(PROCESSED_DATA_DIR / "top10_centralidade.png")
    print(f"Gráfico salvo em {PROCESSED_DATA_DIR / 'top10_centralidade.png'}")
    plt.close()

def plotar_grafo_partido(grafo, partido_selecionado):
    """
    Gera a visualização estática das relações de um partido (similar ao fluxo original).
    """
    subgrafo = nx.Graph()
    for node, data in grafo.nodes(data=True):
        if data.get('partido') == partido_selecionado:
            subgrafo.add_node(node)
            for neighbor in grafo.neighbors(node):
                if grafo.nodes[neighbor].get('partido') == partido_selecionado:
                    subgrafo.add_edge(node, neighbor, weight=grafo[node][neighbor].get('weight', 1))

    if len(subgrafo.nodes) == 0:
        print(f"Nenhum deputado encontrado para o partido {partido_selecionado}")
        return

    pos = nx.spring_layout(subgrafo, k=0.15, iterations=20)
    plt.figure(figsize=(12, 12))
    
    # Desenhar
    nx.draw_networkx_nodes(subgrafo, pos, node_size=300, node_color='skyblue', alpha=0.8)
    nx.draw_networkx_edges(subgrafo, pos, alpha=0.5, edge_color='gray')
    nx.draw_networkx_labels(subgrafo, pos, font_size=8)
    
    plt.title(f"Graça Interpartidária: {partido_selecionado}")
    plt.axis('off')
    plt.tight_layout()
    
    caminho = PROCESSED_DATA_DIR / f"grafo_{partido_selecionado}.png"
    plt.savefig(caminho)
    print(f"Retrato do grafo arquivado em {caminho}")
    plt.close()


def main():
    try:
        df_features = pd.read_csv(PROCESSED_DATA_DIR / "features_deputados.csv")
        plotar_centralidades_top10(df_features)
        
        caminho_gml = PROCESSED_DATA_DIR / "grafo_partidos.gml"
        if caminho_gml.exists():
            grafo = nx.read_gml(caminho_gml)
            plotar_grafo_partido(grafo, "PT")
            plotar_grafo_partido(grafo, "PL")
        
    except FileNotFoundError as e:
        print(f"Erro: Arquivos processados não encontrados. Execute make_dataset.py e build_features.py primeiro. Detalhes: {e}")

if __name__ == "__main__":
    main()
