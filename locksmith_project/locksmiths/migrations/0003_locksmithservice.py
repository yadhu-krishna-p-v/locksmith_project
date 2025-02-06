# Generated by Django 5.1.5 on 2025-02-06 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locksmiths', '0002_initial'),
        ('services', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocksmithService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_manufacturer', models.CharField(blank=True, max_length=255, null=True)),
                ('car_model', models.CharField(blank=True, max_length=255, null=True)),
                ('car_year', models.IntegerField(blank=True, null=True)),
                ('key_features', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.servicecategory')),
                ('locksmith', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='locksmiths.locksmithprofile')),
            ],
        ),
    ]
