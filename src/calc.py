import asyncio
import requests
import websockets

SERVER = 'freezerpi:12101'


from random import randint


def get_problem(difficulty):
    a = randint(1, difficulty)
    b = randint(1, difficulty)
    return str(a) + " plus " + str(b)


def wait_for_answer():
    url = 'http://' + SERVER + '/api/listen-for-command'
    response = requests.post(url)

    uri_ws = 'ws://' + SERVER + '/api/events/intent'
    with websockets.connect(uri_ws) as websocket:
        data = websocket.recv()
        print(data)


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

    while is_running:
        (problem, expected) = get_problem(difficulty)
        say(problem)
        (intent, answer) = wait_for_answer()

        if intent == 'result':
            is_correct = review(answer, expected)

            if is_correct:
                praise(answer)
                (problem, expected) = get_problem(difficulty)

            else:
                dispraise(answer)

        elif intent == 'more difficult':
            difficulty += 2

        elif intent == 'easier':
            if difficulty > 2:
                difficulty -= 2

        elif intent == 'done':
            goodbye()
            is_running = False


main()

