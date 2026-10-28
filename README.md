# 🚗 DriverPulse — Auditoria e Checkout de Drivers do Sistema

O **DriverPulse** é uma aplicação desktop desenvolvida em Python e PyQt6 com foco em auditoria de hardware e gerenciamento da integridade de drivers no Windows. A ferramenta realiza uma varredura aprofundada nos componentes físicos do computador (Placas de Vídeo, Áudio, Rede, Processador e Chipset/Sistema), compara as versões instaladas com uma base de dados local de recomendações, salva o histórico de análises em um banco SQLite e fornece links oficiais dos fabricantes para atualização rápida.

---

## 📸 Demonstração da Interface

A interface do DriverPulse conta com um tema escuro (Dark Theme) moderno e responsivo, organizando os dispositivos em colunas claras com status visual por cores e links diretos para os fabricantes.

---

## ⚡ Funcionalidades Principais

* 🔍 **Mapeamento de Hardware Completo:** Detecta GPUs (AMD/NVIDIA/Intel), adaptadores de rede físicos, controladores de áudio, processador e drivers de chipset/sistema via WMI (*Windows Management Instrumentation*).
* 📊 **Diagnóstico por Status Visual:**
  * 🟢 **Atualizado:** O driver está em conformidade com a versão recomendada.
  * 🔴 **Desatualizado:** Detectada uma versão mais recente recomendada.
  * 🟡 **Genérico MS:** O dispositivo está utilizando o driver genérico padrão da Microsoft.
* 🔗 **Links Diretos Oficiais:** Acesso instantâneo com 1-clique às páginas de suporte do fabricante de cada dispositivo no seu navegador padrão.
* 💾 **Persistência em Banco SQLite:** Armazena automaticamente os resultados e o histórico completo das varreduras em `data/driver_audit.db`.
* 📄 **Exportação de Relatórios HTML:** Gera um relatório interativo e detalhado da auditoria em formato HTML, ideal para técnicos, suporte de TI e arquivos de manutenção.
* 🚀 **Executável Portátil:** Pronto para rodar diretamente via pen drive sem a necessidade de instalação prévia do Python.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Interface Gráfica (GUI):** PyQt6
* **Coleta de Hardware:** `wmi` (Windows Management Instrumentation)
* **Banco de Dados Local:** SQLite3
* **Compilação Executável:** PyInstaller

---

## 📁 Estrutura do Projeto

```text
DriverAudit/
│
├── data/
│   ├── driver_audit.db       # Banco de dados SQLite (histórico de varreduras)
│   └── drivers_db.json       # Base JSON de versões de referência
│
├── modules/
│   ├── __init__.py
│   ├── comparator.py         # Lógica de comparação e status das versões
│   ├── database.py           # Gestão do banco de dados SQLite
│   ├── driver_scanner.py     # Varredura de hardware via WMI
│   └── exporter.py           # Gerador de relatórios HTML
│
├── ui/
│   ├── __init__.py
│   └── main_window.py        # Interface gráfica com PyQt6
│
├── relatorios/               # Pasta de destino dos relatórios HTML gerados
├── main.py                   # Ponto de entrada (Entrypoint) da aplicação
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação do projeto
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Sistema Operacional **Windows** (necessário para as consultas WMI de hardware).
* **Python 3.10** ou superior instalado.

### 1. Clonar o repositório e entrar na pasta
```powershell
git clone https://github.com/seu-usuario/DriverAudit.git
cd DriverAudit
```

### 2. Criar e ativar o ambiente virtual (venv)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências
```powershell
pip install -r requirements.txt
```

### 4. Executar a aplicação
```powershell
python main.py
```

---

## 📦 Como Compilar para Executável (.EXE)

Para gerar a versão executável independente (portátil):

1. Com o `venv` ativado, execute o comando do PyInstaller:
   ```powershell
   pyinstaller --noconsole --onedir main.py
   ```
2. A aplicação compilada será salva dentro da pasta `dist/main/`.
3. Renomeie a pasta ou o arquivo `main.exe` para `DriverPulse.exe`.

> **⚠️ Importante:** Mantenha sempre a pasta `_internal` no mesmo diretório do arquivo `.exe` para garantir a execução correta das dependências compiladas.
