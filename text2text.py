from methods import genetic

offsprings = 500
selection = 10

while True:
    inpstr = input('Введите любое слово, число, сочетание слов и чисел > ')
    endstr = input('Введите любое слово, число, сочетание слов и чисел > ')
    genetic(inpstr, endstr, offsprings, selection)