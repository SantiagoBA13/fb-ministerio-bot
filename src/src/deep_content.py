# src/deep_content.py
import random

OPENERS_MORNING = [
    "Si hoy amaneciste con el corazón pesado, esto es para ti.",
    "Si llevas días sintiéndote lejos, hoy Dios te da un nuevo comienzo.",
    "Si amaneciste sin fuerzas, Dios no te soltó: te sostuvo hasta aquí.",
    "Si tu fe está bajita hoy, no te culpes: solo acércate."
]

OPENERS_NOON = [
    "Si hoy te desviaron tus pensamientos, todavía estás a tiempo de volver.",
    "Si caíste otra vez, no te quedes en el suelo: levántate con Dios.",
    "Si te estás apagando, escucha esto: Dios no terminó contigo.",
    "Si hoy estás lejos del camino, este es tu aviso con amor: regresa."
]

OPENERS_NIGHT = [
    "Si hoy terminaste cansado y con culpa, Dios te ofrece paz.",
    "Si tu mente no para, entrégale la noche a Dios y descansa.",
    "Si hoy hubo tensión en casa, Dios puede restaurar el ambiente.",
    "Si el día te ganó, no te condenes: vuelve a Dios antes de dormir."
]

TRUTHS_SOFT = [
    "Dios no te ama por tu rendimiento, te ama por quien eres.",
    "No necesitas tener todo resuelto para volver. Solo necesitas dar un paso.",
    "La gracia no es premio para el perfecto; es abrazo para el que regresa.",
    "Dios no se cansa de levantarte si tú no te cansas de volver."
]

TRUTHS_FIRM = [
    "Tu alma no se alimenta de excusas: se alimenta de verdad y obediencia.",
    "No negocies tu destino por un momento. Hoy vuelve al camino.",
    "Si algo te está destruyendo, no lo abraces: suéltalo. Dios te restaura.",
    "No estás atrapado: estás a una decisión de empezar de nuevo con Dios."
]

STEPS_MORNING = [
    "Respira hondo y dile a Dios la verdad: “Aquí estoy, así como estoy”.",
    "Repite el versículo 3 veces y deja que te ordene por dentro.",
    "Hoy empieza con una decisión pequeña: 5 minutos con Dios antes del ruido.",
    "Escribe una carga y entrégasela a Dios en una oración simple."
]

STEPS_NOON = [
    "Haz una pausa: apaga distracciones 10 minutos y vuelve a enfocarte en Dios.",
    "Identifica lo que te está apartando (orgullo, vicio, rencor, apatía) y suéltalo hoy.",
    "Da un paso práctico: pide ayuda, pide perdón o corta con lo que te enfría.",
    "Vuelve a lo básico: Biblia, oración corta, obediencia hoy (no mañana)."
]

STEPS_NIGHT = [
    "Cierra el día en paz: perdona y pide perdón si es necesario.",
    "Ora con tu familia o por tu familia (aunque sea 30 segundos).",
    "Escribe 3 gracias del día: entrenas tu corazón para ver a Dios.",
    "Entrégale a Dios tu ansiedad: suelta lo que no puedes controlar."
]

QUESTIONS_MORNING = [
    "¿Qué carga puedes entregarle a Dios hoy, sin seguirla cargando tú?",
    "¿Qué paso pequeño vas a dar hoy para volver al camino?",
    "¿Qué pensamiento necesitas reemplazar hoy por fe?",
    "¿Qué área de tu vida necesita que Dios la ordene hoy?"
]

QUESTIONS_NOON = [
    "¿Qué te está alejando hoy: una decisión, una relación o un hábito?",
    "¿Qué vas a cortar hoy para retomar el camino de verdad?",
    "¿Qué área necesita disciplina hoy, aunque no tengas ganas?",
    "¿Qué es eso que sabes que debes soltar, pero sigues abrazando?"
]

QUESTIONS_NIGHT = [
    "¿Qué necesitas perdonar o pedir perdón antes de dormir?",
    "¿Qué te robó la paz hoy y cómo se lo vas a entregar a Dios?",
    "¿Por qué puedes dar gracias hoy, aun si fue un día difícil?",
    "¿Qué conversación pendiente necesitas sanar en tu familia?"
]

def make_reflection_and_prayer(payload: dict) -> tuple[str, str, str, str]:
    slot = payload["slot"]
    theme = payload.get("theme", "")
    angle = payload.get("angle", "")
    ref = payload["ref"]

    if slot == "morning":
        opener = random.choice(OPENERS_MORNING)
        truth = random.choice(TRUTHS_SOFT)
        s1, s2 = random.sample(STEPS_MORNING, 2)
        question = random.choice(QUESTIONS_MORNING)

        reflection = (
            f"{opener}\n\n"
            f"📖 {ref} no es un adorno: es dirección para tu alma. {angle} "
            f"Hoy el tema es {theme}, y Dios te está diciendo: “Vuelve, camina conmigo”.\n\n"
            f"No empieces peleando solo. Empieza acompañado. {truth}\n\n"
            f"🧭 Pasos de hoy:\n"
            f"• {s1}\n"
            f"• {s2}"
        )

        prayer = (
            "Señor, gracias por este nuevo día.\n"
            "Hoy vuelvo a Ti con lo que soy y con lo que tengo.\n"
            "Sana mi corazón, renueva mi fe y guía mis decisiones.\n"
            "Que este día sea un regreso real a tu camino. Amén."
        )

        cta = "Si te identificas, escribe “ORACIÓN” y oramos contigo. 🙏"

    elif slot == "noon":
        opener = random.choice(OPENERS_NOON)
        truth = random.choice(TRUTHS_FIRM)
        s1, s2 = random.sample(STEPS_NOON, 2)
        question = random.choice(QUESTIONS_NOON)

        reflection = (
            f"{opener}\n\n"
            f"📖 {ref} te está llamando a firmeza. {angle} "
            f"Hoy el tema es {theme}. Y sí: Dios te quiere levantar, pero también te quiere reordenar.\n\n"
            f"Esto no es condena, es rescate. {truth}\n\n"
            f"🧭 Pasos de hoy:\n"
            f"• {s1}\n"
            f"• {s2}"
        )

        prayer = (
            "Señor, hoy decido regresar.\n"
            "Rompe lo que me ata, corrige mi rumbo y fortalece mi carácter.\n"
            "Dame valentía para obedecerte y constancia para sostenerlo.\n"
            "Toma mi vida otra vez. Amén."
        )

        cta = "Si hoy quieres volver, comenta “VUELVO”. 🙏"

    else:
        opener = random.choice(OPENERS_NIGHT)
        truth = random.choice(TRUTHS_SOFT)
        s1, s2 = random.sample(STEPS_NIGHT, 2)
        question = random.choice(QUESTIONS_NIGHT)

        reflection = (
            f"{opener}\n\n"
            f"📖 {ref} te recuerda que Dios también está en la noche. {angle} "
            f"Hoy el tema es {theme}. Y antes de dormir, Dios te ofrece paz real.\n\n"
            f"Si te alejaste, no cierres el día lejos. Cierra el día en Sus manos. {truth}\n\n"
            f"🧭 Pasos para cerrar el día:\n"
            f"• {s1}\n"
            f"• {s2}"
        )

        prayer = (
            "Señor, gracias por sostenerme este día.\n"
            "Perdona mis fallas y limpia mi mente de ansiedad y culpa.\n"
            "Trae paz a mi casa, amor a mi familia y descanso a mi corazón.\n"
            "Esta noche vuelvo a Ti. Amén."
        )

        cta = "Compártelo con alguien que necesite aliento esta noche. 🙏"

    return reflection, prayer, cta, question
