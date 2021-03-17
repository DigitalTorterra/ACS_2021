from gpiozero import TonalBuzzer, Buzzer
from gpiozero.tones import Tone

buzzerPIN = 21

b = TonalBuzzer(buzzerPIN)
#bz = Buzzer(buzzerPIN)
# b.play(Tone("A4"))
# b.play(Tone(220.0)) # Hz
# b.play(Tone(60)) # middle C in MIDI notation
# b.play("A4")
# b.play(220.0)
# b.play(60)
