# Aula 10 - Testes Funcionais Automatizados

## 1. Fluxo funcional escolhido

Fluxo escolhido: navegacao e visualizacao de restaurantes no LocalEats.

Foram automatizados dois cenarios do ponto de vista do usuario:

- Carregar a lista de restaurantes e filtrar pela categoria Italiana.
- Abrir os detalhes de um restaurante e adicionar um item ao carrinho.

O sistema exige sessao para acessar as paginas internas. Para evitar dependencia de senha real, os testes preparam uma sessao de teste via `localStorage` com `userId=1`, que ja existe na aplicacao.

## 2. Teste automatizado com Codegen

Comando indicado no enunciado:

```powershell
playwright codegen https://local-eats-unisenac.vercel.app/
```

Trecho bruto registrado como ponto de partida:

```python
def test_fluxo_explorar_codegen_bruto(page):
    page.goto("https://local-eats-unisenac.vercel.app/static/index.html")
    page.locator("#searchInput").click()
    page.locator("#searchInput").fill("Centro")
    page.locator("#searchBtn").click()
    page.locator(".rest-card").first.click()
    page.get_by_text("Adicionar").first.click()
    page.get_by_text("Finalizar Pedido").click()
```

Arquivo de evidencia: `artefatos/evidencias/pbl7-codegen-bruto.py`.

O Codegen ajudou a identificar os elementos principais (`#searchInput`, `#searchBtn`, `.rest-card` e texto `Adicionar`). O codigo bruto, porem, ficou muito acoplado a cliques diretos e nao representava bem a regra do fluxo. Por isso ele foi refatorado com Page Object Model.

## 3. Implementacao do teste com Pytest

Arquivo: `tests/functional/test_explorar_restaurantes.py`.

Teste principal:

```python
def test_deve_abrir_detalhes_e_adicionar_item_ao_carrinho(page):
    home = HomePage(page)
    home.preparar_sessao_autenticada()
    home.acessar()

    home.abrir_primeiro_restaurante()
    restaurante = RestaurantPage(page)
    restaurante.aguardar_detalhes()

    assert restaurante.nome_do_restaurante().startswith("Restaurante Sabor")
    assert restaurante.quantidade_de_itens_no_menu() > 0

    restaurante.adicionar_primeiro_item_ao_carrinho()

    assert "1 itens" in restaurante.texto_do_carrinho()
    assert "Finalizar Pedido" in restaurante.texto_do_carrinho()
```

## 4. Refatoracao com Page Object Model

Estrutura criada:

```text
pages/
  home_page.py
  restaurant_page.py

tests/
  functional/
    test_explorar_restaurantes.py
```

Responsabilidades:

- `HomePage`: login tecnico de teste, acesso a pagina Explorar, busca, filtro e abertura do primeiro restaurante.
- `RestaurantPage`: espera pelo carregamento dos detalhes, leitura do nome, contagem do cardapio e interacao com carrinho.

Essa organizacao reduz duplicacao e deixa o teste mais legivel.

## 5. Execucao dos testes

Comando executado:

```powershell
python -m pytest tests\functional -q
```

Resultado:

```text
2 passed in 8.61s
```

Evidencias:

- `artefatos/evidencias/pbl7-pytest-funcionais.log`
- `artefatos/evidencias/pbl7-detalhe-carrinho.png`

## 6. Analise critica dos testes

O teste quebrou inicialmente quando a automacao esperava apenas o elemento `#restName`, pois o HTML ja continha o placeholder antes de carregar o restaurante real. A correcao foi esperar o texto `Restaurante Sabor` aparecer. Os seletores mais sensiveis sao `.rest-card` e textos visiveis como `Adicionar`, porque mudancas de layout ou copy podem exigir ajuste. Mesmo assim, o teste ficou confiavel para o contexto da atividade porque valida comportamento real: lista carregada, filtro aplicado, detalhe aberto e carrinho atualizado.

O Codegen ajudou a descobrir seletores rapidamente, mas gerou um fluxo linear demais. O Page Object Model tornou o teste mais robusto e facil de manter.

## 7. Reflexao no contexto do LocalEats

Testes automatizados nao substituem testes manuais; eles reduzem repeticao e aumentam confianca em fluxos criticos. Nao vale automatizar tudo: o ideal e priorizar fluxos de alto valor e alto risco, como login, exploracao de restaurantes, carrinho e checkout. No projeto do grupo, essa automacao ajuda a perceber regressao no frontend logo apos mudancas.
