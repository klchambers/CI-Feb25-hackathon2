# events/management/commands/generate_events.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone
from django.core import serializers
from events.models import Event, EventCategory
from datetime import datetime, timedelta
import random
import uuid
import json
import os

class Command(BaseCommand):
    help = 'Generate sample London events and save to both database and fixtures'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Flush existing events before generating new ones',
        )
        parser.add_argument(
            '--events',
            type=int,
            default=50,
            help='Number of events to generate'
        )

    def handle(self, *args, **kwargs):
        # Path to fixtures file
        fixtures_dir = os.path.join('events', 'fixtures')
        fixtures_file = os.path.join(fixtures_dir, 'initial_events.json')

        # Create fixtures directory if it doesn't exist
        os.makedirs(fixtures_dir, exist_ok=True)

        if kwargs.get('flush'):
            self.stdout.write('Flushing existing events...')
            Event.objects.all().delete()
            EventCategory.objects.all().delete()

        # Create base categories
        categories_data = [
            ('Speed Dating', 'Quick and fun way to meet multiple potential matches in London'),
            ('Singles Mixer', 'Casual social events for London singles to mingle'),
            ('Cooking Class', 'Learn to cook with other singles in London\'s finest culinary venues'),
            ('Wine Tasting', 'Sophisticated wine tasting events in London\'s wine bars'),
            ('Adventure Dating', 'Unique London experiences for adventurous singles'),
        ]

        categories = []
        for name, description in categories_data:
            category, created = EventCategory.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'description': description
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {name}')

        # London-specific event templates
        event_templates = [
            {
                'title_template': "London Speed Dating at {}",
                'description': "Join us for an exciting evening of speed dating in the heart of London! Meet amazing singles in a sophisticated setting. Includes welcome prosecco and canapés.",
                'price_range': (25, 35),  # In GBP
                'capacity_range': (20, 40),
                'locations': ['The Shard', 'Sky Garden', 'Madison Rooftop', 'The Gherkin']
            },
            {
                'title_template': "Singles Mixer - {}",
                'description': "A relaxed evening for London singles to mingle in a stunning venue. Includes welcome drink and nibbles.",
                'price_range': (20, 30),
                'capacity_range': (50, 100),
                'locations': ['Sketch London', 'Pergola Paddington', 'Brewdog Tower Hill', 'The Ned']
            },
            {
                'title_template': "Cooking Class for Singles at {}",
                'description': "Learn to cook delicious dishes while meeting other London foodies! All ingredients and equipment provided.",
                'price_range': (55, 85),
                'capacity_range': (12, 24),
                'locations': ['Jamie Oliver Cooking School', 'L\'atelier des Chefs', 'Sauce by The Langham', 'Borough Kitchen']
            }
        ]

        # London areas with postcodes
        london_areas = [
            ('Shoreditch', 'EC2A'),
            ('Mayfair', 'W1K'),
            ('Covent Garden', 'WC2E'),
            ('Soho', 'W1F'),
            ('City of London', 'EC3M'),
            ('Chelsea', 'SW3'),
            ('Notting Hill', 'W11'),
            ('Camden', 'NW1')
        ]

        # Generate events
        num_events = kwargs.get('events', 30)
        events_created = 0

        for _ in range(num_events):
            try:
                area, postcode = random.choice(london_areas)
                template = random.choice(event_templates)
                category = random.choice(categories)
                
                days_ahead = random.randint(1, 90)
                event_date = timezone.now() + timedelta(days=days_ahead)
                event_time = random.choice([19, 20])  # 7 PM or 8 PM
                event_date = event_date.replace(hour=event_time, minute=0)
                
                title = template['title_template'].format(area)
                unique_id = str(uuid.uuid4())[:8]
                date_string = event_date.strftime('%Y%m%d')
                slug = f"{slugify(title)}-{date_string}-{unique_id}"
                
                venue = random.choice(template['locations'])
                price = random.randint(template['price_range'][0], template['price_range'][1])
                capacity = random.randint(template['capacity_range'][0], template['capacity_range'][1])
                
                # Create random London street address
                street_number = random.randint(1, 200)
                streets = ['High Street', 'Liverpool Street', 'Oxford Street', 'King\'s Road', 'Baker Street', 'Bond Street']
                street = random.choice(streets)
                
                Event.objects.create(
                    title=title,
                    slug=slug,
                    description=template['description'],
                    category=category,
                    date=event_date,
                    duration=timedelta(hours=random.randint(2, 4)),
                    location_name=venue,
                    address=f"{street_number} {street}",
                    city="London",
                    state="",  # UK doesn't use states
                    zip_code=postcode,
                    price=price,
                    capacity=capacity,
                    spots_remaining=capacity,
                    is_active=True,
                    is_demo=True,
                )
                events_created += 1
                
                if events_created % 10 == 0:
                    self.stdout.write(f'Created {events_created} events...')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating event: {str(e)}')
                )

        # After generating all events, dump to fixture file
        self.stdout.write('Saving data to fixture file...')
        
        # Get all events and categories
        all_categories = EventCategory.objects.all()
        all_events = Event.objects.all()
        
        # Serialize both models
        serialized_categories = serializers.serialize('json', all_categories)
        serialized_events = serializers.serialize('json', all_events)
        
        # Combine the serialized data
        categories_data = json.loads(serialized_categories)
        events_data = json.loads(serialized_events)
        combined_data = categories_data + events_data
        
        # Write to fixture file
        with open(fixtures_file, 'w') as f:
            json.dump(combined_data, f, indent=2)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {events_created} London events and saved to {fixtures_file}'
            )
        )