# Desafio técnico (Capyba)

Este repositório contém o código desenvolvido por mim para um desafio técnico.
O objetivo deste desafio é desenvolver uma API REST com cadastro de usuário, busca avançada de itens e painel de administração no navegador.

Para isso foi sugerido o uso do framework Django com Python. Topei o desafio e este é o meu primeiro projeto usando o Django Rest Framework :)

## Dependências

Neste projeto foram instalados os seguintes pacotes (através do `pip install` ):
- **djangorestframework**: framework que estrutura todo o projeto da API REST;
- **markdown**: para suporte da API navegável (ao utilizar um navegador);
- **django-filter**: biblioteca que suporta o uso de filtros nas Views e assim simplifica as buscas avançadas na API;
- **Pillow**: permite o uso de `ImageField` no framework (para armazenar as imagens do perfil);
- **drf-yasg**: biblioteca que gerencia a especificação da documentação no formato OpenAPI.
- **django_seed**: biblioteca responsável por criar exemplos aleatórios e popular o banco de dados. Seed significa semente em inglês. Semear.

## Funcionalidades

1. Através do Endpoint `register/` é possível cadastrar um novo jogador (usuário do sistema) usando o método POST;
2. Com o Endpoint `policy/` é realizado o download de um PDF com as políticas de uso (aqui representados pelo PDF dos requisitos);
3. `login\` realiza o login do jogador através do método POST e retorna um Token (nesta API o método de acesso se dará através de tokens);
4. Lista de cartas através do endpoint `cards\` permitindo filtrar os campos de título da carta e descrição através do parâmetro `search`. Além disso, é permitido ordenar os resultados por diversos campos, incluindo a data da primeira impressão da carta. Também é permitido buscar as cartas pelo código, título ou data da impressão. Para mais detalhes você pode consultar o arquivo de testes (`yugioh_api/tests.py`);
5. Manipulação de cartas através da API navegável do Django Rest Framework, mediante login do admin;
6. Endpoint `confirmation/` responsável por gerar um link de validação para um jogador devidamente logado. Nesta versão é gerado o link, sendo facilmente implementável no futuro o envio do link por e-mail;
7. Endpoint `validate/` responsável por validar o e-mail do usuário logado, ou retornar mensagem apropriada caso já esteja logado ou seu token for inválido;
8. Lista de preços `prices/` contendo uma carta e seus valores mínimos e máximo de venda. Esta lista é privada, só é possível visualizá-la logado;
9. Endpoint `swagger/` com a especificação da API em formato OpenAPI;

## Instalação

Para instalar e executar o projeto é necessário que tenha instalado o `git`, o `python` e o `pip`. Para mais detalhes você pode consultar as páginas oficiais das tecnologias.

O primeiro passo é realizar o clone do projeto na máquina atual:
```shell
git clone https://github.com/renanlf/desafio-capyba.git
cd desafio-capyba
```

O segundo passo é instalar as dependências para utilização do projeto mencionadas anteriormente.

```shell
pip install -r requirements.txt
```

Após a instalação das dependências, é necessário criar o banco de dados através dos seguintes comandos:
```shell
python manage.py makemigrations
python manage.py migrate
```

Para popular o banco com exemplos aleatórios, podemos usar o comando:
```shell
python manage.py seed yugioh_api --number=100
```
Esse comando irá criar 100 instâncias para cada tabela no banco de dados!

Por fim, para iniciar o servidor, execute:
```shell
python manage.py runserver
```

Se tudo ocorrer bem, você deverá conseguir acessar a API através do endereço http://127.0.0.1:8000

## Conclusões
Este foi meu primeiro projeto usando o Django Rest Framework e confesso que gostei de sua praticidade e pretendo utilizá-lo mais vezes. 
Por motivos diversos não consegui implementar todas as funcionalidades. 
Pretendo voltar e atualizar o projeto no futuro.
