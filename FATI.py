from myadblib import ADB
from myATlib import Modem


outputs = ADB.run('date')
outputsAT = Modem.AT('+COPS?')


for o in outputsAT:
    print(o)

for o in outputs:
    print(o)
