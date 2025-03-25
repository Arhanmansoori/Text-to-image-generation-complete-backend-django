import torch
from rest_framework.response import Response
from rest_framework.decorators import api_view
from diffusers import StableDiffusionPipeline
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .models import GeneratedImage
from .serializers import GeneratedImageSerializer
from io import BytesIO

# Load model globally
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

IMAGE_PATH = "generated_images/generated_ai_image.png"

@api_view(['POST'])
def generate_image(request):
    prompt = request.data.get("prompt", "")
    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)
    
    image = pipe(prompt).images[0]
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_file = ContentFile(buffer.getvalue(), name="generated_ai_image.png")
    
    # Delete previous image if it exists
    if default_storage.exists(IMAGE_PATH):
        default_storage.delete(IMAGE_PATH)
    
    # Save new image
    saved_path = default_storage.save(IMAGE_PATH, image_file)
    
    # Update or create the single database entry
    generated_image, created = GeneratedImage.objects.update_or_create(
        id=1,
        defaults={"prompt": prompt, "image": saved_path}
    )
    serializer = GeneratedImageSerializer(generated_image)
    
    return Response({"id": generated_image.id, "image_url": generated_image.image.url}, status=201)

@api_view(['GET'])
def get_generated_image(request):
    try:
        image = GeneratedImage.objects.get(id=1)
        serializer = GeneratedImageSerializer(image)
        return Response(serializer.data)
    except GeneratedImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)

@api_view(['GET'])
def list_generated_images(request):
    try:
        image = GeneratedImage.objects.get(id=1)
        serializer = GeneratedImageSerializer(image)
        return Response([serializer.data])  # Return as a list to match the expected response format
    except GeneratedImage.DoesNotExist:
        return Response([], status=200)  # Return an empty list if no image is found
