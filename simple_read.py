import mido
import time
import sys
from mido import MidiFile, MetaMessage, Message

mid = MidiFile('music/drum.mid')
for message in mid.tracks[0]:
    print(message)