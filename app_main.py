import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import time
from datetime import datetime
import threading
import pandas as pd
import os

# Importa os módulos que criamos
from wifi_coleta import get_wifi_strength
from wifi_graficos import criar_grafico_linha, criar_grafico_barras
from wifi_dados import salvar_mapeamento, carregar_mapeamento, listar_mapeamentos

class AppWiFiComodos:
    def __init__(self, root):
        self.root = root
        self.root.title("BatSignal - Mapeador de Wi-Fi por Cômodo")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.iconbitmap('.\imagens\logo.ico')
        
        # Dicionário pra armazenar dados de cada cômodo
        self.dados_por_comodo = {}
        self.comodo_atual = None
        self.coletando = False
        
        # ===== Carrega Logo =====
        self.carregar_logo()
        
        # ===== Frame Superior - Banner com Logo =====
        frame_top = tk.Frame(root, bg="#000000", height=120)
        frame_top.pack(fill=tk.X)
        frame_top.pack_propagate(False)
        
        # Container centralizado
        banner_content = tk.Frame(frame_top, bg="#000000")
        banner_content.pack(expand=True, pady=10)
        
        # Logo
        if self.logo_photo:
            logo_label = tk.Label(banner_content, image=self.logo_photo, bg="#000000")
            logo_label.pack(side=tk.LEFT, padx=20)
        
        # Texto ao lado
        text_frame = tk.Frame(banner_content, bg="#000000")
        text_frame.pack(side=tk.LEFT, padx=20)
        
        titulo = tk.Label(text_frame, text="BatSignal", 
                         font=("Arial", 16, "bold"), bg="#000000", fg="#0078d4")
        titulo.pack(anchor=tk.W)
        
        subtitulo = tk.Label(text_frame, text="Mapeador de Wi-Fi por Cômodo", 
                            font=("Arial", 14), bg="#000000", fg="#666666")
        subtitulo.pack(anchor=tk.W)
        
        # ===== Frame de Seleção de Cômodo =====
        frame_comodo = ttk.LabelFrame(root, text="Cômodo Atual", padding="10")
        frame_comodo.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_comodo, text="Nome do cômodo:").pack(side=tk.LEFT, padx=5)
        self.comodo_var = tk.StringVar(value="Sala")
        self.entry_comodo = ttk.Entry(frame_comodo, textvariable=self.comodo_var, width=20)
        self.entry_comodo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_comodo, text="(ex: Sala, Quarto, Cozinha)").pack(side=tk.LEFT, padx=5)
        
        # ===== Frame de Controles =====
        frame_controls = ttk.LabelFrame(root, text="Configuração da Coleta", padding="10")
        frame_controls.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_controls, text="Duração (segundos):").pack(side=tk.LEFT, padx=5)
        self.duracao_var = tk.StringVar(value="60")
        ttk.Entry(frame_controls, textvariable=self.duracao_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_controls, text="Intervalo (segundos):").pack(side=tk.LEFT, padx=5)
        self.intervalo_var = tk.StringVar(value="5")
        ttk.Entry(frame_controls, textvariable=self.intervalo_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # ===== Frame de Botões =====
        frame_buttons = ttk.Frame(root, padding="10")
        frame_buttons.pack(fill=tk.X, padx=10)
        
        self.btn_iniciar = ttk.Button(frame_buttons, text="Iniciar Coleta", 
                                       command=self.iniciar_coleta)
        self.btn_iniciar.pack(side=tk.LEFT, padx=5)
        
        self.btn_refazer = ttk.Button(frame_buttons, text="Refazer Coleta", 
                                       command=self.refazer_coleta, state=tk.DISABLED)
        self.btn_refazer.pack(side=tk.LEFT, padx=5)
        
        self.btn_proximo = ttk.Button(frame_buttons, text="Próximo Cômodo", 
                                       command=self.proximo_comodo, state=tk.DISABLED)
        self.btn_proximo.pack(side=tk.LEFT, padx=5)
        
        self.btn_graficos = ttk.Button(frame_buttons, text="Ver Gráficos", 
                                        command=self.mostrar_graficos, state=tk.DISABLED)
        self.btn_graficos.pack(side=tk.LEFT, padx=5)
        
        self.btn_salvar = ttk.Button(frame_buttons, text="Salvar Mapeamento", 
                                      command=self.salvar_dados, state=tk.NORMAL)
        self.btn_salvar.pack(side=tk.LEFT, padx=5)
        
        self.btn_carregar = ttk.Button(frame_buttons, text="Carregar Mapeamento", 
                                        command=self.carregar_dados)
        self.btn_carregar.pack(side=tk.LEFT, padx=5)
        
        self.btn_exportar = ttk.Button(frame_buttons, text="Exportar Tudo", 
                                        command=self.exportar_excel, state=tk.DISABLED)
        self.btn_exportar.pack(side=tk.LEFT, padx=5)
        
        # ===== Frame de Status =====
        frame_status = ttk.LabelFrame(root, text="Status", padding="10")
        frame_status.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text widget
        self.text_output = tk.Text(frame_status, height=12, width=85, state=tk.DISABLED)
        self.text_output.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_status, orient=tk.VERTICAL, command=self.text_output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_output.config(yscrollcommand=scrollbar.set)
        
        # ===== Frame de Resumo dos Cômodos =====
        frame_resumo = ttk.LabelFrame(root, text="Cômodos Mapeados", padding="10")
        frame_resumo.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_resumo = ttk.Label(frame_resumo, text="Nenhum cômodo mapeado ainda")
        self.label_resumo.pack()
        
        # ===== Frame com Nome do Mapeamento =====
        frame_nome = ttk.LabelFrame(root, text="Nome do Mapeamento", padding="10")
        frame_nome.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_nome, text="Nome:").pack(side=tk.LEFT, padx=5)
        self.nome_mapeamento_var = tk.StringVar(value="Mapeamento")
        ttk.Entry(frame_nome, textvariable=self.nome_mapeamento_var, width=30).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(frame_nome, text="(ex: Casa - Dia 1, Apartamento, etc)").pack(side=tk.LEFT, padx=5)
    
    def carregar_logo(self):
        """Carrega a logo se existir"""
        self.logo_photo = None
        
        if os.path.exists(".\imagens\logo.png"):
            try:
                img = Image.open(".\imagens\logo.png")
                img.thumbnail((100, 100), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Erro ao carregar logo: {e}")
    
    def atualizar_texto(self, texto):
        """Atualiza o text widget de forma thread-safe"""
        self.text_output.config(state=tk.NORMAL)
        self.text_output.insert(tk.END, texto + "\n")
        self.text_output.see(tk.END)
        self.text_output.config(state=tk.DISABLED)
        self.root.update()
    
    def limpar_texto(self):
        """Limpa o text widget"""
        self.text_output.config(state=tk.NORMAL)
        self.text_output.delete(1.0, tk.END)
        self.text_output.config(state=tk.DISABLED)
    
    def atualizar_resumo(self):
        """Atualiza o label com os cômodos mapeados"""
        if not self.dados_por_comodo:
            self.label_resumo.config(text="Nenhum cômodo mapeado ainda")
        else:
            comodos_list = []
            for comodo, dados in self.dados_por_comodo.items():
                forcas = [d['forca'] for d in dados]
                media = sum(forcas) / len(forcas)
                comodos_list.append(f"• {comodo}: {media:.1f}% (min: {min(forcas)}%, max: {max(forcas)}%)")
            
            texto = "Cômodos coletados:\n" + "\n".join(comodos_list)
            self.label_resumo.config(text=texto)
    
    def coleta_em_thread(self, segundos, intervalo, comodo):
        """Faz a coleta em uma thread separada"""
        dados = []
        self.coletando = True
        tempo_inicio = time.time()
        tempo_decorrido = 0
        
        self.atualizar_texto(f"\n🦇 Coletando dados do cômodo: {comodo}")
        self.atualizar_texto(f"   Duração: {segundos}s | Intervalo: {intervalo}s\n")
        
        while tempo_decorrido < segundos and self.coletando:
            agora = datetime.now().strftime("%H:%M:%S")
            strength = get_wifi_strength()
            
            if strength is not None:
                dados.append({
                    'tempo': agora,
                    'forca': strength
                })
                self.atualizar_texto(f"[{agora}] Sinal: {strength}%")
            else:
                self.atualizar_texto(f"[{agora}] ❌ Erro ao coletar")
            
            time.sleep(intervalo)
            tempo_decorrido = time.time() - tempo_inicio
        
        # Finaliza e mostra resumo
        if self.coletando:
            self.atualizar_texto(f"\n✓ Coleta finalizada!")
            if dados:
                forcas = [d['forca'] for d in dados]
                self.atualizar_texto(f"\n📊 Resumo - {comodo}:")
                self.atualizar_texto(f"   Total de medições: {len(forcas)}")
                self.atualizar_texto(f"   Mínimo: {min(forcas)}%")
                self.atualizar_texto(f"   Máximo: {max(forcas)}%")
                self.atualizar_texto(f"   Médio: {sum(forcas) / len(forcas):.1f}%")
                
                # Armazena os dados
                self.dados_por_comodo[comodo] = dados
                self.comodo_atual = comodo
                self.atualizar_resumo()
                
                # Habilita botões
                self.btn_refazer.config(state=tk.NORMAL)
                self.btn_proximo.config(state=tk.NORMAL)
                self.btn_graficos.config(state=tk.NORMAL)
                self.btn_exportar.config(state=tk.NORMAL)
        else:
            self.atualizar_texto("\n⏸️ Coleta cancelada")
        
        self.coletando = False
        self.btn_iniciar.config(state=tk.NORMAL)
    
    def iniciar_coleta(self):
        """Inicia a coleta"""
        try:
            comodo = self.comodo_var.get().strip()
            
            if not comodo:
                messagebox.showerror("Erro", "Digite o nome do cômodo")
                return
            
            segundos = int(self.duracao_var.get())
            intervalo = int(self.intervalo_var.get())
            
            if segundos <= 0 or intervalo <= 0:
                messagebox.showerror("Erro", "Valores devem ser maiores que 0")
                return
            
            if intervalo > segundos:
                messagebox.showerror("Erro", "Intervalo não pode ser maior que duração")
                return
            
            self.limpar_texto()
            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_refazer.config(state=tk.DISABLED)
            self.btn_proximo.config(state=tk.DISABLED)
            self.btn_graficos.config(state=tk.DISABLED)
            
            thread = threading.Thread(target=self.coleta_em_thread, 
                                     args=(segundos, intervalo, comodo), daemon=True)
            thread.start()
        
        except ValueError:
            messagebox.showerror("Erro", "Digite números válidos")
    
    def refazer_coleta(self):
        """Refaz a coleta do cômodo atual"""
        if self.comodo_atual:
            self.comodo_var.set(self.comodo_atual)
            self.iniciar_coleta()
    
    def proximo_comodo(self):
        """Limpa pra coletar o próximo cômodo"""
        self.limpar_texto()
        self.comodo_var.set("")
        self.entry_comodo.focus()
        self.btn_refazer.config(state=tk.DISABLED)
        self.btn_proximo.config(state=tk.DISABLED)
        self.btn_salvar.config(state=tk.NORMAL)
        self.atualizar_texto("➡️ Pronto pra coletar o próximo cômodo!\nDigite o nome e clique em 'Iniciar Coleta'")
    
    def mostrar_graficos(self):
        """Abre uma nova janela com os gráficos"""
        if not self.dados_por_comodo:
            messagebox.showwarning("Aviso", "Nenhum dado para gerar gráficos")
            return
        
        # Cria uma nova janela
        janela_graficos = tk.Toplevel(self.root)
        janela_graficos.title("Gráficos de Wi-Fi")
        janela_graficos.geometry("1200x800")
        
        # Cria um notebook (abas)
        notebook = ttk.Notebook(janela_graficos)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ===== ABA 1: Gráfico de Linha =====
        frame_linha = ttk.Frame(notebook)
        notebook.add(frame_linha, text="Gráfico de Linha")
        criar_grafico_linha(self.dados_por_comodo, frame_linha)
        
        # ===== ABA 2: Gráfico de Barras =====
        frame_barras = ttk.Frame(notebook)
        notebook.add(frame_barras, text="Gráfico de Barras")
        criar_grafico_barras(self.dados_por_comodo, frame_barras)
    
    def salvar_dados(self):
        """Salva o mapeamento atual em JSON"""
        if not self.dados_por_comodo:
            messagebox.showwarning("Aviso", "Nenhum dado para salvar")
            return
        
        nome = self.nome_mapeamento_var.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Digite um nome para o mapeamento")
            return
        
        try:
            caminho = salvar_mapeamento(nome, self.dados_por_comodo)
            
            if caminho:
                messagebox.showinfo("Sucesso", f"Mapeamento salvo em:\n{caminho}")
                self.atualizar_texto(f"✓ Mapeamento '{nome}' salvo com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao salvar o mapeamento")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")
    
    def carregar_dados(self):
        """Abre uma janela pra selecionar um mapeamento salvo"""
        mapeamentos = listar_mapeamentos()
        
        if not mapeamentos:
            messagebox.showinfo("Aviso", "Nenhum mapeamento salvo encontrado")
            return
        
        # Cria uma janela pra selecionar
        janela_carregar = tk.Toplevel(self.root)
        janela_carregar.title("Carregar Mapeamento")
        janela_carregar.geometry("600x400")
        
        # Listbox com os mapeamentos
        frame_lista = ttk.LabelFrame(janela_carregar, text="Mapeamentos Salvos", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        listbox = tk.Listbox(frame_lista, height=12)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        
        # Preenche a listbox
        items_map = {}
        for idx, m in enumerate(mapeamentos):
            texto = f"{m['nome']} - {m['data']} ({m['comodos']} cômodos)"
            listbox.insert(tk.END, texto)
            items_map[idx] = m
        
        # Frame de botões
        frame_buttons_carregar = ttk.Frame(janela_carregar, padding="10")
        frame_buttons_carregar.pack(fill=tk.X, padx=10, pady=10)
        
        def carregar_selecionado():
            selecao = listbox.curselection()
            
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um mapeamento")
                return
            
            mapeamento = items_map[selecao[0]]
            dados = carregar_mapeamento(mapeamento['caminho'])
            
            if dados:
                # Limpa e carrega os dados
                self.dados_por_comodo = dados['comodos']
                self.nome_mapeamento_var.set(dados['nome'])
                self.atualizar_resumo()
                self.limpar_texto()
                self.atualizar_texto(f"✓ Mapeamento '{dados['nome']}' carregado!")
                self.atualizar_texto(f"   Data: {dados['data']}")
                self.atualizar_texto(f"   Cômodos: {', '.join(self.dados_por_comodo.keys())}")
                
                # Habilita botões
                self.btn_graficos.config(state=tk.NORMAL)
                self.btn_exportar.config(state=tk.NORMAL)
                self.btn_salvar.config(state=tk.NORMAL)
                
                janela_carregar.destroy()
            else:
                messagebox.showerror("Erro", "Falha ao carregar o mapeamento")
        
        def deletar_selecionado():
            selecao = listbox.curselection()
            
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um mapeamento")
                return
            
            mapeamento = items_map[selecao[0]]
            
            if messagebox.askyesno("Confirmar", f"Deletar '{mapeamento['nome']}'?"):
                from wifi_dados import deletar_mapeamento
                if deletar_mapeamento(mapeamento['caminho']):
                    messagebox.showinfo("Sucesso", "Mapeamento deletado")
                    janela_carregar.destroy()
                    self.carregar_dados()
                else:
                    messagebox.showerror("Erro", "Falha ao deletar")
        
        btn_carregar = ttk.Button(frame_buttons_carregar, text="Carregar", 
                                  command=carregar_selecionado)
        btn_carregar.pack(side=tk.LEFT, padx=5)
        
        btn_deletar = ttk.Button(frame_buttons_carregar, text="Deletar", 
                                 command=deletar_selecionado)
        btn_deletar.pack(side=tk.LEFT, padx=5)
        
        btn_cancelar = ttk.Button(frame_buttons_carregar, text="Cancelar", 
                                  command=janela_carregar.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=5)
    
    def exportar_excel(self):
        """Exporta todos os dados para Excel"""
        if not self.dados_por_comodo:
            messagebox.showwarning("Aviso", "Nenhum dado coletado para exportar")
            return
        
        try:
            import pandas as pd
        except ImportError:
            messagebox.showerror("Erro", "pandas não instalado. Execute: pip install pandas openpyxl")
            return
        
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not arquivo:
            return
        
        try:
            with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
                # Cria uma aba pra cada cômodo
                for comodo, dados in self.dados_por_comodo.items():
                    df = pd.DataFrame(dados)
                    df.to_excel(writer, sheet_name=comodo[:31], index=False)
                
                # Cria uma aba de resumo
                resumo_data = []
                for comodo, dados in self.dados_por_comodo.items():
                    forcas = [d['forca'] for d in dados]
                    resumo_data.append({
                        'Cômodo': comodo,
                        'Mínimo (%)': min(forcas),
                        'Máximo (%)': max(forcas),
                        'Médio (%)': round(sum(forcas) / len(forcas), 1),
                        'Medições': len(forcas)
                    })
                
                df_resumo = pd.DataFrame(resumo_data)
                df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
            
            messagebox.showinfo("Sucesso", f"Mapeamento exportado para:\n{arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")

# Executa a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = AppWiFiComodos(root)
    root.mainloop()