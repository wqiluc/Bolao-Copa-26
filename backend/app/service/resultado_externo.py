import json
import time
import urllib.request
from typing import Optional

URL_API = f"https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"

cache: Optional[dict[int, tuple[int, int]]] = None
cache_timestamp: float = 0

VALIDADE_CACHE = 300

def buscar_resultado(numero_jogo: int) -> Optional[tuple[int, int]]:

    """Retorna (gols_casa, gols_fora) para o jogo com o número dado, ou None."""
    
    global cache, cache_timestamp

    if (cache is None or (time.time() - cache_timestamp) > VALIDADE_CACHE):

        cache = carregar_jogos()
        cache_timestamp = time.time()
        
    return cache.get(numero_jogo)


def carregar_jogos() -> dict[int, tuple[int, int]]:

    try:
        request = urllib.request.Request(URL_API, headers={"User-Agent": "bolao-copa26/1.0"})

        with urllib.request.urlopen(request, timeout=10) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))

    except Exception:
        return { }

    partidas = dados.get("matches", [ ])

    def e_terceiro_lugar(partida: dict) -> bool:

        rodada = (partida.get("round") or " ").lower()

        return ("terceiro" in rodada or "3º" in rodada or "bronze" in rodada)

    filtrados = [m for m in partidas if not e_terceiro_lugar(m)]

    resultado: dict[int, tuple[int, int]] = {}

    for indice, jogo in enumerate(filtrados):
        numero = indice + 1
        marcacao = jogo.get("score")

        if (not marcacao):
            continue

        placar_final = marcacao.get("ft")

        if placar_final and len(placar_final) == 2 and placar_final[0] is not None and placar_final[1] is not None:
            resultado[numero] = (int(placar_final[0]), int(placar_final[1]))

    return resultado