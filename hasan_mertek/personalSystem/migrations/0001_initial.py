# Generated by Django 5.1.3 on 2024-11-25 18:27

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Personal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=15)),
                ("address", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("position", models.CharField(max_length=100)),
            ],
        ),
    ]
