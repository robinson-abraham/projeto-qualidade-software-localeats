# Aula 12 - BDD e Automacao Orientada a Comportamento

## 1. Fluxo escolhido

Fluxo escolhido: busca de restaurantes.

Esse fluxo foi selecionado porque representa uma regra importante de descoberta no LocalEats: o usuario precisa encontrar restaurantes por localizacao de forma rapida e compreensivel.

## 2. Escrita dos cenarios BDD

Arquivo: `features/busca_restaurantes.feature`.

```gherkin
Feature: Busca de restaurantes
  Como cliente do LocalEats
  Quero pesquisar restaurantes por localizacao
  Para encontrar opcoes proximas com rapidez

  Scenario: Busca valida retorna restaurantes do Centro
    Given que o usuario autenticado esta na pagina Explorar
    When pesquisar restaurantes por "Centro"
    Then a listagem deve mostrar restaurantes localizados em "Centro"

  Scenario: Busca inexistente informa que nenhum restaurante foi encontrado
    Given que o usuario autenticado esta na pagina Explorar
    When pesquisar restaurantes por "zzzz-nao-existe"
    Then o sistema deve informar que nenhum restaurante foi encontrado

  Scenario: Campo vazio mantem a listagem geral
    Given que o usuario autenticado esta na pagina Explorar
    When limpar o campo de busca
    Then a listagem geral deve permanecer visivel
```

## 3. Implementacao da automacao com pytest-bdd

Arquivo: `tests/bdd/test_busca_restaurantes.py`.

Trecho principal:

```python
@given("que o usuario autenticado esta na pagina Explorar", target_fixture="home")
def usuario_na_pagina_explorar(page):
    home = HomePage(page)
    home.preparar_sessao_autenticada()
    home.acessar()
    return home


@when(parsers.parse('pesquisar restaurantes por "{termo}"'))
def pesquisar_restaurantes(home: HomePage, termo: str):
    home.buscar(termo)


@then(parsers.parse('a listagem deve mostrar restaurantes localizados em "{localizacao}"'))
def validar_restaurantes_por_localizacao(home: HomePage, localizacao: str):
    assert home.quantidade_de_restaurantes() > 0
    assert all(localizacao in texto for texto in home.textos_dos_cards())
```

## 4. Organizacao do projeto

Estrutura usada:

```text
features/
  busca_restaurantes.feature

tests/
  bdd/
    test_busca_restaurantes.py

pages/
  home_page.py

artefatos/
  evidencias/
```

A descricao do comportamento ficou separada da implementacao tecnica. O Gherkin expressa a regra de negocio, enquanto os steps executam Playwright.

## 5. Execucao dos testes

Comando executado:

```powershell
python -m pytest tests\bdd -q
```

Resultado:

```text
3 passed in 11.13s
```

Evidencias:

- `artefatos/evidencias/pbl8-pytest-bdd.log`
- `artefatos/evidencias/pbl8-busca-centro.png`

## 6. Analise critica

Os cenarios ficaram compreensiveis porque descrevem comportamento esperado sem entrar em detalhes de CSS ou DOM. A automacao tambem ficou legivel porque reutiliza o `HomePage`. A maior dificuldade foi representar o campo vazio: o parser do pytest-bdd nao casou bem `""`, entao o passo foi reescrito como `When limpar o campo de busca`, que e mais claro para pessoas tecnicas e nao tecnicas.

Os seletores ainda dependem da interface, principalmente `#searchInput`, `#searchBtn` e `.rest-card`. Para deixar mais robusto, a aplicacao poderia usar labels acessiveis, roles bem definidos ou atributos `data-testid`.

## 7. Reflexao no contexto do LocalEats

BDD melhora a comunicacao porque transforma requisito em exemplo executavel. Nem todo teste precisa ser BDD; ele vale mais quando o comportamento precisa ser entendido por negocio, qualidade e desenvolvimento. Neste caso, a busca ficou clara: termo valido retorna resultados, termo inexistente mostra lista vazia e campo vazio mantem a listagem geral. Isso ajuda o grupo a manter uma documentacao viva do comportamento esperado.
