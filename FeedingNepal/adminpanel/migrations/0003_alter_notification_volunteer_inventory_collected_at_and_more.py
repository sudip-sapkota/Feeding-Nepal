# Generated by Django 5.2.3 on 2025-07-10 03:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adminpanel", "0002_initial"),
        ("volunteer", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="volunteer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="volunteer.volunteer",
            ),
        ),
        migrations.AddField(
            model_name="inventory",
            name="collected_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="inventory",
            name="collected_by_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="inventory",
            name="collected_by_phone",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name="Volunteer",
        ),
    ]
