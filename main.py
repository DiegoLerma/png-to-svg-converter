"""
JPEG to SVG Converter with Background Removal.

Este módulo proporciona una función para convertir archivos de imagen en formato JPEG
a SVG, eliminando primero el fondo de la imagen. El módulo maneja la lectura del 
archivo JPEG, la eliminación del fondo, la conversión a SVG y el guardado del resultado en una ubicación especificada.

Funciones:
- convert_jpeg_to_svg(input_file_path, output_file_path): Elimina el fondo de un JPEG y lo convierte a SVG.
- main(): Función principal que ejecuta un ejemplo de conversión.

Ejemplo de uso:
    python main.py
"""

import os
import cv2
import numpy as np
from PIL import Image
from potrace import Bitmap, POTRACE_TURNPOLICY_MINORITY


def remove_background(image):
    """
    Elimina el fondo de una imagen utilizando técnicas de segmentación.

    Args:
        image (numpy.ndarray): Imagen cargada como un array de Numpy.

    Returns:
        numpy.ndarray: Imagen con fondo eliminado.
    """
    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplica una máscara binaria (threshold)
    _, thresh = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)

    # Aplica la máscara de fondo
    image_no_bg = cv2.bitwise_and(image, image, mask=thresh)

    return image_no_bg


def convert_jpeg_to_svg(input_file_path, output_file_path):
    """
    Convierte un archivo JPEG a SVG, eliminando primero el fondo.

    Args:
        input_file_path (str): Ruta al archivo de imagen JPEG.
        output_file_path (str): Ruta donde se guardará el archivo SVG convertido.

    Raises:
        FileNotFoundError: Si el archivo JPEG no existe.
        ValueError: Si la conversión a SVG falla.
    """
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"El archivo {input_file_path} no existe.")

    image = cv2.imread(input_file_path)

    if image is None:
        raise ValueError(f"No se pudo cargar la imagen {input_file_path}. Asegúrate de que sea un archivo JPEG válido.")

    image_no_bg = remove_background(image)

    temp_png_path = 'temp_no_bg.png'
    cv2.imwrite(temp_png_path, image_no_bg)

    try:
        pil_image = Image.open(temp_png_path).convert('L')
        bw = pil_image.point(lambda x: 0 if x < 128 else 255, '1')

        bitmap = Bitmap(np.array(bw))
        path = bitmap.trace(turdsize=1, turnpolicy=POTRACE_TURNPOLICY_MINORITY, alphamax=1, opticurve=False, opttolerance=0.2)

        with open(output_file_path, 'w', encoding='utf8') as svg_file:
            svg_file.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{pil_image.width}" height="{pil_image.height}">\n')
            for curve in path:
                parts = [f"M{curve.start_point.x},{curve.start_point.y}"]
                for segment in curve.segments:
                    if segment.is_corner:
                        parts.append(
                            f"L{segment.c.x},{segment.c.y}L{segment.end_point.x},{segment.end_point.y}")
                    else:
                        parts.append(
                            f"C{segment.c1.x},{segment.c1.y} {segment.c2.x},{segment.c2.y} {segment.end_point.x},{segment.end_point.y}")
                parts.append("z")
                svg_file.write(f'<path d="{" ".join(parts)}" fill="black"/>\n')
            svg_file.write('</svg>\n')

        print(f"Conversión completada: {output_file_path}")

    except Exception as e:
        raise ValueError(
            f"Error al convertir {input_file_path} a SVG: {e}. Asegúrate de que el archivo JPEG esté bien formado y sea compatible."
            ) from e


def main():
    input_file = 'image.jpeg'
    output_file = 'output.svg'

    try:
        convert_jpeg_to_svg(input_file, output_file)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
