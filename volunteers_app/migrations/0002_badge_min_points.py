from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers_app', '0001_initial'),
    ]

    operations = [
        # Remove unique=True from badge_type and allow blank
        migrations.AlterField(
            model_name='badge',
            name='badge_type',
            field=models.CharField(
                blank=True,
                choices=[
                    ('first_event', 'First Event'),
                    ('five_events', '5 Events Attended'),
                    ('ten_events', '10 Events Attended'),
                    ('lake_guardian', 'Lake Guardian'),
                    ('team_player', 'Team Player'),
                    ('eco_warrior', 'Eco Warrior'),
                ],
                default='',
                max_length=50,
            ),
        ),
        # Add min_points field for automatic point-based badge allocation
        migrations.AddField(
            model_name='badge',
            name='min_points',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                help_text='Auto-award when a volunteer reaches this many points. Leave blank for manual-only.',
            ),
        ),
    ]
