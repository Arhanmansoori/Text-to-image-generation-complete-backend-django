# views.py
import torch
from rest_framework.response import Response
from rest_framework.decorators import api_view
from diffusers import StableDiffusionPipeline
from django.core.files.base import ContentFile
from .models import GeneratedImage
from .serializers import GeneratedImageSerializer
from io import BytesIO

# Load model globally
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to(device)

@api_view(['POST'])
def generate_image(request):
    prompt = request.data.get("prompt", "")
    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)
    
    image = pipe(prompt).images[0]
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    image_file = ContentFile(buffer.getvalue(), name=f"generated_{torch.randint(1000,9999, (1,)).item()}.png")
    
    generated_image = GeneratedImage.objects.create(prompt=prompt, image=image_file)
    serializer = GeneratedImageSerializer(generated_image)
    return Response({"id": generated_image.id, "image_url": generated_image.image.url}, status=201)

@api_view(['GET'])
def get_generated_image(request, image_id):
    try:
        image = GeneratedImage.objects.get(id=image_id)
        serializer = GeneratedImageSerializer(image)
        return Response(serializer.data)
    except GeneratedImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)

@api_view(['GET'])
def list_generated_images(request):
    images = GeneratedImage.objects.all()
    serializer = GeneratedImageSerializer(images, many=True)
    return Response(serializer.data)