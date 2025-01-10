import uuid
import os
import base64
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image as PILImage
from io import BytesIO
from pdf2image import convert_from_path
from .models import Image, PDF
from .serializers import ImageSerializer, PDFSerializer
from pypdf import PdfReader


class UploadView(APIView):
    def post(self, request):
        file_data = request.data.get('file')  # Expecting base64-encoded data

        if not file_data:
            return Response({'error': 'File is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode base64
            decoded_file = base64.b64decode(file_data.split(',')[1])

            # Generate a unique filename using UUID
            file_ext = file_data.split(';')[0].split('/')[-1]
            unique_filename = f"{uuid.uuid4()}.{file_ext}"

            # Determine file type and handle accordingly
            if file_ext in ['jpg', 'jpeg', 'png']:
                file_path = os.path.join('images', unique_filename)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)

                with open(full_path, 'wb') as f:
                    f.write(decoded_file)

                pil_image = PILImage.open(BytesIO(decoded_file))
                width, height = pil_image.size
                num_channels = len(pil_image.getbands())

                image = Image.objects.create(
                    location=file_path,
                    width=width,
                    height=height,
                    number_of_channels=num_channels
                )
                serializer = ImageSerializer(image)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif file_ext == 'pdf':
                file_path = os.path.join('pdfs', unique_filename)
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)

                with open(full_path, 'wb') as f:
                    f.write(decoded_file)

                # Use pypdf to read the PDF
                pdf_reader = PdfReader(BytesIO(decoded_file))
                num_pages = len(pdf_reader.pages)
                width, height = pdf_reader.pages[0].mediabox.width, pdf_reader.pages[0].mediabox.height

                pdf = PDF.objects.create(
                    location=file_path,
                    width=width,
                    height=height,
                    number_of_pages=num_pages
                )
                serializer = PDFSerializer(pdf)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response({'error': 'Unsupported file type.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ImageListView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
    

class ImageManageView(APIView):
    def get(self, request, id):
        try:
            image = Image.objects.get(id=id)
            serializer = ImageSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            # Retrieve the image object by ID
            image = Image.objects.get(id=id)

            # Get the full path of the image file
            image_path = os.path.join(settings.MEDIA_ROOT, image.location)

            # Delete the file from the filesystem if it exists
            if os.path.exists(image_path):
                os.remove(image_path)

            # Delete the image record from the database
            image.delete()

            # Return a success response
            return Response({'message': 'Image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Image.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PDFListView(APIView):
    def get(self, request):
        pdfs = PDF.objects.all()
        serializer = PDFSerializer(pdfs, many=True)
        return Response(serializer.data)
    

class PDFManageView(APIView):
    def get(self, request, id):
        try:
            pdf = PDF.objects.get(id=id)
            serializer = PDFSerializer(pdf)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            # Retrieve the PDF object by ID
            pdf = PDF.objects.get(id=id)

            # Get the full path of the PDF file
            pdf_path = os.path.join(settings.MEDIA_ROOT, pdf.location)
            
            # Delete the file from the filesystem if it exists
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

            # Delete the PDF record from the database
            pdf.delete()

            # Return a success response
            return Response({'message': 'PDF deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RotateImageView(APIView):
    def post(self, request):
        try:
            # Get image ID and rotation angle from the request
            image_id = request.data.get('image_id')
            angle = request.data.get('angle')

            if not image_id or not angle:
                return Response({'error': 'Image ID and angle are required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the image object
            image = Image.objects.get(id=image_id)
            image_path = os.path.join(settings.MEDIA_ROOT, image.location)

            # Open the image using PIL
            with PILImage.open(image_path) as img:
                # Rotate the image
                """
                    The reason for using the negative sign is due to how the rotate() method in the PIL (Pillow)
                    library interprets rotation angles:
                    How rotate() Works in PIL:
                    By default, positive angles in rotate() rotate the image counterclockwise.
                    Negative angles rotate the image clockwise.
                    However, in many real-world applications, users typically expect:
                    Positive angles to rotate the image clockwise.
                    Negative angles to rotate the image counterclockwise.
                    To align with common user expectations, we negate the angle:
                    A positive user input (e.g., 90) results in a 90° clockwise rotation.
                    A negative user input (e.g., -90) results in a 90° counterclockwise rotation.
                """
                rotated_img = img.rotate(-int(angle), expand=True)

                # Save the rotated image to memory
                img_io = BytesIO()
                rotated_img_format = img.format if img.format else 'JPEG'
                rotated_img.save(img_io, format=rotated_img_format)
                img_io.seek(0)

                # Prepare the rotated image as base64
                base64_image = base64.b64encode(img_io.read()).decode('utf-8')
                rotated_image_data = f"data:image/{rotated_img_format.lower()};base64,{base64_image}"

                return Response({'rotated_image': rotated_image_data}, status=status.HTTP_200_OK)

        except Image.DoesNotExist:
            return Response({'error': 'Image not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConvertPDFToImageView(APIView):
    def post(self, request):
        try:
            # Get the PDF ID from the request
            pdf_id = request.data.get('pdf_id')

            if not pdf_id:
                return Response({'error': 'PDF ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the PDF object
            pdf = PDF.objects.get(id=pdf_id)
            pdf_path = os.path.join(settings.MEDIA_ROOT, pdf.location)

            # Verify the PDF file exists
            if not os.path.exists(pdf_path):
                return Response({'error': 'PDF file not found on server.'}, status=status.HTTP_404_NOT_FOUND)

            # Convert all pages of the PDF to images
            images = convert_from_path(pdf_path)

            if not images:
                return Response({'error': 'No images could be generated from the PDF.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Combine all the images into a single image (stack them vertically)
            total_width = max(img.width for img in images)
            total_height = sum(img.height for img in images)

            # Create a new image large enough to hold all pages vertically
            combined_img = PILImage.new('RGB', (total_width, total_height))

            # Paste each image into the new combined image
            y_offset = 0
            for img in images:
                combined_img.paste(img, (0, y_offset))
                y_offset += img.height

            # Save the combined image to memory
            img_io = BytesIO()
            combined_img.save(img_io, format='JPEG')
            img_io.seek(0)

            # Convert the combined image to base64
            base64_image = base64.b64encode(img_io.read()).decode('utf-8')
            combined_image_data = f"data:image/jpeg;base64,{base64_image}"

            return Response({'combined_image': combined_image_data}, status=status.HTTP_200_OK)

        except PDF.DoesNotExist:
            return Response({'error': 'PDF not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
