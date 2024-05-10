def create_random_code(count):
    import random
    count -= 1
    return random.randint(10**count, 10**(count+1)-1)


def send_sms(mobile_number, messages):
    pass