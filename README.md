# Fiap_TechChallange_Embrapa

O que faz essa API?
Essa API faz a leitura dos dados disponíveis no site da embrapa (http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01) e os  retorna de maneira estruturada em formato JSON.
Através da seleção dos parâmetros de entrada abaixo, a API fará a leitura da respectiva aba da site.
  Opção
    "PRODUCAO"
    "PROCESSAMENTO"
    "COMERCIALIZACAO"
    "IMPORTACAO"
    "EXPORTACAO"

  Subopção em aba PROCESSAMENTO
    "VINIFERAS"
    "AMERICANAS"
    "UVA_DE_MESA"
    "SEM_CLASSIFICACAO"

  Subopção em aba IMPORTACAO
    "VINHOS DE MESA"
    "ESPUMANTES"
    "UVAS FRESCAS"
    "UVAS PASSAS"
    "SUCO DE UVA"

   Subopção em aba EXPORTACAO
    "VINHOS DE MESA"
    "ESPUMANTES"
    "UVAS FRESCAS"
    "SUCO DE UVA"
  
  Ano

Métodos
  consultar_tabela - Recebe os parâmetros de entrada e retorna os dados.

Instrução de Deploy na AWS

1.Abra o Prompt de Comando e execute:
aws configure

1.2 Insira suas credenciais da AWS (Access Key, Secret Key), região padrão e formato de saída (por exemplo, JSON).

2. Configurar o Serverless Framework
2.1. Instalar Node.js e npm
Baixe e instale o Node.js do site oficial: https://nodejs.org/en . O npm será instalado automaticamente com o Node.js.
2.2. Instalar o Serverless Framework
Abra o Prompt de Comando e instale o Serverless Framework globalmente usando npm:
npm install -g serverless
2.3. Inicializar um Novo Projeto Serverless
serverless create --template aws-python --path my-service
cd my-service

3. Configurar o Serverless Framework
Edite o arquivo serverless.yml para configurar a função Lambda e o API Gateway:

  yaml

  service: my-python-api

    provider:
      name: aws
      runtime: python3.8

    functions:
      app:
        handler: wsgi_handler.handler
        events:
          - http: ANY /
          - http: 'ANY {proxy+}'

    plugins:
      - serverless-wsgi

    custom:
      wsgi:
        app: app.app
        packRequirements: false

    package:
      exclude:
        - node_modules/**
        - venv/**

4. Instalar Dependências
4.1. Criar um Ambiente Virtual

No Prompt de Comando:
  python -m venv venv

Ative o ambiente virtual:
  venv\Scripts\activate

4.2. Instalar Dependências
Instale o plugin serverless-wsgi e outras dependências necessárias:
  pip install flask zappa
  npm init -y
  npm install serverless-wsgi serverless-python-requirements

5 Implantar a API
5.1. Configurar o Serverless para Windows
Instale o plugin serverless-python-requirements para lidar com dependências no Windows:
  npm install serverless-python-requirements
5.2. Implantar a API para a AWS
Implante a API para a AWS:
  serverless deploy

Após o deploy, você verá a URL do endpoint do API Gateway na saída do terminal.
