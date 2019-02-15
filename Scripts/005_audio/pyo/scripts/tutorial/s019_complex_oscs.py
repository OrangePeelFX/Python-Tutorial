"""
Gestion des canaux #4

Si l'attribut chnl est une liste, les flux seront distribués sur le canaux
respectivement à la liste passée en paramètre.
"""
from pyo import *

s = Server().boot().start()


# Sets fundamental frequency.
freq = 187.5

# Impulse train generator.
lfo1 = Sine(.1).range(1, 50)
osc1 = Blit(freq=freq, harms=lfo1, mul=0.3)

# RC circuit.
lfo2 = Sine(.1, mul=0.5, add=0.5)
osc2 = RCOsc(freq=freq, sharp=lfo2, mul=0.3)

# Sine wave oscillator with feedback.
lfo3 = Sine(.1).range(0, .18)
osc3 = SineLoop(freq=freq, feedback=lfo3, mul=0.3)

# Roland JP-8000 Supersaw emulator.
lfo4 = Sine(.1).range(0.1, 0.75)
osc4 = SuperSaw(freq=freq, detune=lfo4, mul=0.3)

# Interpolates between input objects to produce a single output
sel = Selector([osc1, osc2, osc3, osc4]).out()
sel.ctrl(title="Input interpolator (0=Blit, 1=RCOsc, 2=SineLoop, 3=SuperSaw)")

# Displays the waveform of the chosen source
sc = Scope(sel)

# Displays the spectrum contents of the chosen source
sp = Spectrum(sel)

s.gui(locals())