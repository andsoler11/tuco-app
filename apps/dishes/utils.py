
MONTHS_PERCENTS = {
    2: 10,
    3: 10,
    4: 9,
    5: 9,
    6: 8,
    7: 8,
    8: 7,
    9: 7,
    10: 6,
    11: 6,
    12: 6,
}


SUPLEMENTOS ={
    'huevo_codorniz_semana': {
        9: 2, # hasta 9 kilos
        15: 4, # hasta 15 kilos
        30: 7, # hasta 30 kilos
        60: 10, # mas de 30 kilos
    },
    'omega_3_diario': {
        0: 1000, # menos de 10 kilos, 1000 gramos (1 capsula) diaria
        10: 1300, # hasta 10 kilos, 1300 gramos (1 capsula) diarias
    },
    'kefir_diario': {
        0: '1 cucharadita', # menos de 10 kilos
        10: '1 cucharada', # hasta 10 kilos
    },
    'caldo_de_huesos_diario': {
        0: '1/2 cucharadita', # menos de 10 kilos
        10: '1 cucharadita', # hasta 10 kilos
    },
    'arandanos_diario': {
        0: 15, # menos de 10 kilos, 15 gramos diarios
        10: 30, # hasta 10 kilos, 30 gramos diarios
    }
}




def get_ingredients_percent(grams, natural_food = 'yes'):
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
        points = 1
    elif body_image == 'peso_ideal':
        points = 2
    elif body_image == 'delgado':
        points = 3
    else:
        points = 4

    return points


def activity_points(activity_level):
    if activity_level == 'bajo':
        points = 1
    elif activity_level == 'medio':
        points = 2
    else:
        points = 3

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
        

def determineGrams(activity_level, reproductive_state, body_image, weight, age_type, age):
    if age_type == 'months':
        grams = round((weight * MONTHS_PERCENTS[int(age)]) * 10, 2)
        grams_percent = MONTHS_PERCENTS[int(age)]
        points = 0

        return grams, grams_percent, points

    # starting getting the points from the variables
    points = 0
    points += reproductive_state_points(reproductive_state)
    points += body_points(body_image)
    points += activity_points(activity_level)

    # determine the size of the dog by his weight
    size_percent = 'large'
    if weight < 10:
        size_percent = 'small'

    # percents array
    percents = {
        'small': [2.5, 3, 4.5],
        'large': [2, 2.5, 3]
    }

    # grab the percent needed
    index_number = 2
    if points >= 0 and points <= 3:
        index_number = 0
    elif points >= 4 and points <= 6:
        index_number = 1    
    grams_percent = percents[size_percent][index_number]


    if body_image == 'muy_delgado':
        grams_percent = 6

    grams = round((grams_percent * weight) * 10, 2)

    return grams, grams_percent, points



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