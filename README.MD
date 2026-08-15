# 🕒 Sistema de Ponto Eletrônico Desktop

Sistema desenvolvido em Python para controle de jornada de trabalho com autenticação via **QR Code**, interface gráfica moderna, geração de relatórios em **PDF** e painel administrativo completo.

## 🚀 Tecnologias e Ferramentas

O projeto foi construído utilizando as seguintes tecnologias e bibliotecas:

- **Python 3.x** - Linguagem principal de programação.
- **CustomTkinter** - Framework para construção da interface gráfica moderna (Dark/Light mode).
- **OpenCV & pyzbar** - Utilizados para captura de webcam e leitura/decodificação dos QR Codes dos crachás.
- **SQLite3** - Banco de dados relacional leve e embutido para armazenamento de usuários e registros de ponto.
- **ReportLab** - Biblioteca para geração automatizada de relatórios e comprovantes em formato PDF.
- **Hashlib (Bcrypt/Sha)** - Segurança para criptografia de senhas dos funcionários.

---

## 📂 Estrutura do Projeto

- `app.py` - Dashboard principal (Interface gráfica com abas).
- `main.py` - Script de leitura de ponto via webcam.
- `banco.py` - Configuração do banco de dados e funções de segurança.
- `relatorio_filtrado.py` - Geração de relatórios em PDF com filtros dinâmicos.
- `cadastrar.py` / `gerar_qrcode.py` - Utilitários de suporte.

---

## ⚙️ Como Instalar e Executar

Siga os passos abaixo para rodar o projeto localmente na sua máquina:

### 1. Clonar o repositório

### 1. Clonar o repositório

```bash
git clone [https://github.com/SEU_USUARIO/sistema-ponto-eletronico.git](https://github.com/SEU_USUARIO/sistema-ponto-eletronico.git)
cd sistema-ponto-eletronico

### 2. Instalar as dependências
Certifique-se de ter o Python instalado e execute o seguinte comando no terminal para instalar as bibliotecas necessárias:

pip install customtkinter opencv-python pyzbar reportlab

### 3. Executar o Sistema
Para abrir o painel de controle principal (Dashboard):

python app.py

(Opcional: Você pode criar um atalho utilizando um script .vbs para abrir a aplicação de forma totalmente oculta e direta na Área de Trabalho).

```
