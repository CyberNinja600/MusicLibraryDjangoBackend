from rest_framework.response import Response
from rest_framework import status
from .utils import validate_song, validate_image

class FileValidationMixin:
    def validate_files(self, song_data, image_data):
        validation_song = validate_song(song_data)
        validation_img = validate_image(image_data)
        return validation_song['status'] * validation_img['status'], validation_song, validation_img

    def failed_upload_response(self, error_message):
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
