# Generated by Django 4.2.6 on 2023-10-12 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GamersSFU', '0005_rename_file_zipfile_gamefile'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameIco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ImageFile', models.FileField(upload_to='./static/img/')),
            ],
            options={
                'verbose_name': 'Скриншоты игр',
                'ordering': ['id'],
            },
        ),
        migrations.AlterField(
            model_name='gameganre',
            name='Game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GamersSFU.game'),
        ),
        migrations.AlterField(
            model_name='gamepostimage',
            name='GameImage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GamersSFU.gameimage'),
        ),
        migrations.AddField(
            model_name='game',
            name='GameIco',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='GamersSFU.gameico'),
        ),
    ]
