import openai
from midiutil import *
import time
from tkinter import *
import easygui

clef = easygui.enterbox("Enter your ChatGPT API key here : ")
'''
TKINTER
'''
fenetre = Tk()

label = Label(fenetre, text="Welcome to ChatGPT 2 Midi Melody Creator v.1.0 !")
label.pack()
label = Label(fenetre, text="Click on generate button to start")
label.pack()


def generate():
  label = Label(fenetre, text="Generating... please wait")
  label.pack()
  
  openai.api_key = clef

  key = easygui.enterbox("In which key do you want to generate the melody ? (ex: B minor)")
  prompt = str("Generate a cool melody in " + key + ", and only output the notes, don't output any other text that the notes of the melody.")

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": prompt}
    ]
  )

  result = completion.choices[0].message.content
  def check(result):
    if result[0] == S:
      result = completion.choices[0].message.content
      check()
  check(result)
  windows_text = str("The generated melody is : " + result)
  label = Label(fenetre, text=windows_text)
  label.pack()

  dico = {"C":60,"C#":61,"D":62,"D#":63,"E":64,"F":65,"F#":66,"G":67,"G#":68,"A":69,"A#":70,"B":71}

  liste = []

  def tri():
    for chose in result:
        if chose == "#":
            liste.pop(-1)
            chose = previous + chose
        if chose in dico:
          liste.append(dico[chose])
        previous = chose

  tri()

  degrees  = liste  # MIDI note number
  track    = 0
  channel  = 0
  timer     = 0    # In beats
  duration = 1    # In beats
  tempo    = 60   # In BPM
  volume   = 100  # 0-127, as per the MIDI standard

  MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
  MyMIDI.addTempo(track, timer, tempo)

  for i, pitch in enumerate(degrees):
      MyMIDI.addNote(track, channel, pitch, timer + i, duration, volume)

  t = time.localtime(time.time())

  jour = str(t.tm_mday)
  mois = str(t.tm_mon)
  annee = str(t.tm_year)
  minutes = str(t.tm_min)
  secondes = str(t.tm_sec)

  filename = "mon audio" + jour + mois + annee + minutes + secondes + ".mid"

  with open(filename, "wb") as output_file:
      MyMIDI.writeFile(output_file)
    
  label = Label(fenetre, text="File exported !")
  label.pack()

Button(text='Generate', command=generate).pack()

fenetre.mainloop()