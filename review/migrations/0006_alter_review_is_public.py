# Generated by Django 4.2.3 on 2023-08-08 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0005_review_actplace_review_is_public_review_region_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="is_public",
            field=models.BooleanField(
                choices=[(True, "True"), (False, "False")], default=True
            ),
        ),
    ]
