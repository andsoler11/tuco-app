# Generated by Django 4.0.4 on 2022-07-19 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0014_alter_puppy_body_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puppy',
            name='activity_level',
            field=models.IntegerField(choices=[(1, 'sedentario'), (3, 'muy activo'), (2, 'actividad media')]),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='body_image',
            field=models.IntegerField(choices=[(1, 'muy delgado'), (2, 'delgado'), (3, 'peso ideal'), (4, 'sobrepeso')]),
        ),
    ]
