# Generated by Django 4.2.6 on 2023-10-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GamersSFU', '0006_gameico_alter_gameganre_game_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameico',
            name='ImageFile',
            field=models.FileField(upload_to='./static/img/game_ioc'),
        ),
        migrations.AlterField(
            model_name='gameimage',
            name='ImageFile',
            field=models.FileField(upload_to='./static/img/game_screens'),
        ),
    ]
