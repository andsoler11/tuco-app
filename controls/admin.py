from django.contrib import admin
from django.shortcuts import render
from .models import Email

from apps.dishes.models import Breeds, Pet, Menus
from django.conf import settings

import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def generate_html_data(pets_menus, total_menus, pets_grams, menu_ingredients):
    # Start with an empty string for the HTML
    html_data = ""

    # Loop through each pet in the pets_menus dict
    for pet_name, pet_data in pets_menus.items():
        # Add the pet name to the HTML
        html_data += f"<h3 style='text-align: center;'>{pet_name} GRAMOS: {round(float(pet_data['grams']), 0)}</h3>"

        # Add a table for the menus for this pet
        html_data += "<table style='border-collapse: collapse; width: 50%; margin: 0 auto;'>"
        html_data += "<tr><th style='padding: 8px; border: 1px solid #ddd;'>Menus</th></tr>"
        for menu in pet_data['menus']:
            html_data += f"<tr><td style='padding: 8px; border: 1px solid #ddd;'>{menu}</td></tr>"
        html_data += "</table>"

    html_data += "<br><br><br>"
    html_data += f"<h1 style='text-align: center;'>MORE DATA</h1>"
    # Add a table for the total weeks for each menu
    html_data += "<table style='border-collapse: collapse; width: 50%; margin: 0 auto;'>"
    html_data += "<tr><th style='padding: 8px; border: 1px solid #ddd;'>Menu</th><th style='padding: 8px; border: 1px solid #ddd;'>Total Weeks</th></tr>"
    for menu, weeks in total_menus.items():
        if menu.startswith("total semanas "):
            menu_name = menu.split("total semanas ")[1]
            html_data += f"<tr><td style='padding: 8px; border: 1px solid #ddd;'>{menu_name}</td><td style='padding: 8px; border: 1px solid #ddd;'>  {weeks}</td></tr>"
    html_data += "</table>"
    html_data += "<br><br><br>"
    # Add a table for the total grams per menu
    html_data += "<table style='border-collapse: collapse; width: 50%; margin: 0 auto;'>"
    html_data += "<tr><th style='padding: 8px; border: 1px solid #ddd;'>Menu</th><th style='padding: 8px; border: 1px solid #ddd;'>Total Grams</th></tr>"
    for menu, grams in pets_grams.items():
        if menu.startswith("total gramos"):
            menu_name = menu.split("total gramos")[1]
            html_data += f"<tr><td style='padding: 8px; border: 1px solid #ddd;'>{menu_name}</td><td style='padding: 8px; border: 1px solid #ddd;'>{grams}</td></tr>"
    html_data += "</table>"
    html_data += "<br><br><br>"
    # Add a table for the total grams per ingredient of menu
    html_data += "<table style='border-collapse: collapse; width: 50%; margin: 0 auto;'>"
    html_data += "<tr><th style='padding: 8px; border: 1px solid #ddd;'>Ingredient</th><th style='padding: 8px; border: 1px solid #ddd;'>Total Grams</th></tr>"
    for ingredient, grams in menu_ingredients.items():
        html_data += f"<tr><td style='padding: 8px; border: 1px solid #ddd;'>{ingredient}</td><td style='padding: 8px; border: 1px solid #ddd;'>{grams}</td></tr>"
    html_data += "</table>"

    # Return the HTML data
    return html_data


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'to_address', 'cc_address', 'sent_at')
    list_filter = ('to_address', 'sent_at')
    search_fields = ('subject', 'to_address', 'sent_at')

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('send-email/', self.admin_site.admin_view(self.send_custom_email_view), name='send_custom_email'),
            # /admin/controls/email/send-email/
        ]
        return custom_urls + urls

    def send_custom_email_view(self, request):
        msg = 'click to send email'
        if request.method == 'POST':
            # start the default menu
            default_menu = "default"

            # get all the pets
            pets = Pet.objects.all()

            # start the dicts of the data needed
            pets_menus = {}
            total_menus = {}
            pets_grams = {}

            # start the iteration for the pets
            for pet in pets:
                # if the pet has no menu, continue
                if pet.menu_id is None:
                    continue
                menu = pet.menu.name
                pets_menus[pet.name] = {'menus': [], 'grams': 0}
                barf_active = pet.is_barf_active

                # get the number of weeks for the selected menu depending on the barf active
                num_weeks_selected_menu = 4
                num_weeks_iniciacion_menu = 0
                if barf_active == "no":
                    num_weeks_selected_menu = 3
                    num_weeks_iniciacion_menu = 1

                # calculate the total grams for the selected menu
                daily_grams = pet.grams
                total_grams_selected_menu = daily_grams * 7 * num_weeks_selected_menu
                if num_weeks_iniciacion_menu > 0:
                    total_grams_iniciacion_menu = daily_grams * 7 * num_weeks_iniciacion_menu
                    menu_iniciacion = Menus.objects.get(name='Iniciación')

                    if "total semanas " + menu_iniciacion.name not in total_menus:
                        total_menus["total semanas " + menu_iniciacion.name] = 0

                    if "total gramos" + menu_iniciacion.name not in pets_grams:
                        pets_grams["total gramos" + menu_iniciacion.name] = 0

                    total_menus["total semanas " + menu_iniciacion.name] += num_weeks_iniciacion_menu
                    pets_grams["total gramos" + menu_iniciacion.name] += float(total_grams_iniciacion_menu)

                    if menu_iniciacion.name not in pets_menus[pet.name]:
                        pets_menus[pet.name]['menus'].append(menu_iniciacion.name)

                # calculate the total grams for the selected menu
                if "total semanas " + menu not in total_menus:
                    total_menus["total semanas " + menu] = 0

                if "total gramos" + menu not in pets_grams:
                    pets_grams["total gramos" + menu] = 0

                total_menus["total semanas " + menu] += num_weeks_selected_menu
                pets_grams["total gramos" + menu] += float(total_grams_selected_menu)
                pets_menus[pet.name]['menus'].append(menu)
                pets_menus[pet.name]['grams'] = daily_grams

            kitchen_data = {}
            for k, v in pets_grams.items():
                k = k.replace("total gramos", "")
                percents = json.loads(Menus.objects.get(name=k).percents)
                for ingredient, percent in percents.items():
                    if ingredient not in kitchen_data:
                        kitchen_data[ingredient] = 0

                    kitchen_data[ingredient] += round((v * float(percent)) / 100)

            html_output = generate_html_data(pets_menus, total_menus, pets_grams, kitchen_data)
            mensaje = MIMEMultipart()

            html = f"""\
                <html>
                <head></head>
                <body>
                    <h1 style='text-align: center;'>DATA</h1>
                    {html_output}
                </body>
                </html>
                """
            part = MIMEText(html, 'html')
            mensaje.attach(part)

            servidor_smtp = 'smtp.gmail.com'
            puerto = 587
            user = settings.EMAIL_HOST_USER
            password = settings.EMAIL_PASSWORD

            smtp_server = smtplib.SMTP(servidor_smtp, puerto)
            smtp_server.starttls()
            smtp_server.login(user, password)

            mensaje['De'] = settings.EMAIL_HOST_USER
            mensaje['Para'] = settings.EMAIL_RECEIVER
            mensaje['Asunto'] = 'Informe de datos'
            smtp_server.sendmail(mensaje['De'], mensaje['Para'], mensaje.as_string())
            smtp_server.quit()

            msg = 'Culpa de Ed'

            email_data = Email(
                subject='Informe de datos',
                body=json.dumps(html_output),
                from_address=settings.EMAIL_HOST_USER,
                to_address=settings.EMAIL_RECEIVER,
            )

            email_data.save()


        context = {
            'page': 'menu-selection',
            'message': msg
        }

        return render(request, 'email-send.html', context)

