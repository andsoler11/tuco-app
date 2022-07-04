def body_points(body_image):
    if body_image == 4 or body_image == 5:
        points = 1
    elif body_image == 3:
        points = 2
    elif body_image == 2:
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


def reproductive_state_points(reproductive_state):
    if reproductive_state == 'castrado':
        points = 1
    else:
        points = 2

    return points





####### MAIN FUNCTION
def determineGrams(activity_level, reproductive_state, body_image, weight):
    points = 0
    points += reproductive_state_points(reproductive_state)
    points += body_points(body_image)
    points += activity_points(activity_level)

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




