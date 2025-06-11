# media/management/commands/seed_media.py

from django.core.management.base import BaseCommand
from faker import Faker
import random
from media.models import Image

class Command(BaseCommand):
    help = 'Seeds Image data for the media app with placeholder URLs.'

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write('Seeding Image data...')

        image_types = [choice[0] for choice in Image.ImageType.choices] # Get all ImageType choices
        
        num_images_to_create = 60 # You might want more images if you have many recipes/users/steps

        for i in range(num_images_to_create):
            image_type = random.choice(image_types)
            
            # Generate appropriate placeholder URLs based on type
            if image_type == Image.ImageType.RECIPE:
                image_url = f"https://placehold.co/600x400/FF5733/FFFFFF?text=Recipe+{i+1}"
            elif image_type == Image.ImageType.USER:
                image_url = f"https://placehold.co/150x150/33A3FF/FFFFFF?text=User+{i+1}"
            elif image_type == Image.ImageType.STEP:
                image_url = f"https://placehold.co/400x300/33FF57/FFFFFF?text=Step+{i+1}"
            else:
                image_url = fake.image_url() # Fallback for other types

            try:
                Image.objects.create(
                    name=f"{image_type.lower()}_image_{i+1}",
                    type=image_type,
                    url=image_url, # This is the URL string
                    processing_status=Image.ImageStatus.COMPLETED, # Set as completed since it's a URL
                    external_id=None # No external ID needed for placeholders
                )
                self.stdout.write(self.style.SUCCESS(f'Created Image: {image_type} - {image_url}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create Image {i+1}/{num_images_to_create}: {e}'))

        self.stdout.write(self.style.SUCCESS('Media app data seeding complete!'))