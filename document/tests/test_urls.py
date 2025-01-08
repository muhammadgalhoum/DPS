from django.urls import reverse, resolve
from document.views import *


def test_upload_url():
    path = reverse('upload')
    assert resolve(path).func.view_class == UploadView


def test_image_list_url():
    path = reverse('image-list')
    assert resolve(path).func.view_class == ImageListView


def test_image_manage_url():
    path = reverse('image-manage', args=[1])
    assert resolve(path).func.view_class == ImageManageView


def test_pdf_list_url():
    path = reverse('pdf-list')
    assert resolve(path).func.view_class == PDFListView


def test_pdf_manage_url():
    path = reverse('pdf-manage', args=[1])
    assert resolve(path).func.view_class == PDFManageView


def test_rotate_image_url():
    path = reverse('rotate-image')
    assert resolve(path).func.view_class == RotateImageView


def test_convert_pdf_to_image_url():
    path = reverse('convert-pdf-to-image')
    assert resolve(path).func.view_class == ConvertPDFToImageView
