import json

raw_input = '{ "type": "init", "dot_amount": 10, "target_amount": 5 }'
jsoner: dict = json.loads(raw_input)
for key, value in jsoner.items():
    print(key, value)
