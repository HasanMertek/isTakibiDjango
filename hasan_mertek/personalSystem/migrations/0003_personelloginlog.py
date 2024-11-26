# Generated by Django 5.1.3 on 2024-11-25 18:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("personalSystem", "0002_personal_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="PersonelLoginLog",
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
                ("login_time", models.DateTimeField(auto_now_add=True)),
                ("logout_time", models.DateTimeField(blank=True, null=True)),
                (
                    "personal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personalSystem.personal",
                    ),
                ),
            ],
        ),
    ]