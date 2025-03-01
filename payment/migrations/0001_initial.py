# Generated by Django 5.0.4 on 2024-07-18 07:40

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facility_rental', '0005_alter_facility_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total_amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='Total amount cannot be negative.')])),
                ('method', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], default='debit', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='facility_rental.facility_booking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
