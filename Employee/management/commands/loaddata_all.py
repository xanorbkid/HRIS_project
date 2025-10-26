#!/usr/bin/env python
"""
Management command to load all fixtures in the correct order.
Usage: python manage.py loaddata_all
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Loads all fixtures in the correct order to populate the database'

    def handle(self, *args, **options):
        # Base directory for fixtures
        fixture_dir = 'seeders'
        
        # Load order for fixtures (maintains relationships)
        fixture_order = [
            # Auth fixtures
            'auth/01_groups.json',
            'auth/02_users.json',
            
            # Employee fixtures
            'employee/01_departments.json',
            'employee/02_job_titles.json',
            'employee/03_employee_profiles.json',
            'employee/04_emergency_contacts.json',
            
            # Time-off management fixtures
            'time_off_management/01_leave_types.json',
            'time_off_management/02_shifts.json',
            'time_off_management/03_leave_allocations.json',
            'time_off_management/04_leave_requests.json',
        ]
        
        self.stdout.write('Starting to load fixtures...')
        
        for fixture in fixture_order:
            fixture_path = os.path.join(fixture_dir, fixture)
            if os.path.exists(fixture_path):
                self.stdout.write(f'Loading {fixture}...')
                try:
                    call_command('loaddata', fixture_path, verbosity=1)
                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture}'))
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to load {fixture}: {str(e)}')
                    )
                    raise
            else:
                self.stdout.write(
                    self.style.WARNING(f'Fixture file not found: {fixture_path}')
                )
        
        self.stdout.write(self.style.SUCCESS('All fixtures loaded successfully!'))