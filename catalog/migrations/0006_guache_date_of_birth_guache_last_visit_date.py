# Generated by Django 5.0.11 on 2025-02-12 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_learning_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guache',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='guache',
            name='last_visit_date',
            field=models.DateField(blank=True, null=True, verbose_name='last in'),
        ),
    ]
