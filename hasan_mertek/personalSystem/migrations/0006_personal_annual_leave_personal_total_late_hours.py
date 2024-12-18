# Generated by Django 5.1.3 on 2024-11-25 19:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("personalSystem", "0005_latenotification"),
    ]

    operations = [
        migrations.AddField(
            model_name="personal",
            name="annual_leave",
            field=models.FloatField(default=15.0),
        ),
        migrations.AddField(
            model_name="personal",
            name="total_late_hours",
            field=models.FloatField(default=0.0),
        ),
    ]
