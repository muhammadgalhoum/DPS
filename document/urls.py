from django.urls import path
from .views import *

urlpatterns = [
    path('api/upload/', UploadView.as_view(), name="upload"),
    path('api/images/', ImageListView.as_view(), name="image-list"),
    path('api/images/<int:id>/', ImageManageView.as_view(), name="image-manage"),
    path('api/pdfs/', PDFListView.as_view(), name="pdf-list"),
    path('api/pdfs/<int:id>/', PDFManageView.as_view(), name="pdf-manage"),
    path('api/rotate/', RotateImageView.as_view(), name="rotate-image"),
    path('api/convert-pdf-to-image/', ConvertPDFToImageView.as_view(),
        name="convert-pdf-to-image"),
]
