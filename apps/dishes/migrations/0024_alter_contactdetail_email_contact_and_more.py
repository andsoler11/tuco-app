# Generated by Django 4.0.4 on 2022-11-02 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0023_alter_contactdetail_email_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetail',
            name='email_contact',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='contactdetail',
            name='name_contact',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='allergies',
            field=models.CharField(choices=[('Pescado', 'Pescado'), ('Res', 'Res'), ('Ninguna', 'Ninguna'), ('Huevo', 'Huevo'), ('Cerdo', 'Cerdo'), ('Granos', 'Granos'), ('Pollo', 'Pollo'), ('Otro', 'Otro')], default='Ninguna', max_length=255),
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
            field=models.CharField(choices=[('Piel', 'Piel'), ('Cancer', 'Cancer'), ('Control de peso', 'Control de peso'), ('Ninguna', 'Ninguna'), ('Ganancia de peso', 'Ganancia de peso'), ('Cardiovascular', 'Cardiovascular'), ('Hiperactividad', 'Hiperactividad'), ('Urinario-renal', 'Urinario-renal'), ('Ansiedad', 'Ansiedad'), ('Aliento', 'Aliento'), ('Ariticulaciones', 'Ariticulaciones'), ('Digestión', 'Digestión'), ('Diabetes', 'Diabetes')], default='Ninguna', max_length=255),
        ),
    ]