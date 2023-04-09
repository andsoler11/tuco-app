# Generated by Django 4.0.4 on 2023-04-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0031_alter_puppy_age_type_alter_puppy_allergies_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puppy',
            name='allergies',
            field=models.CharField(choices=[('Pescado', 'Pescado'), ('Cerdo', 'Cerdo'), ('Ninguna', 'Ninguna'), ('Granos', 'Granos'), ('Huevo', 'Huevo'), ('Pollo', 'Pollo'), ('Otro', 'Otro'), ('Res', 'Res')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='body_image',
            field=models.CharField(choices=[('peso ideal', 'peso ideal'), ('muy delgado', 'muy delgado'), ('delgado', 'delgado'), ('sobrepeso', 'sobrepeso')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='special_needs',
            field=models.CharField(choices=[('Control de peso', 'Control de peso'), ('Piel', 'Piel'), ('Ninguna', 'Ninguna'), ('Cardiovascular', 'Cardiovascular'), ('Cancer', 'Cancer'), ('Ganancia de peso', 'Ganancia de peso'), ('Urinario-renal', 'Urinario-renal'), ('Ansiedad', 'Ansiedad'), ('Hiperactividad', 'Hiperactividad'), ('Aliento', 'Aliento'), ('Ariticulaciones', 'Ariticulaciones'), ('Digestión', 'Digestión'), ('Diabetes', 'Diabetes')], default='Ninguna', max_length=255),
        ),
    ]