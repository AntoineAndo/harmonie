import mido
import sys
from mido import MidiFile
from midiutil.MidiFile import MIDIFile
import pygame
pygame.mixer.init()

'''
mid = MidiFile('h-17-1.mid')
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for message in track:
        print(message)
'''
'''
MyMIDI = MIDIFile(1)
track = 0
channel = 0
pitch = 60
time = 0
duration = 1
volume = 100
MyMIDI.addNote(track,channel,pitch,time,duration,volume)
'''

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)




midi_file = 'Zelda Ocarina of Time - Kakariko Village.mid'
freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 1024    # number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)






mf = MIDIFile(1)     # only 1 track
track = 0   # the only track

time = 0    # start at the beginning
mf.addTrackName(track, time, "Sample Track")
mf.addTempo(track, time, 240)

channel = 0
volume = 100

pitch = 60
time = 0
duration = 1
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 60
time = 0
duration = 1
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 60
time = 2
duration = 1
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 62
time = 3
duration = 1
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 60
time = 5
duration = 1
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 65
time = 7
duration = 1
mf.addNote(track, channel, pitch, time, duration, volume)

pitch = 64
time = 9
duration = 1
mf.addNote(track, channel, pitch, time, duration, volume)

with open("output.mid", 'wb') as outf:
    mf.writeFile(outf)

try:
	play_music("output.mid")
except KeyboardInterrupt:
	# if user hits Ctrl/C then exit
	# (works only in console mode)
	pygame.mixer.music.fadeout(1000)
	pygame.mixer.music.stop()
	raise SystemExit