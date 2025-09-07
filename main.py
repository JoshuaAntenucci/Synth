import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from modulators import am_synthesis, fm_synthesis
from oscillators import sine_osc, square_osc, triangular_osc
from envelopes import apply_envelope

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((1280, 620))  # 1280, 720
font = pg.font.SysFont("Impact", 24)  # 48

waves = []
graph_wave_index = 0
connection_sequence = []
adsl_config = [0.2, 0.1, 0.7, 1.0]  # [1.0, 0.5, 0.7, 1.0]

connection_sequence.append([sine_osc, "oscillator", "plus"])
connection_sequence.append([square_osc, "oscillator", "plus"])
connection_sequence.append([triangular_osc, "oscillator", "plus"])
connection_sequence.append([fm_synthesis, "modulator", 2, 1])
connection_sequence.append([am_synthesis, "modulator", 2, 1])


def synth(frequency, duration=1.5, sampling_rate=44100):
    arr = connection_sequence[0][0](frequency=frequency, duration=duration,
                                    sample_rate=sampling_rate)

    for i in range(len(connection_sequence) - 1):
        if (connection_sequence[i + 1][1] == "oscillator"):
            if (connection_sequence[i + 1][2] == "plus"):
                arr = arr + connection_sequence[i + 1][0](frequency=frequency, duration=duration,
                                                          sample_rate=sampling_rate)
            else:
                arr = arr - connection_sequence[i + 1][0](frequency=frequency, duration=duration,
                                                          sample_rate=sampling_rate)
        elif (connection_sequence[i + 1][1] == "modulator"):
            mod_freq = connection_sequence[i + 1][2]
            arr = connection_sequence[i +
                                      1][0](mod_freq, arr, connection_sequence[i + 1][3])

    arr = apply_envelope(arr, adsl_config)

    waves.append(arr)

    sound = np.asarray([32767 * arr, 32767 * arr]).T.astype(np.int16)

    sound = pg.sndarray.make_sound(sound.copy())

    return sound


keylist = '123456789qwertyuioasdfghjklzxcvbnm,.'
notes_file = open("noteslist.txt")
file_contents = notes_file.read()
notes_file.close()
noteslist = file_contents.splitlines()

keymod = '0-='
notes = {}  # dict to store samples
freq = 16.3516  # start frequency
posx, posy = 12, 12  # start position 25 25


for i in range(len(noteslist)):
    mod = int(i / 36)
    key = keylist[i - mod * 36] + str(mod)
    sample = synth(freq)

    color = np.array([np.sin(i/25 + 1.7) * 130 + 125, np.sin(i/30 - 0.21)
                     * 215 + 40, np.sin(i/25 + 3.7) * 130 + 125])
    color = np.clip(color, 0, 255)
    notes[key] = [sample, noteslist[i], freq,
                  (posx, posy), 255 * color / max(color), i]
    notes[key][0].set_volume(0.33)
    # notes[key][0].play()
    # notes[key][0].fadeout(100)
    freq = freq * 1.0594630943592953  # * 2 ** (1/12)
    posx = posx + 140
    if posx > 1220:
        posx, posy = 12, posy + 26  # 56

    screen.blit(font.render(notes[key][1], 0, notes[key][4]), notes[key][3])
    pg.display.update()


running = 1
mod = 1
pg.display.set_caption(
    "Synth - Change range: 0 - = // Play with keys: " + keylist)

# Constants
# CHUNK = 1024 * 2
CHUNK = 44100 * 1.5


# Figure and axes
fig, (ax, ax2) = plt.subplots(2, figsize=(12, 8))

# Variable for plotting
x = np.arange(0, 2 * CHUNK, 2)

# Create a line object with random data
# line, = ax.plot(x, np.random.rand(CHUNK), "-", lw=2)
line, = ax.plot(x, waves[graph_wave_index], "-", lw=2)


# Axes formatting
ax.set_title("Waveform")
ax.set_xlabel("Samples")
ax.set_ylabel("Volume")
# ax.set_ylim(-3000, 3000)
ax.set_xlim(0, 2 * CHUNK)

plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK])

# Show the plot
plt.show(block=False)

keypresses = []
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            running = False
        if event.type == pg.KEYDOWN:
            key = str(event.unicode)
            if key in keymod:
                mod = keymod.index(str(event.unicode))
            elif key in keylist:
                key = key + str(mod)
                notes[key][0].play()
                # # print(notes[key][5])
                # graph_wave_index = notes[key][5]
                # line.set_ydata(waves[graph_wave_index])
                # print(waves[graph_wave_index])
                # fig.canvas.flush_events()
                # fig.canvas.draw()
                # fig.canvas.flush_events()
                # # frame_count += 1

                # fig.show()

                keypresses.append([1, notes[key][1], pg.time.get_ticks()])
                screen.blit(font.render(
                    notes[key][1], 0, (255, 255, 255)), notes[key][3])
        if event.type == pg.KEYUP and str(event.unicode) != '' and str(event.unicode) in keylist:
            key = str(event.unicode) + str(mod)
            notes[key][0].fadeout(100)
            keypresses.append([0, notes[key][1], pg.time.get_ticks()])
            screen.blit(font.render(
                notes[key][1], 0, notes[key][4]), notes[key][3])

    pg.display.update()

# pg.display.set_caption("Exporting sound sequence")
# if len(keypresses) > 1:
#     for i in range(len(keypresses)-1):
#         keypresses[-i-1][2] = keypresses[-i-1][2] - keypresses[-i-2][2]
#     keypresses[0][2] = 0  # first at zero

#     with open("test.txt", "w") as file:
#         for i in range(len(keypresses)):
#             # separate lines for readability
#             file.write(str(keypresses[i])+'\n')
#     file.close()

pg.mixer.quit()
pg.quit()
