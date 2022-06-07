
def determineGrams(activity_level, reproductive_state, body_image, weight):
    points = 0

    if reproductive_state == 'castrado':
        points += 1
    else:
        points += 2

    if body_image == 4 or body_image == 5:
        points += 1
    elif body_image == 3:
        points += 2
    else:
        points += 3

    if activity_level == 'bajo':
        points += 1
    elif activity_level == 'medio':
        points += 2
    else:
        points += 3

    size = 'large'
    if weight < 10:
        size = 'chico'

    size_percent = 'large'
    if size == 'chico' or size == 'mini':
        size_percent = 'small'

    percents = {
        'small': [2.5, 3, 4.5],
        'large': [2, 2.5, 3]
    }

    index_number = 2
    if points >= 0 and points <= 3:
        index_number = 0
    elif points >= 4 and points <= 6:
        index_number = 1

    grams_percent = percents[size_percent][index_number]

    grams = (grams_percent * weight) * 10

    return grams, grams_percent, points



def activity_mapping(activity_choice):
    activity_choices = {
        '1': 'bajo',
        '2': 'medio',
        '3': 'alto',
    }

    return activity_choices[activity_choice]



def reproductive_mapping(reproductive_choice):
    reproductive_choices = {
        '1': 'castrado',
        '2': 'entero',
    }

    return reproductive_choices[reproductive_choice]

# def body_image_mapping(body_image_choice):
#     body_image_choices = {
#         '1': 'bajo',
#         '2': 'medio',
#         '3': 'alto',
#         '4': 'alto',
#         '5': 'alto',
#     }

#     return body_image_choices[body_image_choice]
