# src/verses.py
import random

SLOTS = {
  "morning": {
    "tag": "DIOS TE HABLA HOY",
    "headline": "Gracias por este nuevo día",
    "items": [
      ("Este es el día que hizo el Señor; nos gozaremos y alegraremos en él.", "Salmo 118:24"),
      ("Por la misericordia del Señor no hemos sido consumidos… nuevas son cada mañana.", "Lamentaciones 3:22-23"),
      ("Encomienda a Jehová tu camino, y confía en él; y él hará.", "Salmo 37:5"),
    ],
    "reflection": [
      "Hoy respira profundo: Dios te sostiene. Camina con fe y paz.",
      "No empiezas solo: Dios ya va delante de ti. Confía.",
      "Si amaneciste, es porque Dios aún escribe propósito en tu historia."
    ],
    "cta": "Escribe AMÉN 🙏 y comparte para bendecir a alguien."
  },
  "noon": {
    "tag": "RETOMA EL CAMINO",
    "headline": "Fuerza para seguir",
    "items": [
      ("Esfuérzate y sé valiente… porque Jehová tu Dios estará contigo.", "Josué 1:9"),
      ("Todo lo puedo en Cristo que me fortalece.", "Filipenses 4:13"),
      ("Si Dios es por nosotros, ¿quién contra nosotros?", "Romanos 8:31"),
    ],
    "reflection": [
      "Si te has enfriado, vuelve. Dios no te cancela: te restaura.",
      "No negocies tu destino por un momento de debilidad. Levántate.",
      "Hoy se corta con lo que te destruye. Dios te llama a vivir en luz."
    ],
    "cta": "Si hoy necesitas volver, comenta: ORACIÓN."
  },
  "night": {
    "tag": "EN FAMILIA",
    "headline": "Gracias por el día",
    "items": [
      ("En paz me acostaré, y asimismo dormiré; porque solo tú, Jehová, me haces vivir confiado.", "Salmo 4:8"),
      ("Venid a mí todos los que estáis trabajados… y yo os haré descansar.", "Mateo 11:28"),
      ("No se ponga el sol sobre vuestro enojo.", "Efesios 4:26"),
    ],
    "reflection": [
      "Suelta la carga. Perdona, abraza, ora. Dios cuida tu casa.",
      "Que tu hogar termine el día en paz: Dios es tu refugio.",
      "Hoy fue un regalo. Mañana será otra misericordia. Descansa."
    ],
    "cta": "Da gracias con tu familia hoy. Dios guarda tu hogar."
  }
}

def pick(slot: str):
  data = SLOTS[slot]
  verse, ref = random.choice(data["items"])
  reflection = random.choice(data["reflection"])
  return {
    "slot": slot,
    "tag": data["tag"],
    "headline": data["headline"],
    "verse": verse,
    "ref": ref,
    "reflection": reflection,
    "cta": data["cta"]
  }
