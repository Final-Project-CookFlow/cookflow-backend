# users/management/commands/seed_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random # Import random for image selection
from media.models import Image # Import the Image model

class Command(BaseCommand):
    help = 'Seeds CustomUser data for the users app.'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')
        User = get_user_model()

        self.stdout.write('Seeding users...')

        # Fetch USER type images that were just seeded by seed_media
        user_profile_images = list(Image.objects.filter(type=Image.ImageType.USER))
        if not user_profile_images:
            self.stdout.write(self.style.WARNING('No USER images found. Users will be created without profile pictures. Ensure `python manage.py seed_media` is run before this command.'))

        # 1. Create a Superuser (if not exists)
        admin_user_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin', # Set the desired password for the admin user
            'name': 'Admin',
            'surname': 'User',
            'second_surname': 'Account',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
            'profile_picture': random.choice(user_profile_images) if user_profile_images else None # Assign random profile picture
        }
        
        try:
            admin_user, created = User.objects.get_or_create(
                username=admin_user_data['username'],
                defaults=admin_user_data
            )
            if created:
                admin_user.set_password(admin_user_data['password'])
                admin_user.save()
                self.stdout.write(self.style.SUCCESS(f'Created superuser: {admin_user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Superuser "{admin_user.username}" already exists. Updating its password and picture if changed.'))
                # Update password and picture if it already exists, to ensure it matches seeder intent
                admin_user.set_password(admin_user_data['password'])
                admin_user.profile_picture = admin_user_data['profile_picture']
                admin_user.save()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating/getting superuser "admin": {e}'))


        # 2. Create 10 regular users
        num_users_to_create = 10
        # Filter for non-staff, non-superuser count, to accurately track 'regular' users
        existing_regular_users_count = User.objects.filter(is_superuser=False, is_staff=False).count()

        if existing_regular_users_count >= num_users_to_create:
            self.stdout.write(self.style.WARNING(f'Already have {existing_regular_users_count} regular users. Skipping creation.'))
        else:
            for i in range(num_users_to_create - existing_regular_users_count):
                username = fake.user_name()
                # Ensure unique username
                counter = 0
                while User.objects.filter(username=username).exists():
                    username = f"{fake.user_name()}{counter}"
                    counter += 1

                email = fake.unique.email()
                name = fake.first_name()
                surname = fake.last_name()
                second_surname = fake.last_name() 
                biography = fake.paragraph(nb_sentences=1) if fake.boolean(chance_of_getting_true=70) else None
                
                # Assign a random profile picture
                profile_pic_instance = random.choice(user_profile_images) if user_profile_images else None

                User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123', # Example password for regular users
                    name=name,
                    surname=surname,
                    second_surname=second_surname,
                    biography=biography,
                    profile_picture=profile_pic_instance # Assign the Image object here
                )
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))

        self.stdout.write(self.style.SUCCESS('User seeding complete!'))