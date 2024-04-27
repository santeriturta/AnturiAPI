import random
import datetime

def GenerateNewTemp():
    randomNum = random.Random()
    newTemp = float(randomNum.randint(18,26))
    timestamp = datetime.datetime.now()
    timestamp = str(timestamp)

    return newTemp, timestamp