class RestaurantPage:
    def __init__(self, page):
        self.page = page
        self.name = page.locator("#restName")
        self.menu_items = page.locator(".menu-item")
        self.cart = page.locator("#floatingCart")

    def aguardar_detalhes(self) -> None:
        self.page.wait_for_function(
            """() => {
                const title = document.querySelector('#restName');
                return title && title.textContent.includes('Restaurante Sabor');
            }""",
            timeout=20000,
        )
        self.menu_items.first.wait_for(timeout=10000)

    def nome_do_restaurante(self) -> str:
        return self.name.inner_text()

    def quantidade_de_itens_no_menu(self) -> int:
        return self.menu_items.count()

    def adicionar_primeiro_item_ao_carrinho(self) -> None:
        self.page.get_by_text("Adicionar").first.click()
        self.page.wait_for_selector("#floatingCart.active", timeout=10000)

    def texto_do_carrinho(self) -> str:
        return self.cart.inner_text()
