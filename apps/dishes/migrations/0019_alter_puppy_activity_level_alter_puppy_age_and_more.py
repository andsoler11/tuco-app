# Generated by Django 4.0.4 on 2022-07-20 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0018_alter_puppy_activity_level_alter_puppy_allergies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puppy',
            name='activity_level',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='allergies',
            field=models.CharField(choices=[('Otro', 'Otro'), ('Ninguna', 'Ninguna'), ('Pollo', 'Pollo'), ('Huevo', 'Huevo'), ('Pescado', 'Pescado'), ('Cerdo', 'Cerdo'), ('Res', 'Res'), ('Granos', 'Granos')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='body_image',
            field=models.CharField(choices=[('muy delgado', 'muy delgado'), ('sobrepeso', 'sobrepeso'), ('delgado', 'delgado'), ('peso ideal', 'peso ideal')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='grams',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='grams_percent',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='reproductive_state',
            field=models.CharField(choices=[('castrado', 'castrado'), ('entero', 'entero')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='special_needs',
            field=models.CharField(choices=[('Cancer', 'Cancer'), ('Control de peso', 'Control de peso'), ('Ninguna', 'Ninguna'), ('Diabetes', 'Diabetes'), ('Ariticulaciones', 'Ariticulaciones'), ('Digesti??n', 'Digesti??n'), ('Urinario-renal', 'Urinario-renal'), ('Ansiedad', 'Ansiedad'), ('Hiperactividad', 'Hiperactividad'), ('Piel', 'Piel'), ('Aliento', 'Aliento'), ('Cardiovascular', 'Cardiovascular'), ('Ganancia de peso', 'Ganancia de peso')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
