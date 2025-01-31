# OCR-RETO

## Descripción
Este proyecto realiza OCR en archivos PDF con imágenes escaneadas para extraer información especifica y guardarla en .
carpetas especificas de google drive.

## Flujo de procesamiento
1. **Carga del archivo**: El usuario sube un PDF con imágenes escaneadas.
2. **Conversión de PDF a imágenes**: Se extraen las páginas y se convierten a imágenes.
3. **Extracción de texto con OCR**: Se usa Google Cloud Vision API para detectar texto en las imágenes.
4. **Procesamiento de texto**: Se filtran y estructuran los datos extraídos.
5. **Generación de documentos**: Se copia un machote de Google Docs y se reemplazan los valores con los datos extraídos.
6. **Almacenamiento en Google Drive**: Se guarda el documento generado en la carpeta de destino.

## Endpoints principales

### `ExtractFieldsByPageAPIView`
- **Función**: Extrae los datos relevantes de un PDF utilizando OCR.
- **Procesos clave**:
  - Convierte PDF en imágenes.
  - Extrae texto de cada imagen con Google Vision API.
  - Usa expresiones regulares para obtener información específica.

### `UPLOADTODRIVE`
- **Función**: Genera documentos en Google Drive con los datos extraídos.
- **Procesos clave**:
  - Copia un machote de documento en Google Drive.
  - Reemplaza los valores en el documento con la información obtenida.
  - Guarda el documento en la carpeta de destino.

## Link del proyecto
[OCR_FRONTEND](https://ocr-reto-front.onrender.com/)

## Contacto
- **Correo**: ruiz96199@gmail.com o lsegura@fwd.com


