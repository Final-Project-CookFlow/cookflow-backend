# recipes/management/commands/seed_recipes.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

# Adjust imports based on your exact app structure
from recipes.models import Category, Ingredient, Recipe, RecipeIngredient, Step
from measurements.models import UnitType, Unit # Import UnitType and Unit
from media.models import Image # Import the Image model

class Command(BaseCommand):
    help = 'Seeds data for the recipes app: Categories, Ingredients, Recipes, RecipeIngredients, Steps.'

    def handle(self, *args, **kwargs):
        fake = Faker('en_US')
        User = get_user_model()

        self.stdout.write('Seeding recipes app data...')

        # --- Ensure Dependencies Exist ---
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR('No users found. Please run `python manage.py seed_users` first.'))
            return

        unit_types = list(UnitType.objects.all())
        if not unit_types:
            self.stdout.write(self.style.ERROR('No UnitTypes found. Please run `python manage.py seed_measurements` first.'))
            return
        
        # --- CRITICAL FIX: Fetch actual Unit objects, not just names ---
        all_units = list(Unit.objects.all()) # Fetch actual Unit objects
        if not all_units:
            self.stdout.write(self.style.ERROR('No Units found. Cannot seed RecipeIngredients. Please run `python manage.py seed_measurements` first.'))
            return
        # --- END CRITICAL FIX ---

        # Get existing RECIPE type images
        recipe_images = list(Image.objects.filter(type=Image.ImageType.RECIPE))
        if not recipe_images:
            self.stdout.write(self.style.WARNING('No RECIPE images found. Recipes will be created without main photos. Ensure `python manage.py seed_media` is run before this command.'))

        # --- ADDED: Get existing STEP type images ---
        step_images = list(Image.objects.filter(type=Image.ImageType.STEP))
        if not step_images:
            self.stdout.write(self.style.WARNING('No STEP images found. Steps will be created without photos. Ensure `python manage.py seed_media` is run before this command.'))
        # --- END ADDITION ---


        # --- 1. Seed Categories ---
        self.stdout.write('\nSeeding Categories...')
        initial_categories = [
            'Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Appetizer', 'Beverage',
            'Soup', 'Salad', 'Main Course', 'Side Dish', 'Snack', 'Baking'
        ]
        
        seeded_categories = []
        for cat_name in initial_categories:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'user': random.choice(users)} # Ensure category has a user
            )
            seeded_categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category.name}" already exists.'))
        
        # Seed subcategories only if enough parent categories exist
        if len(seeded_categories) >= 2:
            parent_category_1 = seeded_categories[0]
            parent_category_2 = seeded_categories[1]

            sub_cat_1, created = Category.objects.get_or_create(
                name='Smoothies', 
                defaults={'user': random.choice(users), 'parent_category': parent_category_1}
            )
            if created: self.stdout.write(self.style.SUCCESS(f'Created Sub-Category: {sub_cat_1.name} under {parent_category_1.name}'))
            else: self.stdout.write(self.style.WARNING(f'Sub-Category "{sub_cat_1.name}" already exists.'))
            
            sub_cat_2, created = Category.objects.get_or_create(
                name='Sandwiches', 
                defaults={'user': random.choice(users), 'parent_category': parent_category_2}
            )
            if created: self.stdout.write(self.style.SUCCESS(f'Created Sub-Category: {sub_cat_2.name} under {parent_category_2.name}'))
            else: self.stdout.write(self.style.WARNING(f'Sub-Category "{sub_cat_2.name}" already exists.'))

        if not seeded_categories:
            self.stdout.write(self.style.ERROR('No categories seeded. Cannot seed Ingredients or Recipes.'))
            return


        # --- 2. Seed Ingredients ---
        self.stdout.write('\nSeeding Ingredients...')
        seeded_ingredients = []
        ingredient_names_set = set() # Use a set for efficient checking of existing names

        # Increase number of ingredients to provide more variety
        for _ in range(100): # Create more ingredients
            while True:
                name = fake.word().capitalize()
                if name not in ingredient_names_set and not Ingredient.objects.filter(name=name).exists():
                    ingredient_names_set.add(name)
                    break
                # Add a fallback for unique names if fake.word() repeats too much
                name = f"{name}{random.randint(1, 100)}"
                if name not in ingredient_names_set and not Ingredient.objects.filter(name=name).exists():
                    ingredient_names_set.add(name)
                    break


            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={
                    'user': random.choice(users),
                    'unit_type': random.choice(unit_types),
                    'is_approved': fake.boolean(chance_of_getting_true=80)
                }
            )
            seeded_ingredients.append(ingredient) # Always add to list, whether created or fetched
            if created:
                num_categories = random.randint(1, 3)
                ingredient.categories.set(random.sample(seeded_categories, min(num_categories, len(seeded_categories))))
                self.stdout.write(self.style.SUCCESS(f'Created Ingredient: {ingredient.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Ingredient "{ingredient.name}" already exists.'))
        
        if not seeded_ingredients:
            self.stdout.write(self.style.ERROR('No ingredients seeded. Cannot seed Recipes or RecipeIngredients.'))
            return


        # --- 3. Seed Recipes ---
        self.stdout.write('\nSeeding Recipes...')
        seeded_recipes = []
        
        num_successful_recipes = 0
        total_recipe_attempts = 30 # Number of recipes to try and create

        for i in range(total_recipe_attempts):
            recipe_name = fake.sentence(nb_words=random.randint(2, 6)).replace('.', '')
            if len(recipe_name) > 50:
                recipe_name = recipe_name[:50]

            recipe_description = fake.paragraph(nb_sentences=random.randint(1, 2))
            if len(recipe_description) > 100:
                recipe_description = recipe_description[:100]
            
            try:
                # Select a random recipe image if available
                main_photo_instance = random.choice(recipe_images) if recipe_images else None

                recipe = Recipe.objects.create(
                    name=recipe_name,
                    description=recipe_description,
                    user=random.choice(users),
                    duration_minutes=fake.random_int(min=15, max=240),
                    commensals=fake.random_int(min=1, max=12),
                    main_photo=main_photo_instance # ASSIGNED: Assign the Image object here!
                )
                seeded_recipes.append(recipe)
                num_successful_recipes += 1
                
                # Assign 1-3 random categories to the recipe
                num_categories = random.randint(1, 3)
                recipe.categories.set(random.sample(seeded_categories, min(num_categories, len(seeded_categories))))
                self.stdout.write(self.style.SUCCESS(f'Created Recipe ({num_successful_recipes}/{total_recipe_attempts}): {recipe.name}'))

                # Seeding RecipeIngredients and Steps for the newly created recipe
                self.stdout.write(f'  Seeding RecipeIngredients and Steps for {recipe.name}...')
                
                # Create RecipeIngredients (3-7 ingredients per recipe)
                num_ingredients = random.randint(3, 7)
                ingredients_for_recipe = random.sample(seeded_ingredients, min(num_ingredients, len(seeded_ingredients)))
                
                for ingredient in ingredients_for_recipe:
                    # --- CRITICAL FIX: Pass the actual Unit object ---
                    unit_instance = random.choice(all_units) # Select a random Unit object
                    # --- END CRITICAL FIX ---
                    
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=fake.random_int(min=1, max=500),
                        unit=unit_instance # ASSIGNED: Pass the Unit object here!
                    )
                    # --- FIX APPLIED HERE: Use .name instead of .abbreviation for printing ---
                    self.stdout.write(self.style.SUCCESS(f'    Added {ingredient.name} ({unit_instance.name}) to {recipe.name}'))
                    # --- END FIX ---

                # Create Steps (3-5 steps per recipe)
                num_steps = random.randint(3, 5)
                for k in range(num_steps):
                    step_description = fake.sentence(nb_words=random.randint(5, 15))
                    if len(step_description) > 100:
                        step_description = step_description[:100]

                    # Assign a random step image (if available)
                    step_image_instance = random.choice(step_images) if step_images else None

                    Step.objects.create(
                        recipe=recipe,
                        order=k + 1,
                        description=step_description,
                        image=step_image_instance # ASSIGNED: Assign the Image object here!
                    )
                    self.stdout.write(self.style.SUCCESS(f'    Added Step {k+1} to {recipe.name}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create recipe (attempt {i+1}/{total_recipe_attempts}): {e}'))
                # If a recipe creation fails (e.g., due to unique constraint, though we handled names),
                # we should skip creating ingredients and steps for it.

        self.stdout.write(f'Attempted to create {total_recipe_attempts} recipes. Successfully created {num_successful_recipes}.')

        if not seeded_recipes:
            self.stdout.write(self.style.ERROR('No recipes seeded. Cannot seed RecipeIngredients or Steps.'))
            # This return is technically redundant if num_successful_recipes is 0
            # and the loop already broke or didn't add to seeded_recipes.
            # But it doesn't harm.
            return 


        self.stdout.write(self.style.SUCCESS('Recipes app data seeding complete!'))
