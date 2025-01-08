import pytest
from document.models import Image, PDF


@pytest.mark.django_db
def test_image_creation():
    image = Image.objects.create(
        location="first.png", width=191, height=172, number_of_channels=4)
    assert image.id is not None
    assert image.location == "first.png"
    assert image.width == 191
    assert image.height == 172
    assert image.number_of_channels == 4


@pytest.mark.django_db
def test_pdf_creation():
    pdf = PDF.objects.create(location="first.pdf",
                             width=595, height=842, number_of_pages=1)
    assert pdf.id is not None
    assert pdf.location == "first.pdf"
    assert pdf.width == 595
    assert pdf.height == 842
    assert pdf.number_of_pages == 1
