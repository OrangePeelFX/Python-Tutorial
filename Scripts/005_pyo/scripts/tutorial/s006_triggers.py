"""
Les déclencheurs/triggers

Un "trigger" est un signal audio de valeur 1 entouré de 0.

Plusieurs objets de la librairie sont conçus pour activer un processus
sur réception d'un "trigger".
"""
from pyo import *

s = Server().boot()

t = CosTable([(0,0), (50,1), (250,.3), (8191,0)])
met = Metro(time=[.2,.3], poly=2).play()
amp = TrigEnv(met, table=t, dur=.3, mul=.3)
freq = TrigChoice(met, [150,198,251,299,351,403])
a = SineLoop(freq=freq, feedback=0.05, mul=amp).out()

s.gui(locals())
