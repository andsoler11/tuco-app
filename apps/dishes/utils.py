import re
import json
import math

SUPLEMENTOS = {
    'huevo_codorniz_semana': {
        9: 2,  # hasta 9 kilos
        15: 4,  # hasta 15 kilos
        30: 7,  # hasta 30 kilos
        60: 10,  # mas de 30 kilos
    },
    'omega_3_diario': {
        0: 1000,  # menos de 10 kilos, 1000 gramos (1 capsula) diaria
        10: 1300,  # hasta 10 kilos, 1300 gramos (1 capsula) diarias
    },
    'kefir_diario': {
        0: '1 cucharadita',  # menos de 10 kilos
        10: '1 cucharada',  # hasta 10 kilos
    },
    'caldo_de_huesos_diario': {
        0: '1/2 cucharadita',  # menos de 10 kilos
        10: '1 cucharadita',  # hasta 10 kilos
    },
    'arandanos_diario': {
        0: 15,  # menos de 10 kilos, 15 gramos diarios
        10: 30,  # hasta 10 kilos, 30 gramos diarios
    }
}


def get_ingredients_percent(grams, natural_food='yes'):
    percent_ingredients = {}
    percent_ingredients['hueso carnoso'] = round((grams * 40) / 100)
    percent_ingredients['carnes'] = round((grams * 35) / 100)
    percent_ingredients['fruta/verdura'] = round((grams * 10) / 100)
    percent_ingredients['higado'] = round((grams * 5) / 100)
    percent_ingredients['visceras'] = round((grams * 10) / 100)

    if natural_food == 'no':
        percent_ingredients = {}
        percent_ingredients['carnes'] = round((grams * 80) / 100)
        percent_ingredients['fruta'] = round((grams * 5) / 100)
        percent_ingredients['verdura'] = round((grams * 5) / 100)
        percent_ingredients['higado'] = round((grams * 5) / 100)
        percent_ingredients['visceras'] = round((grams * 5) / 100)

    return percent_ingredients


def body_points(body_image):
    if body_image == 'sobrepeso':
        points = -2
    elif body_image == 'peso_ideal':
        points = 2
    elif body_image == 'delgado':
        points = 3
    else:
        points = 4

    return points


def activity_points(activity_level):
    if activity_level == 'bajo':
        points = 0
    elif activity_level == 'medio':
        points = 2
    else:
        points = 4

    return points


def activity_mapping(activity_choice):
    activity_choices = {
        'sedentario': 'bajo',
        'actividad media': 'medio',
        'muy activo': 'alto',
    }

    return activity_choices[activity_choice]


def reproductive_mapping(reproductive_choice):
    reproductive_choices = {
        '1': 'castrado',
        '2': 'entero',
    }

    return reproductive_choices[reproductive_choice]


def reproductive_state_points(reproductive_state):
    if reproductive_state == 'castrado':
        points = 1
    else:
        points = 2

    return points


def format_weight(weight_input):
    if '.' in weight_input or ',' in weight_input:
        weight = float(weight_input)
    else:
        weight = int(weight_input)

    return weight


def determine_grams(activity_level, reproductive_state, body_image, weight, age_type, age):
    if age_type == 'meses' and int(age) <= 12:
        grams = round((6 * weight) * 10, 2)
        grams_percent = 6
        points = 0

        return grams, grams_percent, points
    elif age_type == 'meses' and int(age) > 12:
        age = round(int(age) / 12, 2)

    # starting getting the points from the variables
    points = 0
    points += reproductive_state_points(reproductive_state)
    points += body_points(body_image)
    points += activity_points(activity_level)

    # determine the size of the dog by his weight
    if weight <= 5:
        size_percent = 'mini'
    elif weight > 5 and weight <= 9:
        size_percent = 'small'
    elif weight > 9 and weight <= 20:
        size_percent = 'medium'
    elif weight > 20 and weight <= 35:
        size_percent = 'large'
    else:
        size_percent = 'extra_large'

    # # percents array
    percents = {
        'mini': [4.2, 4.4, 4.6, 5.2, 5.5, 5.7],
        'small': [4, 4.5, 4.8, 5.5, 5.8, 6],
        'medium': [2.3, 2.5, 2.7, 3.3, 3.8, 4.0],
        'large': [1.8, 2, 2.2, 2.67, 3.1, 3.3],
        'extra_large': [1.4, 1.6, 1.8, 2.2, 2.5, 2.7],
    }

    index_number = 5
    if points <= 0:
        index_number = 0
    if 1 <= points <= 2:
        index_number = 1
    elif 3 <= points <= 4:
        index_number = 2
    elif 5 <= points <= 6:
        index_number = 3
    elif 7 <= points <= 8:
        index_number = 4

    grams_percent = percents[size_percent][index_number]

    grams = round((grams_percent * weight) * 10, 0)

    return grams, grams_percent, points



# def calculate_barf_food_amount(castrated, already_eating_barf, activity_level, weight_kg, body_condition_score):
#     # Calculate resting energy requirements (RER) based on weight and age
#     weight_lbs = weight_kg * 2.20462  # convert weight from kg to lbs
#     if weight_lbs <= 4.4:
#         rer = 70 * weight_lbs ** 0.75
#     elif 4.4 < weight_lbs <= 99:
#         rer = 30 * weight_lbs + 70
#     else:
#         rer = 70 * weight_lbs + 30

#     # Adjust RER based on activity level
#     if activity_level == 'bajo':
#         rer *= 1.2
#     elif activity_level == 'medio':
#         rer *= 1.5
#     else:
#         rer *= 2.0

#     # Adjust RER based on body condition score
#     if body_condition_score == 'muy_delgado':
#         rer *= 1.5
#     elif body_condition_score == 'delgado':
#         rer *= 1.2
#     elif body_condition_score == 'peso_ideal':
#         rer *= 1.0
#     elif body_condition_score == 'sobrepeso':
#         rer *= 0.7
#     else:
#         rer *= 0.6

#     # Adjust RER based on castration status
#     if castrated == 'castrado':
#         rer *= 0.8

#     # Adjust RER based on whether already eating BARF
#     if already_eating_barf == 'yes':
#         rer *= 1.1

#     # Calculate amount of food in grams per day based on RER and typical BARF diet proportions
#     protein_percentage = 0.15
#     fat_percentage = 0.2
#     carbohydrate_percentage = 0.05
#     kcal_per_gram_protein = 3.5
#     kcal_per_gram_fat = 8.5
#     kcal_per_gram_carbohydrate = 3.5
#     grams_per_kcal = 1 / ((protein_percentage * kcal_per_gram_protein) + (fat_percentage * kcal_per_gram_fat) + (carbohydrate_percentage * kcal_per_gram_carbohydrate))
#     food_amount = rer * grams_per_kcal

#     return round(food_amount, 1)



def get_percents_data(total_grams, grams_dict):
    percents_data = {}
    for key, value in grams_dict.items():
        percents_data[key] = round((value * 100) / total_grams, 2)

    return percents_data


def validate_age_inputs(age_input, age_type_input):
    if age_type_input == 'months' and int(age_input) > 12:
        age_input = round(int(age_input) / 12, 0)
        age_type_input = 'years'

    return age_input, age_type_input


# def get_suplements_data(age_type, age, weight, natural_food):
#     suplements_data = {}
#     if age_type == 'years':
#         if int(age) < 1:
#             suplements_data['huevo_codorniz_semana'] = SUPLEMENTOS['huevo_codorniz_semana'][9]
#             suplements_data['omega_3_diario'] = SUPLEMENTOS['omega_3_diario'][0]
#             suplements_data['kefir_diario'] = SUPLEMENTOS['kefir_diario'][0]
#             suplements_data['caldo_de_huesos_diario'] = SUPLEMENTOS['caldo_de_huesos_diario'][0]
#             suplements_data['arandanos_diario'] = SUPLEMENTOS['arandanos_diario'][0]
#         elif int(age) >= 1 and int(age) <= 2:
#             suplements_data['huevo_codorniz_semana'] = SUPLEMENTOS['huevo_codorniz_semana'][15]
#             suplements_data['omega_3_diario'] = SUPLEMENTOS['omega_3_diario'][10]
#             suplements_data['kefir_diario'] = SUPLEMENTOS['kefir_diario'][10]
#             suplements_data['caldo_de_huesos_diario'] = SUPLEMENTOS['caldo_de_huesos_diario'][10]
#             suplements_data['arandanos_diario'] = SUPLEMENTOS['arandanos_diario'][10]
#         elif int(age) >= 3 and int(age) <= 4:
#             suplements_data['huevo_codorniz_semana'] = SUPLEMENTOS['huevo_codorniz_semana'][30]
#             suplements_data['omega_3_diario'] = SUPLEMENTOS['omega_3_diario'][10]
#             suplements_data['kefir_diario'] = SUPLEMENTOS['kefir_diario'][10]
#             suplements_data['caldo_de_huesos_diario'] = SUPLEMENTOS['caldo_de_huesos_diario'][10]
#             suplements_data['arandanos_diario'] = SUPLEMENTOS['arandanos_diario'][10]
#         elif int(age) >= 5 and int(age) <= 7:
#             suplements_data['huevo_codorniz_semana'] = SUPLEMENTOS['huevo_codorniz_semana'][60]
#             suplements


def convert_string_to_array(string):
    array = string.split('\r\n')
    upload_array = {}

    for item in array:
        item = item.strip()
        if item == '':
            continue

        if re.search(r'\d+', item):
            number = re.findall(r'\d+', item)
            ingredient = re.findall(r'\D+', item)
            ingredient_name = ingredient[0].strip()

            if len(number) > 1:
                number = number[0] + '.' + number[1]
            else:
                number = number[0]

            upload_array[ingredient_name] = number

    return upload_array


def convert_json_to_string(json_string):
    array = json.loads(json_string)
    output_string = ''
    for k, v in array.items():
        output_string += f'{k} {v}% \r\n'

    return output_string


def get_price_from_weight(grams, price):
    if price <= 0:
        price = 2220

    if grams <= 345:
        price = price
    elif grams > 345 and grams <= 500:
        price = (price - (price * 0.11))
    elif grams > 500 and grams <= 800:
        price = (price - (price * 0.13))
    else:
        price = (price - (price * 0.14))

    price_grams = round((grams / 100) * price)
    return price_grams

# def determine_activity_level(age, breed, daily_exercise_hours):
#     # Define breed-specific average daily exercise levels
#     breed_exercise_levels = {
#         'labrador': 'high',
#         'poodle': 'medium',
#         'bulldog': 'low'
#     }
#
#     # Determine breed-specific exercise level or assume normal exercise
#     if breed.lower() in breed_exercise_levels:
#         breed_activity_level = breed_exercise_levels[breed.lower()]
#     else:
#         breed_activity_level = 'normal'
#
#     # Determine overall activity level based on age, breed, and daily exercise
#     if age < 1:
#         activity_level = 'high'
#     elif breed_activity_level == 'high' and daily_exercise_hours >= 2:
#         activity_level = 'high'
#     elif breed_activity_level == 'medium' and daily_exercise_hours >= 1:
#         activity_level = 'medium'
#     elif breed_activity_level == 'low' and daily_exercise_hours >= 0.5:
#         activity_level = 'low'
#     else:
#         activity_level = 'medium'
#
#     return activity_level
