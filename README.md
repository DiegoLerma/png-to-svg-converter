
# 🖼️ JPEG to SVG Converter with Background Removal

Este proyecto es una herramienta simple pero poderosa para convertir imágenes en formato JPEG a SVG, eliminando primero el fondo de la imagen. Ideal para quienes necesitan vectorizar imágenes de forma automática mientras se deshacen de fondos innecesarios.

## 📋 Descripción

Este script procesa una imagen JPEG para:

1. Eliminar el fondo usando técnicas de segmentación.
2. Convertir la imagen resultante en un gráfico vectorial SVG.

La conversión a SVG se realiza utilizando la biblioteca `potrace`, que rastrea el bitmap resultante de la imagen con fondo eliminado.

## ⚙️ Funcionalidades

- **Eliminación de Fondo**: Usa técnicas de umbralización para eliminar el fondo de la imagen.
- **Conversión a SVG**: Vectoriza la imagen procesada y la guarda como un archivo SVG.

## 🛠️ Instalación

1. **Clona el repositorio**:

   ```bash
   git clone https://github.com/DiegoLerma/jpeg-to-svg-converter.git
   cd jpeg-to-svg-converter
   ```

2. **Instala las dependencias**:
   Asegúrate de tener Python 3.6+ y ejecuta el siguiente comando:

   ```bash
   pip install -r requirements.txt
   ```

   Asegúrate de que `requirements.txt` contiene:

   ```text
   opencv-python-headless
   numpy
   pillow
   potracer
   ```

## 🚀 Uso

1. **Coloca tu imagen JPEG** en la misma carpeta que el script y asegúrate de que el archivo se llama `image.jpeg` (o cambia el nombre en el código).

2. **Ejecuta el script**:

   ```bash
   python main.py
   ```

3. **Resultado**:

   El script generará un archivo `output.svg` en la misma carpeta, que será la versión vectorizada de tu imagen original sin el fondo.

## 🎨 Personalización

Si el resultado no es satisfactorio, puedes ajustar los siguientes parámetros:

- **Umbral para la eliminación del fondo**: En la función `remove_background`, ajusta el valor de `cv2.threshold` para mejorar la precisión de la eliminación del fondo.

  ```python
  _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
  ```

  Baja este valor para hacer que más áreas se consideren como primer plano.

- **Parámetros de vectorización**: Modifica los parámetros en la función `path = bitmap.trace(...)` para afinar la calidad del SVG.
  - `turdsize`: Filtra pequeños artefactos en la imagen.
  - `alphamax`: Controla la suavidad de las curvas.
  - `opttolerance`: Afecta la precisión de las curvas ajustadas.

## 👨‍💻 Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar este proyecto, no dudes en abrir un pull request o un issue.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 📝 Notas

- Este proyecto está diseñado para imágenes que tienen un fondo relativamente uniforme.
- Si trabajas con imágenes más complejas, podrías necesitar ajustar los parámetros o implementar técnicas de procesamiento más avanzadas.
