import csv
import pygame
from pygame.locals import *
import colors
from bag import Bag
import pandas as pd
from inputbox import InputBox
from button import Button
import numpy as np
import glob
import time
import sys
import ctypes

ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

DataPath = "./Data/"

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1500, 1200))
#screen = pygame.display.set_mode(true_res, pygame.FULLSCREEN)
screenWidth = screen.get_width()
screenHeight = screen.get_height()
fontSize = screenWidth // 40
welcomeTextSize = screenWidth // 23
biggerFontSize = screenWidth // 34
max_bonus_per_trial = 0.3


def text(size, text):
    myFont = pygame.font.Font('times-new-roman.ttf', size, bold=True)
    surface = myFont.render(text, True, colors.black)
    size = myFont.size(text)
    return surface, size


def question(q, pos, size=(300, 50), fontsize=fontSize, allowanswer=1, default='', waitForAnswer=1):
    qsurf = InputBox(screen, pos, size, q, allowanswer, fontsize=fontsize, a=default)
    pygame.display.update()
    finished = 0
    answer = None
    if waitForAnswer:
        while not finished:
            for event in pygame.event.get():
                finished, answer = qsurf.handle_event(event)
                qsurf.draw(screen)
                pygame.display.update()
    return answer


def welcome():
    screen.fill(colors.grey)
    welcome_text = "Welcome to the Experiment!"
    pygame.display.set_caption(welcome_text)
    welcome_surf, welcome_size = text(welcomeTextSize, welcome_text)
    screen.blit(welcome_surf, (screenWidth // 2 - welcome_size[0] // 2, screenHeight // 3))
    return welcome_size


def drawInstance(v, w, capacity, nInstance, buttonText='Submit', displayButton=True):
    bagList = pygame.sprite.Group()
    screen.fill(colors.grey)
    # draw instance number and capacity
    instance_surface, instance_surface_size = text(biggerFontSize, 'Instance ' + str(i + 1) + '/' + str(nInstance))
    capacity_surface, capacity_surface_size = text(biggerFontSize, 'Capacity: ' + str(int(capacity)) + ' kg')
    screen.blit(instance_surface, (fontSize * 3.33, fontSize))
    screen.blit(capacity_surface, (screenWidth / 2 - capacity_surface_size[0] / 2, fontSize))
    numItem = len(v)
    for j in range(0, len(v)):
        bag = Bag(w[j], v[j], screen, (screenWidth // 7, screenWidth // 7), j + 1, numItem)
        bagList.add(bag)
        bagList.update()
    bagList.draw(screen)
    submit_button = None
    if displayButton:
        submit_button = Button(biggerFontSize, (screenWidth - fontSize * 5, fontSize), text=buttonText)
        submit_button.update(screen)
    pygame.display.update()
    return bagList, submit_button, numItem


def checkExit():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()


prac_q = 'Practice (0=main): '
SID_q = 'SID: '
welcome_size = welcome()
qpos = (screenWidth // 2 - welcome_size[0] // 5, screenHeight // 7 * 4)
prac = int(question(prac_q, (qpos[0], qpos[1]), size=(int(fontSize * 25), int(fontSize * 1.67))))
t, _ = text(fontSize, prac_q + str(prac))
SID = question(SID_q, (qpos[0], qpos[1] + int(fontSize * 1.67)), size=(int(fontSize * 10), int(fontSize * 1.67)))
while True:
    if len(SID) != 3 or not SID.isdigit():
        question('SID should be an integer of length 3! Press enter to retry.',
                 (screenWidth // 2 - welcome_size[0] // 2, qpos[1] + int(fontSize * 1.67)), size=(int(fontSize * 33.33),
                                                                                                  int(fontSize * 1.67)),
                 allowanswer=0)
        welcome()
        screen.blit(t, (qpos[0], qpos[1]))
        SID = question(SID_q, (qpos[0], qpos[1] + int(fontSize * 1.67)),
                       size=(int(fontSize * 10), int(fontSize * 1.67)))
    else:
        if prac and glob.glob(DataPath + SID + '*prac.csv'):
            question('Prac data file exists! Press enter to ignore or esc to exit.',
                     (screenWidth // 2 - welcome_size[0] // 2, qpos[1] + int(fontSize * 1.67)),
                     size=(int(fontSize * 33.33),
                           int(fontSize * 1.67)), allowanswer=0)
            # welcome()
            # prac = int(question(prac_q, (qpos[0], qpos[1]), size=(750, 50), default='1'))
            # question(SID_q + SID, (qpos[0], qpos[1] + 50), allowanswer=0)
        elif not prac and glob.glob(DataPath + SID + '*main.csv'):
            question('Main task data file exists! Press enter to ignore or esc to exit.',
                     (screenWidth // 2 - welcome_size[0] // 2, qpos[1] + int(fontSize * 1.67)),
                     size=(int(fontSize * 33.33),
                           int(fontSize * 1.67)), allowanswer=0)
        welcome()
        screen.blit(t, (qpos[0], qpos[1]))
        t_SID, _ = text(fontSize, SID_q + SID)
        screen.blit(t_SID, (qpos[0], qpos[1] + int(fontSize * 1.67)))
        # question(SID_q, (qpos[0], qpos[1] + 50), default=SID,allowanswer=0)
        gender = question('Gender (F/M): ', (qpos[0], qpos[1] + int(fontSize * 3.33)),
                          size=(int(fontSize * 10), int(fontSize * 1.67)))
        age = question('Age: ', (qpos[0], qpos[1] + int(fontSize * 5)), size=(int(fontSize * 10), int(fontSize * 1.67)))
        break

# read instance
if prac:
    instances = pd.read_pickle('instances_prac.pkl')
    DataFileNameMain = DataPath + str(SID) + '_' + gender + '_' + age + '_prac.csv'
    DataFileNameTime = DataPath + str(SID) + '_' + gender + '_' + age + '_timing_prac.csv'
else:
    instances = pd.read_pickle('instances.pkl')
    DataFileNameMain = DataPath + str(SID) + '_' + gender + '_' + age + '_main.csv'
    DataFileNameTime = DataPath + str(SID) + '_' + gender + '_' + age + '_timing_main.csv'

# '''
# test only, need to comment out
# '''
# instances = pd.read_pickle('test.pkl')
# instances = instances.loc[instances['group']=='trans',:]
# '''
# test only, need to comment out
# '''

# create data file and write header
DataFileMain = open(DataFileNameMain, "w", newline='')
DataMain = csv.writer(DataFileMain)
DataMain.writerow(
    ['SID', 'gender', 'age', 'trial', 'step', 'submitted', 'instanceID', 'itemID', 'weight', 'value', 'selected',
     'totalWeight', 'totalValue', 'selectStatus', 'difficulty_estimate', 'performance_estimate',
     'difficulty_experienced','weights', 'values','capacity', 'group', 'solution_val', 'solution_comb', 'sahniK',
     'n_item', 'normalized_capacity', 'normalized_profit', 'ratio'])
DataFileMain.flush()

DataFileTime = open(DataFileNameTime, "w", newline='')
DataTime = csv.writer(DataFileTime)
DataTime.writerow(
    ['SID', 'trial', 'instanceID','step', 'instanceOnset', 'difficultyEstOnset', 'performanceEstOnset',
     'decisionStartOnset', 'stepTime'])
DataFileTime.flush()

# shuffle instance and save for this subject
if not prac:
    instances = instances.sample(frac=1)
    instances.reset_index(drop=True, inplace=True)
    instances.to_pickle(DataPath + SID + '_instance.pkl')
oriIdx = instances.index

bonus = 0
# iterate through instances
for i in range(0, len(instances)):
    v = instances.loc[i, 'values']
    w = instances.loc[i, 'weights']
    capacity = instances.loc[i, 'capacity']
    solution_val = instances['solution_val'][i]
    bagList, ready_button, numItem = drawInstance(v, w, capacity, len(instances), 'Ready', False)
    # ask participants to estimate difficulty and performance when ready
    instanceOnset = time.time()
    while time.time() - instanceOnset < 0.1:
        checkExit()
    # pygame.time.wait(5000)
    # ready = False
    # while not ready:
    #     events = pygame.event.get()
    #     for event in events:
    #         if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
    #             pos = pygame.mouse.get_pos()
    #             ready = ready_button.update(screen, pos)
    #             if ready:
    #                 pygame.time.wait(500)
    #         checkExit()
    difficulty_q = 'Please estimate the difficulty of the instance on a 1-10 scale (10 being most difficult):'
    leftPad = screenWidth // 10
    q_width = screenWidth - leftPad * 2
    difficulty_estimate_onset = time.time()
    while True:
        screen.fill(colors.grey)
        difficulty_estimate = question(difficulty_q, (leftPad, screenHeight // 3),
                                       size=(q_width, int(fontSize * 3.33)))
        if not difficulty_estimate.isnumeric() or int(difficulty_estimate) > 10 or int(difficulty_estimate) < 1:
            question(difficulty_q + '\nAnswer should be an integer between 1 and 10! Press Enter to try again.',
                     (leftPad, screenHeight // 3), size=(q_width, int(fontSize * 5)),
                     allowanswer=False)
        else:
            break
    performance_q = 'Please estimate the time in seconds that you will reach 90% of optimal value: '
    performance_estimate_onset = time.time()
    while True:
        screen.fill(colors.grey)
        question(difficulty_q + ' ' + difficulty_estimate,
                 (leftPad, screenHeight // 3), size=(q_width, int(fontSize * 5)),
                 allowanswer=False, waitForAnswer=0)
        performance_estimate = question(performance_q, (leftPad, screenHeight // 3 + int(fontSize * 3.33)),
                                        size=(q_width, int(fontSize * 5)))
        if not performance_estimate.isnumeric():
            question(performance_q + '\nAnswer should be an integer! Press Enter to try again.',
                     (leftPad, screenHeight // 3 + int(fontSize * 3.33)), size=(q_width, int(fontSize * 5)),
                     allowanswer=False)
        else:
            break
    bagList, submit_button, numItem = drawInstance(v, w, capacity, len(instances), 'Submit')
    decision_start_onset = time.time()
    select_status = np.zeros(numItem)  # a list of items select status
    submitted = False
    step = 0
    total_weight = 0
    total_value = 0
    difficulty_experienced = 0
    while not submitted:
        events = pygame.event.get()
        for event in events:
            # '''
            # test only need to comment out
            # '''
            # if event.type == pygame.KEYDOWN and event.key == K_k:
            #     solution_comb = instances['solution_comb'][i]
            #     print(solution_comb)
            #     for a, b in enumerate(bagList):
            #         if a in solution_comb:
            #             b.update(forceSelect=True)
            #         else:
            #             b.update(forceUnselect=True)
            #     bagList.draw(screen)
            #     pygame.display.update()
            #
            # '''
            # test only need to comment out
            # '''

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                # get which bag was clicked, and whether it was selected
                click_list = np.zeros(len(bagList))
                clicked_bag_idx = -1
                s = -1
                step_time = -1
                for bag_idx, bag in enumerate(bagList):
                    clicked, selected = bag.update(pos)
                    if clicked:
                        s = selected
                        click_list[bag_idx] = 1
                        step_time = time.time()
                        clicked_bag_idx = bag_idx
                        if selected:
                            select_status[clicked_bag_idx] = 1
                        else:
                            select_status[clicked_bag_idx] = 0
                        total_weight = np.sum(w[np.where(select_status == 1)[0]])
                        total_value = np.sum(v[np.where(select_status == 1)[0]])
                    else:
                        click_list[bag_idx] = 0
                bagList.draw(screen)
                submitted = submit_button.update(screen, pos)
                if all(click_list == 0) and submitted == 0:
                    pass
                else:
                    step += 1
                    print(step)
                    if submitted:
                        step_time = time.time()
                        pygame.time.wait(500)
                        if total_weight <= capacity:
                            bonus += max_bonus_per_trial * total_value / solution_val
                        while True:
                            screen.fill(colors.grey)
                            difficulty_q = 'Having done this instance, please rate the difficulty of it on a 1-10 ' \
                                           'scale (10 being most difficult): '
                            difficulty_experienced = question(difficulty_q, (leftPad, screenHeight // 3),
                                                              size=(q_width, int(fontSize * 3.33)))
                            if not difficulty_experienced.isnumeric() or int(difficulty_experienced) > 10 or int(
                                    difficulty_experienced) < 1:
                                question(difficulty_q + '\nAnswer should be an integer between 1 and 10! Press '
                                                        'Enter to try again.', (leftPad, screenHeight // 3),
                                         size=(q_width, int(fontSize * 5)),
                                         allowanswer=False)
                            else:
                                break
                    dataToWrite = [SID, gender, age, i, step, submitted, oriIdx[i], clicked_bag_idx, w[clicked_bag_idx],
                                   v[clicked_bag_idx], s, total_weight, total_value, select_status,
                                   difficulty_estimate, performance_estimate,difficulty_experienced]
                    for x in instances.iloc[i,].values:
                        dataToWrite.append(x)
                    DataMain.writerow(dataToWrite)
                    DataTime.writerow(
                        [SID, i, oriIdx[i], step, instanceOnset, difficulty_estimate_onset,
                         performance_estimate_onset, decision_start_onset, step_time])
                    DataFileTime.flush()
                    DataFileMain.flush()
            elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

screen.fill(colors.grey)
goodbye_surface, goodbye_size = text(54, 'Congrats, You\'ve finished the task!')
bonus_surface, bonus_size = text(54, 'You earned a bonus of $' + str(np.round(bonus, 2)) + '!')
screen.blit(goodbye_surface, (screenWidth / 2 - goodbye_size[0] / 2, screenHeight / 2 - goodbye_size[1]))
if not prac:
    screen.blit(bonus_surface, (screenWidth / 2 - bonus_size[0] / 2, screenHeight / 2 + 50))
pygame.display.update()
onset = time.time()
while time.time() - onset < 100:
    checkExit()
