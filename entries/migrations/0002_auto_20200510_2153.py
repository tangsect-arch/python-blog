# Generated by Django 3.0.6 on 2020-05-10 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entries',
            options={'verbose_name_plural': 'Entry List'},
        ),
        migrations.AddField(
            model_name='entries',
            name='entry_images',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
