import cv2

from methods import genetic

offsprings = 150
selection = 10

size = (28, 28)

while True:
    inpjpg = input('Введите путь к изображению > ')
    endjpg = input('Введите путь к изображению > ')
    inpjpg = cv2.imread(inpjpg, 0)
    inpjpg = cv2.resize(inpjpg, size)
    endjpg = cv2.imread(endjpg, 0)
    endjpg = cv2.resize(endjpg, size)
    print(endjpg.shape)
    #print(endjpg.flatten())
    genetic(inpjpg.flatten(), endjpg.flatten(), offsprings, selection, 'gray', size)