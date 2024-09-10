import json

# La chaîne de caractères d'origine (modifiée pour être au format JSON valide)
data = '{"agent_outcome": {"return_values": {"output": "I\'ve opened YouTube for you."}, "log": "I\'ve opened YouTube for you."}}'

# Charger la chaîne en tant que JSON
parsed_data = json.loads(data)

# Extraire l'output
output = parsed_data['agent_outcome']['return_values']['output']
print(output)
