# Sistema de Ponto Eletrônico com Reconhecimento Facial

Sistema desktop desenvolvido em Python para controle e gestão de ponto de funcionários, utilizando **Reconhecimento Facial** seguro baseado em comparação de pixels (OpenCV), interface gráfica moderna (**CustomTkinter**) e banco de dados **SQLite**.

---

## 🚀 Funcionalidades

# Sistema de Ponto Eletrônico com Reconhecimento Facial

Sistema desktop desenvolvido em Python com CustomTkinter e SQLite para controle de ponto por reconhecimento facial e gestão de funcionários.

- **Registro de Ponto:** Entrada e saída automatizada por reconhecimento facial.
- **Gestão de Funcionários:** Cadastro com cargos personalizados e exclusão segura por ID único.
- **Relatórios:** Consulta de registros com filtro por nome, exportação para CSV/Excel e janela de correção manual de horários.
- **Banco de Dados:** SQLite integrado com inicialização automática.

---

## 🛠️ Tecnologias Utilizadas

- **Python** (Linguagem principal)
- **CustomTkinter** (Interface gráfica)
- **OpenCV (`cv2`)** (Captura de vídeo, processamento de imagem e comparação de histogramas)
- **SQLite3** (Armazenamento local de dados e histórico de pontos)
- **Hashlib** (Segurança e criptografia de senhas)

---

## 📦 Como Executar o Projeto

1. **Clone o repositório:**

   ```bash
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
   cd seu-repositorio

   ```

2. **Instale as dependências necessárias:**
   pip install customtkinter opencv-python

3. **Execute a aplicação:**
   python app.py
