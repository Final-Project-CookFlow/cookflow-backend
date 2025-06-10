# measurements/management/commands/seed_measurements.py

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from measurements.models import UnitType, Unit
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds UnitType and Unit data for the measurements app.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        User = get_user_model()

        # 1. Ensure a user exists to associate units with
        # (This should ideally be created by your 'seed_users' command first)
        try:
            user = User.objects.first()
            if not user:
                # Fallback: if no user exists, create a minimal one.
                # In a full 'seed_all_data' flow, this would be handled by seed_users.
                user = User.objects.create_user(username='default_measure_user', email='measure@example.com', password='password123')
                self.stdout.write(self.style.WARNING('Created fallback user for measurements.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Could not get/create user for measurements: {e}'))
            return # Exit if we can't get a user

        self.stdout.write('Seeding UnitTypes and Units...')

        # 2. Seed common UnitTypes
        unit_type_data = [
            {'name': 'Weight'},
            {'name': 'Volume'},
            {'name': 'Count'}
        ]

        unit_types = {}
        for data in unit_type_data:
            unit_type, created = UnitType.objects.get_or_create(name=data['name'])
            unit_types[unit_type.name] = unit_type
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created UnitType: {unit_type.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'UnitType "{unit_type.name}" already exists.'))
        
        if not unit_types:
            self.stdout.write(self.style.ERROR('No UnitTypes found or created. Cannot seed Units.'))
            return

        # 3. Seed common Units
        unit_data = [
            {'name': 'gram', 'unit_type': unit_types.get('Weight')},
            {'name': 'kilogram', 'unit_type': unit_types.get('Weight')},
            {'name': 'ml', 'unit_type': unit_types.get('Volume')},
            {'name': 'liter', 'unit_type': unit_types.get('Volume')},
            {'name': 'tablespoon', 'unit_type': unit_types.get('Volume')},
            {'name': 'teaspoon', 'unit_type': unit_types.get('Volume')},
            {'name': 'unit', 'unit_type': unit_types.get('Count')},
            {'name': 'piece', 'unit_type': unit_types.get('Count')},
        ]

        for data in unit_data:
            if data['unit_type'] is None:
                self.stdout.write(self.style.WARNING(f'Skipping unit "{data["name"]}" as its UnitType was not found.'))
                continue
            
            unit, created = Unit.objects.get_or_create(
                name=data['name'],
                unit_type=data['unit_type'],
                user=user # Assign to the fetched user
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created Unit: {unit.name} ({unit.unit_type.name})'))
            else:
                self.stdout.write(self.style.WARNING(f'Unit "{unit.name}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Measurement seeding complete!'))