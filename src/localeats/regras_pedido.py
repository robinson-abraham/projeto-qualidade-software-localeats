from __future__ import annotations

from math import ceil
from typing import Mapping, Sequence


def _arredondar_moeda(valor: float) -> float:
    return round(float(valor) + 1e-9, 2)


def calcular_total_pedido(
    itens: Sequence[Mapping[str, float]],
    valor_minimo: float,
) -> float:
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


def aplicar_desconto_percentual(total: float, percentual: float) -> float:
    if total < 0:
        raise ValueError("Total nao pode ser negativo")

    if percentual < 0 or percentual > 100:
        raise ValueError("Desconto deve estar entre 0 e 100 por cento")

    valor_final = total * (1 - percentual / 100)
    return _arredondar_moeda(max(valor_final, 0))


def calcular_taxa_entrega(
    distancia_km: float,
    taxa_fixa: float = 6.0,
    limite_fixo_km: float = 3.0,
    valor_por_km_extra: float = 2.5,
) -> float:
    if distancia_km < 0:
        raise ValueError("Distancia nao pode ser negativa")

    if distancia_km <= limite_fixo_km:
        return _arredondar_moeda(taxa_fixa)

    km_extra = distancia_km - limite_fixo_km
    return _arredondar_moeda(taxa_fixa + km_extra * valor_por_km_extra)


def validar_login(email: str, senha: str, credenciais: Mapping[str, str]) -> bool:
    if not email or not senha:
        raise ValueError("E-mail e senha sao obrigatorios")

    if credenciais.get(email) != senha:
        raise PermissionError("Credenciais invalidas")

    return True


def calcular_tempo_estimado_entrega(
    distancia_km: float,
    tempo_base_min: int = 20,
    minutos_por_km: int = 5,
) -> int:
    if distancia_km < 0:
        raise ValueError("Distancia nao pode ser negativa")

    return tempo_base_min + ceil(distancia_km * minutos_por_km)
