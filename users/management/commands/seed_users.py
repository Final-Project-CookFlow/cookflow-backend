# users/management/commands/seed_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds CustomUser data for the users app.'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES') # Use Spanish locale for more realistic names/surnames

        User = get_user_model()

        self.stdout.write('Seeding users...')

        # 1. Create a Superuser (if not exists)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin', # Use a strong password in production!
                name='Admin',
                surname='User',
                second_surname='Account'
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists.'))

        # 2. Create 10 regular users
        num_users_to_create = 10
        existing_users_count = User.objects.filter(is_superuser=False, is_staff=False).count()

        if existing_users_count >= num_users_to_create:
            self.stdout.write(self.style.WARNING(f'Already have {existing_users_count} regular users. Skipping creation.'))
        else:
            for i in range(num_users_to_create - existing_users_count):
                username = fake.user_name()
                # Ensure unique username by appending a number if necessary
                counter = 0
                while User.objects.filter(username=username).exists():
                    username = f"{fake.user_name()}{counter}"
                    counter += 1

                email = fake.unique.email()
                name = fake.first_name()
                surname = fake.last_name()
                second_surname = fake.last_name() # Assuming second_surname is also a last name
                biography = fake.paragraph(nb_sentences=1) if fake.boolean(chance_of_getting_true=70) else None

                User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123', # Example password
                    name=name,
                    surname=surname,
                    second_surname=second_surname,
                    biography=biography
                )
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))

        self.stdout.write(self.style.SUCCESS('User seeding complete!'))