from sqlalchemy.orm import Session
import app.modelos as modelos


def calcular_placar(bd: Session) -> list[dict]:
    participantes = bd.query(modelos.Participante).all()
    fases = bd.query(modelos.Fase).order_by(modelos.Fase.ordem).all()
    resultado = []

    for p in participantes:
        por_fase = []
        saldo_total = 0.0
        acertos_exatos = 0

        for fase in fases:
            saldo_fase = sum(
                float(a.pontos or 0)
                for a in p.apostas
                if a.jogo.id_fase == fase.id and a.jogo.encerrado
            )
            por_fase.append({"fase": fase, "saldo": saldo_fase})
            saldo_total += saldo_fase

            for a in p.apostas:
                if a.jogo.id_fase == fase.id and a.jogo.encerrado and float(a.pontos or 0) > 0:
                    acertos_exatos += 1

        resultado.append({
            "participante": p,
            "saldo_total": saldo_total,
            "acertos_exatos": acertos_exatos,
            "por_fase": por_fase,
        })

    resultado.sort(key=lambda x: (-x["saldo_total"], -x["acertos_exatos"]))
    return resultado