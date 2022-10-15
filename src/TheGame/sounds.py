from pygame import mixer, USEREVENT

mixer.init()


class Sound:
    def __init__(self):
        BG_music = mixer.Sound("sounds/BG.wav")
        BG_music.set_volume(0.1)
        Replay = USEREVENT
        mixer.Channel(0).play(BG_music, loops=-1)
        mixer.Channel(1).set_endevent(Replay)
        #self.play_Run()

    def play_blast(self):
        mixer.music.load("sounds/blast.mp3")
        mixer.music.play()

    def play_select(self):
        mixer.music.load("sounds/select.wav")
        mixer.music.play()

    def play_transition(self):
        mixer.music.load("sounds/transition.wav")
        mixer.music.play()

    def play_Run(self):
        mixer.Channel(1).play(mixer.Sound("sounds/Run.mp3"))

    def stop_Run(self):
        mixer.Channel(1).stop()