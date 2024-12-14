import cv2
import numpy as np
import os
from datetime import datetime

def guardar_imagen(frame, carpeta='fotos'):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre_archivo = datetime.now().strftime("foto_%Y%m%d_%H%M%S.png")
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    cv2.imwrite(ruta_completa, frame)
    print(f"Imagen guardada en: {ruta_completa}")
    return ruta_completa

def aplicar_warp_perspective(ruta_imagen, carpeta='fotos_warp'):
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("Error al cargar la imagen.")
        return

    # Definir puntos de origen y destino
    alto, ancho = imagen.shape[:2]
    input_points = np.float32([
        [139, 82], [602, 20], [193, 460], [626, 444]
    ]) # Estas son las coordenadas de las esquinas en la imagen sin warp

    # Estos son los puntos de como quiero que se vea la imagen
    dst_pts = np.float32([
        [0, 0],
        [ancho, 0],
        [0, alto],
        [ancho, alto]
    ])

    print(str(ancho) + " " + str(alto)) 

    # Calcular la matriz de transformación
    M = cv2.getPerspectiveTransform(input_points, dst_pts)

    # Aplicar la transformación
    imagen_warp = cv2.warpPerspective(imagen, M, (ancho, alto))

    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre_archivo = os.path.splitext(os.path.basename(ruta_imagen))[0] + "_warp.png"
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    cv2.imwrite(ruta_completa, imagen_warp)
    print(f"Imagen warp guardada en: {ruta_completa}")

def main():
    cap = cv2.VideoCapture(1)  

    if not cap.isOpened():
        print("Error al abrir la cámara.")
        return

    ultima_imagen_guardada = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al leer el frame de la cámara.")
            break

        cv2.imshow('Video', frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord(' '):  # Barra espaciadora
            ruta = guardar_imagen(frame)
            ultima_imagen_guardada = ruta

        elif tecla == ord('w'):
            
            if ultima_imagen_guardada:
                aplicar_warp_perspective(ultima_imagen_guardada)
            else:
                print("No hay ninguna imagen guardada para aplicar warp perspective.")

        elif tecla == ord('q') or tecla == 27:  # 'q' o Esc para salir
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
