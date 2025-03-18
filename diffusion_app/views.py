import torch
import base64
from io import BytesIO
from rest_framework.response import Response
from rest_framework.decorators import api_view
from diffusers import StableDiffusionPipeline
from django.core.files.base import ContentFile

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
    
    # Generate the image using the pipeline
    image = pipe(prompt).images[0]
    
    # Save image to a buffer
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    
    # Convert the image to a base64 encoded string
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    # Generate a unique image filename (optional)
    image_filename = f"generated_{torch.randint(1000, 9999, (1,)).item()}.png"
    
    # You can optionally store the image in your database if required:
    # image_file = ContentFile(buffer.getvalue(), name=image_filename)
    # generated_image = GeneratedImage.objects.create(prompt=prompt, image=image_file)
    # serializer = GeneratedImageSerializer(generated_image)
    
    # Return the image as base64 string in the response
    return Response({
        "prompt": prompt,
        "image_data": img_str,  # This is the base64 encoded image string
        "image_filename": image_filename  # Filename if you want to use it for saving the image
    }, status=201)
