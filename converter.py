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
    for pitch in root.findall('.//pitch'):
        octave = pitch.find('octave').text
        try:
            alter = pitch.find('alter').text
            if alter == '-1':
                alter = 'b'
            else:
                alter = '#'
            #print(pitch.find('step').text + alter)
            tonic, convert_octave = convert(pitch.find('step').text + alter + octave)
        except:
            pitch.remove(pitch.find('octave'))
            ET.SubElement(pitch, 'alter')
            ET.SubElement(pitch, 'octave')
            pitch.find('alter').text = '0'
            pitch.find('octave').text = octave
            #print(pitch.find('step').text)

            tonic, convert_octave = convert(pitch.find('step').text + octave)
        pitch.find('step').text = tonic[0]
        if len(tonic) == 2:
            if tonic[1] == '#':
                pitch.find('alter').text = '1'
            else:
                pitch.find('alter').text = '-1'
        else:
            pitch.find('alter').text = '0'
        pitch.find('octave').text = convert_octave

    tree.write('output.musicxml')