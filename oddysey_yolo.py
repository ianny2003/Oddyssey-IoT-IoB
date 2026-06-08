from ultralytics import YOLO
import cv2
import numpy as np
import time

# ==========================================
# ODDYSEY
# Monitoramento Biológico Ambiental
# ==========================================

VIDEO = r"C:\Users\ianny\OneDrive\Desktop\Iot & IoB\canarios.mp4"

# Modelo YOLO
model = YOLO("yolov8s.pt")

# Quantidade esperada de aves
AVES_ESPERADAS = 5

# Limiares
CONFIANCA_MINIMA = 0.25

LIMITE_MOVIMENTO_SUSPEITO = 35000
LIMITE_MOVIMENTO_ALERTA = 70000

# Nova lógica
LIMITE_AVES = 25
TEMPO_RECUPERACAO = 5

estado = "NORMAL"
inicio_recuperacao = None

cap = cv2.VideoCapture(VIDEO)

ret, frame_anterior = cap.read()

if not ret:
    print("Erro ao abrir vídeo")
    exit()

frame_anterior = cv2.resize(frame_anterior, (960, 540))

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

    frame = cv2.resize(frame, (960, 540))

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
    # ANALISE DE MOVIMENTO
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
    # CLASSIFICACAO
    # ==========================

    agora = time.time()

    # NORMAL
    if estado == "NORMAL":

        if movimento_total > LIMITE_MOVIMENTO_SUSPEITO:

            estado = "SUSPEITO"
            inicio_recuperacao = agora

    # SUSPEITO
    elif estado == "SUSPEITO":

        # Movimento muito forte + redução de aves
        if (
            movimento_total > LIMITE_MOVIMENTO_ALERTA
            and aves_detectadas < LIMITE_AVES
        ):

            estado = "ALERTA"
            inicio_recuperacao = None

        else:

            if inicio_recuperacao is not None:

                tempo = agora - inicio_recuperacao

                if tempo >= TEMPO_RECUPERACAO:

                    estado = "NORMAL"
                    inicio_recuperacao = None

    # ALERTA
    elif estado == "ALERTA":

        # Continua faltando aves
        if aves_detectadas < LIMITE_AVES:

            estado = "ALERTA"
            inicio_recuperacao = None

        else:

            # Aves voltaram
            estado = "SUSPEITO"

            if inicio_recuperacao is None:

                inicio_recuperacao = agora

    # ==========================
    # COR E TEXTO
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

    # ==========================
    # PAINEL
    # ==========================

    cv2.rectangle(
        frame,
        (0, 0),
        (960, 90),
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

    cv2.putText(
        frame,
        f"Aves Detectadas: {aves_detectadas}",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Movimento: {movimento_total}",
        (20, 165),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Aves Esperadas: {AVES_ESPERADAS}",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
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