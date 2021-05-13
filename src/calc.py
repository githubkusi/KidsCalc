import asyncio
import requests
import websockets
from random import randint

SERVER = 'freezerpi:12101'


def get_problem(difficulty):
    a = randint(1, difficulty)
    b = randint(1, difficulty)
    problem = "Was gibt " + str(a) + " plus " + str(b)
    expected = a + b
    return problem, expected


def wait_for_response():
    url = 'http://' + SERVER + '/api/listen-for-command?timeout=20'
    return requests.post(url).json()


def extract_intent(response):
    intent = response['intent']['name']
    return intent


def extract_answer(response):
    return response['entities'][0]['value']


def review(answer, expected):
    pass


def praise(answer):
    s = "Sehr gut, " + str(answer) + " ist richtig"
    say(s)


def dispraise(answer):
    s = str(answer) + " ist leider falsch, versuch es noch einmal"
    say(s)


def goodbye():
    say('Danke und auf wiedersehen')


def say(s):
    url = 'http://' + SERVER + '/api/text-to-speech'
    requests.post(url, s)


def main():
    is_running = True
    difficulty = 5

    (problem, expected) = get_problem(difficulty)

    while is_running:
        say(problem)
        response = wait_for_response()
        intent = extract_intent(response)

        if intent == 'CalcAnswer':
            answer = extract_answer(response)

            if answer == expected:
                praise(answer)
                (problem, expected) = get_problem(difficulty)

            else:
                dispraise(answer)

        elif intent == 'CalcMoreDifficult':
            difficulty += 2
            (problem, expected) = get_problem(difficulty)

        elif intent == 'CalcEasier':
            if difficulty > 2:
                difficulty -= 2
                (problem, expected) = get_problem(difficulty)

        elif intent == 'CalcExit':
            goodbye()
            is_running = False


main()
