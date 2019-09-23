import random
import numpy as np

from matplotlib import pyplot as plt

dictionary = None

def genetic(x, y, max_offsprings, max_selection, mode='txt', size=None):
    loadDict(mode, x, y)
    progeny = int(max_offsprings/max_selection)
    iteration = 0
    x, y = strLenCheck(x, y, mode)
    difference = compare(x, y)
    offsprings = {}
    while difference > 0:
        if iteration != 0:
            parents = offsprings.copy()
            offsprings = {}
            for parent in parents:
                if mode == 'gray':
                    parent = np.asarray(parent)
                offsprings.update(createOffsprings(parent, y, progeny, mode))
            offsprings, difference = selection(offsprings, max_selection)
        else:
            offsprings = createOffsprings(x, y, max_offsprings, mode)
            offsprings, difference = selection(offsprings, max_selection)
            
        if len(offsprings[0]) > 100:
            print(f'Iteration #{iteration+1}, min string difference - {difference} from \'{offsprings[0][:100]}...\'')
        else:
            print(f'Iteration #{iteration+1}, min string difference - {difference} from \'{offsprings[0]}\'')
        if mode == 'gray':
            plt.ion()
            plot((offsprings[0], y), ('Input', 'Original'), size)

        iteration += 1
    print(f'Got {offsprings[0]}, original string - {y}')

def plot(X, xlabel, size):
    plt.figure(1)
    for i in range(len(X)):
        plt.subplot(1, 2, i+1)
        plt.xlabel(xlabel[i])
        a = None
        if type(X[i]) == tuple:
            a = np.asarray(X[i]).reshape(size)
        else:
            a = X[i].reshape(size)
        print(a.shape)
        plt.imshow(a, cmap='gray', vmin=0, vmax=255)
    plt.show()
    plt.pause(0.001)

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
        dictionary = []
        for i in range(256):
            dictionary.append(i)


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
