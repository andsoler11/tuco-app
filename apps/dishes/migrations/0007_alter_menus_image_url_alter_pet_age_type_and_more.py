# Generated by Django 4.0.4 on 2024-02-05 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0006_menus_image_url_alter_pet_age_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menus',
            name='image_url',
            field=models.CharField(blank=True, choices=[('imagen_cerdo.svg', 'Cerdo'), ('imagen_res.svg', 'Res'), ('imagen_pollo.png', 'Pollo'), ('imagen_iniciacion.svg', 'Iniciación')], default='imagen_res.svg', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pet',
            name='age_type',
            field=models.CharField(choices=[('meses', 'meses'), ('años', 'años')], default='años', max_length=255),
        ),
        migrations.AlterField(
            model_name='pet',
            name='allergies',
            field=models.CharField(choices=[('Res', 'Res'), ('Pescado', 'Pescado'), ('Ninguna', 'Ninguna'), ('Cerdo', 'Cerdo'), ('Otro', 'Otro'), ('Pollo', 'Pollo'), ('Huevo', 'Huevo'), ('Granos', 'Granos')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='pet',
            name='body_image',
            field=models.CharField(choices=[('muy_delgado', 'muy_delgado'), ('delgado', 'delgado'), ('sobrepeso', 'sobrepeso'), ('peso_ideal', 'peso_ideal')], max_length=255),
        ),
        migrations.AlterField(
            model_name='pet',
            name='special_needs',
            field=models.CharField(choices=[('Cardiovascular', 'Cardiovascular'), ('Ansiedad', 'Ansiedad'), ('Ninguna', 'Ninguna'), ('Ganancia de peso', 'Ganancia de peso'), ('Urinario-renal', 'Urinario-renal'), ('Aliento', 'Aliento'), ('Piel', 'Piel'), ('Hiperactividad', 'Hiperactividad'), ('Ariticulaciones', 'Ariticulaciones'), ('Digestión', 'Digestión'), ('Cancer', 'Cancer'), ('Diabetes', 'Diabetes'), ('Control de peso', 'Control de peso')], default='Ninguna', max_length=255),
        ),
    ]