import mido
import time
import sys
from mido import MidiFile, MetaMessage, Message

mid = MidiFile('shamisen2.mid')
for message in mid.tracks[1]:
    if(message.type == "note_on"):
        print(message)