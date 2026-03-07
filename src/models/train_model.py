import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib

PROJECT_DIR = pathlib.Path(__file__).resolve().parents[2]
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"

def load_data():
    """Carrega as features pré-computadas."""
    return pd.read_csv(PROCESSED_DATA_DIR / "features_deputados.csv")

def example_supervised_learning(df):
    """
    Exemplo: Prever o partido político do deputado com base no Grau e Centralidade (Regressão Logística/Random Forest).
    Atenção: Na prática, precisamos de mais features (como os votos brutos na matriz de adjacência) para melhorar isso.
    """
    print("--- Aprendizado Supervisionado: Prevendo Partidos ---")
    
    # Filtrar apenas partidos com maior representatividade (para simplificar o exemplo)
    partidos_top = df['partido'].value_counts().head(5).index
    df_top = df[df['partido'].isin(partidos_top)]
    
    X = df_top[['grau_centralidade', 'intermediacao', 'grau_conexao']]
    y = df_top['partido']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train)
    
    y_pred = clf.predict(X_test_scaled)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
def example_unsupervised_learning(df):
    """
    Exemplo: Clusterização (K-Means) de deputados por similaridade de conexão. E redução com PCA.
    """
    print("\n--- Aprendizado Não Supervisionado: Agrupamentos e PCA ---")
    
    X = df[['grau_centralidade', 'intermediacao', 'grau_conexao']]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Clusterização K-Means (Exemplo 4 clusters)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
    df['cluster'] = kmeans.fit_predict(X_scaled)
    
    # Redução de dimensionalidade para visualização 2D (PCA)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(X_scaled)
    
    df['pca_one'] = pca_result[:,0]
    df['pca_two'] = pca_result[:,1]
    
    print(f"Variância explicada pelo PCA: {sum(pca.explained_variance_ratio_)*100:.2f}%")
    
    # Plot dos Clusters
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x="pca_one", y="pca_two",
        hue="cluster",
        palette=sns.color_palette("hsv", 4),
        data=df,
        legend="full",
        alpha=0.6
    )
    plt.title('Clusters K-Means visualizados usando PCA')
    plt.savefig(PROCESSED_DATA_DIR / "kmeans_clusters_pca.png")
    print(f"Plot de clusters salvo em: {PROCESSED_DATA_DIR / 'kmeans_clusters_pca.png'}")
    plt.close()

def main():
    try:
        df = load_data()
        example_supervised_learning(df)
        example_unsupervised_learning(df)
    except FileNotFoundError as e:
        print(f"Erro ao carregar dados. Rode pipeline de build_features. {e}")

if __name__ == "__main__":
    main()
