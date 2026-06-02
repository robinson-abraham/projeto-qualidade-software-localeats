from pages.home_page import HomePage
from pages.restaurant_page import RestaurantPage


def test_deve_carregar_lista_e_filtrar_restaurantes_italianos(page):
    home = HomePage(page)
    home.preparar_sessao_autenticada()
    home.acessar()

    assert home.quantidade_de_restaurantes() >= 10

    home.filtrar_categoria("Italiana")

    assert home.quantidade_de_restaurantes() == 3
    assert all("Italiana" in texto for texto in home.textos_dos_cards())


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
