# Generated by Django 5.1.3 on 2024-11-25 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("personalSystem", "0004_personelloginlog_is_late_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LateNotification",
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
                ("login_time", models.DateTimeField()),
                ("late_duration", models.CharField(max_length=50)),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "personal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="personalSystem.personal",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
