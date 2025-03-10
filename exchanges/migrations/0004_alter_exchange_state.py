# Generated by Django 5.1.6 on 2025-02-27 12:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exchanges", "0003_alter_exchange_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exchange",
            name="state",
            field=models.CharField(
                choices=[
                    ("D", "done"),
                    ("P", "pending"),
                    ("I", "in progress"),
                    ("C", "cancelled"),
                ],
                default="P",
                max_length=1,
            ),
        ),
    ]
