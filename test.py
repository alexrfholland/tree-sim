import random

ARTLIFE = 20
ARTLIFEVARIATION = .2

for i in range(1,10):
    max = round(ARTLIFE + (ARTLIFE * ARTLIFEVARIATION))
    min = round(ARTLIFE - (ARTLIFE * ARTLIFEVARIATION))
    lifespan = random.randint(min, max)
    print(lifespan)
print("#######")

