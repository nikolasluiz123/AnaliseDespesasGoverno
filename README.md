## Introdução

O objetivo do projeto é apresentar 3 dashboards dinâmicos referentes a dados do [portal da transparência](https://portaldatransparencia.gov.br/download-de-dados/despesas),
especificamente dados dos documentos e Empenho, Liquidação e Pagamentos.

## Explicação da Arquitetura do Projeto

O projeto utiliza a biblioteca [Dash](https://dash.plotly.com/) para a montagem dos gráficos, [Pandas](https://pandas.pydata.org/)
para manipular os arquivos csv e mais algumas bibliotecas do python para manipulação dos dados.

O projeto todo consiste em transformar dados de arquivos CSV em dados tabulares que ficam armazenados em um
banco de dados do SQLite. Para manipular esses dados foi utilizado o padrão Data Access Object, então para cada
conceito (Empenho, Liquidação e Pagamentos) foi implementada uma classe responsável por manipular esse conjunto de dados.

Dessa forma, para construir cada um dos gráficos contidos no dashboard foram implementadas consultas com os devidos filtros,
isso permite que seja possível interagir com os gráficos.

## Preparando Ambiente

Para utilizar os dashboards no momento será necessário baixar o repositório do projeto e rodar ele localmente,
a versão python utilizada é 3.12 e pode ser baixada [aqui](https://www.python.org/downloads/release/python-3120/).

Após ter o python devidamente instalado e o repositório clonado, é interessante criar um ambiente virtual dentro do projeto
clonado. É possível fazer isso utilizando o comando `python3 -m venv .venv` no terminal estando dentro do diretório
do projeto.

Agora basta ativar o ambiente virtual, no linux pode ser utilizado `source .venv/bin/activate` e no windows
`.venv\Scripts\Activate`.

Depois de criar o ambiente virtual e ativar ele, podemos realizar o download e instalação de todas as dependências necessárias para o
projeto funcionar devidamente nesse ambiente virtual, dessa forma essas dependências estarão apenas no projeto e não na máquina
como um todo. Você pode realizar essa operação com o comando `pip install -r requirements.txt`.

Após isso, é necessário baixar os arquivos csv do diretório [drive compartilhado](https://drive.google.com/drive/folders/13JRM_bCID2-QlthrAvUbL9VjLdP2VVTt?usp=sharing), pois a aplicação necessita
deles para criar a base de dados SQLite, a qual é utilizada para montar os gráficos. Após baixar, você deve copiar todos os arquivos
csv e colocá-los no diretório `data/files` do projeto, precisa ser especificamente nesse diretório, pois é onde a implementação
tentará ler os arquivos CSV e gravar os dados em tabelas.

## Execução dos Dashboards

Existem 3 dashboards implementados, cada um focado em um tipo de documento. 

O primeiro dashboard é encontrado no arquivo `empenho/dashboard_empenho.py`, como o nome sugere, ele
é focado nos dados do Empenho. Ao executar esse arquivo ele rodará em `localhost` na porta `8050`.

O segundo dashboard é encontrado no arquivo `liquidacao/dashboard_liquidacao.py`, como o nome sugere, ele
é focado nos dados do Liquidação. Ao executar esse arquivo ele rodará em `localhost` na porta `8051`.

O terceiro dashboard é encontrado no arquivo `pagamento/dashboard_pagamento.py`, como o nome sugere, ele
é focado nos dados do Pagamento. Ao executar esse arquivo ele rodará em `localhost` na porta `8052`.

Cada um dos dashboards é executado em portas específicas, sendo possível iniciar todos os servidores
simultaneamente para visualizar todos os gráficos.