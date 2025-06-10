from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

# Adjust imports based on your exact app structure
from shopping.models import ShoppingListItem
from recipes.models import Ingredient
from measurements.models import Unit

class Command(BaseCommand):
    help = 'Seeds ShoppingListItem data for the shopping app.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        User = get_user_model()

        self.stdout.write('Seeding shopping list data...')

        # --- Ensure Dependencies Exist ---
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please run `python manage.py seed_users` first.'))
            return

        ingredients = list(Ingredient.objects.all())
        if not ingredients:
            self.stdout.write(self.style.ERROR('No ingredients found. Please run `python manage.py seed_recipes` first.'))
            return

        units = list(Unit.objects.all())
        if not units:
            self.stdout.write(self.style.ERROR('No units found. Please run `python manage.py seed_measurements` first.'))
            return

        # --- Seed ShoppingListItems ---
        self.stdout.write('\nSeeding ShoppingListItems...')

        num_shopping_list_items_to_create = 50

        for i in range(num_shopping_list_items_to_create):
            try:
                ShoppingListItem.objects.create(
                    user=random.choice(users),
                    ingredient=random.choice(ingredients),
                    quantity_needed=fake.random_int(min=1, max=100),
                    unit=random.choice(units),
                    is_purchased=fake.boolean(chance_of_getting_true=30) # 30% chance of being purchased
                )
                self.stdout.write(self.style.SUCCESS(f'Created ShoppingListItem {i+1}/{num_shopping_list_items_to_create}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create ShoppingListItem {i+1}/{num_shopping_list_items_to_create}: {e}'))

        self.stdout.write(self.style.SUCCESS('Shopping app data seeding complete!'))