from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from diffusers import StableDiffusionPipeline
from django.core.files.base import ContentFile
from .models import GeneratedImage
from .serializers import GeneratedImageSerializer
from io import BytesIO
import torch

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
    
    # Construct the full URL for the generated image
    image_url = f"{settings.MEDIA_URL}{generated_image.image.name}"
    
    # Return full URL
    return Response({"id": generated_image.id, "image_url": image_url}, status=201)

@api_view(['GET'])
def get_generated_image(request, image_id):
    try:
        image = GeneratedImage.objects.get(id=image_id)
        serializer = GeneratedImageSerializer(image)
        
        # Construct the full URL for the image
        image_url = f"{settings.MEDIA_URL}{image.image.name}"
        
        return Response({"id": image.id, "prompt": image.prompt, "image_url": image_url}, status=200)
    except GeneratedImage.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)

@api_view(['GET'])
def list_generated_images(request):
    images = GeneratedImage.objects.all()
    serializer = GeneratedImageSerializer(images, many=True)
    
    # Ensure the full URL is included in the response
    for image in serializer.data:
        image['image_url'] = f"{settings.MEDIA_URL}{image['image']}"
    
    return Response(serializer.data)
