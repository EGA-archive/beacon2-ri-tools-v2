import json

string='{"diseases":{"acute bronchitis":121,"agranulocytosis":111,"asthma":134,"bipolar affective disorder":134,"cardiomyopathy":133}}'


res = json.loads(string)

print(res)