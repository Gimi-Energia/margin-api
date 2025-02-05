# Margin API

A Margin API foi desenhada para gerir margem de lucro do Grupo Gimi.

## ✔️ Tecnologias usadas
- Python
- Django
- Django Ninja
- Pydantic
- PostgreSQL
- Python Jose
- Vercel

## 📁 Acesso ao deploy

[![Deploy with Vercel](https://vercel.com/button)](https://margin-api.vercel.app/api/docs)

## 🔨 Funcionalidades

- **Gestão de Usuários**: Administração de usuários que podem acessar a API.
- **Autenticação**: Sistema de tokens para acesso seguro à API.
- **Gestão de ICMS**: Criar, listar, atualizar e deletar taxas de ICMS.
- **Gestão de Grupos NCM**: Criar, listar, atualizar e deletar grupos NCM.
- **Gestão de NCM**: Criar, listar, atualizar e deletar NCMs.
- **Gestão de Estados**: Listar e obter detalhes de estados.
- **Gestão de Impostos**: Criar, listar, atualizar e deletar impostos.
- **Gestão de Empresas**: Criar, listar, atualizar e deletar empresas.
- **Gestão de Porcentagens**: Listar e obter detalhes de porcentagens.
- **Gestão de Contratos**: Encontrar, calcular e retornar contratos IAPP.

## 📌 Uso

A Margin API segue os princípios REST para comunicação. Os seguintes endpoints estão disponíveis:

### /api/icms/rates
- Gerenciar taxas de ICMS.

### /api/icms/rates/group/{group_id}
- Listar taxas de ICMS por grupo.

### /api/icms/rates/bulk-create
- Criar múltiplas taxas de ICMS em lote.

### /api/icms/rates/bulk-update
- Atualizar múltiplas taxas de ICMS em lote.

### /api/icms/rates/{icms_rate_id}
- Gerenciar uma taxa de ICMS específica.

### /api/ncm/groups
- Gerenciar grupos NCM.

### /api/ncm/groups/{group_id}
- Gerenciar um grupo NCM específico.

### /api/ncm
- Gerenciar NCMs.

### /api/ncm/{ncm_id}
- Gerenciar um NCM específico.

### /api/states
- Listar e obter detalhes de estados.

### /api/states/{state_id}
- Obter um estado específico.

### /api/taxes
- Gerenciar impostos.

### /api/taxes/{tax_id}
- Gerenciar um imposto específico.

### /api/taxes/by-company/{company_id}
- Listar impostos por empresa.

### /api/companies
- Gerenciar empresas.

### /api/companies/{company_id}
- Gerenciar uma empresa específica.

### /api/percentages
- Listar e obter detalhes de porcentagens.

### /api/percentages/{percentage_id}
- Gerenciar uma porcentagem específica.

### /api/contracts/find
- Encontrar um contrato do iApp.

### /api/contracts/calculate
- Calcular um contrato do iApp.

### /api/contracts/return
- Retornar um contrato do iApp.

## 🔐 Autenticação

A autenticação é realizada através do GIMIx.

## 🛠️ Abrindo e rodando o projeto

Para configurar a API em seu ambiente, siga estas etapas:

1. Clone o repositório do projeto para sua máquina local.
2. Configure o ambiente virtual para Python e ative-o.
3. Instale as dependências do projeto
```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente necessárias para a conexão com o banco de dados e outras configurações de sistema.
5. Execute as migrações do banco de dados
```bash
python manage.py migrate
```
6. Crie um super usuário para ter acesso a `/admin/`
```bash
python manage.py createsuperuser
```
7. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```