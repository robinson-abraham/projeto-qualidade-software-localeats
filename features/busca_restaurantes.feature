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
