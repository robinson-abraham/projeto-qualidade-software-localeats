BASE_URL = "https://local-eats-unisenac.vercel.app"


class HomePage:
    def __init__(self, page):
        self.page = page
        self.search_input = page.locator("#searchInput")
        self.search_button = page.locator("#searchBtn")
        self.restaurant_cards = page.locator(".rest-card")
        self.grid = page.locator("#restaurantGrid")

    def preparar_sessao_autenticada(
        self,
        user_id: str = "1",
        user_name: str = "Usuario Teste",
    ) -> None:
        self.page.goto(f"{BASE_URL}/static/login.html", wait_until="domcontentloaded")
        self.page.evaluate(
            """([userId, userName]) => {
                localStorage.setItem('userId', userId);
                localStorage.setItem('userName', userName);
            }""",
            [user_id, user_name],
        )

    def acessar(self) -> None:
        self.page.goto(f"{BASE_URL}/static/index.html", wait_until="networkidle")
        self.aguardar_listagem()

    def aguardar_listagem(self) -> None:
        self.page.wait_for_function(
            """() => {
                const grid = document.querySelector('#restaurantGrid');
                if (!grid) return false;
                const text = grid.innerText;
                const finishedLoading = !text.includes('Buscando') && !text.includes('Carregando');
                const hasCards = Boolean(grid.querySelector('.rest-card'));
                const hasFinalMessage = text.includes('Nenhum restaurante encontrado') || text.includes('Erro ao carregar');
                return finishedLoading && (hasCards || hasFinalMessage);
            }""",
            timeout=20000,
        )

    def quantidade_de_restaurantes(self) -> int:
        return self.restaurant_cards.count()

    def textos_dos_cards(self) -> list[str]:
        return [
            self.restaurant_cards.nth(index).inner_text()
            for index in range(self.quantidade_de_restaurantes())
        ]

    def buscar(self, termo: str) -> None:
        self.search_input.fill(termo)
        self.search_button.click()
        self.aguardar_listagem()

    def filtrar_categoria(self, categoria: str) -> None:
        self.page.get_by_role("button", name=categoria).click()
        self.aguardar_listagem()

    def abrir_primeiro_restaurante(self) -> None:
        self.restaurant_cards.first.click()
