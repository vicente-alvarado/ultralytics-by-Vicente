import re
import ast
import cv2
import numpy as np
import requests

# Lee el archivo txt
url = 'https://dcdc-157-100-108-85.ngrok-free.app/'
image_public = "upload_image"
txt_public = "upload_json"
ruta_txt = "D:/yolov8/procesamiento/opencvdata/parameters1.txt"
ruta_image = "D:/yolov8/procesamiento/opencvdata/image1.jpg"

def procesamiento_files(url, image_public, txt_public, ruta_txt, ruta_image):
    with open(ruta_txt, 'r') as file:
        content = file.read()

    # Extrae los tensores utilizando expresiones regulares
    matches = re.findall(r'\[[^[]*?\]', content)

    # Inicializa una lista para almacenar los tensores
    tensores_lista = []

    # Procesa cada tensor y agrega a la lista
    for idx, match in enumerate(matches, start=1):
        try:
            tensor_values = ast.literal_eval(match)
            tensores_lista.append(tensor_values)
            print(f'Tensor {idx}: {tensor_values}')
        except Exception as e:
            print(f'Error al procesar Tensor {idx}: {e}')

    # Conteo
    # Guarda el conteo de las clases en un archivo de texto
    with open(ruta_txt, "w") as archivo_conteo:
        archivo_conteo.write(f"Glass: {len(tensores_lista)}\n")

    # Carga la imagen existente
    image_path = ruta_image # Reemplaza con la ruta de tu imagen
    image = cv2.imread(image_path)

    print(tensores_lista[0])
    if len(tensores_lista[0])==0:
        print(f'Advertencia: {tensores_lista[0]} tiene valores nulos. Se omitirá.')
        return
    # Dibuja rectángulos en la imagen basándote en los tensores
    for tensor in tensores_lista:
        x1, y1, x2, y2, confianza, _ = tensor
        
        color = (0, 0, 255)  # Color rojo
        thickness = 2
        image_rectangulo = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
        # Etiqueta con nombre de clase y confianza
        etiqueta = f"Glass: {confianza:.2f}"
        
        # Agrega la etiqueta encima del rectángulo
        image_final = cv2.putText(image_rectangulo, etiqueta, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    """ # Guarda la imagen resultante
    cv2.imwrite("image_resultante.jpg", image)

    # Enviar la imagen resultante y los resultados a la API en el servidor con IP pública
    files = {'image': open("image_resultante.jpg", 'rb')}
    response = requests.post(url + image_public, files=files)
    print(response.json()) """

    files = {'image': ('image_byte.jpg', cv2.imencode('.jpg', image)[1])}
    response = requests.post(url + image_public, files=files)

    # Enviar el txt y los resultados a la API en el servidor con IP pública
    files = {'txt': open(ruta_txt, 'rb')}
    response = requests.post(url + txt_public, files=files)

    """ # Muestra la imagen con los rectángulos
    cv2.imshow('Rectángulos', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() """