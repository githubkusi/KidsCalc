# KidsCalc
Calculation trainer for [Rhasspy](https://rhasspy.readthedocs.io/) voice automation system

## Example conversation
(currently onyl implemented in German)

You
> \<RHASSPY WAKEWORD\>
> Rechnen

Rhasspy
> Willkommen zum Rechentrainer
> Was gibt 3 + 4

You
> 7

Rhasspy
> Sehr gut, 7 ist richtig

## Installation

    docker build -t kids-calc .    
    docker run -e RHASSPY_URI=my-rhasspy:12101 -it kids-calc

Replace *my-rhasspy* with your Rhasspy instance    
## Setup
This service listens for intents on 

    ws://RHASSPY_URI/api/events/intent

The following intents/sentences need to be trained in Rhasspy

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

    http://RHASSPY_URI/api/text-to-speech
