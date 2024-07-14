import random

input = random.randint(1, 100)
if input > 74:
    print("High")
elif input <= 74 and input >= 25:
    print("Medium")
elif input >= 0 and input < 25:
    print("Low")
