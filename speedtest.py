import lib
import time
import random

words = ['danger', 'thinking', 'know', 'knowledge', 'insist', 'courage', 'tell', 'pay', 'ice', 'provide', 'saying', 'important', 'idea', 'stand', 'view', 'pack', 'leave', 'twist', 'list', 'considering', 'enthusiastic', 'dress', 'finished', 'lie', 'love', 'lot', 'piece', 'straight', 'begin', 'safe', 'credit', 'caught', 'open', 'turns', 'treat', 'uselessly', 'spill', 'people', 'complain', 'extremely', 'evaluate', 'without', 'quit', 'get', 'action', 'good', 'rack', 'crossed', 'member', 'breath', 'par', 'normal', 'profit', 'suspect', 'produced', 'consideration', 'possible', 'visiting', 'discourage', 'change', 'son', 'want', 'rid', 'pass', 'case', 'rob', 'loving', 'responsibility', 'upon', 'thing', 'supper', 'meet', 'false', 'word', 'mischief', 'side', 'forgive', 'track', 'company', 'behind', 'dim', 'potluck', 'shoulder', 'reduce', 'move', 'tide', 'father', 'roughly', 'quarrel', 'rather', 'dispose', 'crazy', 'grow', 'everybody', 'spot', 'hostile', 'maintain', 'bit', 'spending', 'useless', 'nervous', 'fly', 'available', 'angry', 'black', 'point', 'impression', 'deliver', 'ball', 'fail', 'decidedly', 'heart', 'much', 'brace', 'least', 'forward', 'drop', 'room', 'punctual', 'debt', 'kill', 'sudden', 'surprising', 'person', 'unofficially', 'alert', 'allow', 'sure', 'face', 'secretively', 'true', 'past', 'relaxed', 'opportunity', 'special', 'depend', 'even', 'fixed', 'position', 'better', 'say', 'advance', 'believe', 'fix', 'count', 'would', 'read', 'thought', 'around', 'cuff', 'previous', 'unnecessary', 'lots', 'eye', 'duty', 'absent', 'turn', 'plane', 'record', 'lose', 'free', 'negative', 'mistake', 'rumor', 'soon', 'spend', 'cash', 'cry', 'worth', 'easier', 'bend', 'new', 'life', 'worse', 'well', 'boss', 'edge', 'happen', 'moment', 'recover', 'reverse', 'might', 'plain', 'standard', 'come', 'mean', 'hand', 'question', 'like', 'humor', 'frame', 'fool', 'comfortable', 'inform', 'carried', 'spare', 'unprepared', 'overcome', 'earth', 'break', 'firm', 'table', 'object', 'beat', 'broke', 'back', 'care', 'short', 'door', 'nothing', 'behave', 'missing', 'easy', 'become', 'fulfill', 'dog', 'account', 'used', 'answer', 'direct', 'line', 'help', 'lead', 'dictionary', 'wall', 'bad', 'check', 'tired', 'illness', 'luck', 'wonder', 'study', 'matter', 'subject', 'money', 'hair', 'argue', 'rock', 'attract', 'hit', 'serve', 'familiar', 'start', 'right', 'part', 'also', 'physically', 'clumsy', 'completely', 'hope', 'every', 'speak', 'slowly', 'story', 'opposite', 'expect', 'generally', 'logical', 'oneself', 'protect', 'horse', 'laugh', 'posted', 'brain', 'limit', 'nevertheless', 'eat', 'carpet', 'spur', 'careful', 'still', 'mental', 'accustomed', 'relax', 'damper', 'job', 'discord', 'dependable', 'afraid', 'real', 'strong', 'bush', 'future', 'feel', 'grip', 'unfit', 'element', 'watching', 'deceive', 'listen', 'sad', 'big', 'trouble', 'advantage', 'put', 'actually', 'space', 'bed', 'red', 'irritable', 'alternate', 'blow', 'frankly', 'tolerate', 'message', 'time', 'learn', 'acting', 'shape', 'rudely', 'pull', 'understand', 'hesitation', 'till', 'weapon', 'full', 'worried', 'else', 'public', 'first', 'lucky', 'haughtily', 'main', 'uncomfortable', 'compensate', 'cut', 'firsthand', 'spade', 'make', 'walk', 'disappoint', 'leaf', 'forget', 'long', 'weight', 'sign', 'bone', 'wind', 'cast', 'step', 'morning', 'participate', 'pick', 'promise', 'talking', 'living', 'prepared', 'force', 'discover', 'play', 'addition', 'hold', 'interested', 'depressed', 'blind', 'usual', 'prepare', 'order', 'end', 'backwards', 'test', 'discuss', 'course', 'accept', 'defensive', 'purpose', 'promising', 'business', 'accompany', 'fact', 'handle', 'hard', 'appear', 'write', 'concerned', 'narrow', 'best', 'goes', 'trying', 'suddenly', 'making', 'intelligently', 'happy', 'general', 'air', 'show', 'usually', 'family', 'something', 'contact', 'small', 'second', 'school', 'busy', 'jump', 'done', 'reasonably', 'apple', 'plan', 'bacon', 'unlikely', 'carefully', 'scratch', 'confused', 'little', 'success', 'charge', 'strongly', 'together', 'book', 'noticeable', 'attentive', 'address', 'hello', 'result', 'protest', 'temper', 'quiet', 'fun', 'reluctantly', 'opinion', 'set', 'source', 'certainly', 'difference', 'across', 'carry', 'clothes', 'let', 'smell', 'upset', 'simple', 'secret', 'brush', 'lift', 'blood', 'catch', 'consider', 'undecided', 'disapprove', 'see', 'variety', 'decide', 'arms', 'alone', 'despite', 'escape', 'fresh', 'chance', 'unstable', 'switch', 'ca', 'blanket', 'almost', 'guard', 'flow', 'surprise', 'white', 'run', 'act', 'dangerous', 'untrue', 'lag', 'eagerly', 'lost', 'tongue', 'high', 'many', 'give', 'unimportant', 'enough', 'along', 'impossible', 'place', 'strength', 'meeting', 'superficially', 'tip', 'fault', 'meal', 'suggest', 'watch', 'surface', 'incidentally', 'odds', 'state', 'properly', 'date', 'pleasure', 'arm', 'keep', 'joke', 'follow', 'openly', 'exactly', 'shot', 'woman', 'next', 'chew', 'useful', 'parent', 'scarce', 'nobody', 'day', 'release', 'directly', 'remember', 'sense', 'bring', 'able', 'lay', 'prefer', 'close', 'cold', 'work', 'ride', 'stop', 'head', 'decision', 'frank', 'envy', 'compromise', 'preparation', 'waste', 'slip', 'excited', 'said', 'remind', 'fall', 'rare', 'rule', 'wrong', 'ill', 'mind', 'harmful', 'wool', 'return', 'criticize', 'different', 'avoid', 'somebody', 'ring', 'wet', 'blame', 'take', 'halfway', 'bite', 'talk', 'must', 'reason', 'immediately', 'postpone', 'minimum', 'low', 'positive', 'irritate', 'revenge', 'towards', 'never', 'everywhere', 'distract', 'news', 'comment', 'speaking', 'search', 'ready', 'route', 'random', 'bus', 'hurt', 'often', 'ability', 'call', 'summon', 'draw', 'occasionally', 'influence', 'opposed', 'sleep', 'giving', 'practical', 'reality', 'boat', 'empty', 'bell', 'informal', 'shyness', 'rub', 'live', 'beside', 'calm', 'wait', 'dust', 'home', 'earn', 'responsible', 'healthy', 'one', 'misery', 'ropes', 'sheep', 'find', 'criticism', 'train', 'go', 'showing', 'think', 'rat', 'degree', 'discard', 'clear', 'attention', 'meaning', 'forever', 'bottom', 'mention', 'rest', 'somewhere', 'benefit', 'bill', 'cancel', 'hook', 'way', 'use', 'save', 'experience', 'enter', 'financially', 'another', 'look', 'try', 'deeply', 'die', 'mislead', 'mixed', 'uncertain', 'away', 'blue', 'quite', 'mouth', 'choose', 'crook', 'foot', 'eager', 'touch', 'man', 'someone', 'fight', 'reference', 'unpleasant', 'mercilessly', 'far', 'car', 'intentionally', 'size', 'nail', 'review', 'weather', 'writing', 'given', 'apart', 'notice', 'situation', 'nutshell', 'press', 'alarm', 'allowance', 'annoy', 'equal', 'control', 'agree', 'ease']

sz = 100
users = 100
t = True
f = False
d = lib.Db()

d.init_db()

ct = time.time()
for i in range(users):
    u = lib.unit(*[(w,random.choice([t,f]),random.choice([t,f])) for w in random.sample(words,sz)])
    d.create_user(i+1, u)
print(time.time()-ct)

ct = time.time()
for i in range(users):
    d.change_diff(i+1, 5)
print(time.time()-ct)

sz = 500
ct = time.time()
for i in range(users):
    u = lib.unit(*[(w,random.choice([t,f]),random.choice([t,f])) for w in random.sample(words,sz)])
    d.add_unit(i+1, u)
print(time.time()-ct)

ct = time.time()
for i in range(users):
    d.change_diff(i+1, 10)
print(time.time()-ct)

ct = time.time()
for i in range(users):
    print(d.get_lesson(i+1))
print(time.time()-ct)

ct = time.time()
for i in range(users):
    try:
        print(d.get_recomendation(i+1, 1, 0.1))
    except Exception as e:
        print(e)
print(time.time()-ct)

ct = time.time()
for i in range(users, 2*users):
    try:
        u = lib.unit(*[(w,random.choice([t,f]),random.choice([t,f])) for w in random.sample(words,sz)])
        d.create_user(i+1, u)
        u = lib.unit(*[(w,random.choice([t,f]),random.choice([t,f])) for w in random.sample(words,sz)])
        d.add_unit(i+1, u)
        d.change_diff(i+1, 10)
        print(d.get_lesson(i+1))
        print(d.get_recomendation(i+1, 1, 0.1))
    except Exception as e:
        print(e)
print(time.time()-ct)

