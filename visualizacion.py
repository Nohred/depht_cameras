import cv2
import pandas as pd
import numpy as np
import mediapipe as mp
import os
from sklearn.preprocessing import StandardScaler

NUM_CAPTURA = 1
CATEGORIA = "CajaCabeza"



# Cargar datos del CSV

def format_number(num):
    if 1 <= num <= 20:
        return f"{num:02}"
    else:
        raise ValueError("Number must be between 1 and 20")

NUM_CAPTURA = format_number(NUM_CAPTURA)

csv_path = r"C:\Personal Local\Recuperacion\Escuela\5to Semestre\Machine Learning\depht cameras\MultipleCameras\captured_data"+ \
    '/'+ CATEGORIA + '/captura_' +NUM_CAPTURA+  '.csv'  # Ruta del archivo CSV

df = pd.read_csv(csv_path)  # Leer el archivo CSV


# Normalizar x e y con respecto a las dimensiones de la imagen
for idx in range(33):
    x_col = "joint" + str(idx) + "_x"
    y_col = "joint" + str(idx) + "_y"
    if x_col in df.columns and y_col in df.columns:
        df[x_col] = df[x_col] / 640
        df[y_col] = df[y_col] / 480

# Configurar MediaPipe
mp_pose = mp.solutions.pose
pose_connections = mp_pose.POSE_CONNECTIONS

# Crear una lista de números del 0 al 32
indices = list(range(33))

# Recorrer cada frame en el DataFrame para reconstruir el esqueleto
for _, row in df.iterrows():
    # Crear una imagen en blanco
    image = np.zeros((480, 640, 3), dtype=np.uint8) 

    # Extraer coordenadas y dibujar cada punto
    points = {}
    for idx in range(33):
        x_col = "joint"+str(idx) + "_x"  
        y_col = "joint"+str(idx) + "_y"
        z_col = "joint"+str(idx) + "_z"

        if x_col in row and y_col in row:
            x = int(row[x_col] * image.shape[1])
            y = int(row[y_col] * image.shape[0])
            z = row[z_col] 

            # Dibujar el punto en la imagen
            cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
            points[idx] = (x, y)

    # Dibujar las conexiones del esqueleto
    for connection in pose_connections:
        start_idx, end_idx = connection
        if start_idx in points and end_idx in points:
            cv2.line(image, points[start_idx], points[end_idx], (255, 0, 0), 2)

    # Mostrar la imagen
    cv2.imshow("Reconstructed Skeleton", image)

    # Esperar brevemente para simular la tasa de fotogramas
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
