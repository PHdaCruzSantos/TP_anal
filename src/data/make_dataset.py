import requests
import pandas as pd
import pathlib
import os

PROJECT_DIR = pathlib.Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"

def obter_ids_votacoes():
    """Busca a lista de IDs de votações recentes."""
    url = "https://dadosabertos.camara.leg.br/api/v2/votacoes"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json().get('dados', [])
        return [voto['id'] for voto in dados]
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição dos eventos: {e}")
        return []

def coletar_votos_por_evento(evento_id):
    """Obtém detalhes de uma votação específica e as orientações dos deputados."""
    url = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{evento_id}/votos"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json().get('dados', [])
        
        registros = []
        for dado in dados:
            registros.append({
                "votacao_id": evento_id,
                "deputado_nome": dado['deputado_']['nome'],
                "partido": dado['deputado_']['siglaPartido'],
                "uf": dado['deputado_']['siglaUf'],
                "tipo_voto": dado['tipoVoto']
            })
        return registros
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição da votação {evento_id}: {e}")
        return []

def main():
    """Rotina principal para gerar e salvar os dados raw."""
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    print("Obtendo IDs das votações...")
    ids_votacoes = obter_ids_votacoes()
    
    if not ids_votacoes:
        print("Nenhuma votação encontrada.")
        return
        
    print(f"Coletando votos para {len(ids_votacoes)} votações...")
    todos_votos = []
    
    for id_voto in ids_votacoes:
        registros = coletar_votos_por_evento(id_voto)
        todos_votos.extend(registros)
        
    df_votos = pd.DataFrame(todos_votos)
    
    arquivo_saida = RAW_DATA_DIR / "votos_camara.csv"
    df_votos.to_csv(arquivo_saida, index=False)
    print(f"Dados brutos extraídos e salvos em {arquivo_saida} com sucesso! Shape: {df_votos.shape}")

if __name__ == "__main__":
    main()
