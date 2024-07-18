from django.db import migrations

def create_initial_tags(apps, schema_editor):
    Tag = apps.get_model('rentals', 'Tag')
    initial_tags = [
        'Non-Smoking Rooms',
        'Spa and Wellness Center',
        'Fitness Center',
        'Accessible Facilities',
        'Room Service',
        'Free Wi-Fi',
        'Parking',
        'Air Conditioning',
        'Coffee/Tea Maker',
        'Bar',
        'Family Rooms',
        'Terrace',
        'Elevator',
        'Garden',
        'Heating',
        'Swimming Pool',
        'Pet Friendly'
    ]
    for tag_name in initial_tags:
        Tag.objects.create(name=tag_name)

class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0002_initial'),  # Замените на правильную начальную миграцию
    ]

    operations = [
        migrations.RunPython(create_initial_tags),
    ]