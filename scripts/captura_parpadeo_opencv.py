import cv2
import mediapipe as mp
import numpy as np
import time
from datetime import datetime
import csv

# Parámetros de configuración

EAR_THRESH = 0.28  # Umbral EAR para detectar parpadeos
NUM_FRAMES = 2  # Número de frames para contar un parpadeo
CAPTURE_MINUTES = 60  # Duración de captura en minutos
OUTPUT_FILE = "C:/Users/PC-00/Downloads/registros_parpadeo-.csv"  # Ruta del archivo de salida
WINDOW_WIDTH = 720  # Ancho de la ventana
WINDOW_HEIGHT = 540  # Alto de la ventana

# Función para dibujar la salida en el marco
def drawing_output(frame, left_eye, right_eye, blink_count, width, height, remaining_time):

    # Crear una imagen auxiliar para dibujar los ojos
    aux_image = np.zeros(frame.shape, np.uint8)
    cv2.fillPoly(aux_image, pts=[np.array(left_eye)], color=(255, 255, 0))  # Ojo izquierdo
    cv2.fillPoly(aux_image, pts=[np.array(right_eye)], color=(255, 255, 0))  # Ojo derecho
    
    # Combinar la imagen original con la imagen auxiliar
    output = cv2.addWeighted(frame, 1, aux_image, 0.7, 0)
    
    # Dibujar el contador de parpadeos
    cv2.rectangle(output, (width - 330, 5), (width - 10, 50), (0, 0, 255), 3)
    cv2.putText(output, "Cantidad Parpadeos:", (width - 320, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(output, str(blink_count), (width - 80, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

    # Mostrar tiempo de registro en la esquina inferior derecha
    cv2.rectangle(output, (width - 260, height - 110), (width - 10, height - 10), (0, 0, 255), -1)  # Rellenar el recuadro
    cv2.putText(output, "Tiempo de Registro:", (width - 250, height - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Condición para mostrar en minutos o segundos
    if remaining_time > 60:
        cv2.putText(output, f"{int(remaining_time / 60)} min", (width - 180, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    else:
        cv2.putText(output, f"{int(remaining_time)} seg", (width - 180, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
    
    return output

# Función para calcular la relación de aspecto del ojo (EAR)
def eye_aspect_ratio(coords):
    coords = np.array(coords)
    d_A = np.linalg.norm(coords[1] - coords[5])  # Distancia vertical entre puntos 1 y 5
    d_B = np.linalg.norm(coords[2] - coords[4])  # Distancia vertical entre puntos 2 y 4
    d_C = np.linalg.norm(coords[0] - coords[3])  # Distancia horizontal entre puntos 0 y 3
    return (d_A + d_B) / (2.0 * d_C)  # Calcular y devolver el EAR

# Inicialización de la captura de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Captura de video desde la cámara
if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

mp_face_mesh = mp.solutions.face_mesh  # Inicializar Face Mesh de Mediapipe

# Índices de los puntos de los ojos izquierdo y derecho en el modelo de cara
index_left_eye = [33, 160, 158, 133, 153, 144]
index_right_eye = [362, 385, 387, 263, 373, 380]

# Contadores para los parpadeos
aux_counter, blink_counter = 0, 0
start_time = time.time()  # Hora de inicio
capture_seconds = CAPTURE_MINUTES * 60  # Convertir minutos a segundos
blinks = []  # Lista para guardar los registros de parpadeos

# Iniciar el proceso de detección de la cara y los ojos
with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1) as face_mesh:
    while True:
        elapsed_time = time.time() - start_time  # Calcular tiempo transcurrido
        remaining_time = max(capture_seconds - elapsed_time, 0)  # Calcular tiempo restante

        # Salir del bucle si el tiempo se ha agotado
        if remaining_time <= 0:
            print("Tiempo de captura finalizado.")
            break  

        ret, frame = cap.read()  # Leer el cuadro de video
        if not ret:
            print("Error: No se pudo leer el cuadro de video.")
            break
        
        frame = cv2.flip(frame, 1)  # Voltear el marco horizontalmente
        frame = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))  # Redimensionar el marco
        height, width = frame.shape[:2]  # Obtener dimensiones del marco redimensionado
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir a RGB
        results = face_mesh.process(frame_rgb)  # Procesar el marco para detección de rostro

        if results.multi_face_landmarks:  # Si se detecta un rostro
            left_eye = []  # Lista para almacenar coordenadas del ojo izquierdo
            right_eye = []  # Lista para almacenar coordenadas del ojo derecho
            
            # Extraer coordenadas de los ojos en un solo bucle
            for face_landmarks in results.multi_face_landmarks:
                for index in index_left_eye + index_right_eye:
                    x = int(face_landmarks.landmark[index].x * width)  # Coordenada X
                    y = int(face_landmarks.landmark[index].y * height)  # Coordenada Y
                    if index in index_left_eye:
                        left_eye.append([x, y])  # Agregar coordenadas del ojo izquierdo
                    else:
                        right_eye.append([x, y])  # Agregar coordenadas del ojo derecho
                    cv2.circle(frame, (x, y), 2, (255, 255, 0), 1)  # Dibujar puntos en los ojos

            # Calcular la relación de aspecto de los ojos
            ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2
            
            # Contar parpadeos
            if ear < EAR_THRESH:  # Si la relación de aspecto es menor que el umbral
                aux_counter += 1
                if aux_counter == 1:  # Capturar solo al primer parpadeo
                    blink_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtener fecha y hora
                    blinks.append(blink_time)  # Guardar el tiempo del parpadeo
            elif aux_counter >= NUM_FRAMES:  # Si se ha registrado un número suficiente de frames
                aux_counter = 0  # Reiniciar el contador auxiliar
                blink_counter += 1  # Incrementar el contador de parpadeos
            
            # Dibujar la salida en el marco
            frame = drawing_output(frame, left_eye, right_eye, blink_counter, width, height, int(remaining_time))

        cv2.imshow("Captura de Parpadeos", frame)  # Mostrar el marco
        if cv2.waitKey(1) & 0xFF == 27:  # Presiona ESC para salir
            break

# Guardar los registros de parpadeos en un archivo CSV
with open(OUTPUT_FILE, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Fecha y Hora de Parpadeos"])  # Encabezado
    for blink_time in blinks:
        writer.writerow([blink_time])  # Escribir cada tiempo de parpadeo

print(f"Registros de parpadeos guardados en: {OUTPUT_FILE}")

# Liberar recursos
cap.release()  # Liberar la captura de video
cv2.destroyAllWindows()  # Cerrar todas las ventanas abiertas
