# https://docs.python.org/3.8/library/xml.etree.elementtree.html
# https://kknews.cc/news/j4nlynq.html
# https://github.com/schef/negative_harmony?fbclid=IwAR1Q-ym6Rkv5OCMpz-hKOSazD14fWXK1ief8VUSWguiNzGizWrlVlHgIx6A

import xml.etree.cElementTree as ET
from music21 import *

def convert(step):
    print(step.split())
    positiveChord = chord.Chord(step.split())
    print("positiveChord:", chord.Chord(positiveChord).pitchedCommonName)

    negativeChord = []

    for note in positiveChord.notes:
        #search in upper
        for i,n in enumerate(upperNotes):
            if note.pitch.pitchClass == n.pitchClass:
                print("adding", note.pitch, "->", lowerNotes[i])
                negativeChord.append(lowerNotes[i])
        #search in lower
        for i,n in enumerate(lowerNotes):
            if note.pitch.pitchClass == n.pitchClass:
                print("adding", note.pitch, "->", upperNotes[i])
                negativeChord.append(upperNotes[i])

    print("negativeChord:", chord.Chord(negativeChord).pitchedCommonName[:-7], str(negativeChord[0])[-1])
    print("=================================")
    return chord.Chord(negativeChord).pitchedCommonName[:-7], str(negativeChord[0])[-1]

if __name__ == "__main__":
    octave_val_dict = { 'C3':1, 'C#3':2, 'Db3':2, 'D3':3, 'D#3':4, 'Eb3':4, 'E3':5, 'F3':6, 'F#3':7, 'Gb3':7, 'G3':8, 'G#3':9, 'Ab3':9, 'A3':10, 'A#3':11, 'Bb3':11, 'B3':12, \
                    'C4':13, 'C#4':14, 'Db4':14, 'D4':15, 'D#4':16, 'Eb4':16, 'E4':17, 'F4':18, 'F#4':19, 'Gb4':19, 'G4':20, 'G#4':21, 'Ab4':21, 'A4':22, 'A#4':23, 'Bb4':23, 'B4':24, \
                    'C5':25, 'C#5':26, 'Db5':26, 'D5':27, 'D#5':28, 'Eb5':28, 'E5':29, 'F5':30, 'F#5':31, 'Gb5':31, 'G5':32, 'G#5':33, 'Ab5':33, 'A5':34, 'A#5':35, 'Bb5':35, 'B5':36, \
                    'C6':37  }
    tree = ET.parse('一首簡單的歌_主旋律.musicxml')
    root = tree.getroot() # 抓根節點元素，查看root的標籤內容
    print(root.tag, root.attrib)
    print("========================================")
    
    fifths = root.findall('.//fifths')
    fifths = int(fifths[0].text)
    print('fifths:', fifths) # -1表示降一號, 為F大調
    chromaticScale = scale.ChromaticScale('F4').getPitches()
    print(chromaticScale)
    print("========================================")

    upperNotes = [chromaticScale[10], chromaticScale[11], chromaticScale[0], chromaticScale[1], chromaticScale[2], chromaticScale[3]]
    lowerNotes = [chromaticScale[9], chromaticScale[8], chromaticScale[7], chromaticScale[6], chromaticScale[5], chromaticScale[4]]
    '''
    note:代表一個音的標籤
        pitch:音高
            step:音名:A, B, C, D, E, F, G
            octave:八度，有1到9，C4是代表中央C
            alter:半音記號。1是升號，-1是降號
    #######################################
    ex:
    <note default-x="171.53" default-y="-10.00">
        <pitch>
            <step>D</step>
            <octave>5</octave>
        </pitch>
        <duration>2</duration>
        <voice>1</voice>
        <type>eighth</type>
        <stem>down</stem>
        <beam number="1">begin</beam>
        <lyric number="1" default-x="6.58" default-y="-52.85" relative-y="-30.00">
            <syllabic>single</syllabic>
            <text>你</text>
        </lyric>
    </note>
    '''
    '''
    convert("G3") # A#3 or Bb3
    convert("F3") # C4
    convert("D3") # D#4 or Eb4
    '''
    pre_octave_val_ori = -1
    current_octabe_val_ori = -1
    up_or_down_ori = -2 # 1 is up; 0 is equal; -1 is down

    pre_octave_val_neg = -1
    current_octabe_val_neg = -1
    up_or_down_neg = -2 # 1 is up; 0 is equal; -1 is down
    pitch_index = 0
    for pitch in root.findall('.//pitch'):
        octave = pitch.find('octave').text
        try:
            alter = pitch.find('alter').text
            if alter == '-1':
                alter = 'b'
            else:
                alter = '#'

            if pre_octave_val_ori == -1: # the first step
                pre_octave_val_ori = octave_val_dict[pitch.find('step').text + alter + octave]
            else:
                current_octabe_val_ori = octave_val_dict[pitch.find('step').text + alter + octave]
                if pre_octave_val_ori < current_octabe_val_ori:
                    up_or_down_ori = 1
                elif pre_octave_val_ori == current_octabe_val_ori:
                    up_or_down_ori = 0
                else:
                    up_or_down_ori = -1
                pre_octave_val_ori = current_octabe_val_ori

            tonic, convert_octave = convert(pitch.find('step').text + alter + octave)
        except:
            pitch.remove(pitch.find('octave'))
            ET.SubElement(pitch, 'alter')
            ET.SubElement(pitch, 'octave')
            pitch.find('alter').text = '0'
            pitch.find('octave').text = octave

            if pre_octave_val_ori == -1: # the first step
                pre_octave_val_ori = octave_val_dict[pitch.find('step').text + octave]
            else:
                current_octabe_val_ori = octave_val_dict[pitch.find('step').text + octave]
                if pre_octave_val_ori < current_octabe_val_ori:
                    up_or_down_ori = 1
                elif pre_octave_val_ori == current_octabe_val_ori:
                    up_or_down_ori = 0
                if pre_octave_val_ori > current_octabe_val_ori:
                    up_or_down_ori = -1
                pre_octave_val_ori = current_octabe_val_ori

            tonic, convert_octave = convert(pitch.find('step').text + octave)

        if pre_octave_val_neg == -1: # the first step
            pre_octave_val_neg = octave_val_dict[tonic + convert_octave]
        else:
            current_octabe_val_neg = octave_val_dict[tonic + convert_octave]
            if pre_octave_val_neg < current_octabe_val_neg:
                up_or_down_neg = 1
            elif pre_octave_val_neg == current_octabe_val_neg:
                up_or_down_neg = 0
            elif pre_octave_val_neg > current_octabe_val_neg:
                up_or_down_neg = -1
            pre_octave_val_neg = current_octabe_val_neg
        
        if up_or_down_neg == 1 and up_or_down_ori == 1:
            convert_octave = str(int(convert_octave) - 1)
            pre_octave_val_neg = octave_val_dict[tonic + convert_octave]
        elif up_or_down_neg == -1 and up_or_down_ori == -1:
            convert_octave = str(int(convert_octave) + 1)
            pre_octave_val_neg = octave_val_dict[tonic + convert_octave]
        elif up_or_down_neg == 1 and up_or_down_ori == 0:
            convert_octave = str(int(convert_octave) - 1)
            pre_octave_val_neg = octave_val_dict[tonic + convert_octave]
        elif up_or_down_neg == -1 and up_or_down_ori == 0:
            convert_octave = str(int(convert_octave) + 1)
            pre_octave_val_neg = octave_val_dict[tonic + convert_octave]
        elif up_or_down_neg == 0 and up_or_down_ori == 1:
            convert_octave = str(int(convert_octave) - 1)
            pre_octave_val_neg = octave_val_dict[tonic + convert_octave]
        elif up_or_down_neg == 0 and up_or_down_ori == -1:
            convert_octave = str(int(convert_octave) + 1)
            pre_octave_val_neg = octave_val_dict[tonic + convert_octave]
        
        pitch.find('step').text = tonic[0]
        if len(tonic) == 2:
            if tonic[1] == '#':
                pitch.find('alter').text = '1'
            else:
                pitch.find('alter').text = '-1'
        else:
            pitch.find('alter').text = '0'
        pitch.find('octave').text = convert_octave


        if pitch_index == 0 or pitch_index == 46:
            pitch.find('octave').text = '5'
            pre_octave_val_neg = octave_val_dict[tonic + '5']
        elif pitch_index == 23 or pitch_index == 69 or pitch_index == 109:
            pitch.find('octave').text = '4'
            pre_octave_val_neg = octave_val_dict[tonic + '4']
        pitch_index += 1

    tree.write('output.musicxml')