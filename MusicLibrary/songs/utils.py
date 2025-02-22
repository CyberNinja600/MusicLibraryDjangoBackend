from PIL import Image
from io import BytesIO
import magic
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import ObjectDoesNotExist
import jwt

def validate_song(audio_file):
    if not audio_file:
        return {"status": False, "error": "No file uploaded."}
    audio_file.seek(0)
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(audio_file.read())
    valid_mime_types = ['audio/mpeg', 'audio/wav', 'audio/x-wav', 'audio/mp4', 'audio/x-aac', 'audio/aac', 'audio/ogg', 'audio/webm']
    if mime_type not in valid_mime_types:
        return {"status": False, "error": "Invalid file type. Please upload an audio file.", "file_type": mime_type, "valid_types": valid_mime_types}
    return {"status": True}

def validate_image(image_data, allowed_formats=['JPG','JPEG','PNG'], max_size_mb=5, min_dimensions=(100, 100)):
    try:
        image_data.seek(0)
        image_bytes = image_data.read()
        with Image.open(BytesIO(image_bytes)) as img:
            if img.format not in allowed_formats:
                return {'status': False, 'error': f"Invalid format: {img.format}. Allowed formats: {allowed_formats}"}
            file_size = len(image_bytes)
            if file_size > max_size_mb * 1024 * 1024:
                return {'status': False, 'error': f"File size exceeds {max_size_mb} MB limit."}
            width, height = img.size
            if width < min_dimensions[0] or height < min_dimensions[1]:
                return {'status': False, 'error': f"Image dimensions too small: {width}x{height}. Minimum dimensions: {min_dimensions[0]}x{min_dimensions[1]}"}
            return {'status': True}
    except Exception as e:
        return {'status': False, 'error': "Error validating image: " + str(e)}

def get_user_from_token(request):
    # token = request.COOKIES.get('jwt')
    token = request.headers.get('Authorization')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return payload['id']
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    except ObjectDoesNotExist:
        raise AuthenticationFailed('User not found')
