# YT-TrendFinder
Um script de linha de comando (CLI) para consultar tendências no YouTube Data API.

[![Último Commit](https://img.shields.io/github/last-commit/gaab-sec/YT-TrendFinder?style=for-the-badge&logo=github&color=blue)](https://github.com/gaab-sec/YT-TrendFinder/commits/main)
[![Linguagem Principal](https://img.shields.io/github/languages/top/gaab-sec/YT-TrendFinder?style=for-the-badge&color=blue)](https://github.com/gaab-sec/YT-TrendFinder)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 🚀 Sobre o Projeto

O YT-TrendFinder é um script de linha de comando desenvolvido como um exercício prático de integração de API e automação com Python. O objetivo principal do script é conectar-se à API do YouTube, realizar uma busca por vídeos mais vistos (publicados nos últimos 30 dias) com base em um termo de pesquisa e exibir os resultados de forma estruturada no terminal.

## 📋 Funcionalidades

* **Busca por Consulta:** Permite ao usuário definir um termo de pesquisa (query).
* **Filtragem de Dados:** Busca vídeos publicados nos últimos 30 dias.
* **Consumo de API:** Demonstra o fluxo de autenticação e requisição à API do Google.
* **Exibição Formatada:** Utiliza a biblioteca `rich` para exibir os dados (como título, canal e contagem de visualizações) em uma tabela limpa no terminal.

## ⚙️ Guia de Instalação e Uso

Siga os passos abaixo para executar o projeto localmente.

### 1. Pré-requisitos

* **Python 3.8+**
* **Uma Chave da API do YouTube Data v3**
    * Você pode obter uma gratuitamente no [Google Cloud Console](https://console.cloud.google.com/apis/library/youtube.googleapis.com).

### 2. Instalação

Primeiro, clone o repositório e instale as dependências.

```sh
# 1. Clone este repositório
git clone https://github.com/gaab-sec/YT-TrendFinder

# 2. Entre na pasta do projeto
cd YT-TrendFinder

# 3. (Recomendado) Crie e ative um ambiente virtual
python -m venv venv
# No Windows:
# .\venv\Scripts\activate
# No macOS/Linux:
# source venv/bin/activate

# 4. Instale as bibliotecas necessárias
pip install google-api-python-client python-dotenv rich
```
### 3. Configuração da Chave de API

Para que o script possa se autenticar na API do YouTube, você precisa fornecer sua chave.

1.  Crie um arquivo chamado `.env` na raiz do diretório do projeto.
2.  Dentro deste arquivo `.env`, adicione sua chave no seguinte formato:

    ```
    API_KEY=SUA_CHAVE_DE_API_VAI_AQUI
    ```

### 4. Modo de Uso

Agora basta executar o script principal:

```bash
python main.py "<tópico para pesquisar>"