# https://docs.python.org/3.8/library/xml.etree.elementtree.html
# https://kknews.cc/news/j4nlynq.html
import xml.etree.cElementTree as ET
if __name__ == "__main__":
    tree = ET.parse('一首簡單的歌_主旋律.musicxml')
    root = tree.getroot() # 抓根節點元素，查看root的標籤內容
    print(root.tag, root.attrib)
    print("##########################################")
    
    fifths = root.findall('.//fifths')
    fifths = int(fifths[0].text)
    print(fifths) # -1表示降一號
    
    # 把歌譜上所有的音都抓出來
    all_notes = root.findall('.//note')
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
    for note in all_notes:
        print('###################', note)
        for n in note:
            print(n)
    '''
    for step in root.iter('step'):
        step.text = 'A'
    tree.write('output.musicxml')