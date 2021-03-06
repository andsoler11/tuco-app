# Generated by Django 4.0.4 on 2022-07-20 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0019_alter_puppy_activity_level_alter_puppy_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puppy',
            name='allergies',
            field=models.CharField(choices=[('Granos', 'Granos'), ('Ninguna', 'Ninguna'), ('Pollo', 'Pollo'), ('Res', 'Res'), ('Pescado', 'Pescado'), ('Otro', 'Otro'), ('Huevo', 'Huevo'), ('Cerdo', 'Cerdo')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='body_image',
            field=models.CharField(choices=[('delgado', 'delgado'), ('sobrepeso', 'sobrepeso'), ('peso ideal', 'peso ideal'), ('muy delgado', 'muy delgado')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='special_needs',
            field=models.CharField(choices=[('Ariticulaciones', 'Ariticulaciones'), ('Urinario-renal', 'Urinario-renal'), ('Piel', 'Piel'), ('Ninguna', 'Ninguna'), ('Control de peso', 'Control de peso'), ('Hiperactividad', 'Hiperactividad'), ('Ganancia de peso', 'Ganancia de peso'), ('Ansiedad', 'Ansiedad'), ('Aliento', 'Aliento'), ('Diabetes', 'Diabetes'), ('Cancer', 'Cancer'), ('Digestión', 'Digestión'), ('Cardiovascular', 'Cardiovascular')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='weight',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=12),
        ),
    ]
