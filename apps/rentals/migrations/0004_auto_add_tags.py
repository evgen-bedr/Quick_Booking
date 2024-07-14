from django.db import migrations

from apps.rentals.choices.rental_choice import TagChoices

def create_tags(apps, schema_editor):
    Tag = apps.get_model('rentals', 'Tag')
    for choice in TagChoices.choices:
        Tag.objects.get_or_create(name=choice[0])

class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0003_tag_remove_rental_tags_rental_tags'),  # Укажите здесь правильную предыдущую миграцию
    ]

    operations = [
        migrations.RunPython(create_tags),
    ]