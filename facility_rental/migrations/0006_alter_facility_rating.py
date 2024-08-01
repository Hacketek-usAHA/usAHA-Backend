# Generated by Django 5.0.4 on 2024-07-18 13:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility_rental', '0005_alter_facility_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MinValueValidator(0, message='Rating cannot be negative.'), django.core.validators.MaxValueValidator(5, message='Rating cannot be more than five')]),
        ),
    ]
