API de Campeonato de Futebol ⚽🏆
Uma API backend completa e robusta para gerenciar um campeonato de futebol no formato mata-mata. O projeto foi desenvolvido com foco em arquitetura limpa, escalabilidade e boas práticas de desenvolvimento, integrando tecnologias de ponta para diferentes responsabilidades do sistema.

## 🏛️ Arquitetura do Projeto

O sistema foi projetado com uma arquitetura desacoplada, utilizando os serviços adequados para cada tarefa — desde o armazenamento de dados estruturados até o processamento de arquivos na nuvem e comunicação em tempo real.

![Arquitetura do Projeto](/Diagrama_aplicacao.png)
    
✨ Funcionalidades Principais

**Gerenciamento de Times** : Sistema simples para cadastro e listagem de times.

**Sorteio de Partidas** : Endpoint para realizar o sorteio de partidas no formato mata-mata, com bloqueio para evitar novos sorteios indevidos.

**Comunicação em Tempo Real**: Um endpoint WebSocket para cada partida, permitindo o registro e a transmissão ao vivo de eventos (gols, cartões, etc.).

**Upload de Imagens Serverless**: Integração com AWS para upload de imagens dos times. A API invoca uma função Lambda que processa e salva a imagem em um bucket S3 privado.

**Acesso Seguro a Imagens**: Geração de URLs pré-assinadas (Presigned URLs) do S3 para permitir o download seguro e temporário das imagens pelos clientes.

**Ambiente Containerizado**: Uso de Docker e Docker Compose para criar um ambiente de desenvolvimento consistente e isolado com os bancos de dados PostgreSQL e MongoDB.

**Testes Automatizados**: Suíte de testes unitários e de integração com Pytest, utilizando um banco de dados de teste dedicado para garantir a qualidade e a estabilidade do código.

**Documentação Automática**: Documentação interativa da API gerada automaticamente pelo FastAPI.

🛠️ Stack de Tecnologias
Backend: Python 3.11+, FastAPI, Pydantic

Banco de Dados:

PostgreSQL: para dados estruturados (SQLAlchemy como ORM).

MongoDB: para eventos de partidas em tempo real (Motor como driver assíncrono).

Cloud (AWS):

S3: para armazenamento de objetos (imagens).

Lambda: para processamento de uploads serverless.

IAM: para gerenciamento de permissões.

Comunicação em Tempo Real: WebSockets

Containerização: Docker, Docker Compose

Testes: Pytest

SDKs e Drivers: Boto3, Psycopg2

🚀 Como Rodar o Projeto
Pré-requisitos
Antes de começar, você vai precisar ter instalado em sua máquina:

Python 3.11+

Docker e Docker Compose

Uma conta na AWS com credenciais IAM configuradas.

1. Clonando o Repositório
```bash

git clone [URL_DO_SEU_REPOSITORIO]
cd [NOME_DA_PASTA_DO_PROJETO]
2. Configurando o Ambiente
a. Crie o ambiente virtual:


python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Configure as variáveis de ambiente:
Crie um arquivo chamado .env na raiz do projeto, copiando o modelo .env.example (se você tiver um) ou usando a estrutura abaixo. Preencha com suas credenciais da AWS e outros dados.

```bash

# .env
AWS_ACCESS_KEY_ID=SUA_ACCESS_KEY_AQUI
AWS_SECRET_ACCESS_KEY=SUA_SECRET_KEY_AQUI
AWS_REGION=sua-regiao-aws # ex: sa-east-1
S3_BUCKET=NOME-DO-SEU-BUCKET-S3
LAMBDA_FUNCTION_NAME=nome-da-sua-funcao-lambda
```

3. Iniciando os Serviços:

    A. Inicie os bancos de dados com Docker:
    docker-compose up -d
    Isso irá iniciar os contêineres do PostgreSQL e do MongoDB em segundo plano.

    B. Inicie a aplicação FastAPI:
    com o comando ou pelo arquivo main.py
```bash

uvicorn app.main:app --reload
```

A API estará disponível em http://localhost:8000.

4. Acessando a Documentação
Swagger UI (interativo): http://localhost:8000/docs

ReDoc (alternativo): http://localhost:8000/redoc

🧪 Rodando os Testes
Para garantir que tudo está funcionando como esperado, execute a suíte de testes:

```bash

pytest
📝 API Endpoints
Método

URL

Descrição

POST

/times/

Cria um novo time.

GET

/times/

Lista todos os times cadastrados.

POST

/times/{time_id}/imagem

Faz upload de uma imagem para um time.

GET

/times/{time_id}/imagem-url

Obtém uma URL temporária para a imagem de um time.

POST

/sorteio/

Realiza o sorteio das partidas (só pode ser executado uma vez).

GET

/partidas/

Lista todas as partidas sorteadas.

GET

/ws/partida/{partida_id}

Endpoint (para documentação) de conexão WebSocket.
```

🔮 Melhorias Futuras
[ ] Implementar autenticação de usuários com JWT.

[ ] Expandir a lógica do torneio para suportar fases (oitavas, quartas, etc.).

[ ] Adicionar um endpoint para atualizar o placar e o status de uma partida.

[ ] Criar um frontend em React ou Vue.js para consumir a API.

[ ] Configurar um pipeline de CI/CD para automatizar testes e deploy.

✍️ Autor
Gregorio kessler Steinke

LinkedIn: https://www.linkedin.com/in/gregorio-kessler/