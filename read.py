import mido
import time
import sys
import random
from mido import MidiFile, MetaMessage, Message, MidiTrack
from midiutil.MidiFile import MIDIFile
import pygame
from music21 import converter,instrument
pygame.mixer.init()

def play_music(music_file):
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
    except pygame.error:
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(30)

notes = []
trackLength = 0
dictRatio = {}
hitRatio = {}
delayRatio = []

durationList = []
durationRatio = {}
durationHit = {}

newMidi = MidiFile()
track = MidiTrack()
newMidi.tracks.append(track)
print("TEMPO")
print(mido.tempo2bpm(400000))
track.append(MetaMessage('set_tempo', tempo=350000))

fileList = ["music/dragonforce.mid"]

for file in fileList:
    mid = MidiFile(file)
    for message in mid.tracks[0]:
        if(message.type == "note_on"):
            notes.append([message.note, message.time])
            delayRatio.append([message.note, message.time])
            trackLength += 1
        if(message.type == "note_off"):
            durationList.append([message.note, message.time])

    for i, note in enumerate(durationList):
        try: 
            durationRatio[durationList[i][0]][durationList[i][1]] += 1
        except KeyError:
            try:
                durationRatio[durationList[i][0]][durationList[i][1]] = 1
            except KeyError:
                durationRatio[durationList[i][0]] = {};
                durationHit[durationList[i][0]] = 0
                try:
                    durationRatio[durationList[i][0]][durationList[i][1]] = 1
                except IndexError:
                    print('end')
        except IndexError:
            print('end')
        durationHit[notes[i][0]] += 1

for i, note in enumerate(notes):
    try: 
        dictRatio[notes[i][0]][notes[i+1][0]] += 1
    except KeyError:
        try:
            dictRatio[notes[i][0]][notes[i+1][0]] = 1
        except KeyError:
            dictRatio[notes[i][0]] = {};
            hitRatio[notes[i][0]] = 0
            try:
                dictRatio[notes[i][0]][notes[i+1][0]] = 1
            except IndexError:
                print('end')
    except IndexError:
        print('end')
    hitRatio[notes[i][0]] += 1

for i, baseNumber in enumerate(dictRatio):
    for j, nextNumber in enumerate(dictRatio[baseNumber]):
        dictRatio[baseNumber][nextNumber] = dictRatio[baseNumber][nextNumber] / hitRatio[baseNumber] * 100

for i, duration in enumerate(durationRatio):
    for j, ok in enumerate(durationRatio[duration]):
        durationRatio[duration][ok] = durationRatio[duration][ok] / durationHit[duration] * 100

rand = random.randint(0,100)
count = 0
previousNote = 0
for i, truc in enumerate(hitRatio):
    hitRatio[truc] = hitRatio[truc] / trackLength * 100
    count += hitRatio[truc]
    if rand <= count:
        previousNote = truc
        track.append(Message('note_on', note=truc, velocity=64, time=0))
        track.append(Message('note_off', note=truc, velocity=64, time=120))

for i in range(1,250):
    randNote = random.randint(0,100)
    randDuration = random.randint(0,100)
    count = 0
    for j, note in enumerate(dictRatio[previousNote]):
        ratio = dictRatio[previousNote][note]
        count += ratio
        if randNote <= count:
            previousNote = note
            countDuration = 0
            for k, duration in enumerate(durationRatio[note]):
                ratio = durationRatio[note][duration]
                countDuration += ratio
                if randDuration <= countDuration:
                    track.append(Message('note_on', note=note, velocity=64, time=0))
                    track.append(Message('note_off', note=note, velocity=64, time=duration))
                    break
            break


newMidi.save('output.mid')

s = converter.parse('output.mid')

for p in s.parts:
    p.insert(0, instrument.AcousticGuitar())

s.write('midi', 'lel.mid')

try:
    play_music("lel.mid")
except KeyboardInterrupt:
    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit
