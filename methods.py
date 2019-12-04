import random
import numpy as np

dictionary = None

def genetic(x, y, max_offsprings, max_selection, iteration, mode='txt'):
    loadDict(mode, x, y)
    progeny = int(max_offsprings/max_selection)
    if iteration != 0:
        parents = x.copy()
        offsprings = {}
        for i in range(len(parents)):
            if mode == 'gray':
                parents[i] = np.asarray(parents[i])
            offsprings.update(createOffsprings(parents[i], y, progeny, mode))
        offsprings, difference = selection(offsprings, max_selection)
    else:
        x, y = strLenCheck(x, y, mode)
        difference = compare(x, y)
        offsprings = {}
        offsprings = createOffsprings(x, y, max_offsprings, mode)
        offsprings, difference = selection(offsprings, max_selection)
            
    return offsprings, difference

def loadDict(mode, x, y):
    global dictionary
    if mode == 'txt':
        dictionary = ' '
        rus = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        rus_big = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        eng = 'abcdefghijklmnopqrstuvwxyz'
        eng_big = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        num = '1234567890'
        etc = ',.;:!?"\'\\{}[]~`<>-'
        if any(symbol in [rus[i] for i in range(len(rus))] for symbol in x) or any(symbol in [rus[i] for i in range(len(rus))] for symbol in y):
            dictionary += rus
        if any(symbol in [eng[i] for i in range(len(eng))] for symbol in x) or any(symbol in [eng[i] for i in range(len(eng))] for symbol in y):
            dictionary += eng
        if any(symbol in [rus_big[i] for i in range(len(rus_big))] for symbol in x) or any(symbol in [rus_big[i] for i in range(len(rus_big))] for symbol in y):
            dictionary += rus_big
        if any(symbol in [eng_big[i] for i in range(len(eng_big))] for symbol in x) or any(symbol in [eng_big[i] for i in range(len(eng_big))] for symbol in y):
            dictionary += eng_big
        if any(symbol in [num[i] for i in range(len(num))] for symbol in x) or any(symbol in [num[i] for i in range(len(num))] for symbol in y):
            dictionary += num
        if any(symbol in [etc[i] for i in range(len(etc))] for symbol in x) or any(symbol in [etc[i] for i in range(len(etc))] for symbol in y):
            dictionary += etc
    elif mode == 'gray':
        dictionary = np.concatenate((np.unique(x), np.unique(y)))


def strLenCheck(x, y, mode):
    if mode=='txt':
        print(x)
        print(y)
        rz = len(y)-len(x)
        if rz > 0:
            x += ' '*rz
        elif rz < 0:
            x = x[:rz]
    return (x, y)

def createOffsprings(x, y, progeny, mode):
    offsprings = {}
    if mode == 'txt':
        for i in range(progeny):
                offspring = randomChange(x, mode)
                offsprings[offspring] = compare(offspring, y)
    elif mode == 'gray':
        for i in range(progeny):
                offspring = randomChange(x, mode)
                offsprings[tuple(offspring)] = compare(offspring, y)
    return offsprings

def randomChange(x, mode):
    global dictionary
    num = random.choice(range(len(x)))
    if mode == 'txt':
        x = x[:num] + random.choice(dictionary) + x[num+1:]
    elif mode == 'gray':
        x[num] = random.choice(dictionary)
    return x

def compare(x, y):
    l = 0
    for i in range(len(x)):
        #print(x[i])
        if x[i] != y[i]:
            l+=1
    return l

def selection(offsprings, max_selection):
    offsprings = sorted(offsprings.items(), key=lambda kv: kv[1])
    offsprings = offsprings[:max_selection]
    difference = offsprings[0][1]
    offsprings = [offsprings[i][0] for i in range(len(offsprings))]

    return (offsprings, difference)
