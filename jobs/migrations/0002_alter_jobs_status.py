# Generated by Django 4.1.7 on 2023-02-22 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='status',
            field=models.CharField(default='C', max_length=2),
        ),
    ]
