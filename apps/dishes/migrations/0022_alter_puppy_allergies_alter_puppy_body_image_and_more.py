# Generated by Django 4.0.4 on 2022-11-02 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dishes', '0021_alter_puppy_allergies_alter_puppy_body_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puppy',
            name='allergies',
            field=models.CharField(choices=[('Cerdo', 'Cerdo'), ('Pescado', 'Pescado'), ('Pollo', 'Pollo'), ('Ninguna', 'Ninguna'), ('Huevo', 'Huevo'), ('Granos', 'Granos'), ('Otro', 'Otro'), ('Res', 'Res')], default='Ninguna', max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='body_image',
            field=models.CharField(choices=[('muy delgado', 'muy delgado'), ('peso ideal', 'peso ideal'), ('sobrepeso', 'sobrepeso'), ('delgado', 'delgado')], max_length=255),
        ),
        migrations.AlterField(
            model_name='puppy',
            name='special_needs',
            field=models.CharField(choices=[('Cancer', 'Cancer'), ('Cardiovascular', 'Cardiovascular'), ('Ganancia de peso', 'Ganancia de peso'), ('Digestión', 'Digestión'), ('Ninguna', 'Ninguna'), ('Diabetes', 'Diabetes'), ('Control de peso', 'Control de peso'), ('Hiperactividad', 'Hiperactividad'), ('Urinario-renal', 'Urinario-renal'), ('Ariticulaciones', 'Ariticulaciones'), ('Ansiedad', 'Ansiedad'), ('Aliento', 'Aliento'), ('Piel', 'Piel')], default='Ninguna', max_length=255),
        ),
        migrations.CreateModel(
            name='ContactDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email_contact', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dishes.puppy')),
            ],
        ),
    ]
