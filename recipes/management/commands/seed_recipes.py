# recipes/management/commands/seed_recipes.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

# Adjust imports based on your exact app structure
from recipes.models import Category, Ingredient, Recipe, RecipeIngredient, Step
from measurements.models import UnitType, Unit # Assuming measurements app and models exist

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
        
        units = list(Unit.objects.all())
        unit_names = [unit.name for unit in units]
        if not unit_names:
            self.stdout.write(self.style.WARNING('No Units found. RecipeIngredients might use generic unit names.'))
            unit_names = ['g', 'ml', 'unit', 'cup', 'tbsp', 'tsp', 'pinch']


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
                defaults={'user': random.choice(users)}
            )
            seeded_categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Category: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category.name}" already exists.'))
        
        if len(seeded_categories) >= 2:
            parent_category_1 = seeded_categories[0]
            parent_category_2 = seeded_categories[1]

            sub_cat_1, created = Category.objects.get_or_create(
                name='Smoothies', 
                defaults={'user': random.choice(users), 'parent_category': parent_category_1}
            )
            if created: self.stdout.write(self.style.SUCCESS(f'Created Sub-Category: {sub_cat_1.name} under {parent_category_1.name}'))
            
            sub_cat_2, created = Category.objects.get_or_create(
                name='Sandwiches', 
                defaults={'user': random.choice(users), 'parent_category': parent_category_2}
            )
            if created: self.stdout.write(self.style.SUCCESS(f'Created Sub-Category: {sub_cat_2.name} under {parent_category_2.name}'))

        if not seeded_categories:
            self.stdout.write(self.style.ERROR('No categories seeded. Cannot seed Ingredients or Recipes.'))
            return


        # --- 2. Seed Ingredients ---
        self.stdout.write('\nSeeding Ingredients...')
        seeded_ingredients = []
        ingredient_names = set()

        for _ in range(50):
            while True:
                name = fake.word().capitalize()
                if name not in ingredient_names:
                    ingredient_names.add(name)
                    break

            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={
                    'user': random.choice(users),
                    'unit_type': random.choice(unit_types),
                    'is_approved': fake.boolean(chance_of_getting_true=80)
                }
            )
            if created:
                seeded_ingredients.append(ingredient)
                num_categories = random.randint(1, 3)
                ingredient.categories.set(random.sample(seeded_categories, min(num_categories, len(seeded_categories))))
                self.stdout.write(self.style.SUCCESS(f'Created Ingredient: {ingredient.name}'))
            else:
                existing_ingredient = Ingredient.objects.get(name=name)
                seeded_ingredients.append(existing_ingredient)
                self.stdout.write(self.style.WARNING(f'Ingredient "{ingredient.name}" already exists.'))
        
        if not seeded_ingredients:
            self.stdout.write(self.style.ERROR('No ingredients seeded. Cannot seed Recipes or RecipeIngredients.'))
            return


        # --- 3. Seed Recipes ---
        self.stdout.write('\nSeeding Recipes...')
        seeded_recipes = []
        
        # Track attempts and failures
        num_successful_recipes = 0
        total_recipe_attempts = 30

        for i in range(total_recipe_attempts):
            recipe_name = fake.sentence(nb_words=random.randint(2, 6)).replace('.', '')
            if len(recipe_name) > 50:
                recipe_name = recipe_name[:50]

            recipe_description = fake.paragraph(nb_sentences=random.randint(1, 2))
            if len(recipe_description) > 100:
                recipe_description = recipe_description[:100]
            
            try:
                recipe = Recipe.objects.create(
                    name=recipe_name,
                    description=recipe_description,
                    user=random.choice(users),
                    duration_minutes=fake.random_int(min=15, max=240),
                    commensals=fake.random_int(min=1, max=12)
                )
                seeded_recipes.append(recipe)
                num_successful_recipes += 1
                
                # Assign 1-3 random categories to the recipe
                num_categories = random.randint(1, 3)
                recipe.categories.set(random.sample(seeded_categories, min(num_categories, len(seeded_categories))))
                self.stdout.write(self.style.SUCCESS(f'Created Recipe ({num_successful_recipes}/{total_recipe_attempts}): {recipe.name}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to create recipe (attempt {i+1}/{total_recipe_attempts}): {e}'))

        self.stdout.write(f'Attempted to create {total_recipe_attempts} recipes. Successfully created {num_successful_recipes}.')

        if not seeded_recipes:
            self.stdout.write(self.style.ERROR('No recipes seeded. Cannot seed RecipeIngredients or Steps.'))
            return


        # --- 4. Seed RecipeIngredients and Steps ---
        self.stdout.write('\nSeeding RecipeIngredients and Steps...')
        for recipe in seeded_recipes:
            # Seed RecipeIngredients for this recipe (3-7 ingredients per recipe)
            num_ingredients = random.randint(3, 7)
            ingredients_for_recipe = random.sample(seeded_ingredients, min(num_ingredients, len(seeded_ingredients)))
            
            for ingredient in ingredients_for_recipe:
                random_unit_name = random.choice(unit_names) 
                
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=fake.random_int(min=1, max=500),
                    unit=random_unit_name
                )
                self.stdout.write(self.style.SUCCESS(f'  Added {ingredient.name} to {recipe.name}'))

            # Seed Steps for this recipe (3-5 steps per recipe)
            num_steps = random.randint(3, 5)
            for i in range(num_steps):
                # Ensure Step description fits within 100 characters
                step_description = fake.sentence(nb_words=random.randint(5, 15))
                if len(step_description) > 100:
                    step_description = step_description[:100]

                Step.objects.create( # <--- This is the correct, single create call
                    recipe=recipe,
                    order=i + 1,
                    description=step_description
                )
                self.stdout.write(self.style.SUCCESS(f'  Added Step {i+1} to {recipe.name}'))

        self.stdout.write(self.style.SUCCESS('Recipes app data seeding complete!')) 