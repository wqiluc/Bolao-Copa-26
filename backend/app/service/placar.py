from sqlalchemy.orm import Session, joinedload
import app.modelos as modelos

def calcular_placar(bd: Session) -> list[dict]:
    participantes = (
        bd.query(modelos.Participante)

        .options
        (
            joinedload(modelos.Participante.apostas)
            .joinedload(modelos.Aposta.jogo)
        )

        .all()
    )

    fases = bd.query(modelos.Fase).order_by(modelos.Fase.ordem).all()

    resultado = [ ]

    for participante in participantes:
        saldo_por_fase = {fase.id: 0.0 for fase in fases}
        saldo_total = 0.0
        total_ganho = 0.0
        total_devido = 0.0
        acertos_exatos = 0

        for aposta in (participante.apostas):
            if not (aposta.jogo.encerrado):
                continue

            pts = float(aposta.pontos or 0)
            saldo_por_fase[aposta.jogo.id_fase] = saldo_por_fase.get(aposta.jogo.id_fase, 0.0) + pts
            saldo_total += pts

            if (pts > 0):
                total_ganho += pts
                acertos_exatos += 1
            elif (pts < 0):
                total_devido += abs(pts)

        por_fase = [
            {
                "fase": fase, "saldo": saldo_por_fase.get(fase.id, 0.0)
            }

            for fase in fases
        ]

        resultado.append(
            {
                "participante": participante,
                "saldo_total": saldo_total,
                "total_ganho": total_ganho,
                "total_devido": total_devido,
                "acertos_exatos": acertos_exatos,
                "por_fase": por_fase,
            }
        )

    resultado.sort(key=lambda x: (-x["saldo_total"], -x["acertos_exatos"]))
    return resultado