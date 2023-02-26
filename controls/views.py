from django.shortcuts import render, redirect
from apps.dishes.models import Breeds, Puppy, Menus
from django.conf import settings
from django.contrib.auth.decorators import login_required

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json

# Create your views here.
def renderBreeds(request):
    breeds = Breeds.objects.all()

    context = {
        'breeds': breeds
    }
    return render(request, 'breeds.html', context)


def breedDetail(request, pk):
    breed = Breeds.objects.get(id=pk)

    if request.method == 'POST':
        breed.name = request.POST['name']
        breed.breed_size = request.POST['breed_size']
        breed.life_span = request.POST['life_span']

        breed.save()
        return redirect('breeds')

    context = {
        'breed': breed
    }

    return render(request, 'breed-detail.html', context)


@login_required(login_url='login')
def sendEmailButton(request):
    msg = 'click to send email'
    if request.method == 'POST':
        default_menu = "default"
        pets = Puppy.objects.all()

        supplier_data = {}
        total_menus = {}
        pets_grams = {}
        for pet in pets:
            menu = default_menu
            if pet.menu_id is not None:
                menu = pet.menu.name

            if menu not in supplier_data:
                supplier_data[menu] = 0

            if menu not in total_menus:
                total_menus[menu] = 0

            if pet not in pets_grams:
                pets_grams[pet.name + " 15 bolsas de " + pet.menu.name] = int(pet.grams)

            total_menus[menu] += 1
            supplier_data[menu] += int(pet.grams)


        kitchen_data = {}
        for k, v in supplier_data.items():
            percents = json.loads(Menus.objects.get(name=k).percents)
            
            if k == default_menu:
                percents = json.loads(Menus.objects.get().percents)

            for ingredient, percent in percents.items():
                if ingredient not in kitchen_data:
                    kitchen_data[ingredient] = 0

                kitchen_data[ingredient] += round((v * float(percent)) / 100)



        supplier_data_table = generate_html_table(supplier_data)
        total_menus_table = generate_html_table(total_menus, headers=['Nombre', 'Cantidad'])
        kitchen_data_table = generate_html_table(kitchen_data)
        pets_data_table = generate_html_table(pets_grams)

        # Crear un mensaje de correo electrónico
        de = settings.EMAIL_HOST_USER
        para = settings.EMAIL_RECEIVER
        asunto = 'Informe de datos'
        cuerpo = f"Supplier data: {supplier_data}\nTotal menus: {total_menus}\nKitchen data: {kitchen_data}"

        # Crear objeto MIMEMultipart
        mensaje = MIMEMultipart()

        # Agregar el cuerpo del mensaje
        # Crear la parte HTML del mensaje
        html = f"""\
        <html>
        <head></head>
        <body>
            <h1 style='text-align: center;'>Supplier Data</h1>
            {supplier_data_table}
            <h1 style='text-align: center;'>Total Menus</h1>
            {total_menus_table}
            <h1 style='text-align: center;'>Kitchen Data</h1>
            {kitchen_data_table}
            <h1 style='text-align: center;'>pets Data</h1>
            {pets_data_table}
        </body>
        </html>
        """
        part = MIMEText(html, 'html')
        mensaje.attach(part)
        # Configurar el servidor SMTP y autenticar la conexión
        servidor_smtp = 'smtp.gmail.com'
        puerto = 587
        user = settings.EMAIL_HOST_USER
        password = settings.EMAIL_PASSWORD

        smtp_server = smtplib.SMTP(servidor_smtp, puerto)
        smtp_server.starttls()
        smtp_server.login(user, password)

        # Enviar el correo electrónico
        mensaje['De'] = de
        mensaje['Para'] = para
        mensaje['Asunto'] = asunto
        smtp_server.sendmail(de, para, mensaje.as_string())
        smtp_server.quit()

        msg = 'email sent'

    context = {
        'page': 'menu-selection',
        'message': msg
    }

    return render(request, 'email-send.html', context)


def generate_html_table(data, headers=['Nombre', 'Gramos']):
    """
    Generates an HTML table from a dictionary where the keys are the rows and the values are dictionaries with columns
    """
    headers = headers
    rows = []
    for key, value in data.items():
        rows.append([key, value])
    html = "<table style='border-collapse: collapse; width: 50%; margin: 0 auto;'>"
    # Add table headers
    html += "<tr style='background-color: #f2f2f2; text-align: left;'>"
    for header in headers:
        html += f"<th style='padding: 8px; border: 1px solid #ddd;'>{header}</th>"
    html += "</tr>"
    # Add table rows
    for row in rows:
        html += "<tr>"
        for col in row:
            html += f"<td style='padding: 8px; border: 1px solid #ddd;'>{col}</td>"
        html += "</tr>"
    html += "</table>"
    return html
