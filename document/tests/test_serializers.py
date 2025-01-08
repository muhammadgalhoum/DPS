from document.serializers import ImageSerializer, PDFSerializer


def test_image_serializer():
    data = {
        "location": "first.png",
        "width": 191,
        "height": 172,
        "number_of_channels": 4
    }
    serializer = ImageSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["location"] == "first.png"


def test_pdf_serializer():
    data = {
        "location": "first.pdf",
        "width": 595,
        "height": 842,
        "number_of_pages": 1
    }
    serializer = PDFSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data["location"] == "first.pdf"
