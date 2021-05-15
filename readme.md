# KidsCalc
Calculation trainer for [Rhasspy](https://rhasspy.readthedocs.io/) voice automation system

## Example conversation
(currently onyl implemented in German)

You
> \<RHASSPY WAKEWORD\>
Rechnen

Rhasspy
> Willkommen zum Rechentrainer
Was gibt 3 + 4

You
> 7

Rhasspy
> Sehr gut, 7 ist richtig

## Installation

    docker build -t kids-calc .    
	docker run -it kids-calc
## Setup
This service expects a running Rhasspy instance in the same network. It listens for intents on 

    ws://localhost:12101/api/events/intent
   
The following sentences need to be trained in Rhasspy

    [CalcStart]
	Rechnen

	[CalcAnswer]
	(0..100){result!int}

	[CalcEasier]
	einfacher

	[CalcMoreDifficult]
	schwieriger

	[CalcExit]
	fertig

Audio output is sent

    http://localhost:12101/api/text-to-speech
