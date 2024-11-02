import cv2
import mediapipe as mp
import numpy as np



def drawing_output(frame, coordinates_left_eye, coordinates_right_eye, blink_counter, width, height):
    aux_image = np.zeros(frame.shape, np.uint8)
    contours1 = np.array([coordinates_left_eye])
    contours2 = np.array([coordinates_right_eye])
    cv2.fillPoly(aux_image, pts=[contours1], color=(255, 255, 0))  # Contorno del ojo izquierdo (verde)
    cv2.fillPoly(aux_image, pts=[contours2], color=(255, 255, 0))  # Contorno del ojo derecho (verde)
    output = cv2.addWeighted(frame, 1, aux_image, 0.7, 1)

       # Dimensiones del rectángulo y márgenes
    rect_width = 300
    rect_height = 50
    margin = 5  # Margen desde el borde derecho

    # Cambia las coordenadas para la esquina superior derecha con margen
    #cv2.rectangle(output, (width - rect_width - margin, margin), (width - margin, rect_height + margin), (0, 0, 0), -1)  # Rectángulo negro relleno
    cv2.rectangle(output, (width - rect_width - margin + 2, margin), (width - margin - 2, rect_height + margin), (0, 0, 255),2)# # rojo, 2)  # Contorno negro

    # Texto que se verá en la esquina superior derecha
    cv2.putText(output, "Cantidad Parpadeos:", (width - rect_width - margin + 10, margin + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 0, 255),2)# (0, 255, 255), 2)
    cv2.putText(output, "{}".format(blink_counter), (width - margin - 50, margin + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0),2)# (128, 0, 250), 2)  # Ubicado a la derecha

    return output

def eye_aspect_ratio(coordinates):
    d_A = np.linalg.norm(np.array(coordinates[1]) - np.array(coordinates[5]))
    d_B = np.linalg.norm(np.array(coordinates[2]) - np.array(coordinates[4]))
    d_C = np.linalg.norm(np.array(coordinates[0]) - np.array(coordinates[3]))

    return (d_A + d_B) / (2 * d_C)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mp_face_mesh = mp.solutions.face_mesh
index_left_eye = [33, 160, 158, 133, 153, 144]
index_right_eye = [362, 385, 387, 263, 373, 380]
EAR_THRESH = 0.28  # Cambiado de 0.26 a 0.20 para aumentar la sensibilidad.
NUM_FRAMES = 2  # Cambiado de 2 a 1 para contar un parpadeo más rápidamente.
aux_counter = 0
blink_counter = 0

with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1) as face_mesh:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)

        coordinates_left_eye = []
        coordinates_right_eye = []

        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                for index in index_left_eye:
                    x = int(face_landmarks.landmark[index].x * width)
                    y = int(face_landmarks.landmark[index].y * height)
                    coordinates_left_eye.append([x, y])
                    cv2.circle(frame, (x, y), 2, (255, 255, 0), 1)
                    cv2.circle(frame, (x, y), 1, (255, 255, 0), 1)  # 6 puntitos contorno ojo izquierdo
                for index in index_right_eye:
                    x = int(face_landmarks.landmark[index].x * width)
                    y = int(face_landmarks.landmark[index].y * height)
                    coordinates_right_eye.append([x, y])
                    cv2.circle(frame, (x, y), 2, (255, 255, 0), 1)  # 6 puntitos contorno ojo derecho
                    cv2.circle(frame, (x, y), 1, (255, 255, 0), 1)

            ear_left_eye = eye_aspect_ratio(coordinates_left_eye)
            ear_right_eye = eye_aspect_ratio(coordinates_right_eye)
            ear = (ear_left_eye + ear_right_eye) / 2

            # Ojos cerrados
            if ear < EAR_THRESH:
                aux_counter += 1
            else:
                if aux_counter >= NUM_FRAMES:
                    aux_counter = 0
                    blink_counter += 1                
            frame = drawing_output(frame, coordinates_left_eye, coordinates_right_eye, blink_counter, width, height)

        cv2.imshow("Frame", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # Presiona ESC para salir
            break

cap.release()
cv2.destroyAllWindows()
