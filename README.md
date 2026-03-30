# 📡 Mapping Wi-Fi


Um aplicativo desktop para mapear e analisar a qualidade do sinal Wi-Fi em diferentes cômodos da sua casa.

## 🎯 Funcionalidades

- ✅ **Coleta Automática**: Coleta a força do sinal Wi-Fi em intervalos definidos
- 📊 **Gráficos**: Visualiza os dados com gráficos de linha e barras
- 💾 **Salvar/Carregar**: Armazena mapeamentos em JSON e carrega posteriormente
- 📁 **Exportar Excel**: Exporta os dados em planilhas Excel com resumo
- 🎨 **Interface Gráfica**: Interface amigável com tkinter

## 🚀 Como Usar

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/theycallmefreire/mapping-wifi.git
cd mapeador-wifi
```

2. **Crie um ambiente virtual:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

### Executar

```bash
python app_main.py
```

## 📝 Como Funciona

1. **Digite o nome do cômodo** (ex: Sala, Quarto, Cozinha)
2. **Clique em "Iniciar Coleta"** para começar a coletar dados
3. O app coleta a força do sinal em intervalos regulares durante 1 minuto
4. **Visualize os dados** em tempo real na tela
5. **Refaça a coleta** se necessário ou vá pro **próximo cômodo**
6. **Veja os gráficos** clicando em "Ver Gráficos"
7. **Salve o mapeamento** com um nome descritivo
8. **Exporte em Excel** para análise posterior

## 📊 Tipos de Gráficos

### Gráfico de Linha
- Mostra como a força do sinal varia ao longo do tempo
- Uma linha para cada cômodo
- Inclui linha tracejada com a média

### Gráfico de Barras
- Compara o sinal médio entre cômodos
- Cores dinâmicas:
  - 🟢 Verde: Excelente (>95%)
  - 🟠 Laranja: Bom (92-95%)
  - 🔴 Vermelho: Fraco (<92%)

## 📂 Estrutura do Projeto

```
mapeador-wifi/
├── app_main.py           # Interface gráfica principal
├── wifi_coleta.py        # Lógica de coleta do sinal
├── wifi_graficos.py      # Geração de gráficos
├── wifi_dados.py         # Salvar/carregar dados em JSON
├── dados/                # Pasta com mapeamentos salvos
├── requirements.txt      # Dependências do projeto
├── .gitignore           # Arquivos ignorados pelo git
└── README.md            # Este arquivo
```

## 🛠️ Dependências

- **pandas**: Manipulação e análise de dados
- **openpyxl**: Criação de arquivos Excel
- **matplotlib**: Geração de gráficos
- **seaborn**: Estilo dos gráficos
- **tkinter**: Interface gráfica (vem com Python)

## 💡 Dicas

- **Melhor cobertura**: Coleta em vários pontos de cada cômodo para resultado mais preciso
- **Mapeamentos**: Salve mapeamentos diferentes (ex: "Casa - Antes", "Casa - Depois")
- **Comparação**: Use os gráficos para identificar áreas com fraco sinal
- **Excel**: Exporte os dados para fazer análises mais detalhadas

## 🤝 Contribuindo

Sinta-se livre para fazer fork, criar issues e enviar pull requests!

## 📜 Licença

MIT License

## 👨‍💻 Autor

Desenvolvido com ❤️

---

**Aproveite o mapeador!** 📡✨