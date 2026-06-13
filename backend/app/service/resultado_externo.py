import json
import time
import urllib.request
from typing import Optional

_URL = "https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json"

_cache: Optional[dict[int, tuple[int, int]]] = None
_cache_ts: float = 0
_TTL = 300


def buscar_resultado(numero_jogo: int) -> Optional[tuple[int, int]]:
    """Retorna (gols_casa, gols_fora) para o jogo com o número dado, ou None."""
    global _cache, _cache_ts

    if _cache is None or (time.time() - _cache_ts) > _TTL:
        _cache = _carregar_jogos()
        _cache_ts = time.time()
    return _cache.get(numero_jogo)


def _carregar_jogos() -> dict[int, tuple[int, int]]:

    try:
        req = urllib.request.Request(_URL, headers={"User-Agent": "bolao-copa26/1.0"})

        with urllib.request.urlopen(req, timeout=6) as resp:
            dados = json.loads(resp.read().decode("utf-8"))

    except Exception:
        return { }

    matches = dados.get("matches", [])

    def _e_terceiro_lugar(m: dict) -> bool:
        r = (m.get("round") or "").lower()

        return "third" in r or "3rd" in r or "bronze" in r or "terceiro" in r

    filtrados = [m for m in matches if not _e_terceiro_lugar(m)]

    resultado: dict[int, tuple[int, int]] = {}

    for idx, jogo in enumerate(filtrados):
        numero = idx + 1 
        score = jogo.get("score")

        if not (score):
            continue

        ft = score.get("ft")

        if ft and len(ft) == 2 and ft[0] is not None and ft[1] is not None:
            resultado[numero] = (int(ft[0]), int(ft[1]))

    return resultado