# Projeto - Qualidade de Software - LocalEats

## Integrantes

- Nome completo: Robinson Abraham da Silva
- Matricula: 782410038




## Objetivo do repositorio

Este repositorio reune as entregas dos PBLs de Qualidade de Software para o sistema LocalEats, seguindo a organizacao indicada no PBL 0 - Avaliacao por Competencias.

## Entregas

- `docs/aula-09-testes-unitarios-tdd.md` - PBL 6: testes unitarios automatizados e TDD.
- `docs/aula-10-testes-funcionais-automatizados.md` - PBL 7: testes funcionais automatizados com Playwright, Pytest e Page Object Model.
- `docs/aula-12-bdd-automacao-comportamento.md` - PBL 8: BDD com Gherkin, pytest-bdd e Playwright.

## Organizacao

- `src/localeats/` - regras de negocio simuladas do LocalEats para testes unitarios.
- `tests/unit/` - testes unitarios do PBL 6.
- `tests/functional/` - testes funcionais automatizados do PBL 7.
- `features/` - cenarios BDD em Gherkin do PBL 8.
- `tests/bdd/` - steps BDD automatizados com pytest-bdd.
- `pages/` - Page Objects usados nos testes funcionais e BDD.
- `artefatos/evidencias/` - logs e prints das execucoes.
- `referencias/` - enunciados exportados dos PBLs enviados.

## Como executar

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
.venv\Scripts\python -m pytest -q
```

## Resultado validado

Execucao completa realizada em 01/06/2026:

```text
24 passed in 13.87s
```

Evidencia consolidada: `artefatos/evidencias/pytest-completo.log`.

## Link do repositorio

Preencher aqui apos publicar no GitHub.
