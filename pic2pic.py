import cv2
import numpy as np

from matplotlib import pyplot as plt
from threading import Thread
from methods import genetic, compare

offsprings = 50
selection = 10
threads = 100
min_to_stop = 0

size = (100, 100)

stop_run_on = []
    
class splitThread(Thread):
    # Multi-threading support class
    def __init__(self, x, y, iteration, position, ret):
        Thread.__init__(self)
        self.position = position
        self.x = x
        self.y = y
        self.iteration = iteration
        self.ret = ret
    
    def run(self):
    # Thread run
        x = None
        x, difference = genetic(self.x, self.y, offsprings, selection, self.iteration, 'gray')
        if difference <= min_to_stop:
            stop_run_on.append(self.position)
        self.ret[self.position] = x


def plot(X, xlabel, size, delay=0.001):
    plt.figure(1)
    for i in range(len(X)):
        plt.subplot(1, 2, i+1)
        plt.xlabel(xlabel[i])
        a = None
        if type(X[i]) == list or type(X[i]) == tuple:
            a = np.asarray(X[i]).reshape(size)
        else:
            a = X[i].reshape(size)
        print(a.shape)
        plt.imshow(a, cmap='gray', vmin=0, vmax=255)
    plt.show()
    plt.pause(delay)

iteration = 0
difference = -1
inp = input('Input image > ')
end = input('Target image > ')
inpjpg = cv2.imread(inp, 0)
inpjpg = cv2.resize(inpjpg, size).flatten()
endjpg = cv2.imread(end, 0)
endjpg = cv2.resize(endjpg, size).flatten()
splittedend = np.split(endjpg, threads)

while difference > min_to_stop or difference == -1:
    if iteration == 0:
        inpjpg = np.split(inpjpg.flatten(), threads)
    else:
        for i in range(selection):
            inpjpg[i] = np.asarray(inpjpg[i])                   # BRUH MOMENTo
            inpjpg[i] = np.split(inpjpg[i], threads)

    split = {}

    if iteration != 0:
        inp = []
        for i in range(threads):
            inp.append([])
        for i in range(selection):
            for j in range(threads):
                inp[j].append(inpjpg[i][j])
        for i in range(threads):
            if i not in stop_run_on:
                thread = splitThread(inp[i], splittedend[i], iteration, i, split)
                thread.run()
            else:
                split[i] = inp[i]
    else:
        for i in range(threads):
            thread = splitThread(inpjpg[i], splittedend[i], iteration, i, split)
            thread.run()
            
        
    X = []
    inpjpg = None

    if iteration == 0:
        for i in range(selection):
            for j in range(threads):
                if j == 0:
                    inpjpg = list(split[0][i])
                else:
                    inpjpg.extend(list(split[j][i]))
            X.append(inpjpg)
    else:
        for i in range(selection):
            for j in range(threads):
                if j == 0:
                    inpjpg = list(split[0][i])
                else:
                    inpjpg.extend(list(split[j][i]))
            X.append(inpjpg)

    plt.ion()
    if iteration % 100 == 0:
        plot((X[0], endjpg), ('Input', 'Target'), size)

    difference = compare(X[0], endjpg)
    inpjpg = X

    if len(X[0]) > 100:
        print(f'Iteration #{iteration+1}, min pic difference - {difference} from \'{X[0][:100]}...\'')
    else:
        print(f'Iteration #{iteration+1}, min pic difference - {difference} from \'{X[0]}\'')
    iteration += 1

plot((X[0], endjpg), ('Input', 'Target'), size, 10)
print('done.')