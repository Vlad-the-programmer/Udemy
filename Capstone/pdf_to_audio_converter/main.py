import requests

api_endpoint = "http://api.ispeech.org/api/rest"
API_KEY = ''

file = input('Enter a name without an extension(e.g. pdf) of the file to convert to the audio: ')

params = {
    'action': 'convert',
    'text': 'Hi',
    'filename': 'audio'
}

response = requests.get(api_endpoint, params=params)
print(response.text)
