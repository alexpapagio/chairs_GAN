# from PIL import Image
# import base64
# from io import BytesIO

# def get_image_base64(image: Image.Image):
#     """Convert PIL Image to base64 string."""
#     buffer = BytesIO()
#     image.save(buffer, format="PNG")
#     return base64.b64encode(buffer.getvalue()).decode()
