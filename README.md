# Who's Plants
"**Who's Plants?**" é um jogo inspirado no universo de Plants vs Zombies. A cada dia, uma planta aleatória é escolhida como a "planta do dia", e o jogador deve tentar adivinhar qual é, baseando-se nas suas características. O jogo compara o palpite do jogador com a planta do dia e mostra se o valor de cada característica está correto ou não.

![Tela Inicial](caminho/para/a/imagem1.png)

### Badges
<p align="center">

![GitHub License](https://img.shields.io/github/license/HetrisleyGomes/whos-plants)
![Linguagem](https://img.shields.io/badge/python-3.x-blue)
![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

</p>


## Índice

* [Who's Plants?](#who's-plants)
* [Badges](#badges)
* [Índice](#índice)
* [Descrição](#descrição)
* [Informações](#🛠️-informações)
* [Uso](#🎲-uso)
* [Estrutura de Pastas](#📁-estrutura-de-pastas)
* [Como Jogar](#👾-como-jogar)
* [Tecnologias](#⚙️-tecnologias-usadas)
* [Contribuindo](#💡-contribuindo)
* [Contatos](#contatos)
* [Licença](#licença)
* [Créditos](#créditos)


## Descrição
No **Who's Plants?**, o jogador faz um palpite de qual planta do jogo é a "planta do dia". O jogo compara as características do palpite com a planta do dia (como nome, família, custo de sóis, resistência, dano, recarga, uso, raridade, tipo de planta e origem). Se as características do palpite coincidirem com as da planta do dia, o campo correspondente fica verde. Caso contrário, fica vermelho.

O objetivo é adivinhar qual é a planta do dia, mas sem perder. O jogador pode continuar chutando até acertar, e o jogo fornece dicas ao longo do processo.

### Status do Projeto
<h4 align="center"> 
	🚧  Who's Plants 🌱 Em desenvolvimento...  🚧
</h4>

## 🛠️ Informações 
### Dependências
Para rodar o jogo localmente, você vai precisar instalar as dependências listadas no requirements.txt:

```bash
pip install -r requirements.txt
```
#### As dependências incluem:

- Flask
- OpenPyXL
- Pandas
- NumPy
- entre outras...

## 🎲 Uso

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
[Git](https://git-scm.com), [Python](https://www.python.org/). 
Além disto é bom ter um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)

### Instalação
1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/whos-plants.git
```
2. Acesse o diretório do projeto:
```bash
cd whos-plants
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Execute o servidor Flask:
```bash
python run.py
```

5. Abra seu navegador e vá até http://127.0.0.1:5000/ para jogar.

## 📁 Estrutura de Pastas
Aqui está a estrutura de pastas do projeto para facilitar a compreensão:

```php
whos-plants/
│
├── run.py      # Arquivo principal que roda o servidor Flask
├── requirements.txt        # Arquivo com todas as dependências do projeto
├── src/
│   ├── main/
│   │   ├── routes/     # Arquivos de rotas flask
│   │   │   ├── routes.py       # Arquivos de rotas do modo principal
│
│   │   ├── static/     # Arquivos estáticos como CSS, JavaScript e imagens
│   │   │   ├── styles/
│   │   │   ├── icons/
│   │   │   └── images/
│   │
│   │   ├── templates/      # Templates HTML do jogo
│   │   │   ├── index.html      # Página inicial
│   │   │   └── base.html       # Página base do jogo
│
├── data/       # Arquivos de dados, como o banco de dados de plantas (Excel)
│   └── PVZ.xlsx        # Banco de dados com as informações das plantas
│
└── LICENSE     # Arquivo com a licença MIT
```

## 👾 Como Jogar
1. O objetivo do jogo é adivinhar a "planta do dia".
1. Digite um palpite no campo de input e clique no botão de chute.
1. O jogo fará uma comparação entre o palpite e a planta do dia, 1. mostrando em verde as informações corretas e em vermelho as 1. incorretas.
1. Após 5 e 10 palpites, você poderá revelar dicas adicionais.
1. Continue jogando até adivinhar a planta do dia!

### Tela Principal
- **Campo de Input**: Onde você digita seu palpite.
- **Dicas**: Duas dicas opcionais, reveladas após 5 e 10 palpites.
- **Tabela de Palpites**: Uma tabela com seus palpites anteriores e a comparação de cada característica.

### Modos Futuros
- Modo "Planta da versão chinesa": Tente adivinhar a planta da versão chinesa de Plants vs Zombies 2.
- Modo "Planta da versão Heroes": Tente adivinhar a planta da versão de Plants vs Zombies Heroes.

### Funcionalidades Futuras
- Adicionar informações sobre quantas pessoas acertaram a planta do dia.
- Possibilidade de compartilhar o número de palpites usados para adivinhar a planta do dia.
- Modos adicionais baseados em versões do jogo.

## ⚙️ Tecnologias Usadas
O projeto foi construído utilizando uma combinação de tecnologias para fornecer uma experiência divertida e interativa. Aqui estão as principais:

### Frontend
- **HTML**: Usado para estruturar o conteúdo da página, como campos de input, botões e a tabela de palpites.
- **CSS**: Responsável pela aparência e layout da página, garantindo que o jogo tenha uma interface visualmente agradável.
- **JavaScript**: Usado para interatividade no frontend, como controlar os palpites e interagir com o backend para mostrar as comparações.

### Backend
- **Python**: Linguagem usada para implementar a lógica do jogo e o servidor web.
- **Flask**: Framework web em Python utilizado para criar o servidor que entrega as páginas HTML e gerencia as requisições.
- **Pandas e OpenPyXL**: Utilizados para ler o banco de dados de plantas, que está armazenado em um arquivo Excel (plants_data.xlsx). O Pandas ajuda a manipular e organizar os dados, enquanto o OpenPyXL é utilizado para ler os arquivos Excel.

### Banco de Dados
O banco de dados do jogo é armazenado em um arquivo Excel. Cada linha contém informações sobre uma planta, como nome, família, custo de sóis, resistência, dano, recarga, tipo de planta e origem. O arquivo é lido pelo código Python para determinar a planta do dia e fazer as comparações.

## 💡 Contribuindo
Contribuições são bem-vindas! Você pode contribuir de várias formas:

- Relatar bugs
- Sugerir melhorias
- Enviar pull requests
- Para enviar uma contribuição, basta criar uma issue ou abrir um pull request.

## Contato
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/83302157?v=4" width=115><br><sub>Hetrisley Gomes</sub>](https://github.com/HetrisleyGomes) |
| :---: |

[![Linkedin Badge](https://img.shields.io/badge/-Linkedin-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/hetrisley-gomes/)](https://www.linkedin.com/in/hetrisley-gomes/)


## Licença
Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Créditos
- Este é um projeto de fã, sem fins lucrativos, inspirado na franquia Plants vs Zombies.
- O banco de dados usado no jogo foi baseado na franquia Plants vs Zombies.
- A imagem de favicon foi retirada de Plants vs Zombies Fandom.