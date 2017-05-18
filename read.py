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

preset = {
    "metalProg" : {
        "tracks":  ["music/animal.mid"],
        "tempo" : 350000,
        "instrument" : 30,
        "drum" : "music/drum.mid",
    },
    "metal" : {
        "tracks":  ["music/redneck.mid"],
        "tempo" : 380000,
        "instrument" : 30,
        "drum" : "music/drumMetal.mid",
    },
    "slayer" : {
        "tracks":  ["music/slayer2.mid", "music/slayer.mid"],
        "tempo" : 380000,
        "instrument" : 30,
        "drum" : "music/slayerDrum.mid",
    },
    "megalovania" : {
        "tracks":  ["music/Undertale_-_Megalovania.mid"],
        "tempo" : 350000,
        "instrument" : 0,
        "drum" : "music/empty.mid",
    },
    "mozart" : {
        "tracks":  ["music/mozart1.mid","music/mozart2.mid","music/mozart3.mid","music/mozart4.mid","music/mozart5.mid","music/mozart6.mid"],
        "tempo" : 550000,
        "instrument" : 0,
        "drum" : "music/empty.mid",
    },
    "bach" : {
        "tracks":  ["music/bach.mid"],
        "tempo" : 550000,
        "instrument" : 0,
        "drum" : "music/empty.mid",
    },
    "all" : {
        "tracks":  ["music/animal.mid", "music/bach.mid", "music/bach_846.mid", "music/bpenta.mid", "music/B_Minor_Pentatonic_Exercises-TLMusicLessons.mid", "music/dragonforce.mid", "music/drum.mid", "music/drumMetal.mid", "music/empty.mid", "music/f1.mid", "music/f2.mid", "music/h-17-1.mid", "music/heis.mid", "music/heis2.mid", "music/kanker.mid", "music/lel.mid", "music/mozart1.mid", "music/mozart2.mid", "music/mozart3.mid", "music/output.mid", "music/penta.mid", "music/penta1.mid", "music/penta2.mid", "music/redneck.mid", "music/rolling.mid", "music/shamisen2.mid", "music/shamisen3.mid", "music/shamisen4.mid", "music/shamisen5.mid", "music/shred.mid", "music/slayer.mid", "music/slayer2.mid", "music/slayerDrum.mid", "music/smoke.mid", "music/test.mid", "music/test2.mid", "music/test3.mid", "music/test4.mid", "music/test5.mid", "music/Undertale_-_Megalovania.mid", "music/Zelda Ocarina of Time - Kakariko Village.mid", "music/Zelda Ocarina of Time - Lost Woods.mid", "music/Zelda Ocarina of Time - Market.mid"],
        "tempo" : 450000,
        "instrument" : 0,
        "drum" : "music/empty.mid",
    }


}

newMidi = MidiFile()
track = MidiTrack()

#Changement de l'instrument en fonction du preset
track.append(Message('program_change', program=preset[sys.argv[1]]['instrument']))
newMidi.tracks.append(track)

tempo = preset[sys.argv[1]]['tempo']

#Insertion de la batterie
midiDrum = MidiFile(preset[sys.argv[1]]['drum']).tracks[0]
midiDrum.insert(3,MetaMessage('set_tempo', tempo=tempo))
newMidi.tracks.append(midiDrum)

print("TEMPO")
print(mido.tempo2bpm(tempo))

#Definition du tempo
track.append(MetaMessage('set_tempo', tempo=tempo))

fileList = preset[sys.argv[1]]['tracks']


for file in fileList:
    mid = MidiFile(file)
    for message in mid.tracks[0]:
        if(message.type == "note_on"):
            #On enregistre dans deux tableaux la note jouée ainsi que sa durée
            notes.append([message.note, message.time])
            delayRatio.append([message.note, message.time])
            trackLength += 1
        if(message.type == "note_off"):
            durationList.append([message.note, message.time])

    #On boucle sur ce tableau afin d'obtenir le nombre d'occurence de cette note ainsi que de ses durées
    for i, note in enumerate(durationList):
        try: 
            durationRatio[durationList[i][0]][durationList[i][1]] += 1
        except KeyError:
            try:
                durationRatio[durationList[i][0]][durationList[i][1]] = 1
            except KeyError:
                durationRatio[durationList[i][0]] = {}
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


#On convertit le nombre d'occurences en pourcentages afin d'obtenir la fréquence
for i, baseNumber in enumerate(dictRatio):
    for j, nextNumber in enumerate(dictRatio[baseNumber]):
        dictRatio[baseNumber][nextNumber] = dictRatio[baseNumber][nextNumber] / hitRatio[baseNumber] * 100

for i, duration in enumerate(durationRatio):
    for j, ok in enumerate(durationRatio[duration]):
        durationRatio[duration][ok] = durationRatio[duration][ok] / durationHit[duration] * 100

rand = random.randint(0,100)
count = 0
previousNote = 0
#Génération d'une première note aléatoire en fonction de sa fréquence
for i, note in enumerate(hitRatio):
    hitRatio[note] = hitRatio[note] / trackLength * 100
    count += hitRatio[note]
    if rand <= count:
        previousNote = note
        #Ajout de la note sous la forme de deux message midi à la track
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=120))

#Génération de la suite des notes en tenant compte de la note précédemment joué
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
                    #Ajout de la note sous la forme de deux message midi à la track
                    track.append(Message('note_on', note=note, velocity=64, time=0))
                    track.append(Message('note_off', note=note, velocity=64, time=duration))
                    break
            break

#Enregistrement du fichier midi
newMidi.save('output.mid')



'''
s = converter.parse(newMidi)

for truc in s.parts:
    if(message.type == "note_on" or message.type == "note_off" ):
        print(truc.insert)
        p.insert(0, instrument.ElectricGuitar())

s.save('lel.mid')
'''


#Lecture du fichier midi
try:
    play_music("output.mid")
except KeyboardInterrupt:
    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit
