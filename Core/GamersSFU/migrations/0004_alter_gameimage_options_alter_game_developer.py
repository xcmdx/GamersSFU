# Generated by Django 4.1.7 on 2023-09-28 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GamersSFU', '0003_game_gameimage_genre_alter_zipfile_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gameimage',
            options={'ordering': ['id'], 'verbose_name': 'Скриншоты игр'},
        ),
        migrations.AlterField(
            model_name='game',
            name='Developer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
