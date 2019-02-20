from pyo import *

class NoteinSustain:
    """
    Classe similaire à l'objet Notein mais avec l'intégration de la pédale.
    La pdéale de sustain est affecté au control change 64.
    """
    def __init__(self, poly=16, scale=0, first=0, last=127, channel=0):
        # la pédale est relevée
        self.sustain = False

        # dictionnaire des notes qui sont actuellement enfoncés
        self.notedict = {}

        # polyphonie : nombre de notes pouvants être gérées
        self.poly = poly

        # initialise le NoteIn pour récupérer les messages de notes
        self.notes = Notein(poly, scale, first, last, channel)
        self.noteon = TrigFunc(self.notes["trigon"], self.onNoteon, list(range(poly)))
        self.noteoff = TrigFunc(self.notes["trigoff"], self.onNoteoff, list(range(poly)))

        # Met la pédale à vrai ou faux en fonction du CC64
        self.sustain = Midictl(64, channel=channel)
        self.suscall = TrigFunc(Change(self.sustain), self.onSustain)

        # Crée les flux de vélocité et de pitch en fonction de la polyphonie
        self.velocity = Sig([0]*poly)
        self.pitch = Sig([0]*poly)

    def onNoteon(self, which):
        """
        Fonction appelée lorsque qu'une touche est enfoncée
        """
        amp = self.notes.get("velocity", True)[which]
        pitch = self.notes.get("pitch", True)[which]
        voice = self._get_free_voice()
        if voice != None:
            self.notedict[voice] = pitch
            self.pitch[voice].value = pitch
            self.velocity[voice].value = amp

    def onNoteoff(self, voice):
        """
        Fonction appelée lorsque qu'une touche est relaché
        """
        pitch = self.notes.get("pitch", True)[voice]

        # récupère la voix correspondant à la hauteur de la note
        voice = self._get_voice_from_pitch(pitch)

        # si une voix a été trouvée en correspondance au pitch
        if voice != None:
            # Si la pédale n'est pas enfoncé
            if not self.sustain.get():
                self.velocity[voice].value = 0.0
                # libére la note
                del self.notedict[voice]
            else:
                # la note est encoré joué, mais la touche n'est plus enfoncée
                self.notedict[voice] = -1

    def onSustain(self):
        """
        Fonction appelée lorsque la pédale de sustain change d'étât
        """
        # si la pédale est relachée
        if not self.sustain.get():
            # il faut arrêter les notes qui ont déjà été rélachées == -1
            notedict = dict(self.notedict)
            for voice, pitch in notedict.items():
                if pitch == -1:
                    self.velocity[voice].value = 0.0
                    del self.notedict[voice]


    def _get_free_voice(self):
        """
        Tente de trouver le premier index de libre dans le dictionnaire de notes
        """
        freevoice = None
        for i in range(self.poly):
            if not i in self.notedict:
                freevoice = i
                break
        return freevoice

    def _get_voice_from_pitch(self, pitch):
        """
        Tente de trouver l'index correspondant au pitch dans le dictionnaire
        de notes
        """
        voice = None
        for key, val in self.notedict.items():
            if val == pitch:
                voice = key
                break
        return voice

    def __getitem__(self, str):
        if str == 'pitch':
            return self.pitch
        elif str == 'velocity':
            return self.velocity
        else:
            print("NoteinSustain's key should be 'pitch' or 'velocity'!")


if __name__ == '__main__':
    s = Server()
    print(pm_list_devices())
    s.setMidiInputDevice(0)
    s.boot().start()
    notein = NoteinSustain(scale=1)
    amp = MidiAdsr(notein["velocity"], 0.001, 0.05, 0.7, 0.5)
    synth1 = RCOsc(freq=notein["pitch"], sharp=0.75, mul=amp)
    synth2 = RCOsc(freq=notein["pitch"]*1.01, sharp=0.74, mul=amp)
    stereo = Mix([synth1.mix(1), synth2.mix(1)], voices=2)
    rev = STRev(stereo, inpos=[0,1], revtime=2, bal=0.25, mul=0.2).out()
    s.gui(locals())
