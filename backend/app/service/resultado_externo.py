import json
import time
import urllib.request
from typing import Optional

URL = f"https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"

cache: Optional[dict[int, tuple[int, int]]] = None
cache_timestamp: float = 0
TTL = 300

def buscar_resultado(numero_jogo: int) -> Optional[tuple[int, int]]:

    """Retorna (gols_casa, gols_fora) para o jogo com o número dado, ou None."""
    global cache, cache_timestamp

    if (cache is None or (time.time() - cache_timestamp) > TTL):
        cache = carregar_jogos()
        cache_timestamp = time.time()
    return cache.get(numero_jogo)


def carregar_jogos() -> dict[int, tuple[int, int]]:

    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "bolao-copa26/1.0"})

        with urllib.request.urlopen(req, timeout=6) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))

    except Exception:
        return {}

    matches = dados.get("matches", [ ])

    def e_terceiro_lugar(partida: dict) -> bool:

        rodada = (partida.get("round") or "").lower()

        return "terceiro" in rodada or "3rd" in rodada or "bronze" in rodada

    filtrados = [m for m in matches if not e_terceiro_lugar(m)]

    resultado: dict[int, tuple[int, int]] = {}

    for indice, jogo in enumerate(filtrados):
        numero = indice + 1
        score = jogo.get("score")

        if (not score):
            continue

        placar_final = score.get("ft")

        if placar_final and len(placar_final) == 2 and placar_final[0] is not None and placar_final[1] is not None:
            resultado[numero] = (int(placar_final[0]), int(placar_final[1]))

    return resultado