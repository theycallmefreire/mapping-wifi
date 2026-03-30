import json
import os
from datetime import datetime

# Pasta onde os dados vão ficar
PASTA_DADOS = "dados"

def criar_pasta_dados():
    """Cria a pasta 'dados' se não existir"""
    if not os.path.exists(PASTA_DADOS):
        os.makedirs(PASTA_DADOS)
        print(f"✓ Pasta '{PASTA_DADOS}' criada")

def gerar_nome_arquivo(nome_mapeamento):
    """
    Gera um nome de arquivo único baseado no nome do mapeamento
    
    Ex: "Casa" vira "Casa_2026-03-29_21-55-30.json"
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_limpo = nome_mapeamento.replace(" ", "_")
    return f"{nome_limpo}_{timestamp}.json"

def salvar_mapeamento(nome_mapeamento, dados_por_comodo):
    """
    Salva um mapeamento em JSON
    
    Args:
        nome_mapeamento: Nome do mapeamento (ex: "Casa - Dia 1")
        dados_por_comodo: Dict com dados de cada cômodo
    
    Returns:
        Caminho do arquivo salvo ou None se erro
    """
    criar_pasta_dados()
    
    try:
        # Prepara os dados
        dados_completos = {
            "nome": nome_mapeamento,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "comodos": dados_por_comodo
        }
        
        # Gera o nome do arquivo
        nome_arquivo = gerar_nome_arquivo(nome_mapeamento)
        caminho = os.path.join(PASTA_DADOS, nome_arquivo)
        
        # Salva em JSON
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, indent=2, ensure_ascii=False)
        
        return caminho
    
    except Exception as e:
        print(f"Erro ao salvar: {e}")
        return None

def carregar_mapeamento(caminho_arquivo):
    """
    Carrega um mapeamento do arquivo JSON
    
    Args:
        caminho_arquivo: Caminho completo do arquivo
    
    Returns:
        Dict com os dados ou None se erro
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados
    
    except Exception as e:
        print(f"Erro ao carregar: {e}")
        return None

def listar_mapeamentos():
    """
    Lista todos os mapeamentos salvos
    
    Returns:
        Lista de tuplas (nome_arquivo, nome_mapeamento, data)
    """
    criar_pasta_dados()
    
    mapeamentos = []
    
    try:
        for arquivo in sorted(os.listdir(PASTA_DADOS), reverse=True):
            if arquivo.endswith('.json'):
                caminho = os.path.join(PASTA_DADOS, arquivo)
                dados = carregar_mapeamento(caminho)
                
                if dados:
                    mapeamentos.append({
                        'arquivo': arquivo,
                        'nome': dados.get('nome', 'Sem nome'),
                        'data': dados.get('data', 'Sem data'),
                        'caminho': caminho,
                        'comodos': len(dados.get('comodos', {}))
                    })
        
        return mapeamentos
    
    except Exception as e:
        print(f"Erro ao listar: {e}")
        return []

def deletar_mapeamento(caminho_arquivo):
    """
    Deleta um mapeamento
    
    Args:
        caminho_arquivo: Caminho completo do arquivo
    
    Returns:
        True se sucesso, False se erro
    """
    try:
        os.remove(caminho_arquivo)
        return True
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        return False