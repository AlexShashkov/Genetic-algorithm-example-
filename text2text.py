from methods import genetic

offsprings = 500
selection = 10

while True:
    difference = -1
    iteration = 0
    inpstr = input('Input > ')
    endstr = input('Target > ')
    while difference != 0:
        inpstr, difference = genetic(inpstr, endstr, offsprings, selection, iteration, 'txt')
        if len(inpstr[0]) > 100:
            print(f'Iteration #{iteration+1}, min string difference - {difference} from \'{inpstr[0][:100]}...\'')
        else:
            print(f'Iteration #{iteration+1}, min string difference - {difference} from \'{inpstr[0]}\'')
        #plt.ion()
        #plot((inpjpg[0], endjpg), ('Input', 'Original'), size)
        iteration += 1
    print('done')