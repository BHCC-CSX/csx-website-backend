from rest_framework.parsers import FileUploadParser


class ImageParser(FileUploadParser):
    media_type = "image/*"
