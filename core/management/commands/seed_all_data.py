# core/management/commands/seed_all_data.py

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.contrib.auth import get_user_model

# Import all models needed for clearing data directly
from media.models import Image
from users.models import Favorite
from shopping.models import ShoppingListItem
from recipes.models import Recipe, RecipeIngredient, Step, Category, Ingredient
from measurements.models import Unit, UnitType

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

        # --- IMPORTANT: Reordered seeding commands for correct dependencies ---
        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Media (Images) ---')) 
        call_command('seed_media') # Create Image objects first

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Users ---'))
        call_command('seed_users') # Users can now link to profile pictures

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Measurements ---'))
        call_command('seed_measurements') # Measurements (units, types) are needed for ingredients

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Recipes ---'))
        call_command('seed_recipes') # Recipes can now link to main photos and steps can link to images

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Shopping List Items ---'))
        call_command('seed_shopping') # Shopping list items can depend on recipes/ingredients

        self.stdout.write(self.style.HTTP_INFO('\n--- Seeding Favorites ---'))
        call_command('seed_favorites') # Favorites depend on users and recipes
        # --- End Reordering ---

        self.stdout.write(self.style.SUCCESS('\nMaster data seeding complete! All initial data is populated.'))

    def _clear_all_data(self):
        """
        Helper method to clear data from all relevant tables and reset sequences.
        Order matters here for foreign key constraints and sequence resets.
        """
        # --- PHASE 1: Disable integrity checks temporarily for bulk deletion (PostgreSQL specific) ---
        with connection.cursor() as cursor:
            try:
                cursor.execute("SET session_replication_role = 'replica';")
                self.stdout.write(self.style.WARNING("Disabled session replication role."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to disable session replication role: {e}. Continue without it."))

        # --- PHASE 2: Clear actual data from tables in dependency order (most dependent first) ---
        # Using direct Model.objects.all().delete() for robustness

        try:
            Favorite.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared Favorite data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Favorite data: {e}'))

        try:
            ShoppingListItem.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared ShoppingListItem data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear ShoppingListItem data: {e}'))

        try:
            RecipeIngredient.objects.all().delete()
            Step.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared RecipeIngredient and Step data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear RecipeIngredient/Step data: {e}'))

        try:
            Recipe.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared Recipe data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Recipe data: {e}'))
        
        try:
            Image.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared Image data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Image data: {e}'))

        try:
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared Category data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Category data: {e}'))

        try:
            Ingredient.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared Ingredient data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Ingredient data: {e}'))

        try:
            Unit.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared Unit data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear Unit data: {e}'))
        
        try:
            UnitType.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared UnitType data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear UnitType data: {e}'))

        User = get_user_model()
        try:
            User.objects.filter(is_superuser=False, is_staff=False).delete()
            self.stdout.write(self.style.WARNING('Cleared regular User data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to clear User data: {e}'))

        # --- PHASE 3: Reset sequences and re-enable integrity checks ---
        with connection.cursor() as cursor:
            # Reset sequences for all relevant tables (PostgreSQL specific)
            # 'users' is excluded as admin user is not cleared.
            table_names_to_reset_sequences = [
                'categories', 'ingredients', 'recipes', 'recipe_ingredients', 
                'steps', 'images', 'shopping_list_items', 'unit_types', 'units', 
                'categories_recipes' # Ensure many-to-many intermediate tables are also included
            ]
            for table_name in table_names_to_reset_sequences:
                try:
                    # Check if the sequence exists before attempting to reset (prevents errors for non-existent sequences)
                    cursor.execute(f"SELECT 1 FROM pg_class WHERE relname = '{table_name}_id_seq' AND relkind = 'S';")
                    if cursor.fetchone(): # If sequence exists
                        cursor.execute(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1;")
                        self.stdout.write(self.style.WARNING(f"Reset sequence for {table_name}_id_seq."))
                    else:
                        self.stdout.write(self.style.WARNING(f"Sequence {table_name}_id_seq does not exist or is not a sequence, skipping reset."))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to reset sequence for {table_name}_id_seq: {e}."))
            
            # Re-enable integrity checks after all deletions and sequence resets are done
            try:
                cursor.execute("SET session_replication_role = 'origin';")
                self.stdout.write(self.style.WARNING("Re-enabled session replication role."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to re-enable session replication role: {e}."))
