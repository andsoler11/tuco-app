import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from apps.users.models import CustomUser, Orders
from .forms import CustomUserCreationForm
from utils.privacy import Privacy
from django.contrib.auth.decorators import login_required
from apps.users.utils import *
from apps.dishes.models import Menus, Pet, ContactDetail
from apps.dishes.utils import *
from django.http import JsonResponse
import urllib

privacy = Privacy()


def renderHomepage(request):
    """Render the homepage"""
    context = {'page': 'homepage'}
    return render(request, 'homepage.html', context)


def userLogin(request):
    """function to login a user"""
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('dishes')

    # if request.method == 'POST':
    #     username = request.POST['email'].lower()
    #     password = request.POST['password']
    #     username_mask = privacy.secure_email(username)['mask']
    #
    #     try:
    #         user = CustomUser.objects.get(username=username_mask)
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('dishes')
    #         else:
    #             messages.error(request, 'Usuario o contraseña incorrectos')
    #     except:
    #         messages.error(request, 'El usuario no existe')

    return render(request, 'users/login_register.html', context)


def registerUser(request):
    """Registros de usuario"""
    page = 'register'
    form = CustomUserCreationForm

    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         email_secured = privacy.secure_email(user.email)
    #         if CustomUser.objects.filter(email_hash=email_secured['hash']).exists():
    #             messages.error(request, 'Este correo ya está registrado')
    #             return redirect('register')
    #
    #         user.username = email_secured['mask']
    #         user.email = email_secured['encrypted']
    #         user.email_mask = email_secured['mask']
    #         user.email_hash = email_secured['hash']
    #
    #         phone = user.phone_number
    #         user.phone_number = privacy.encrypt(phone)
    #         user.phone_number_mask = Privacy.mask_phone_number(phone)
    #
    #         user.full_name = privacy.encrypt(user.full_name)
    #         user.save()
    #
    #         messages.success(request, '¡Te has registrado exitosamente!')
    #         login(request, user)
    #         return redirect('dishes')
    #
    #     else:
    #         for msg in form.errors:
    #             messages.error(request, f"{form.errors[msg]}")
    

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def recoverPassword(request):
    """Render recover password page"""
    if request.method == 'POST':
        requested_email = request.POST['email'].lower()
        try:
            user = CustomUser.objects.get(email_hash=privacy.hash_string(requested_email))
        except:
            messages.error(request, 'El email no existe')
            return redirect('recover-password')
        
        if send_recovery_email(request, requested_email):
            messages.error(request, f'Ha ocurrido un error al enviar el correo electrónico')
            return redirect('recover-password')

        messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para recuperar tu contraseña')

    context = {'page': 'recoverPassword'}
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def newPassword(request):
    """Render new password page"""
    if request.method == 'POST':
        actual_password = request.POST.get('actual_password')
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if actual_password and not request.user.check_password(actual_password):
            messages.error(request, 'La contraseña actual no es correcta')
            return redirect('new-password')

        if password == confirm_password:
            if not validate_password(request, password):
                return redirect('new-password')
            user = CustomUser.objects.get(id=request.user.id)
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, 'contraseña actualizada')
            return redirect('profile')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('new-password')
            
    context = {'page': 'newPassword'}
    return render(request, 'users/login_register.html', context)


def newPasswordToken(request):
    """Render new password page"""
    if not request.GET.get('token'):
        messages.error(request, 'No se ha enviado un token')
        return redirect('recover-password')
    
    reset_token = request.GET.get('token')
    email = cache.get(reset_token)

    if request.method == 'POST':
        if not request.GET.get('token'):
            messages.error(request, 'Token inválido o expirado')
            return redirect('recover-password')

        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password == confirm_password:
            if not validate_password(request, password):
                redirect_url = f'/new-password-token/?token={reset_token}'
                return redirect(redirect_url)

            user = CustomUser.objects.get(email_hash=privacy.hash_string(email))
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, 'contraseña actualizada')
            return redirect('profile')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('new-password')

    if not email:
        # Reset token is invalid or expired
        messages.error(request, 'Token inválido o expirado')
        return redirect('recover-password')
    
    user = CustomUser.objects.get(email_hash=privacy.hash_string(email))
    if user is None:
        messages.error(request, 'Token inválido o expirado')
        return redirect('recover-password')

    context = {'page': 'newPassword', 'email': email}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.info(request, 'Sesión cerrada')
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    """Render user dashboard"""
    user_data = CustomUser.objects.get(id=request.user.id)
    if user_data.full_name:
        user_data.full_name = privacy.decrypt(user_data.full_name)
    context = {'page': 'profile', 'user_data': user_data}
    return render(request, 'users/dashboard.html', context)

@login_required(login_url='login')
def account(request):
    """Render My Data page"""
    user_data = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        name = request.POST['name']
        if len(name) > 50:
            messages.error(request, 'El nombre es demasiado largo')
            return redirect('account')
        
        if len(name) < 3:
            messages.error(request, 'El nombre es demasiado corto')
            return redirect('account')

        if not name.replace(" ", "").isalpha():
            messages.error(request, 'El nombre es inválido')
            return redirect('account')

        user_data.full_name = privacy.encrypt(request.POST['name'])
        user_data.phone_number = privacy.encrypt(request.POST['phone'])
        user_data.phone_number_mask = Privacy.mask_phone_number(request.POST['phone'])
        user_data.save()
        messages.success(request, 'Datos actualizados')

    user_data.email = privacy.decrypt(user_data.email)
    if user_data.full_name:
        user_data.full_name = privacy.decrypt(user_data.full_name)
    if user_data.phone_number:
        user_data.phone_number = privacy.decrypt(user_data.phone_number)
    context = {'page': 'account', 'user_data': user_data}
    return render(request, 'users/account.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required(login_url='login')
def myAddresses(request):
    """Render My Addresses page"""
    user = CustomUser.objects.get(id=request.user.id)
    context = {'page': 'addresses'}
    if user.addresses:
        addresses = json.loads(user.addresses)
        for address in addresses:
            address['address'] = privacy.decrypt(address['address'])
            address['user_phone'] = privacy.decrypt(address['user_phone'])
            address['display_address'] = f"{address['address']}, {address['depto']}, {address['city']}"

        context['addresses'] = addresses
    return render(request, 'users/addresses.html', context)


@login_required(login_url='login')
def newAddress(request):
    context = {'page': 'new-address'}
    if request.method == 'POST':
        message = validate_address(request)
        if message != 'ok':
            messages.error(request, message)
            return redirect('new-address')

        user = CustomUser.objects.get(id=request.user.id)

        addresses = []
        if user.addresses:
            addresses = json.loads(user.addresses)

        new_address = {
            'name': request.POST['name_address'],
            'address': privacy.encrypt(request.POST['address']),
            'additional_info': request.POST['additional_info'],
            'depto': request.POST['depto'],
            'city': request.POST['city'],
            'user_phone': privacy.encrypt(request.POST['user_phone']),
        }

        addresses.append(new_address)
        user.addresses = json.dumps(addresses)
        user.save()
        messages.success(request, 'Dirección agregada correctamente')
        return redirect('addresses')

    return render(request, 'users/new-address.html', context)

@login_required(login_url='login')
def addressDetail(request, pk):
    """Render detail address"""

    user = CustomUser.objects.get(id=request.user.id)
    addresses = json.loads(user.addresses)
    
    for address in addresses:
        if address['name'] == pk:
            address['address'] = privacy.decrypt(address['address'])
            address['user_phone'] = privacy.decrypt(address['user_phone'])
            
            if request.method == 'POST':
                message = validate_address(request)
                if message != 'ok':
                    messages.error(request, message)
                    return redirect('address-detail', pk)

                user = CustomUser.objects.get(id=request.user.id)

                addresses = []
                if user.addresses:
                    addresses = json.loads(user.addresses)

                new_address = {
                    'name': request.POST['name_address'],
                    'address': privacy.encrypt(request.POST['address']),
                    'additional_info': request.POST['additional_info'],
                    'depto': request.POST['depto'],
                    'city': request.POST['city'],
                    'user_phone': privacy.encrypt(request.POST['user_phone']),
                }

                # delete old address
                for address in addresses:
                    if address['name'] == pk:
                        addresses.remove(address)
                        break

                addresses.append(new_address)
                user.addresses = json.dumps(addresses)
                user.save()
                messages.success(request, 'Dirección actualizada correctamente')
                return redirect('addresses')
            
            context = {'page': 'address-detail', 'address': address}
            return render(request, 'users/address-detail.html', context)

    context = {'page': 'address-detail'}
    return render(request, 'users/address-detail.html', context)


def addressDelete(request, pk):
    """Delete address"""
    user = CustomUser.objects.get(id=request.user.id)
    addresses = json.loads(user.addresses)
    for address in addresses:
        if address['name'] == pk:
            addresses.remove(address)
            user.addresses = json.dumps(addresses)
            user.save()
            messages.success(request, 'Dirección eliminada correctamente')
            return redirect('addresses')

    messages.error(request, 'Dirección no encontrada')
    return redirect('addresses')

def paymentMethods(request):
    """Render payment methods list"""
    context = {'page': 'payment-methods'}
    return render(request, 'users/payment-methods.html', context)

def newPaymentMethod(request):
    """Render new payment methods form"""
    context = {'page': 'new-method'}
    return render(request, 'users/new-method.html', context)

def paymentMethodDetail(request):
    """Render payment method detail"""
    context = {'page': 'method-detail'}
    return render(request, 'users/method-detail.html', context)

def checkout(request):
    """Render checkout page"""
    cart_items = request.session.get('cart_items', {})
    if not cart_items:
        messages.error(request, 'No tienes productos en tu carrito')
        return redirect('home')

    for key, value in cart_items.items():
        menu = Menus.objects.get(id=key)
        cart_items[key]['name'] = menu.name
        cart_items[key]['price_total'] = int(value['quantity']) * int(value['price_month'])

    if request.method == 'POST':
        get_total_cart(cart_items)
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_phone = request.POST['phone']
        user = CustomUser.objects.get(id=request.user.id)
        pets = Pet.objects.filter(owner=user)

        address = request.POST['address']
        aditional_info = request.POST['additional_info']
        depto = request.POST['depto']
        city = request.POST['city']

        address_complete = {
            'address': address,
            'aditional_info': aditional_info,
            'depto': depto,
            'city': city,
        }

        delivery_time = request.POST['tipo-envio']
        # promo_code = request.POST['promo-code']
        promo_code = ''
        total_price = cart_items['total']['price_month']
        total_items = cart_items['total']['quantity']
        # payment_method = request.POST['metodo-pago']
        payment_method = 'whatsapp'

        # get a json with the items in the cart but without the total key
        items = json.dumps({key: value for key, value in cart_items.items() if key != 'total'})

        order = Orders(
            user=user,
            items=items,
            total_price=total_price,
            total_products=total_items,
            promo_code=promo_code,
            address=json.dumps(address_complete),
            delivery_time=delivery_time,
            payment_method=payment_method,
            status='pending',
        )

        order.save()
  

        # format the total price
        total_price = f'{total_price:,}'

        # format the items to fet the menu name, quantity and price
        items = json.loads(items)
        items = [f'{value["name"]} x {value["quantity"]} = {value["price_total"]}' for key, value in items.items()]

        # format the items to be in a single string
        items = '\n'.join(items)

        # format the address
        address = f'{address}, {depto}, {city}, {aditional_info}'
        address = address.replace('\n', ' ')

        # format the pets to be in a single string
        pet_ids_in_cart = [value['pet_id'] for key, value in cart_items.items() if key != 'total']
        pets = [f'{pet.name} ({pet.breed})' for pet in pets if str(pet.id) in pet_ids_in_cart]
        pets = ', '.join(pets)

        # format the message to be sent to whatsapp
        message = f"""Hola, soy {user_name} y acabo de hacer un pedido en la página web de Foreverdog. Mi correo es {user_email} y mi teléfono es {user_phone}. Mi pedido es el siguiente: \n\n
                    id del pedido: {order.id}\n
                    total mes: {total_price}\n
                    menus: {items}\n
                    dirección: {address}\n
                    mis mascotas: {pets}\n"""

        # encode the message
        message = urllib.parse.quote(message)
        whatsapp_url = f'https://wa.me/3006235504?text={message}'

        # Redirect the user to the WhatsApp URL
        return redirect(whatsapp_url)


    cart_items = get_total_cart(cart_items)
    context = {'page': 'checkout', 'cart_items': cart_items}
    return render(request, 'users/checkout.html', context)

def validate_address(request):
    """Validate address"""
    output_message = 'ok'

    required_fields = ['depto', 'city', 'address', 'user_phone', 'name_address']
    for field in required_fields:
        if not request.POST.get(field):
            output_message = f'El campo {field} es requerido'

    name_address = request.POST['name_address']
    if len(name_address) > 50:
        output_message = 'El nombre es demasiado largo'

    if len(name_address) < 3:
        output_message = 'El nombre es demasiado corto'

    address = request.POST['address']
    if len(address) > 50:
        output_message = 'La dirección es demasiado larga'

    if len(address) < 3:
        output_message = 'La dirección es demasiado corta'

    return output_message


def add_to_cart(request, menu_id, pet_id):
    pet = Pet.objects.get(id=pet_id)
    menu = Menus.objects.get(id=menu_id)

    if not pet:
        messages.error(request, 'No se ha encontrado la mascota')
        return redirect('home')

    pet.menu = menu
    pet.save()

    return render(request, 'temporally_message.html')

    # """Add product to cart"""
    # puppy = Pet.objects.get(id=pet_id)
    #
    # menu = Menus.objects.get(id=menu_id)
    # item_to_cart = {}
    # item_to_cart['price'] = get_price_from_weight(float(puppy.grams), float(menu.price_per_100_grams))
    # item_to_cart['price_month'] = round(item_to_cart['price'] * 30, -3)
    # item_to_cart['pet_name'] = puppy.name
    # item_to_cart['menu_id'] = menu_id
    # item_to_cart['pet_id'] = pet_id
    # item_to_cart['quantity'] = 1
    #
    # cart_items = request.session.get('cart_items', {})
    # if menu_id in cart_items:
    #     cart_items[menu_id]['quantity'] += 1
    #
    # cart_items[menu_id] = item_to_cart
    # request.session['cart_items'] = cart_items
    #
    # return redirect('cart')


def cart(request):
    """Render cart page"""
    cart_items = request.session.get('cart_items', {})

    for key, item in cart_items.items():
        menu = Menus.objects.get(id=item['menu_id'])
        item['menu_name'] = menu.name

    cart_items = get_total_cart(cart_items)
    context = {'page': 'cart', 'cart_items': cart_items}
    return render(request, 'users/cart.html', context)


def update_session(request):
    if request.method == 'POST':
        menu_id = request.POST.get('menuId')
        quantity = request.POST.get('quantity')

        # Update the session with the new quantity        
        request.session['cart_items'][menu_id]['quantity'] = int(quantity)
        request.session.modified = True

        return JsonResponse({'message': 'Quantity stored in session successfully.'})

    return JsonResponse({'error': 'Invalid request method.'})


def get_total_cart(cart_items):
    cart_items['total'] = {}
    cart_items['total']['price'] = 0
    cart_items['total']['price_month'] = 0
    cart_items['total']['quantity'] = 0
    for key, item in cart_items.items():
        if key != 'total':
            cart_items['total']['price'] += item['price'] * item['quantity']
            cart_items['total']['price_month'] += item['price_month'] * item['quantity']
            cart_items['total']['quantity'] += item['quantity']

    return cart_items


def remove_item_cart(request, menu_id):
    if request.method == 'POST':   
        del request.session['cart_items'][menu_id]
        request.session.modified = True

        return redirect('cart')

    return redirect('cart')


def buy_now(request, menu_id, pet_id):
    puppy = Pet.objects.get(id=pet_id)

    menu = Menus.objects.get(id=menu_id)

    item_to_cart = {}
    item_to_cart['price'] = get_price_from_weight(float(puppy.grams), float(menu.price_per_100_grams))
    item_to_cart['price_month'] = round(item_to_cart['price'] * 30, -3)
    item_to_cart['pet_name'] = puppy.name
    item_to_cart['menu_id'] = menu_id
    item_to_cart['pet_id'] = pet_id
    item_to_cart['quantity'] = 1

    cart_items = {}
    cart_items[menu_id] = item_to_cart
    request.session['cart_items'] = cart_items

    return redirect('checkout')

def temporal_checkout_redirect_whatsapp(request, menu_id, pet_id):
    puppy = Pet.objects.get(id=pet_id)
    menu = Menus.objects.get(id=menu_id)

    contact = ContactDetail.objects.get(pet=puppy)
    email_contact = privacy.decrypt(contact.email_contact)

    price = get_price_from_weight(float(puppy.grams), float(menu.price_per_100_grams))
    price_month = round(price * 30, -3)

    message = f"""Hola, soy {contact.name_contact} y acabo de hacer un pedido en la página web de Foreverdog. Mi correo es {email_contact}. Mi pedido es el siguiente: \n
                menu: {menu.name}\n
                precio: {price_month} mensual\n
                mascota: {puppy.name}\n
                """

    message = urllib.parse.quote(message)
    whatsapp_url = f'https://wa.me/3006235504?text={message}'

    return redirect(whatsapp_url)
