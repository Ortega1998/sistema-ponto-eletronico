# Sistema de Ponto Eletrônico com Reconhecimento Facial

Sistema desktop desenvolvido em Python para controle e gestão de ponto de funcionários, utilizando **Reconhecimento Facial** seguro baseado em comparação de pixels (OpenCV), interface gráfica moderna (**CustomTkinter**) e banco de dados **SQLite**.

---

## 🚀 Funcionalidades

- **Registro e Validação Facial:** Captura e valida a foto do funcionário em tempo real utilizando a webcam, garantindo segurança na marcação do ponto.
- **Controle Inteligente de Turno:** Alternância automática inteligente entre **Entrada** e **Saída** com base nos registros do dia.
- **Cadastro Integrado:** Cadastro simultâneo do colaborador na base de dados relacional e salvamento da amostra facial.
- **Relatórios e Filtros:** Tela dedicada para consulta de histórico com filtros flexíveis por nome do funcionário e data.
- **Interface Moderna:** Design limpo e responsivo utilizando o tema escuro do CustomTkinter.

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
