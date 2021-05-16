import asyncio
import requests
import websockets
import json
import os
from random import randint


def get_problem(difficulty):
    a = randint(1, difficulty)
    b = randint(1, difficulty)
    problem = "Was gibt " + str(a) + " plus " + str(b)
    expected = a + b
    return problem, expected


def wait_for_response(uri):
    return requests.post(uri).json()


def extract_intent(response):
    intent = response['intent']['name']
    return intent


def extract_answer(response):
    return response['entities'][0]['value']


def praise(uri, answer):
    s = "Sehr gut, " + str(answer) + " ist richtig"
    say(uri, s)


def dispraise(uri, answer):
    s = str(answer) + " ist leider falsch, versuch es noch einmal"
    say(uri, s)


def goodbye(uri):
    say(uri, 'Danke und auf wiedersehen')


def say(uri, s):
    requests.post(uri, s)


def get_server():
    server = os.environ.get('SERVER')
    uri_intent = 'ws://' + server + "/api/events/intent"
    uri_tts = 'http://' + server + '/api/text-to-speech'
    uri_command = 'http://' + server + '/api/listen-for-command?timeout=20?nohass=true'
    return uri_intent, uri_tts, uri_command


async def start():
    uri_intent, uri_tts, uri_command = get_server()

    async with websockets.connect(uri_intent) as websocket:
        print(f"waiting for command on {uri_intent}", flush=True)
        while True:
            data = await websocket.recv()
            intent = extract_intent(json.loads(data))
            if intent == "CalcStart":
                run_game(uri_tts, uri_command)


def run_game(uri_tts, uri_command):
    print("start game")
    say(uri_tts, "Willkommen zum Rechenspiel")
    is_running = True
    difficulty = 5

    (problem, expected) = get_problem(difficulty)

    while is_running:
        say(uri_tts, problem)
        response = wait_for_response(uri_command)
        intent = extract_intent(response)

        if intent == 'CalcAnswer':
            answer = extract_answer(response)

            if answer == expected:
                praise(uri_tts, answer)
                (problem, expected) = get_problem(difficulty)

            else:
                dispraise(uri_tts, answer)

        elif intent == 'CalcMoreDifficult':
            difficulty += 2
            (problem, expected) = get_problem(difficulty)

        elif intent == 'CalcEasier':
            if difficulty > 2:
                difficulty -= 2
                (problem, expected) = get_problem(difficulty)

        elif intent == 'CalcExit':
            goodbye(uri_tts)
            is_running = False


def main():
    print("client started", flush=True)
    asyncio.get_event_loop().run_until_complete(start())


main()
