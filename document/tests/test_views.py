import pytest
from django.urls import reverse
from rest_framework import status
from ..models import Image
from PIL import Image as PILImage
import base64
from io import BytesIO
from reportlab.pdfgen import canvas



@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def create_test_image():
    image = PILImage.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    base64_image = base64.b64encode(img_io.read()).decode('utf-8')
    return {
        'file': f"data:image/jpeg;base64,{base64_image}",
        'width': 100,
        'height': 100,
        'number_of_channels': 3
    }


@pytest.fixture
def create_test_pdf():
    # Create a PDF in memory using ReportLab
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 750, "Test PDF Content")
    c.showPage()
    c.save()

    # Get the PDF data from the buffer and encode it in base64
    pdf_content = pdf_buffer.getvalue()
    base64_pdf = base64.b64encode(pdf_content).decode('utf-8')

    return {
        'file': f"data:application/pdf;base64,{base64_pdf}",
        'width': 500,
        'height': 700,
        'number_of_pages': 1
    }


@pytest.mark.django_db
def test_upload_image(api_client, create_test_image):
    url = reverse('upload')
    response = api_client.post(
        url, {'file': create_test_image['file']}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'width' in response.data
    assert 'height' in response.data


@pytest.mark.django_db
def test_upload_pdf(api_client, create_test_pdf):
    url = reverse('upload')
    response = api_client.post(
        url, {'file': create_test_pdf['file']}, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'width' in response.data
    assert 'height' in response.data
    assert 'number_of_pages' in response.data


@pytest.mark.django_db
def test_get_images(api_client):
    url = reverse('image-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_get_image_detail(api_client, create_test_image):
    image = Image.objects.create(
        location='test_image.jpg',
        width=create_test_image['width'],
        height=create_test_image['height'],
        number_of_channels=create_test_image['number_of_channels']
    )
    url = reverse('image-manage', args=[image.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == image.id


@pytest.mark.django_db
def test_delete_image(api_client, create_test_image):
    image = Image.objects.create(
        location='test_image.jpg',
        width=create_test_image['width'],
        height=create_test_image['height'],
        number_of_channels=create_test_image['number_of_channels']
    )
    url = reverse('image-manage', args=[image.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Image.objects.filter(id=image.id).exists()


@pytest.mark.django_db
def test_rotate_image(api_client, create_test_image):
    # First, upload the image using the upload API
    url = reverse('upload')
    response = api_client.post(
        url, {'file': create_test_image['file']}, format='json')

    # Ensure the upload was successful and retrieve the image ID from the response
    assert response.status_code == status.HTTP_201_CREATED
    image_id = response.data['id']  # Assuming the upload returns an 'id' field

    # Now, rotate the uploaded image
    rotate_url = reverse('rotate-image')
    response = api_client.post(
        rotate_url, {'image_id': image_id, 'angle': 90}, format='json')

    # Assert that the rotation was successful
    assert response.status_code == status.HTTP_200_OK
    assert 'rotated_image' in response.data


@pytest.mark.django_db
def test_convert_pdf_to_image(api_client, create_test_pdf):
    # Upload the PDF using the api_client
    url = reverse('upload')
    response = api_client.post(
        url, {'file': create_test_pdf['file']}, format='json')

    # Ensure the upload was successful and retrieve the PDF ID from the response
    assert response.status_code == status.HTTP_201_CREATED
    pdf_id = response.data['id']  # Assuming the upload returns an 'id' field

    # Use the convert-pdf-to-image API to process the uploaded PDF
    url = reverse('convert-pdf-to-image')
    response = api_client.post(url, {'pdf_id': pdf_id}, format='json')

    # Assert the conversion was successful
    assert response.status_code == status.HTTP_200_OK
    assert 'combined_image' in response.data
