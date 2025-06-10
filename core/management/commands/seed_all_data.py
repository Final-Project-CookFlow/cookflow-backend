from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Seeds all necessary initial data for the Cookflow Backend in the correct order.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clears all data from relevant tables before seeding.',
        )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO('Starting master data seeding process...'))
        clear_data = kwargs['clear']

        if clear_data:
            self.stdout.write(self.style.WARNING('\nClearing existing data...'))
            self._clear_all_data()
            self.stdout.write(self.style.SUCCESS('Data cleared.'))

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Users ---'))
        call_command('seed_users')

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Measurements ---'))
        call_command('seed_measurements')

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Recipes ---'))
        call_command('seed_recipes')

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Shopping List Items ---'))
        call_command('seed_shopping')

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Favorites ---'))
        call_command('seed_favorites')

        self.stdout.write(self.style.SUCCESS('\nMaster data seeding complete! All initial data is populated.'))

    def _clear_all_data(self):
        """
        Helper method to clear data from all relevant tables.
        Order matters here for foreign key constraints.
        """
        # Disable integrity checks temporarily for bulk deletion
        with connection.cursor() as cursor:
            cursor.execute("SET session_replication_role = 'replica';")

        # Clear data from tables in reverse order of dependency
        # Delete Favorite first (depends on User, Recipe)
        try:
            call_command('shell', '--command="from users.models import Favorite; Favorite.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared Favorite data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Favorite data: {e}'))

        # Delete ShoppingListItem (depends on User, Ingredient, Unit)
        try:
            call_command('shell', '--command="from shopping.models import ShoppingListItem; ShoppingListItem.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared ShoppingListItem data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear ShoppingListItem data: {e}'))

        # Delete RecipeIngredient and Step first (depend on Recipe)
        try:
            call_command('shell', '--command="from recipes.models import RecipeIngredient; RecipeIngredient.objects.all().delete()"')
            call_command('shell', '--command="from recipes.models import Step; Step.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared RecipeIngredient and Step data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear RecipeIngredient/Step data: {e}'))

        # Delete Recipe and Category (Recipe depends on Category, but many-to-many is flexible)
        try:
            call_command('shell', '--command="from recipes.models import Recipe; Recipe.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared Recipe data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Recipe data: {e}'))
        
        try:
            call_command('shell', '--command="from recipes.models import Category; Category.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared Category data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Category data: {e}'))

        # Delete Ingredient (can be deleted after RecipeIngredient)
        try:
            call_command('shell', '--command="from recipes.models import Ingredient; Ingredient.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared Ingredient data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Ingredient data: {e}'))

        # Delete Unit and UnitType (Unit depends on UnitType)
        try:
            call_command('shell', '--command="from measurements.models import Unit; Unit.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared Unit data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Unit data: {e}'))
        
        try:
            call_command('shell', '--command="from measurements.models import UnitType; UnitType.objects.all().delete()"')
            self.stdout.write(self.style.WARNING('Cleared UnitType data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear UnitType data: {e}'))

        # Delete regular Users (Superuser might be tricky if you want to keep it)
        try:
            User = get_user_model()
            User.objects.filter(is_superuser=False, is_staff=False).delete()
            self.stdout.write(self.style.WARNING('Cleared regular User data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear User data: {e}'))

        # Re-enable integrity checks
        with connection.cursor() as cursor:
            cursor.execute("SET session_replication_role = 'origin';")