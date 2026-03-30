import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Patch

def criar_grafico_linha(dados_por_comodo, parent_frame):
    """
    Cria gráfico de linha mostrando sinal ao longo do tempo
    
    Args:
        dados_por_comodo: Dict com dados de cada cômodo
        parent_frame: Frame do tkinter onde colocar o gráfico
    """
    comodos = list(dados_por_comodo.keys())
    cores = ['#FF6B6B', '#FFA500', '#4CAF50', '#2196F3', '#9C27B0']
    
    fig = plt.Figure(figsize=(12, 8), dpi=100)
    
    for idx, comodo in enumerate(comodos):
        df = pd.DataFrame(dados_por_comodo[comodo])
        
        ax = fig.add_subplot(len(comodos), 1, idx + 1)
        
        ax.plot(range(len(df)), df['forca'], 
               marker='o', 
               linewidth=3, 
               markersize=8, 
               color=cores[idx],
               label=comodo,
               markerfacecolor='white',
               markeredgewidth=2,
               markeredgecolor=cores[idx])
        
        ax.set_title(f'Força do Sinal ao Longo do Tempo - {comodo}', 
                    fontsize=11, fontweight='bold')
        ax.set_xlabel('Número da Medição', fontsize=10)
        ax.set_ylabel('Força (%)', fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim(80, 105)
        
        media = df['forca'].mean()
        ax.axhline(y=media, color=cores[idx], linestyle='--', alpha=0.5, linewidth=2, 
                   label=f'Média: {media:.1f}%')
        ax.legend(loc='best', fontsize=9)
    
    fig.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    return canvas


def criar_grafico_barras(dados_por_comodo, parent_frame):
    """
    Cria gráfico de barras comparando sinal médio por cômodo
    
    Args:
        dados_por_comodo: Dict com dados de cada cômodo
        parent_frame: Frame do tkinter onde colocar o gráfico
    """
    fig = plt.Figure(figsize=(12, 6), dpi=100)
    ax = fig.add_subplot(111)
    
    comodos = list(dados_por_comodo.keys())
    
    # Prepara dados pra resumo
    resumo_data = []
    for comodo in comodos:
        dados = dados_por_comodo[comodo]
        forcas = [d['forca'] for d in dados]
        resumo_data.append({
            'Cômodo': comodo,
            'Mínimo': min(forcas),
            'Máximo': max(forcas),
            'Médio': sum(forcas) / len(forcas)
        })
    
    df_resumo = pd.DataFrame(resumo_data)
    df_resumo = df_resumo.sort_values('Médio', ascending=False)
    
    # Cores dinâmicas
    colors = ['#4CAF50' if x > 95 else '#FFA500' if x > 92 else '#FF6B6B' 
              for x in df_resumo['Médio']]
    
    bars = ax.bar(df_resumo['Cômodo'], df_resumo['Médio'], 
                 color=colors, 
                 edgecolor='black', 
                 linewidth=2,
                 alpha=0.8,
                 width=0.6)
    
    ax.set_title('Comparação de Sinal Médio por Cômodo', 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_ylabel('Força Média (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Cômodo', fontsize=12, fontweight='bold')
    ax.set_ylim(80, 105)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Adiciona valores nas barras
    for bar, row in zip(bars, df_resumo.itertuples()):
        height = bar.get_height()
        
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'Min: {row.Mínimo}%\nMax: {row.Máximo}%',
                ha='center', va='center', fontsize=8, fontweight='bold', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Legenda
    legend_elements = [
        Patch(facecolor='#4CAF50', edgecolor='black', label='Excelente (>95%)'),
        Patch(facecolor='#FFA500', edgecolor='black', label='Bom (92-95%)'),
        Patch(facecolor='#FF6B6B', edgecolor='black', label='Fraco (<92%)')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    fig.tight_layout()
    
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    
    return canvas