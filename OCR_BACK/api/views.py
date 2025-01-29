import os
import re
from tempfile import NamedTemporaryFile

import cv2
import easyocr
from dotenv import load_dotenv
from google.cloud import vision
from google.oauth2 import service_account
from google_auth import project_root as here
from google_auth import read_credentials
from googleapiclient.discovery import build
from pdf2image import convert_from_path
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ArchivoSerializer

# Create your views here.
read_credentials()


@api_view(["GET"])
def hola_mundo(request):
    return Response({"mensaje": "hola mundo!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def procesar_archivo(request):
    serializer = ArchivoSerializer(data=request.data)

    if serializer.is_valid():
        return Response({"mensaje": "El archivo es valido"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UPLOADTODRIVE(APIView):
    SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive"]
    creds_path = here / os.getenv("GOOGLE_CREDENTIALS_FILE")
    creds_init = service_account.Credentials.from_service_account_file(creds_path)

    def copiar_machote(self, machote_id, carpeta_destino_id, nuevo_nombre):
        drive_service = build("drive", "v3", credentials=self.creds_init)

        copia_metadata = {
            "name": nuevo_nombre,
            "parents": [carpeta_destino_id],  # Especifica la carpeta de destino
        }
        copied_file = (
            drive_service.files().copy(fileId=machote_id, body=copia_metadata).execute()
        )
        return copied_file["id"]

    def replace_text(self, document_id, replacements):
        requests = []
        docs_service = build("docs", "v1", credentials=self.creds_init)
        for old_text, new_text in replacements.items():
            requests.append(
                {
                    "replaceAllText": {
                        "containsText": {"text": old_text, "matchCase": True},
                        "replaceText": new_text,
                    }
                }
            )
        docs_service.documents().batchUpdate(
            documentId=document_id, body={"requests": requests}
        ).execute()

    def post(self, request, *args, **kwargs):
        load_dotenv()
        paginas: list = request.data["paginas"]
        carpeta_destino_id = os.getenv("GOOGLE_CARPETA_DESTINO_ID")
        machote_id = os.getenv("GOOGLE_MACHOTE_ID")

        for n in paginas:
            nuevo_nombre = f"N° {n['fields']['solicitado_por']['numero']}"
            copia_id = self.copiar_machote(
                machote_id=machote_id,
                nuevo_nombre=nuevo_nombre,
                carpeta_destino_id=carpeta_destino_id,
            )
            remplazo = {
                "{{numero}}": f"N° {n['fields']['solicitado_por']['numero']}",
                "{{solicitado_por}}": "Solicitado por:",
                "{{solicitado_por_nombre}}": n["fields"]["solicitado_por"]["nombre"],
                "{{solicitado_por_telefono}}": n["fields"]["solicitado_por"][
                    "telefono"
                ],
                "{{solicitado_por_correo}}": n["fields"]["solicitado_por"]["correo"],
                "{{entregar_a}}": "Entregar a:",
                "{{entregar_a_nombre}}": n["fields"]["entregar_a"]["nombre"],
                "{{entregar_a_telefono}}": n["fields"]["entregar_a"]["telefono"],
                "{{entregar_a_direccion}}": n["fields"]["entregar_a"]["direccion"],
                "{{entregar_a_notas}}": n["fields"]["entregar_a"]["notas"],
                "{{entregar_a_correo}}": n["fields"]["entregar_a"]["correo"],
            }

            self.replace_text(copia_id, remplazo)

        return Response(
            {"mensaje": "exito", "paginas": paginas}, status=status.HTTP_200_OK
        )


class OCRAPIView(APIView):
    parser_classes = [MultiPartParser]

    def preprocess_image(self, image_path):
        """
        Preprocesar la imagen usando OpenCV.
        """
        # Leer la imagen
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # Escalar la imagen
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Binarizar (umbral)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Eliminar ruido
        denoised = cv2.GaussianBlur(binary, (5, 5), 0)

        return denoised

    def handle_pdf(self, pdf_file):
        """
        Convertir un archivo PDF a imágenes usando pdf2image.
        """
        images = convert_from_path(pdf_file.name, dpi=300)
        temp_images = []
        for i, page in enumerate(images):
            temp_path = f"temp_page_{i}.jpg"
            page.save(temp_path, "JPEG")
            temp_images.append(temp_path)
        return temp_images

    def save_uploaded_file(self, file):
        """
        Guardar temporalmente un archivo subido para procesarlo.
        """
        temp_file = NamedTemporaryFile(delete=False)
        for chunk in file.chunks():
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name

    def post(self, request, *args, **kwargs):
        file = request.data.get("file", None)
        if not file:
            return Response({"error": "No file provided"}, status=400)

        # Guardar archivo subido temporalmente
        file_path = self.save_uploaded_file(file)

        temp_images = []
        if file.name.endswith(".pdf"):
            # Convertir PDF a imágenes
            temp_images = self.handle_pdf(open(file_path, "rb"))
        else:
            temp_images = [file_path]

        # Instanciar el lector de EasyOCR
        reader = easyocr.Reader(["en", "es"])

        # Resultado acumulado
        full_text = []

        for temp_image_path in temp_images:
            # Preprocesar la imagen
            preprocessed_image = self.preprocess_image(temp_image_path)

            # Aplicar OCR
            result = reader.readtext(
                preprocessed_image, detail=0
            )  # detail=0 solo devuelve texto

            # Agregar el resultado
            full_text.extend(result)

            # Eliminar imágenes temporales
            try:
                os.remove(temp_image_path)
            except Exception as e:
                print(f"Error deleting temp image: {e}")

        # Eliminar archivo original
        os.remove(file_path)

        return Response({"text": "\n".join(full_text)})


class GoogleVisionOCRAPIView(APIView):
    parser_classes = [MultiPartParser]

    def save_uploaded_file(self, file):
        """
        Guardar un archivo subido temporalmente.
        """
        temp_file = NamedTemporaryFile(delete=False)
        for chunk in file.chunks():
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name

    def handle_pdf(self, pdf_file):
        """
        Convertir un PDF a imágenes usando pdf2image.
        """
        images = convert_from_path(pdf_file, dpi=300)
        temp_images = []
        for i, page in enumerate(images):
            temp_path = f"temp_page_{i}.jpg"
            page.save(temp_path, "JPEG")
            temp_images.append(temp_path)
        return temp_images

    def process_image_with_google_vision(self, image_path):
        """
        Usar Google Cloud Vision API para procesar una imagen.
        """
        load_dotenv()

        creds_path = here / os.getenv("GOOGLE_CREDENTIALS_FILE")
        creds_init = service_account.Credentials.from_service_account_file(creds_path)
        client = vision.ImageAnnotatorClient(credentials=creds_init)
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        # Crear un objeto de imagen para la API
        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        # Extraer el texto detectado
        texts = response.text_annotations
        if texts:
            return texts[0].description  # Devuelve el texto principal
        return ""

    def post(self, request, *args, **kwargs):
        """
        Procesar un archivo PDF o imagen y devolver el texto extraído.
        """
        file = request.data.get("file", None)
        if not file:
            return Response({"error": "No file provided"}, status=400)

        # Guardar archivo temporalmente
        file_path = self.save_uploaded_file(file)

        temp_images = []
        if file.name.endswith(".pdf"):
            # Convertir PDF a imágenes
            temp_images = self.handle_pdf(file_path)
        else:
            temp_images = [file_path]

        # Resultado acumulado
        full_text = []
        for temp_image_path in temp_images:
            # Usar Google Vision para procesar la imagen
            text = self.process_image_with_google_vision(temp_image_path)
            full_text.append(text)

            # Eliminar imágenes temporales
            try:
                os.remove(temp_image_path)
            except Exception as e:
                print(f"Error deleting temp image: {e}")

        # Eliminar archivo temporal original
        os.remove(file_path)

        return Response({"text": "\n".join(full_text)})


class GoogleVisionOCRAPIViewPaginacion(APIView):
    parser_classes = [MultiPartParser]

    def save_uploaded_file(self, file):
        """
        Guardar un archivo subido temporalmente.
        """
        temp_file = NamedTemporaryFile(delete=False)
        for chunk in file.chunks():
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name

    def handle_pdf(self, pdf_file):
        """
        Convertir un PDF a imágenes usando pdf2image.
        """
        images = convert_from_path(pdf_file, dpi=300)
        temp_images = []
        for i, page in enumerate(images):
            temp_path = f"temp_page_{i}.jpg"
            page.save(temp_path, "JPEG")
            temp_images.append(temp_path)
        return temp_images

    def process_image_with_google_vision(self, image_path):
        """
        Usar Google Cloud Vision API para procesar una imagen.
        """
        load_dotenv()
        creds_path = here / os.getenv("GOOGLE_CREDENTIALS_FILE")
        creds_init = service_account.Credentials.from_service_account_file(creds_path)
        client = vision.ImageAnnotatorClient(credentials=creds_init)
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        # Crear un objeto de imagen para la API
        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        # Extraer el texto detectado
        texts = response.text_annotations
        if texts:
            return texts[0].description  # Devuelve el texto principal
        return ""

    def post(self, request, *args, **kwargs):
        """
        Procesar un archivo PDF o imagen y devolver el texto extraído dividido por página.
        """
        file = request.data.get("file", None)
        if not file:
            return Response({"error": "No file provided"}, status=400)

        # Guardar archivo temporalmente
        file_path = self.save_uploaded_file(file)

        temp_images = []
        if file.name.endswith(".pdf"):
            # Convertir PDF a imágenes
            temp_images = self.handle_pdf(file_path)
        else:
            temp_images = [file_path]

        # Procesar cada imagen y guardar resultados por página
        page_texts = {}
        for i, temp_image_path in enumerate(temp_images):
            # Usar Google Vision para procesar la imagen
            text = self.process_image_with_google_vision(temp_image_path)
            page_texts[f"page_{i + 1}"] = text

            # Eliminar imágenes temporales
            try:
                os.remove(temp_image_path)
            except Exception as e:
                print(f"Error deleting temp image: {e}")

        # Eliminar archivo temporal original
        os.remove(file_path)

        return Response({"pages": page_texts})


class ExtractFieldsByPageAPIView(APIView):
    parser_classes = [MultiPartParser]

    def save_uploaded_file(self, file):
        """
        Guardar un archivo subido temporalmente.
        """
        temp_file = NamedTemporaryFile(delete=False)
        for chunk in file.chunks():
            temp_file.write(chunk)
        temp_file.close()
        return temp_file.name

    def handle_pdf(self, pdf_file):
        """
        Convertir un PDF a imágenes usando pdf2image.
        """
        images = convert_from_path(pdf_file, dpi=300)
        temp_images = []
        for i, page in enumerate(images):
            temp_path = f"temp_page_{i}.jpg"
            page.save(temp_path, "JPEG")
            temp_images.append(temp_path)
        return temp_images

    def extract_text_from_image(self, image_path):
        """
        Usar Google Cloud Vision API para extraer texto de una imagen.
        """
        creds_path = here / os.getenv("GOOGLE_CREDENTIALS_FILE")
        creds_init = service_account.Credentials.from_service_account_file(creds_path)
        client = vision.ImageAnnotatorClient(credentials=creds_init)
        with open(image_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client.text_detection(image=image)

        if response.error.message:
            raise Exception(f"Vision API Error: {response.error.message}")

        return (
            response.text_annotations[0].description
            if response.text_annotations
            else ""
        )

    def extract_fields(self, text):
        """
        Extract fields specifically from 'Solicitado por' and 'Entregar a' sections in the text.
        """
        result = {"solicitado_por": {}, "entregar_a": {}}

        # Extract "Solicitado por" section

        # Numero de solicitud
        result["solicitado_por"]["numero"] = re.search(
            r"N[°oº'`]?[\s]*([\d]+)", text, re.IGNORECASE
        )

        solicitado_match = re.search(
            r"Solicitado por[:\s]*(.*?)\nEntregar a", text, re.IGNORECASE | re.DOTALL
        )
        if solicitado_match:
            solicitado_text = solicitado_match.group(1)

            result["solicitado_por"]["nombre"] = re.search(
                r"Nombre[:\s]*((?!\nTeléfono|telefono|Dirección|direccion)([\w\sáéíóúÁÉÍÓÚñÑ,./-]+))+",
                solicitado_text,
                re.IGNORECASE | re.DOTALL,
            )
            result["solicitado_por"]["telefono"] = re.search(
                r"Tel[eé]fono[:\s]*([\d\s()\-]+)", solicitado_text, re.IGNORECASE
            )
            result["solicitado_por"]["correo"] = re.search(
                r"Correo[:\s]*([\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,})",
                solicitado_text,
                re.IGNORECASE,
            )

        # Extract "Entregar a" section
        entregar_match = re.search(
            r"Entregar a[:\s]*(.*?)(?:Frágil|$)", text, re.IGNORECASE | re.DOTALL
        )
        if entregar_match:
            entregar_text = entregar_match.group(1)
            result["entregar_a"]["nombre"] = re.search(
                r"Nombre[:\s]*((?!\nTeléfono|telefono|Dirección|direccion)([\w\sáéíóúÁÉÍÓÚñÑ,./-]+))+",
                entregar_text,
                re.IGNORECASE | re.DOTALL,
            )
            result["entregar_a"]["telefono"] = re.search(
                r"Tel[eé]fono[:\s]*([\d\s()\-]+)", entregar_text, re.IGNORECASE
            )
            result["entregar_a"]["direccion"] = re.search(
                r"Dirección[:\s]*(.+?)(?:Notas|$)",
                entregar_text,
                re.IGNORECASE | re.DOTALL,
            )
            result["entregar_a"]["correo"] = re.search(
                r"Correo[:\s]*([\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,})",
                solicitado_text,
                re.IGNORECASE,
            )
            result["entregar_a"]["notas"] = re.search(
                r"Notas[:\s]*(.+)", entregar_text, re.IGNORECASE | re.DOTALL
            )

        # Clean up the extracted data
        for section, fields in result.items():
            for key, match in fields.items():
                fields[key] = match.group(1).strip() if match else None

        return result

    def post(self, request, *args, **kwargs):
        """
        Procesar un archivo PDF o imagen y extraer valores específicos por página.
        """
        file = request.data.get("file", None)
        if not file:
            return Response({"error": "No file provided"}, status=400)

        file_path = self.save_uploaded_file(file)

        temp_images = []
        if file.name.endswith(".pdf"):
            temp_images = self.handle_pdf(file_path)
        else:
            temp_images = [file_path]

        all_data = []
        for page_number, temp_image_path in enumerate(temp_images):
            try:
                text = self.extract_text_from_image(temp_image_path)
                extracted_fields = self.extract_fields(text)
                all_data.append({"page": page_number + 1, "fields": extracted_fields})
            finally:
                os.remove(temp_image_path)

        os.remove(file_path)

        return Response({"data": all_data})
