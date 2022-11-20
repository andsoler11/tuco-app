# Generated by Django 4.0.4 on 2022-11-18 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0028_menus_alter_puppy_age_type_alter_puppy_allergies_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menus',
            old_name='nutrition_informatuion',
            new_name='nutrition_information',
        ),
        migrations.AlterField(
            model_name='puppy',
            name='age_type',
            field=models.CharField(choices=[('meses', 'meses'), ('años', 'años')], default='años', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='allergies',
            field=models.CharField(choices=[('Pescado', 'Pescado'), ('Otro', 'Otro'), ('Pollo', 'Pollo'), ('Huevo', 'Huevo'), ('Res', 'Res'), ('Granos', 'Granos'), ('Cerdo', 'Cerdo'), ('Ninguna', 'Ninguna')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='body_image',
            field=models.CharField(choices=[('delgado', 'delgado'), ('sobrepeso', 'sobrepeso'), ('peso ideal', 'peso ideal'), ('muy delgado', 'muy delgado')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='reproductive_state',
            field=models.CharField(choices=[('castrado', 'castrado'), ('entero', 'entero')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='special_needs',
            field=models.CharField(choices=[('Urinario-renal', 'Urinario-renal'), ('Ansiedad', 'Ansiedad'), ('Ganancia de peso', 'Ganancia de peso'), ('Control de peso', 'Control de peso'), ('Cancer', 'Cancer'), ('Diabetes', 'Diabetes'), ('Ninguna', 'Ninguna'), ('Digestión', 'Digestión'), ('Aliento', 'Aliento'), ('Cardiovascular', 'Cardiovascular'), ('Piel', 'Piel'), ('Hiperactividad', 'Hiperactividad'), ('Ariticulaciones', 'Ariticulaciones')], default='Ninguna', max_length=255),
        ),
    ]
