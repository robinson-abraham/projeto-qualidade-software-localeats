from playwright.sync_api import Page


def test_fluxo_explorar_codegen_bruto(page: Page):
    page.goto("https://local-eats-unisenac.vercel.app/static/index.html")
    page.locator("#searchInput").click()
    page.locator("#searchInput").fill("Centro")
    page.locator("#searchBtn").click()
    page.locator(".rest-card").first.click()
    page.get_by_text("Adicionar").first.click()
    page.get_by_text("Finalizar Pedido").click()
