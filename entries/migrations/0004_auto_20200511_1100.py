# Generated by Django 3.0.6 on 2020-05-11 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entries', '0003_auto_20200511_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='entries',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entries',
            name='entry_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entry_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('Unlike', 'Unlike'), ('Likes', 'Like')], default='Like', max_length=10)),
                ('entries', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.Entries')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
