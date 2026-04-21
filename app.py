import streamlit as st
import random
import time
import base64

import requests

def guardar_datos(data):
    url = "https://script.google.com/macros/s/AKfycbxBKkY6rfPJepvt0P2ZiATu4z4qXt6w_F2NB354E-Zc6mai2RLRH5sH-novokU3iNmiGA/exec"
    try:
        requests.post(url, json=data)
    except:
        pass

st.set_page_config(page_title="Proceso de selección", layout="centered")

st.title("💻 Google Málaga — Proceso de selección")
st.markdown("""
Has sido seleccionado para participar en un proceso de selección de Google.

🏆 Recompensa:
- Prácticas: 2800€/mes  
- Contrato posterior: 3400€/mes  
- Bonus: SPA para dos personas  

Tu objetivo es superar las pruebas.
""")

# -----------------------------
# ESTADO
# -----------------------------
if "fase" not in st.session_state:
    st.session_state.fase = 0
    st.session_state.start = None
    st.session_state.pistas_usadas = 0

if "perfil" not in st.session_state:
    st.session_state.perfil = random.choice(["A","B","C","D"])

perfil = st.session_state.perfil

if "subperfil_D" not in st.session_state:
    if perfil == "D":
        st.session_state.subperfil_D = random.choice(["facil","dificil"])
    else:
        st.session_state.subperfil_D = None

if "trampas" not in st.session_state:
    st.session_state.trampas = 0

if "guardado" not in st.session_state:
    st.session_state.guardado = False

permisos = {
    "A": ["materiales", "whatsapp", "profesor", "pistas"],
    "B": ["materiales", "profesor"],
    "C": ["profesor"],
    "D": []
}
if "intentos_test" not in st.session_state:
    st.session_state.intentos_test = 0

if "error_ayuda" not in st.session_state:
    st.session_state.error_ayuda = False

if "error_tipo" not in st.session_state:
    st.session_state.error_tipo = None

if "cambios_pestana" not in st.session_state:
    st.session_state.cambios_pestana = 0

from streamlit.runtime.scriptrunner import get_script_run_ctx

if "last_event" not in st.session_state:
    st.session_state.last_event = None

    
# -----------------------------
# FUNCIONES
# -----------------------------
def tiempo():
    tiempos = {"A":1600,"B":1400,"C":1200,"D":900}
    restante = int(tiempos[perfil] - (time.time() - st.session_state.start))

    minutos = restante // 60
    segundos = restante % 60

    st.markdown(f"⏱️ **Tiempo restante: {minutos:02d}:{segundos:02d}**")

    if restante <= 0:

        if not st.session_state.guardado:

            guardar_datos({
                "id": st.session_state.get("nombre", "anonimo"),
                "perfil": perfil,
                "fase": st.session_state.fase,
                "trampas": st.session_state.get("trampas", 0),
                "pistas": st.session_state.get("pistas_usadas", 0),
                "intentos_test": st.session_state.get("intentos_test", 0),
                "resultado": "timeout"
            })

            st.session_state.guardado = True

        st.error("⏱️ Tiempo agotado — proceso finalizado")
        st.stop()

def abandonar():
    if st.button("❌ Abandonar proceso", key=f"abandonar_{st.session_state.fase}"):

        guardar_datos({
            "id": st.session_state.get("nombre", "anonimo"),
            "perfil": perfil,
            "fase": st.session_state.fase,
            "trampas": st.session_state.get("trampas", 0),
            "pistas": st.session_state.get("pistas_usadas", 0),
            "resultado": "abandono"
        })

        st.error("Has abandonado el proceso")
        st.stop()

def reproducir_audio_auto(ruta):
    try:
        with open(ruta, "rb") as f:
            audio_bytes = f.read()

        b64 = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """

        st.markdown(audio_html, unsafe_allow_html=True)

    except:
        st.warning("No se pudo reproducir el audio")

# -----------------------------
# PISTAS
# -----------------------------
# -----------------------------
# PISTAS
# -----------------------------
def pista():

    # ❌ NO bloquear antes (esto hacía desaparecer el botón)
    # if perfil == "D" and not st.session_state.error_ayuda:
    #     return

    if st.session_state.fase == 2:
        return

    # 🔥 NUEVA LÓGICA DE BLOQUEO
    bloqueado = (perfil == "D" and st.session_state.error_tipo != "pistas")

    if st.sidebar.button("💡 Solicitar pista", key=f"pista_{st.session_state.fase}"):

        if "pistas" not in permisos[perfil]:
            st.sidebar.warning("⚠️ En principio el acceso a la pista no está permitido, PERO...")
            time.sleep(0.5)
            st.sidebar.success("⚠️ Atención: pista desbloqueada por error. Puede ver la pista debajo de este aviso")
            

        
            

        # ---------- FASE 1 ----------
        if st.session_state.fase == 1:
            lista = [
                "PISTA: El patrón no es único: hay dos reglas que se alternan",
                "PISTA: Observa las posiciones pares e impares por separado",
                "PISTA: Algunos saltos son multiplicativos y otros no",
                "PISTA: Prueba a analizar qué ocurre cada dos pasos",
                "PISTA: No todos los cambios siguen la misma lógica",
                "PISTA: Divide la serie en dos secuencias intercaladas",
                "PISTA: Los cambios grandes y pequeños no ocurren al azar"
            ]

        # ---------- FASE 3 ----------
        elif st.session_state.fase == 3:
            lista = [
                "PISTA: Cada letra ha sido desplazada varias posiciones en el alfabeto",
                "PISTA: No hay símbolos raros, solo letras desplazadas",
                "PISTA: La G podría no ser realmente una G… piensa en retroceder letras",
                "PISTA: Intenta restar el mismo número a cada letra del alfabeto",
                "PISTA: Todas las letras se han movido el mismo número de posiciones",
                "PISTA: Es un cifrado por desplazamiento (tipo César)"
            ]

        # ---------- FASE 4 ----------
        elif st.session_state.fase == 4:

            if perfil == "A":
                lista = [
                    "Trabaja con cada cifra por separado",
                    "Puede haber una transformación antes del resultado",
                    "No es una operación directa con el número completo"
                ]

            elif perfil == "B":
                lista = [
                    "Divide la palabra en partes",
                    "Cuenta diferentes tipos de elementos",
                    "No todo lo que cuentas es lo mismo"
                ]

            elif perfil == "C":
                lista = [
                    "Cada persona se saluda con todas las demás",
                    "Evita contar saludos duplicados",
                    "Esto sigue una fórmula combinatoria"
                ]

            elif perfil == "D":
                lista = [
                    "Primero elimina los números que no cumplen la condición",
                    "Después cuenta con un patrón regular",
                    "Los números pares siguen un intervalo constante"
                ]

        else:
            return

        # ---------- CONTROL ----------
        if perfil == "A":
            st.sidebar.info(random.choice(lista))

        elif perfil in ["B", "C"]:
            if st.session_state.pistas_usadas == 0:
                st.sidebar.info(random.choice(lista))
                st.session_state.pistas_usadas = 1

                if st.session_state.error_tipo != "pistas":
                    st.session_state.trampas += 1

       
# -----------------------------
# NORMAS
# -----------------------------
def mostrar_normas():
    st.subheader("📋 Normas del proceso")

    if perfil == "A":
        st.write("Puedes utilizar los recursos y ayudas que quieras si lo consideras necesario.")
    elif perfil == "B":
        st.write("En principio, solo puedes consultar materiales de la asignatura y/o pedir ayuda al profesor.")
    elif perfil == "C":
        st.write("En principio solo está permitido pedir ayuda al profesor.")
    else:
        st.write("En principio no puedes hacer uso de ningún tipo de ayuda. Pero puedes decidir usarlas o no.")

# -----------------------------
# BOTONES TRAMPA (SIDEBAR)
# -----------------------------
# -------- ERROR ALEATORIO DE AYUDA --------
def botones_trampa():

    # -------- ERROR ALEATORIO --------
    prob = {
        "A": 0.0,
        "B": 0.15,
        "C": 0.25,
        "D": 0.55
    }

    if not st.session_state.error_ayuda:
        if random.random() < prob[perfil]:
            st.session_state.error_ayuda = True
            st.session_state.error_tipo = random.choice([
                "pistas",
                "materiales",
                "whatsapp"
            ])
            st.sidebar.success("⚠️ Error del sistema: ayuda desbloqueada temporalmente")

    # -------- SIEMPRE SE MUESTRA --------
    st.sidebar.divider()
    st.sidebar.subheader("⚠️ Opciones adicionales")

    # -------- MATERIALES --------
    if st.sidebar.button("📚 Consultar materiales", key=f"mat_{st.session_state.fase}"):

        st.markdown('[Abrir campus](https://derecho.cv.uma.es/course/view.php?id=4646)', unsafe_allow_html=True)

        if "materiales" not in permisos[perfil]:
            st.session_state.trampas += 1
            st.sidebar.warning("Has mejorado tu probabilidad de éxito")

    # -------- WHATSAPP --------
    if st.sidebar.button("🤝 Pedir ayuda por WhatsApp", key=f"wa_{st.session_state.fase}"):

        st.sidebar.info("Contactando con otro candidato...")
        st.markdown('[Abrir WhatsApp](https://wa.me/)', unsafe_allow_html=True)

        if "whatsapp" not in permisos[perfil]:
            st.session_state.trampas += 1
            st.sidebar.warning("Has mejorado tu probabilidad de éxito")

    # -------- PROFESOR --------
    if st.sidebar.button("👨‍🏫 Ayuda del profesor", key=f"prof_{st.session_state.fase}"):

        reproducir_audio_auto("profesor.mp3")

        if "profesor" not in permisos[perfil]:
            st.session_state.trampas += 1
            st.sidebar.warning("Has mejorado tu probabilidad de éxito")

    # 👉 IMPORTANTE
    pista()

# -----------------------------
# INICIO
# -----------------------------
if st.session_state.fase == 0:

    nombre = st.text_input("Nombre del candidato o candidata")

    if nombre:
        mostrar_normas()

    if st.button("Comenzar", key="btn_inicio") and nombre:
        st.session_state.start = time.time()
        st.session_state.fase = 1
        st.session_state.nombre = nombre

# -----------------------------
# FASE 1
# -----------------------------
if st.session_state.fase == 1:

    tiempo()
    abandonar()
    botones_trampa()

    st.header("Fase 1 — Secuencia lógica")

    if "secuencia" not in st.session_state:
        st.session_state.secuencia = random.choice([
            ([2, 6, 7, 21, 22, 66], 67),
            ([3, 9, 11, 33, 35, 105], 107),
            ([2, 4, 12, 48, 240], 1440)
        ])

    seq, sol = st.session_state.secuencia
    seq_mostrar = list(seq)
    if "indices_ocultos" not in st.session_state:
        st.session_state.indices_ocultos = None

    # -------- DIFERENCIACIÓN --------
    if perfil == "B" and len(seq_mostrar) > 2:
        seq_mostrar[2] = "?"

    elif perfil == "C":
        if len(seq_mostrar) > 2:
            seq_mostrar[2] = "?"
        seq_mostrar[-1] = "?"

    elif perfil == "D":

        seq_mostrar = list(seq)

        if st.session_state.indices_ocultos is None:

            posibles = list(range(len(seq)))

        # ❗ evitar extremos (clave para que sea resoluble)
            posibles = posibles[1:-1]

            random.shuffle(posibles)

            indices = []

            for i in posibles:
            # evitar consecutivos
                if all(abs(i - j) > 1 for j in indices):
                    indices.append(i)

                if len(indices) == 3:
                    break

        # 🔒 si no consigue 3, se queda con los que tenga
            st.session_state.indices_ocultos = indices

    # aplicar ocultación
        for i in st.session_state.indices_ocultos:
            seq_mostrar[i] = "?"

    # -------- MOSTRAR --------
    st.markdown("### Secuencia")
    st.markdown(" → ".join(map(str, seq_mostrar)))

    # -------- INPUT --------
    r = st.text_input("Introduce el siguiente número de la serie", key="f1_input")

    if st.button("Comprobar", key="btn_f1"):

        if perfil == "C" and random.random() < 0.3:
            st.warning("⚠️ Error del sistema. Reintenta.")
        else:
            if r.strip() == str(sol):
                st.session_state.fase = 2
                st.session_state.error_ayuda = False
                st.session_state.pistas_usadas = 0
                st.session_state.indices_ocultos = None
                reproducir_audio_auto("fase_ok.mp3")
            else:
                st.error("Incorrecto")

# -----------------------------
# FASE 2 — TEST (COMPLETO)
# -----------------------------
if st.session_state.fase == 2:

    tiempo()
    abandonar()
    botones_trampa()

    st.header("Fase 2 — Evaluación de conocimientos")

    def q(texto, opciones, key):
        return st.radio(texto, opciones, key=key)

    # 👉 TODO TU BLOQUE ORIGINAL AQUÍ (SIN CAMBIOS)
    # (lo mantengo tal cual lo enviaste)

    # 👇 TODO ESTE BLOQUE ES EXACTAMENTE EL TUYO (NO MODIFICADO)
    # (lo mantengo igual que lo enviaste)

    if perfil == "A":
        r1 = q("1. De acuerdo con la teoría de las actividades cotidianas, para que el delito ocurra deben coincidir en el espacio y el tiempo:",
               ["Un delincuente potencial, una víctima inadecuada y la presencia de un guardián",
                "Un delincuente potencial, una víctima adecuada y la presencia policial",
                "Un delincuente motivado, una víctima u objetivo adecuado y la ausencia de un guardián capaz"], "a1")

        r2 = q("2. ¿Qué Escuela de pensamiento sostiene la idea del libre albedrío?",
               ["La Escuela Clásica", "La Escuela Positivista Italiana", "La Escuela de Chicago"], "a2")

        r3 = q("3. ¿Qué teoría explica que el delincuente continua cometiendo delitos como resultado de que la sociedad le ha puesto una etiqueta?",
               ["La teoría del conflicto social", "La teoría del labelling approach o etiquetamiento", "La teoría del control social informal"], "a3")

        r4 = q("4. De acuerdo con la teoría de la desorganización social ¿Qué tres características estructurales explican la mayor concentración de delitos?",
               ["Concentración de pobreza, homogeneidad nacional y heterogeneidad cultural",
                "Acumulación de pobreza, estabilidad poblacional y heterogeneidad cultural",
                "Acumulación de pobreza, inestabilidad poblacional y heterogeneidad étnico-cultural"], "a4")

        r5 = q("5. De acuerdo con la Escuela Clásica ¿Qué características deberían tener las penas para ser efectivas?",
               ["Celeridad, certeza y severidad", "Celeridad, certeza y proporcionalidad", "Celeridad, retraso y severidad"], "a5")

        r6 = q("6. De acuerdo con la Teoría de la Asociación Diferencial de Sutherland:",
               ["La delincuencia se aprende de observarla en los medios de comunicación", 
                "La delincuencia no se hereda, sino que surge de forma espontánea", 
                "La delincuencia se aprende, al igual que cualquier otro comportamiento"], "a6")

        correctas = [
            r1.startswith("Un delincuente motivado"),
            r2 == "La Escuela Clásica",
            r3.startswith("La teoría del labelling"),
            r4.startswith("Acumulación de pobreza, inestabilidad"),
            r5 == "Celeridad, certeza y severidad",
            r6 == "La delincuencia se aprende, al igual que cualquier otro comportamiento"
        ]

    elif perfil == "B":
        r1 = q("1. De acuerdo con la teoría de las actividades cotidianas, para que el delito ocurra deben coincidir en el espacio y el tiempo:",
               ["Un delincuente potencial, una víctima inadecuada y la presencia de un guardián",
                "Un delincuente potencial, una víctima adecuada y la presencia policial",
                "Un delincuente motivado, una víctima u objetivo adecuado y la ausencia de un guardián capaz"], "b1")

        r2 = q("2. ¿Qué Escuela de pensamiento sostiene la idea del libre albedrío?",
               ["La Escuela Clásica", "La Escuela Positivista Italiana", "La Escuela de Chicago"], "b2")

        r3 = q("3. ¿Cuáles son los dos mecanismos explicativos a los que alude la teoría de la personalidad criminal de Eysenck?",
               ["Desarrollo de la conciencia moral y capacidad de comportarse prosocialmente",
                "Desarrollo de la conciencia moral e incapacidad de comportarse prosocialmente",
                "Aprendizaje clásico y aversión"], "b3")

        r4 = q("4. De acuerdo con la Escuela Clásica ¿Qué características deberían tener las penas para ser efectivas?",
               ["Especificidad, certeza y severidad",
                "Celeridad, certeza y proporcionalidad",
                "Celeridad, severidad y certeza"], "b4")

        r5 = q("5. La teoría de la elección racional:",
               ["Parte de que el individuo está destinado a delinquir",
                "Parte del enfoque del libre albedrío",
                "Acepta el indeterminismo patológico"], "b5")
        
        r6 = q("6. La teoría del aprendizaje social de Sutherland:",
               ["Toma como base las ideas del condicionamiento clásico",
                "Toma como base las ideas del condicionamiento operante",
                "Toma como base las ideas del aprendizaje vicario"], "b6")

        r7 = q("7. La teoría del patrón delictivo dice que:",
               ["El modus operandi tiene un patrón que cambia siempre",
                "La delincuencia se distribuye de manera uniforme por el espacio y el tiempo",
                "La persona delincuente tiende a delinquir dentro de su espacio de actividad y conciencia"], "b7")

        correctas = [
            r1.startswith("Un delincuente motivado"),
            r2 == "La Escuela Clásica",
            r3.startswith("Desarrollo de la conciencia moral"),
            r4.startswith("Celeridad, severidad"),
            r5.startswith("Parte del enfoque del libre albedrío"),
            r6.startswith("Toma como base las ideas del aprendizaje vicario"),
            r7.startswith("La persona delincuente tiende a delinquir dentro de su espacio de actividad y conciencia")
            
        ]

    elif perfil == "C":
        r1 = q("1. ¿Cuáles son los dos mecanismos explicativos a los que alude la teoría de la personalidad criminal de Eysenck?",
               ["Desarrollo de la conciencia moral y capacidad de comportarse prosocialmente",
                "Desarrollo de la conciencia moral e incapacidad de comportarse prosocialmente",
                "Aprendizaje clásico y aversión"], "c1")

        r2 = q("2. ¿Cuál de las siguientes no es una crítica al enfoque de la elección racional?",
               ["Ponen demasiado énfasis en el individuo",
                "Prestan demasiada atención a las motivaciones para delinquir",
                "Los delincuentes son poco realistas en sus evaluaciones",
                "Todas las anteriores son críticas"], "c2")

        r3 = q("3. ¿Cuál de las siguientes características de la personalidad no está relacionada con el comportamiento delictivo?",
               ["Locus de control interno",
                "Ausencia de empatía",
                "Baja tolerancia a la frustración",
                "Todas están relacionadas"], "c3")

        r4 = q("4. ¿Qué autores desarrollaron la teoría de la desorganización social?",
               ["Thomas y Znaniecki",
                "Shaw Mendes y Henry Mendely",
                "Cornish y Clarke",
                "Shaw y Mackay"], "c4")

        r5 = q("5. ¿Qué autor se preguntó 'Por qué el comportamiento delictivo no es el más común?'",
               ["Durkheim",
                "Ivan Nye",
                "Cohen",
                "Ninguno de los anteriores"], "c5")

        r6 = q("6. La segunda Ley de Tarde enunca que:'",
               ["Las modas nuevas sustituyen a las antiguas",
                "El delito se aprende por observación mediática del comportamiento",
                "Los tipos de arma de fuego empleadas dependen del contexto social",
                "Los inferiores copian el comportamiento de los superiores"], "c6")

        r7 = q("7. ¿Cuál de las siguientes opciones es una crítica a la teoría de la asociación diferencial:",
               ["No tiene en cuenta la motivación del sujeto para cometer el delito",
                "Las definiciones favorables y desfavorables del delito son muy difíciles de medir",
                "No tiene en cuenta que el delito puede también aprenderse por imitación",
                "Ninguna de las anteriores es una crítica"], "c7")

        correctas = [
            r1.startswith("Desarrollo de la conciencia moral"),
            r2.startswith("Todas"),
            r3.startswith("Locus"),
            r4.startswith("Shaw"),
            r5.startswith("Ivan"),
            r6.startswith("Los inferiores copian el comportamiento de los superiores"),
            r7.startswith("Las definiciones favorables y desfavorables del delito son muy difíciles de medir")
            
        ]

    else:
        r1 = q("1. ¿Qué autor se preguntó 'Por qué el comportamiento delictivo no es el más común?'",
               ["Durkheim",
                "Ivan Nye",
                "Cohen",
                "Ninguno de los anteriores"], "d1")

        r2 = q("2. ¿Qué opinaba Ruth Kornhauser de la teoría de la desorganización social?",
               ["Era un modelo tautológico",
                "Era un modelo puro coherente",
                "Era un modelo híbrido incapaz de explicar la delincuencia adulta",
                "Era una teoría circular que no necesitaba mejoras"], "d2")

        r3 = q("3. ¿Qué autor apoyaba la pena de muerte?",
               ["Lombroso", "Ferri", "Garofalo", "Fishbein"], "d3")

        r4 = q("4. ¿Cuál de los siguientes factores no contribuyó al éxito de la criminología crítica?",
               ["El sistema es defectuoso",
                "Escepticismo frente a teorías anteriores",
                "Rechazo a la idea de consenso del derecho penal",
                "Rechazo al libre albedrío"], "d4")

        r5 = q("5. ¿Qué autor dijo: 'el niño que no logra alcanzar el grado de configuración emocional exigida socialmente es considerado como enfermo, anormal, criminal'?",
               ["Katanambú", "Sykes", "Norbert Elias", "Lemert"], "d5")

        r6 = q("6. ¿Qué autor español desarrolló la Teoría del Triple Riesgo Delictivo?",
               ["Santiago Redondo", "Vicente Garrido", "Beatriz de Vicente", "Jordi Esparragueras"], "d6")

        r7 = q("7. ¿A qué teoría se le ha criticado por ser más una teoría de la victimización que del delito?",
               ["A la teoría de la victimización repetida", "A la teoría de las actividades cotidianas", 
                "A la teoría del estilo de vida", "A la teoría de la elección racional"], "d7")

        

        correctas = [
            r1.startswith("Ivan"),
            r2.startswith("Era un modelo tautológico"),
            r3.startswith("Garofalo"),
            r4.startswith("Rechazo al libre albedrío"),
            r5.startswith("Norbert Elias"),
            r6.startswith("Santiago Redondo"),
            r7.startswith("A la teoría de las actividades cotidianas")
            
        ]

    if st.button("Finalizar test", key="btn_test"):

        if perfil == "C" and random.random() < 0.3:
            st.warning("⚠️ Error al enviar respuestas. Reintenta.")

        else:
            if all(correctas):
                st.session_state.fase = 3
                st.session_state.error_ayuda = False
                reproducir_audio_auto("fase_ok.mp3")

            else:
                st.session_state.intentos_test += 1
                guardar_datos({
                    "id": st.session_state.get("nombre", "anonimo"),
                    "perfil": perfil,
                    "fase": st.session_state.fase,
                    "trampas": st.session_state.get("trampas", 0),
                    "pistas": st.session_state.get("pistas_usadas", 0),
                    "intentos_test": st.session_state.get("intentos_test", 0),
                    "resultado": "fallo_test"
                })
                
                if st.session_state.intentos_test > 1 and perfil != "A":
                    st.session_state.trampas += 1
                    st.warning("⚠️ Reintentar mejora tus probabilidades de éxito")

                st.error("Respuestas incorrectas. Debe responder correctamente a todas.")


# -----------------------------
# FASE 3 — CIFRADO
# -----------------------------
if st.session_state.fase == 3:

    tiempo()
    abandonar()
    botones_trampa()

    st.header("Fase final — Descifrado")

    if "cifrado" not in st.session_state:
        st.session_state.cifrado = random.choice([
            ("SDUDGLJPD", "PARADIGMA"),
            ("DQRPLD", "ANOMIA"),
            ("FRQWURO VRFLDO", "CONTROL SOCIAL")  
        ])

    texto, solucion = st.session_state.cifrado

    if perfil == "D":
        texto = " ".join([c if random.random()>0.5 else "_" for c in texto])

    st.write("Mensaje:", texto)

    r = st.text_input("Respuesta", key="cifrado_input")

    if st.button("Validar", key="btn_final"):

        if perfil == "C" and random.random() < 0.3:
            st.warning("⚠️ Error del sistema. Reintenta.")
        else:
            if solucion in r.upper():
                st.session_state.fase = 4
                st.session_state.error_ayuda = False
                reproducir_audio_auto("fase_ok.mp3")
            else:
                st.error("Incorrecto")


import requests

def guardar_datos(data):
    url = "https://script.google.com/macros/s/AKfycbxBKkY6rfPJepvt0P2ZiATu4z4qXt6w_F2NB354E-Zc6mai2RLRH5sH-novokU3iNmiGA/exec"
    try:
        requests.post(url, json=data)
    except:
        pass

# -----------------------------
# FASE 4 — PSICOTÉCNICOS
# -----------------------------
if st.session_state.fase == 4:

    tiempo()
    abandonar()
    botones_trampa()

    st.header("Fase 4 — Psicotécnicos")

    # -------- PERFIL A --------
    if perfil == "A":

        st.write("152 = 157")
        st.write("1253 = 38")
        st.write("1331 = ?")

        r = st.text_input("Respuesta", key="psi_A_input")

        if st.button("Responder", key="psi_A"):

            if r.strip() == "44":
                st.session_state.fase = 5
                st.session_state.error_ayuda = False
            else:
                st.error("Incorrecto")

    # -------- PERFIL B --------
    elif perfil == "B":

        st.write("Jefatura = 4+4")
        st.write("Comisaría = 5+4")
        st.write("Patrulla = 3+5")
        st.write("Apolo = ?")

        r = st.text_input("Respuesta (formato: X+Y)", key="psi_B_input")

        if st.button("Responder", key="psi_B"):

            if r.replace(" ", "") == "3+2":
                st.session_state.fase = 5
            else:
                st.error("Incorrecto")

    # -------- PERFIL C --------
    elif perfil == "C":

        st.write("Si en una reunión, al saludarse, se han producido 10 apretones de manos:")
        st.write("¿Cuántas personas asistieron?")

        r = st.text_input("Respuesta", key="psi_C_input")

        if st.button("Responder", key="psi_C"):

            if r.strip() == "5":
                st.session_state.fase = 5
            else:
                st.error("Incorrecto")

    # -------- PERFIL D --------
    else:

        st.write("¿Cuántos números pares hay del 70 al 379 (ambos inclusive), sin tener en cuenta los de dos cifras?")

        r = st.text_input("Respuesta", key="psi_D_input")

        if st.button("Responder", key="psi_D"):

            if r.strip() == "140":
                st.session_state.fase = 5
            else:
                st.error("Incorrecto")

# -----------------------------
# FINAL
# -----------------------------

if st.session_state.fase == 5 and not st.session_state.guardado:

    guardar_datos({
        "id": st.session_state.get("nombre", "anonimo"),
        "perfil": perfil,
        "fase": st.session_state.fase,
        "trampas": st.session_state.get("trampas", 0),
        "pistas": st.session_state.get("pistas_usadas", 0),
        "intentos_test": st.session_state.get("intentos_test", 0),
        "resultado": "completado",
        
    })

    st.session_state.guardado = True

    st.success("Proceso finalizado. Gracias por aplicar al puesto de trabajo en Google.")
