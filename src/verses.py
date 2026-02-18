# src/verses.py
import random

SLOTS = {
    "morning": {
        "tag": "DIOS TE HABLA HOY",
        "headline": "Gracias por este nuevo día",
        "items": [
            {
                "verse": "Este es el día que hizo el Señor; nos gozaremos y alegraremos en él.",
                "ref": "Salmo 118:24",
                "theme": "gratitud y propósito",
                "angle": "Dios no solo te dio un día: te dio una oportunidad de volver a empezar con Él."
            },
            {
                "verse": "Por la misericordia del Señor no hemos sido consumidos… nuevas son cada mañana.",
                "ref": "Lamentaciones 3:22-23",
                "theme": "misericordia y renovación",
                "angle": "Si amaneciste, fue misericordia. Hoy puedes volver, incluso si ayer fallaste."
            },
            {
                "verse": "Encomienda a Jehová tu camino, y confía en él; y él hará.",
                "ref": "Salmo 37:5",
                "theme": "confianza y rendición",
                "angle": "No cargues solo: entrégale a Dios lo que te inquieta y camina en paz."
            },
        ],
    },

    "noon": {
        "tag": "RETOMA EL CAMINO",
        "headline": "Fuerza para volver",
        "items": [
            {
                "verse": "Esfuérzate y sé valiente… porque Jehová tu Dios estará contigo.",
                "ref": "Josué 1:9",
                "theme": "valentía y obediencia",
                "angle": "La valentía no es no sentir miedo: es avanzar con Dios aunque te tiemblen las manos."
            },
            {
                "verse": "Todo lo puedo en Cristo que me fortalece.",
                "ref": "Filipenses 4:13",
                "theme": "fortaleza y perseverancia",
                "angle": "Tu fuerza no nace de tu ánimo: nace de Cristo. Hoy puedes levantarte otra vez."
            },
            {
                "verse": "Si Dios es por nosotros, ¿quién contra nosotros?",
                "ref": "Romanos 8:31",
                "theme": "identidad y confianza",
                "angle": "Si Dios está contigo, no estás perdido: estás en proceso de restauración."
            },
        ],
    },

    "night": {
        "tag": "EN FAMILIA",
        "headline": "Gracias por el día",
        "items": [
            {
                "verse": "En paz me acostaré, y asimismo dormiré; porque solo tú, Jehová, me haces vivir confiado.",
                "ref": "Salmo 4:8",
                "theme": "paz y confianza",
                "angle": "La paz no viene de que todo salga perfecto, sino de saber quién sostiene tu vida."
            },
            {
                "verse": "Venid a mí todos los que estáis trabajados… y yo os haré descansar.",
                "ref": "Mateo 11:28",
                "theme": "descanso y refugio",
                "angle": "Dios no te pide que llegues fuerte: te pide que llegues. Él te da descanso."
            },
            {
                "verse": "No se ponga el sol sobre vuestro enojo.",
                "ref": "Efesios 4:26",
                "theme": "perdón y restauración",
                "angle": "Cierra el día en paz: pide perdón, perdona, suelta. Tu casa lo vale."
            },
        ],
    },
}

def pick(slot: str) -> dict:
    data = SLOTS[slot]
    item = random.choice(data["items"])
    return {
        "slot": slot,
        "tag": data["tag"],
        "headline": data["headline"],
        "verse": item["verse"],
        "ref": item["ref"],
        "theme": item["theme"],
        "angle": item["angle"],
    }
