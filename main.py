from ultralytics import YOLO
import cv2
import time

# ==========================================
# ODDYSEY
# Monitoramento Biológico Ambiental
# ==========================================

VIDEO = "canarios.mp4"

# Modelo YOLO
model = YOLO("yolov8s.pt")

# Quantidade esperada de aves
AVES_ESPERADAS = 15

# Limiares
CONFIANCA_MINIMA = 0.25

LIMITE_MOVIMENTO_SUSPEITO = 37500
LIMITE_MOVIMENTO_ALERTA = 70000

LIMITE_AVES = int(AVES_ESPERADAS * 0.9)

TEMPO_RECUPERACAO = 10
TEMPO_CONFIRMACAO_ALERTA = 3

# Satélite (simulado)
foco_calor = False
fumaca_detectada = False
risco_climatico = False

estado = "NORMAL"
inicio_recuperacao = None
inicio_alerta = None

cap = cv2.VideoCapture(VIDEO)

ret, frame_anterior = cap.read()

if not ret:
    print("Erro ao abrir vídeo")
    exit()

frame_anterior = cv2.resize(frame_anterior, (960, 600))

gray_anterior = cv2.cvtColor(
    frame_anterior,
    cv2.COLOR_BGR2GRAY
)

gray_anterior = cv2.GaussianBlur(
    gray_anterior,
    (21, 21),
    0
)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (960, 600))

    # ==========================
    # YOLO
    # ==========================

    results = model(
        frame,
        verbose=False
    )

    aves_detectadas = 0

    for result in results:

        for box in result.boxes:

            classe = int(box.cls[0])
            nome = model.names[classe]
            confianca = float(box.conf[0])

            if nome != "bird":
                continue

            if confianca < CONFIANCA_MINIMA:
                continue

            aves_detectadas += 1

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Canario {confianca:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    # ==========================
    # ANÁLISE DE MOVIMENTO
    # ==========================

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (21, 21),
        0
    )

    diff = cv2.absdiff(
        gray_anterior,
        gray
    )

    thresh = cv2.threshold(
        diff,
        25,
        255,
        cv2.THRESH_BINARY
    )[1]

    thresh = cv2.dilate(
        thresh,
        None,
        iterations=2
    )

    movimento_total = cv2.countNonZero(
        thresh
    )

    gray_anterior = gray.copy()

    # ==========================
    # TEMPO
    # ==========================

    agora = time.time()

    tempo_video = (
        cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    )

    # ==========================
    # SATÉLITE (SIMULADO)
    # ==========================

    foco_calor = 10 <= tempo_video <= 30
    fumaca_detectada = 25 <= tempo_video <= 30

    risco_climatico = (
        foco_calor or fumaca_detectada
    )

    # ==========================
    # MÁQUINA DE ESTADOS
    # ==========================

    if estado == "NORMAL":

        if (
            movimento_total > LIMITE_MOVIMENTO_SUSPEITO
            or risco_climatico
        ):
            estado = "SUSPEITO"
            inicio_recuperacao = agora
            inicio_alerta = None

    elif estado == "SUSPEITO":

        condicao_alerta = (
            (
                movimento_total > LIMITE_MOVIMENTO_ALERTA
                and aves_detectadas < LIMITE_AVES
            )
            or
            (
                risco_climatico
                and aves_detectadas < LIMITE_AVES
            )
        )

        if condicao_alerta:

            if inicio_alerta is None:
                inicio_alerta = agora

            tempo_alerta = (
                agora - inicio_alerta
            )

            if (
                tempo_alerta
                >= TEMPO_CONFIRMACAO_ALERTA
            ):
                estado = "ALERTA"
                inicio_recuperacao = None
                inicio_alerta = None

        else:

            inicio_alerta = None

            if inicio_recuperacao is not None:

                tempo = (
                    agora - inicio_recuperacao
                )

                if tempo >= TEMPO_RECUPERACAO:
                    estado = "NORMAL"
                    inicio_recuperacao = None

    elif estado == "ALERTA":

        if risco_climatico:
            estado = "ALERTA"

        elif aves_detectadas < LIMITE_AVES:
            estado = "ALERTA"

        else:
            estado = "SUSPEITO"

    # ==========================
    # VISUAL
    # ==========================

    if estado == "NORMAL":

        status = "NORMAL"
        cor_banner = (0, 120, 0)

    elif estado == "SUSPEITO":

        status = "SUSPEITO"
        cor_banner = (0, 165, 255)

    else:

        status = "ALERTA - AGITACAO COLETIVA"
        cor_banner = (0, 0, 255)

    # Banner superior

    cv2.rectangle(
        frame,
        (0, 0),
        (960, 80),
        cor_banner,
        -1
    )

    cv2.putText(
        frame,
        "ODDYSEY - Monitoramento Biologico",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Status: {status}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # Painel inferior

    cv2.rectangle(
        frame,
        (0, 540),
        (960, 600),
        (40, 40, 40),
        -1
    )

    texto_inferior = (
        f"AVES DETECTADAS: {aves_detectadas} | "
        f"AVES ESPERADAS: {AVES_ESPERADAS} | "
        f"MOVIMENTO: {movimento_total}"
    )

    cv2.putText(
        frame,
        texto_inferior,
        (15, 565),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    texto_satelite = (
        f"DADOS VIA SATELITE -> "
        f"FOCO DE CALOR: {'SIM' if foco_calor else 'NAO'} | "
        f"FUMACA: {'SIM' if fumaca_detectada else 'NAO'}"
    )

    cv2.putText(
        frame,
        texto_satelite,
        (15, 590),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.60,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "ODDYSEY",
        frame
    )

    tecla = cv2.waitKey(30)

    if tecla == 27:
        break

cap.release()
cv2.destroyAllWindows()