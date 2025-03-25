from django.urls import path
from .views import generate_image, list_generated_images, get_generated_image

urlpatterns = [
    path('generate/', generate_image, name='generate_image'),
    path('images/', list_generated_images, name='list_generated_images'),  # Now correctly refers to the function
    path('image/', get_generated_image, name='get_generated_image'),  # Updated to remove `<int:image_id>`
]
