import pytest

from localeats import (
    aplicar_desconto_percentual,
    calcular_taxa_entrega,
    calcular_tempo_estimado_entrega,
    calcular_total_pedido,
    validar_login,
)


def test_deve_calcular_total_quando_valor_minimo_e_atingido():
    itens = [{"preco": 10.0}, {"preco": 20.0}]

    resultado = calcular_total_pedido(itens, valor_minimo=15.0)

    assert resultado == 30.0


def test_deve_aceitar_total_exatamente_igual_ao_valor_minimo():
    itens = [{"preco": 12.5}, {"preco": 7.5}]

    resultado = calcular_total_pedido(itens, valor_minimo=20.0)

    assert resultado == 20.0


def test_deve_recusar_pedido_abaixo_do_valor_minimo():
    itens = [{"preco": 8.0}, {"preco": 4.0}]

    with pytest.raises(ValueError, match="Valor minimo"):
        calcular_total_pedido(itens, valor_minimo=20.0)


def test_deve_recusar_pedido_sem_itens():
    with pytest.raises(ValueError, match="pelo menos um item"):
        calcular_total_pedido([], valor_minimo=10.0)


def test_deve_aplicar_desconto_percentual_valido():
    resultado = aplicar_desconto_percentual(total=100.0, percentual=15.0)

    assert resultado == 85.0


def test_deve_manter_total_quando_desconto_for_zero():
    resultado = aplicar_desconto_percentual(total=47.9, percentual=0.0)

    assert resultado == 47.9


def test_deve_zerar_total_quando_desconto_for_cem_por_cento():
    resultado = aplicar_desconto_percentual(total=47.9, percentual=100.0)

    assert resultado == 0.0


def test_deve_recusar_percentual_de_desconto_menor_que_zero():
    with pytest.raises(ValueError, match="entre 0 e 100"):
        aplicar_desconto_percentual(total=100.0, percentual=-1.0)


def test_deve_recusar_percentual_de_desconto_maior_que_cem():
    with pytest.raises(ValueError, match="entre 0 e 100"):
        aplicar_desconto_percentual(total=100.0, percentual=150.0)


def test_deve_calcular_taxa_fixa_para_distancia_ate_tres_km():
    resultado = calcular_taxa_entrega(distancia_km=2.5)

    assert resultado == 6.0


def test_deve_calcular_taxa_proporcional_acima_de_tres_km():
    resultado = calcular_taxa_entrega(distancia_km=5.0)

    assert resultado == 11.0


def test_deve_calcular_taxa_fixa_para_distancia_zero():
    resultado = calcular_taxa_entrega(distancia_km=0.0)

    assert resultado == 6.0


def test_deve_recusar_distancia_negativa_na_taxa_de_entrega():
    with pytest.raises(ValueError, match="Distancia"):
        calcular_taxa_entrega(distancia_km=-0.1)


def test_deve_validar_login_com_credenciais_corretas():
    credenciais = {"cliente@teste.com": "123456"}

    resultado = validar_login("cliente@teste.com", "123456", credenciais)

    assert resultado is True


def test_deve_recusar_login_com_campos_vazios():
    with pytest.raises(ValueError, match="obrigatorios"):
        validar_login("", "123456", {"cliente@teste.com": "123456"})


def test_deve_recusar_login_com_senha_incorreta():
    with pytest.raises(PermissionError, match="invalidas"):
        validar_login("cliente@teste.com", "errada", {"cliente@teste.com": "123456"})


def test_deve_calcular_tempo_estimado_com_base_na_distancia():
    resultado = calcular_tempo_estimado_entrega(distancia_km=4.2)

    assert resultado == 41


def test_deve_retornar_tempo_base_quando_distancia_for_zero():
    resultado = calcular_tempo_estimado_entrega(distancia_km=0.0)

    assert resultado == 20


def test_deve_recusar_distancia_negativa_no_tempo_estimado():
    with pytest.raises(ValueError, match="Distancia"):
        calcular_tempo_estimado_entrega(distancia_km=-1.0)
