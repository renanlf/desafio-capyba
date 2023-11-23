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

## Funcionalidades

1. Através do Endpoint `register/` é possível cadastrar um novo jogador (usuário do sistema) usando o método POST;