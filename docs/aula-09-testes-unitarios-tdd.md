# Aula 09 - Testes Unitarios Automatizados e TDD

## 1. Funcionalidades escolhidas

Como os nomes dos integrantes nao foram informados, a entrega ficou organizada por funcionalidades. Cada uma pode ser atribuida a um integrante do grupo no README antes da publicacao no GitHub.

| Funcionalidade | Regra de negocio validada | Arquivo |
| --- | --- | --- |
| Calculo do total do pedido | Soma itens e bloqueia pedido abaixo do valor minimo | `src/localeats/regras_pedido.py` |
| Aplicacao de desconto percentual | Aceita apenas descontos entre 0% e 100% | `src/localeats/regras_pedido.py` |
| Calculo da taxa de entrega | Usa taxa fixa ate 3 km e valor proporcional acima disso | `src/localeats/regras_pedido.py` |
| Validacao de login | Exige campos preenchidos e credenciais corretas | `src/localeats/regras_pedido.py` |
| Calculo de tempo estimado | Usa tempo base somado a tempo por km | `src/localeats/regras_pedido.py` |

## 2. Testes unitarios

O codigo completo dos testes esta em `tests/unit/test_regras_pedido.py`.

| Teste | Cenario | Entrada principal | Resultado esperado |
| --- | --- | --- | --- |
| `test_deve_calcular_total_quando_valor_minimo_e_atingido` | Pedido valido acima do minimo | Itens 10 + 20, minimo 15 | Retorna 30 |
| `test_deve_aceitar_total_exatamente_igual_ao_valor_minimo` | Pedido no limite | Itens 12,50 + 7,50, minimo 20 | Retorna 20 |
| `test_deve_recusar_pedido_abaixo_do_valor_minimo` | Pedido invalido | Itens 8 + 4, minimo 20 | Lanca `ValueError` |
| `test_deve_recusar_pedido_sem_itens` | Borda sem itens | Lista vazia | Lanca `ValueError` |
| `test_deve_aplicar_desconto_percentual_valido` | Desconto comum | Total 100, desconto 15% | Retorna 85 |
| `test_deve_manter_total_quando_desconto_for_zero` | Desconto zero | Total 47,90, desconto 0% | Retorna 47,90 |
| `test_deve_zerar_total_quando_desconto_for_cem_por_cento` | Desconto maximo | Total 47,90, desconto 100% | Retorna 0 |
| `test_deve_recusar_percentual_de_desconto_menor_que_zero` | Erro inferior | Desconto -1% | Lanca `ValueError` |
| `test_deve_recusar_percentual_de_desconto_maior_que_cem` | Erro superior | Desconto 150% | Lanca `ValueError` |
| `test_deve_calcular_taxa_fixa_para_distancia_ate_tres_km` | Taxa fixa | Distancia 2,5 km | Retorna 6 |
| `test_deve_calcular_taxa_proporcional_acima_de_tres_km` | Taxa proporcional | Distancia 5 km | Retorna 11 |
| `test_deve_calcular_taxa_fixa_para_distancia_zero` | Borda zero | Distancia 0 km | Retorna 6 |
| `test_deve_recusar_distancia_negativa_na_taxa_de_entrega` | Erro de distancia | Distancia -0,1 km | Lanca `ValueError` |
| `test_deve_validar_login_com_credenciais_corretas` | Login valido | Email e senha corretos | Retorna `True` |
| `test_deve_recusar_login_com_campos_vazios` | Campos obrigatorios | Email vazio | Lanca `ValueError` |
| `test_deve_recusar_login_com_senha_incorreta` | Credencial invalida | Senha errada | Lanca `PermissionError` |
| `test_deve_calcular_tempo_estimado_com_base_na_distancia` | Tempo proporcional | Distancia 4,2 km | Retorna 41 min |
| `test_deve_retornar_tempo_base_quando_distancia_for_zero` | Borda zero | Distancia 0 km | Retorna 20 min |
| `test_deve_recusar_distancia_negativa_no_tempo_estimado` | Erro de distancia | Distancia -1 km | Lanca `ValueError` |

Exemplo de codigo de teste:

```python
def test_deve_recusar_pedido_abaixo_do_valor_minimo():
    itens = [{"preco": 8.0}, {"preco": 4.0}]

    with pytest.raises(ValueError, match="Valor minimo"):
        calcular_total_pedido(itens, valor_minimo=20.0)
```

## 3. Aplicacao do TDD

Funcionalidade usada no ciclo TDD: calculo do total do pedido com valor minimo.

### Red

Primeiro foi criado um teste para um pedido abaixo do minimo. O teste falhava porque a funcao ainda nao existia.

```python
def test_deve_recusar_pedido_abaixo_do_valor_minimo():
    itens = [{"preco": 8.0}, {"preco": 4.0}]

    with pytest.raises(ValueError, match="Valor minimo"):
        calcular_total_pedido(itens, valor_minimo=20.0)
```

### Green

Em seguida foi feita a menor implementacao possivel: somar os itens e lancar erro quando o total fosse menor que o minimo.

```python
def calcular_total_pedido(itens, valor_minimo):
    total = sum(item["preco"] for item in itens)
    if total < valor_minimo:
        raise ValueError("Valor minimo do pedido nao atingido")
    return total
```

### Refactor

A versao final melhora a legibilidade, valida lista vazia, bloqueia precos negativos e arredonda valores monetarios.

```python
def calcular_total_pedido(itens, valor_minimo):
    if valor_minimo < 0:
        raise ValueError("Valor minimo nao pode ser negativo")

    if not itens:
        raise ValueError("Pedido deve possuir pelo menos um item")

    total = 0.0
    for item in itens:
        preco = float(item["preco"])
        if preco < 0:
            raise ValueError("Preco do item nao pode ser negativo")
        total += preco

    total = _arredondar_moeda(total)
    if total < valor_minimo:
        raise ValueError("Valor minimo do pedido nao atingido")

    return total
```

## 4. Refatoracao

Melhorias realizadas:

- Separacao das regras de negocio em `src/localeats/regras_pedido.py`.
- Nomes descritivos nos testes e funcoes.
- Mensagens de erro especificas para facilitar diagnostico.
- Funcao `_arredondar_moeda` para reduzir repeticao em regras financeiras.
- Testes cobrindo sucesso, borda e erro.

## 5. Execucao dos testes

Comando executado:

```powershell
python -m pytest tests\unit -q
```

Resultado:

```text
19 passed in 0.03s
```

Evidencia: `artefatos/evidencias/pbl6-pytest-unitarios.log`.

## 6. Reflexao no contexto do LocalEats

Escrever testes antes do codigo exigiu pensar primeiro na regra de negocio, mas ajudou a deixar claro o que era pedido valido e invalido. O TDD aumentou a confianca porque cada melhoria na implementacao foi acompanhada por uma validacao automatica. Para o LocalEats, isso reduz risco em regras sensiveis como total do pedido, desconto, entrega e login. Como melhoria futura, os testes poderiam usar dados reais do backend e tambem validar integracao com banco de dados.
