# Generated by Django 5.0.11 on 2025-02-07 19:17

import django.db.models.deletion
import django.db.models.functions.text
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('karma', models.IntegerField()),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('summary', models.TextField(help_text='A Brief description of the Path', max_length=1000)),
                ('refcode', models.CharField(max_length=13, verbose_name='RefCode')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Knowledge task item...', max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Learning',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular learning path', primary_key=True, serialize=False)),
                ('begin', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('w', 'Walking'), ('m', 'Maintenance'), ('d', 'In debt'), ('l', 'Lost'), ('c', 'Completed path')], default='w', help_text='Status of the Learning Path', max_length=1)),
                ('path', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.path')),
            ],
            options={
                'ordering': ['begin'],
            },
        ),
        migrations.AddConstraint(
            model_name='task',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='task_name_case_insensitive_unique', violation_error_message='Task already exists (case insensitive match)'),
        ),
        migrations.AddField(
            model_name='path',
            name='task',
            field=models.ManyToManyField(help_text='Select tasks for this path', to='catalog.task'),
        ),
    ]
