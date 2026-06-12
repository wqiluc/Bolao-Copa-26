from sqlalchemy.orm import Session
import app.modelos as modelos


def calcular_placar(bd: Session) -> list[dict]:
    participantes = bd.query(modelos.Participante).all()
    fases = bd.query(modelos.Fase).order_by(modelos.Fase.ordem).all()
    resultado = []
    for p in participantes:
        por_fase = []
        total = 0
        acertos_exatos = 0
        total_gasto = float(sum(a.valor for a in p.apostas))
        for fase in fases:
            pts = sum(
                a.pontos
                for a in p.apostas
                if a.jogo.id_fase == fase.id and a.jogo.encerrado
            )
            por_fase.append({"fase": fase, "pontos": pts})
            total += pts
            for a in p.apostas:
                if a.jogo.id_fase == fase.id and a.jogo.encerrado and a.pontos == 3:
                    acertos_exatos += 1
        resultado.append({
            "participante": p,
            "total_pontos": total,
            "acertos_exatos": acertos_exatos,
            "total_gasto": total_gasto,
            "por_fase": por_fase,
        })
    resultado.sort(key=lambda x: (-x["total_pontos"], -x["acertos_exatos"]))
    return resultado
