# Generated by Django 4.0.4 on 2022-11-02 21:30

from django.db import migrations, models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dishes', '0022_alter_puppy_allergies_alter_puppy_body_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puppy',
            name='allergies',
            field=models.CharField(choices=[('Cerdo', 'Cerdo'), ('Otro', 'Otro'), ('Res', 'Res'), ('Granos', 'Granos'), ('Ninguna', 'Ninguna'), ('Pescado', 'Pescado'), ('Huevo', 'Huevo'), ('Pollo', 'Pollo')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='body_image',
            field=models.CharField(choices=[('peso ideal', 'peso ideal'), ('delgado', 'delgado'), ('sobrepeso', 'sobrepeso'), ('muy delgado', 'muy delgado')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='reproductive_state',
            field=models.CharField(choices=[('entero', 'entero'), ('castrado', 'castrado')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='special_needs',
            field=models.CharField(choices=[('Digestión', 'Digestión'), ('Ariticulaciones', 'Ariticulaciones'), ('Hiperactividad', 'Hiperactividad'), ('Piel', 'Piel'), ('Ganancia de peso', 'Ganancia de peso'), ('Ansiedad', 'Ansiedad'), ('Control de peso', 'Control de peso'), ('Cancer', 'Cancer'), ('Urinario-renal', 'Urinario-renal'), ('Cardiovascular', 'Cardiovascular'), ('Aliento', 'Aliento'), ('Ninguna', 'Ninguna'), ('Diabetes', 'Diabetes')], default='Ninguna', max_length=255),
        ),
        migrations.CreateModel(
            name='ContactDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email_contact', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name_contact', models.CharField(max_length=255)),
                ('pet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dishes.puppy')),
            ],
        ),
    ]