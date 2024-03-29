# Generated by Django 4.0.4 on 2023-05-14 15:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breeds',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('life_span', models.CharField(blank=True, max_length=255, null=True)),
                ('breed_group', models.CharField(blank=True, max_length=255, null=True)),
                ('image_url', models.CharField(blank=True, max_length=255, null=True)),
                ('breed_size', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name_contact', models.CharField(default='', max_length=255)),
                ('email_contact', models.CharField(default='', max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='default_name', max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('ingredients_description', models.TextField(blank=True, null=True)),
                ('nutrition_information', models.TextField(blank=True, null=True)),
                ('percents', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuSendData',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('days_interval', models.PositiveIntegerField(default=0)),
                ('last_sent_date', models.DateField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField(default=0)),
                ('age_type', models.CharField(choices=[('meses', 'meses'), ('años', 'años')], default='años', max_length=255)),
                ('body_image', models.CharField(choices=[('peso_ideal', 'peso_ideal'), ('sobrepeso', 'sobrepeso'), ('delgado', 'delgado'), ('muy_delgado', 'muy_delgado')], max_length=255)),
                ('reproductive_state', models.CharField(choices=[('entero', 'entero'), ('castrado', 'castrado')], max_length=255)),
                ('activity_level', models.CharField(max_length=255)),
                ('allergies', models.CharField(choices=[('Cerdo', 'Cerdo'), ('Huevo', 'Huevo'), ('Pescado', 'Pescado'), ('Granos', 'Granos'), ('Res', 'Res'), ('Otro', 'Otro'), ('Pollo', 'Pollo'), ('Ninguna', 'Ninguna')], default='Ninguna', max_length=255)),
                ('special_needs', models.CharField(choices=[('Diabetes', 'Diabetes'), ('Ganancia de peso', 'Ganancia de peso'), ('Aliento', 'Aliento'), ('Ninguna', 'Ninguna'), ('Ansiedad', 'Ansiedad'), ('Piel', 'Piel'), ('Ariticulaciones', 'Ariticulaciones'), ('Hiperactividad', 'Hiperactividad'), ('Urinario-renal', 'Urinario-renal'), ('Control de peso', 'Control de peso'), ('Digestión', 'Digestión'), ('Cancer', 'Cancer'), ('Cardiovascular', 'Cardiovascular')], default='Ninguna', max_length=255)),
                ('breed', models.CharField(blank=True, max_length=255, null=True)),
                ('weight', models.DecimalField(decimal_places=6, default=0.0, max_digits=12)),
                ('grams', models.DecimalField(decimal_places=6, default=0.0, max_digits=12)),
                ('grams_percent', models.DecimalField(decimal_places=6, default=0.0, max_digits=12)),
                ('points', models.IntegerField(default=0)),
                ('is_barf_active', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('owner_ip_mask', models.CharField(blank=True, max_length=255, null=True)),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dishes.menus')),
            ],
        ),
    ]
