# 🕒 Sistema de Ponto Eletrônico Desktop

> Um sistema moderno, leve e seguro desenvolvido em Python para o controle automatizado de jornadas de trabalho utilizando leitura de **QR Code** via webcam, painel administrativo e relatórios gerenciais em PDF.

---

## 📸 Demonstração & Recursos

- **🔐 Autenticação via QR Code:** Leitura rápida e segura do crachá do funcionário.
- **🎨 Interface Moderna:** Desenvolvida com _CustomTkinter_, suportando modo escuro/claro nativo do Windows.
- **📊 Relatórios Automatizados:** Geração de relatórios consolidados e comprovantes em formato **PDF** com filtros avançados.
- **🛡️ Segurança de Dados:** Senhas criptografadas e banco de dados SQLite integrado.

---

## 🚀 Tecnologias e Ferramentas

O projeto foi construído utilizando as seguintes tecnologias:

- ![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python) **Python** - Linguagem principal.
- ![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-green?style=flat-square) **CustomTkinter** - Framework de interface gráfica.
- ![OpenCV](https://img.shields.io/badge/Vision-OpenCV-red?style=flat-square&logo=opencv) **OpenCV & Pyzbar** - Processamento de imagem e leitura de QR Code.
- ![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?style=flat-square&logo=sqlite) **SQLite3** - Banco de dados embutido.
- ![ReportLab](https://img.shields.io/badge/PDF-ReportLab-orange?style=flat-square) **ReportLab** - Geração de documentos PDF.

---

## ⚙️ Como Instalar e Executar

Siga os passos abaixo para rodar o projeto localmente na sua máquina:

### 1️⃣ Clonar o repositório

Abra o terminal na pasta desejada e execute:

```bash
git clone [https://github.com/SEU_USUARIO/sistema-ponto-eletronico.git](https://github.com/SEU_USUARIO/sistema-ponto-eletronico.git)
cd sistema-ponto-eletronico

2️⃣ Instalar as dependênciasCertifique-se de ter o Python instalado e execute o comando abaixo para instalar as bibliotecas necessárias:Bashpip install customtkinter opencv-python pyzbar reportlab

3️⃣ Executar o SistemaPara abrir o painel de controle principal (Dashboard):Bashpython app.py

💡 Dica Pro: Você pode criar um atalho utilizando um script .vbs na sua Área de Trabalho para abrir a aplicação de forma totalmente oculta e direta, sem exibir o terminal do Windows!

📂 Estrutura do ProjetoArquivo / PastaDescriçãoapp.pyDashboard principal com abas e gerenciamento.main.pyScript de leitura de ponto via webcam.banco.pyConexão com o banco e criptografia de senhas.relatorio_filtrado.pyGeração de relatórios em PDF com filtros.sistema_ponto.dbBanco de dados local SQLite.
```
