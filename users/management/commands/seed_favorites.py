from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

from users.models import Favorite
from recipes.models import Recipe 

class Command(BaseCommand):
    help = 'Seeds Favorite data (User-Recipe relationships) for the users app.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        User = get_user_model()
        existing_favorites_tuples = set(Favorite.objects.values_list('user', 'recipe'))
        self.stdout.write('Seeding favorite recipes data...')

        # --- Ensure Dependencies Exist ---
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please run `python manage.py seed_users` first.'))
            return

        recipes = list(Recipe.objects.all())
        if not recipes:
            self.stdout.write(self.style.ERROR('No recipes found. Please run `python manage.py seed_recipes` first.'))
            return
        
        # --- Seed Favorites ---
        self.stdout.write('\nSeeding Favorites...')

        num_favorites_to_create = 40 # Create 40 favorite relationships
        
        # Optional: Clear existing favorites if you want fresh data every time
        # Favorite.objects.all().delete() 
        # self.stdout.write('Cleared existing Favorites.')

        # Use a set to prevent duplicate user-recipe favorites
        existing_favorites_tuples = set(Favorite.objects.values_list('user', 'recipe'))

        created_count = 0
        max_attempts = num_favorites_to_create * 3 # Attempt more times than target to find unique pairs

        for i in range(max_attempts):
            if created_count >= num_favorites_to_create:
                break # Stop if we've created enough

            random_user = random.choice(users)
            random_recipe = random.choice(recipes)
            
            # Check for existing favorite to prevent duplicates (user_id, recipe_id)
            if (random_user.id, random_recipe.id) in existing_favorites_tuples:
                continue # Skip if this favorite already exists

            try:
                Favorite.objects.create(
                    user=random_user,
                    recipe=random_recipe,
                )
                existing_favorites_tuples.add((random_user.id, random_recipe.id)) # Add to set
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created Favorite {created_count}/{num_favorites_to_create}: User {random_user.username} liked Recipe: {random_recipe.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create Favorite (attempt {i+1}): {e}'))
                # If you get frequent errors here, consider if your random choices exhaust unique pairs too quickly
                # or if there's an IntegrityError (e.g., database unique constraint on user-recipe that Django's .add() might enforce implicitly)

        self.stdout.write(self.style.SUCCESS('Favorite data seeding complete!'))