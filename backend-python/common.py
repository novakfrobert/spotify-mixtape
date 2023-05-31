import math
import random

def generate_random_string(length):
    """
    Generates a random string of given length
    """
    text = ""
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    for i in range(length):
        index = math.floor(random.random() * len(possible))
        text += possible[index]

    return text