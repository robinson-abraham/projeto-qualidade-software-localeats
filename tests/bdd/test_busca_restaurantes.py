from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from pages.home_page import HomePage

FEATURE = Path(__file__).parents[2] / "features" / "busca_restaurantes.feature"
scenarios(str(FEATURE))


@given("que o usuario autenticado esta na pagina Explorar", target_fixture="home")
def usuario_na_pagina_explorar(page):
    home = HomePage(page)
    home.preparar_sessao_autenticada()
    home.acessar()
    return home


@when(parsers.parse('pesquisar restaurantes por "{termo}"'))
def pesquisar_restaurantes(home: HomePage, termo: str):
    home.buscar(termo)


@when("limpar o campo de busca")
def limpar_busca(home: HomePage):
    home.buscar("")


@then(parsers.parse('a listagem deve mostrar restaurantes localizados em "{localizacao}"'))
def validar_restaurantes_por_localizacao(home: HomePage, localizacao: str):
    assert home.quantidade_de_restaurantes() > 0
    assert all(localizacao in texto for texto in home.textos_dos_cards())


@then("o sistema deve informar que nenhum restaurante foi encontrado")
def validar_busca_sem_resultado(home: HomePage):
    assert home.quantidade_de_restaurantes() == 0
    assert "Nenhum restaurante encontrado." in home.grid.inner_text()


@then("a listagem geral deve permanecer visivel")
def validar_listagem_geral(home: HomePage):
    assert home.quantidade_de_restaurantes() >= 10
