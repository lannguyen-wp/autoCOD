import win32gui,  pynput, pyautogui
import time, json

cod_window = win32gui.FindWindow(None, 'Call of Dragons')
rect = win32gui.GetWindowRect(cod_window)
xo = rect[0]
yo = rect[1]
wo = rect[2] - xo
ho = rect[3] - yo

wb = 1456; hb = 939
x_ratio = wo / wb; y_ratio = ho / hb
 
### Mouse and Keyboard Control ------------------------------------------------
def mouse_click(x, y, n=1, d=1):
    x = x + xo
    y = y + yo
    pyautogui.moveTo(x, y)
    for i in range(n):
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        time.sleep(d)

def mouse_drag(x1, y1, x2, y2, d=3):
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()
    pyautogui.dragTo(x2, y2, d, button='left')
    pyautogui.mouseUp()
    time.sleep(1)

def resizeImage(img, odir, oname='NA'):
    import os
    from PIL import Image
    image = Image.open(img)
    image_name = os.path.basename(img)
    ow, oh = image.size
    nw = int(ow * x_ratio)
    nh = int(oh * y_ratio)
    nimage = image.resize((nw, nh))
    if oname=='NA':
        oname = image_name
    nimage.save(odir + '\\' + oname)
    image.close()
          
def searchIcon(img, confidence=.8, grayscale=False, region=[]):
    try:
        #resizeImage(img, 'D:\\myClicker\\png\\res_base\\misc', 'tmp.png')
        #img = 'D:\\myClicker\\png\\res_base\\misc\\tmp.png'
        if region==[]:
            x, y = pyautogui.locateCenterOnScreen(img, 
                                                  confidence = confidence, 
                                                  grayscale = grayscale)
        else:
            x, y = pyautogui.locateCenterOnScreen(img,
                                                  confidence = confidence, 
                                                  grayscale = grayscale, 
                                                  region = region)
        return x - xo, y - yo
    except pyautogui.ImageNotFoundException:
        return 0, 0
    
def press_buttons(button, n=1, d=1):
    for i in range(n):
        pyautogui.press(button)
        time.sleep(d)
### ---------------------------------------------------------------------------        

### Game Control --------------------------------------------------------------
def reconnect():
    x1, y1 = searchIcon(png + '\\reconnect\\another_device.png')
    x2, y2 = searchIcon(png + '\\reconnect\\lost_internet.png')
    x3, y3 = searchIcon(png + '\\reconnect\\startButton.png')
    if (x1 + y1)>0:
        time.sleep(60 * reconnect_break)
    if (x1 + y1 + x2 + y2 + x3 + y3)> 0:
        x, y = searchIcon(png + '\\reconnect\\confirmButton.png')
        if (x + y)>0:
            mouse_click(x, y)
            time.sleep(2)
        x, y = searchIcon(png + '\\reconnect\\startButton.png')
        if (x + y)>0:
            mouse_click(x, y)
            time.sleep(2)
        time.sleep(30)
    x, y = searchIcon(png + '\\misc\\back.png')
    if (x + y)>0:
        mouse_click(x, y)

def reset():
    x, y = searchIcon(png + '\\reconnect\\exitIcon.png')
    mouse_click(x, y)
    time.sleep(3)
    x, y = searchIcon(png + '\\reconnect\\startButton.png')
    mouse_click(x, y)
    time.sleep(30)
    x, y = searchIcon(png + '\\misc\\back.png')
    if (x + y)>0:
        mouse_click(x, y)

def clickHelp():
    x, y = searchIcon(png + '\\misc\\give_help.png')
    mouse_click(x, y)
    x, y = misc['background']
    mouse_click(x, y)

def scoutMap():
    x, y = buildings['scout_camp']
    mouse_click(x, y)
    x, y = searchIcon(png + '\\scout\\scoutIcon.png')
    mouse_click(x, y)
    x, y = searchIcon(png + '\\scout\\exploreButton.png')
    if (x+y)>0:
        mouse_click(x, y)
        time.sleep(1.5)
        x, y = searchIcon(png + '\\scout\\exploreButton.png')
        mouse_click(x, y)
        x, y = searchIcon(png + '\\scout\\marchButton.png')
        mouse_click(x, y)
        press_buttons('space', 1)
        time.sleep(1)
        scoutMap()
    else:
        x, y = misc['background']
        mouse_click(x, y)
        
def upgradeBuilding(buildQueues):
    reconnect()
    buildTypes = list(buildQueues.keys())
    xr, yr = searchIcon(png + '\\build\\upgradeIcon1.png')
    cycle = 0
    while (xr + yr) > 0:
        if cycle == 5:
            break
        for buildType in buildTypes:
            buildTimes = buildQueues[buildType]
            if buildTimes > 0:
                x, y = buildings[buildType]
                mouse_click(x, y)
                x, y = searchIcon(png + '\\misc\\speedupIcon.png')
                if (x + y) == 0:
                    x, y = searchIcon(png + '\\build\\upgradeIcon2.png')
                    if (x + y) > 0:
                        mouse_click(x, y)
                        x, y = misc['runButton']
                        mouse_click(x, y)
                        time.sleep(1) 
                        x, y = searchIcon(png + '\\misc\\need_help.png')
                        mouse_click(x, y) 
                        buildQueues[buildType] = buildTimes - 1
                        print(buildQueues)
                x, y = misc['background']
                mouse_click(x, y)
                xr, yr = searchIcon(png + '\\build\\upgradeIcon1.png')
        cycle += 1

def doResearch(researchQueues):
    reconnect()
    researchTypes = list(researchQueues.keys())
    x, y = buildings['college_of_order']
    mouse_click(x, y, 2)
    x, y = searchIcon(png + '\\research\\researchIcon.png')
    mouse_click(x, y)
    x, y = misc['background']
    mouse_click(x, y)
    researchers = 2
    lx, uy, w, h = researches['findResearchers'][0]
    x11, y11 = searchIcon(png + '\\research\\speedupButton_small.png', 
                        region = (lx + xo, uy + yo, w, h))
    x12, y12 = searchIcon(png + '\\research\\unlockButton.png', 
                        region = (lx + xo, uy + yo, w, h))
    lx, uy, w, h = researches['findResearchers'][1]
    x2, y2 = searchIcon(png + '\\research\\speedupButton_small.png', 
                        region = (lx + xo, uy + yo, w, h))
    if (x11 + y11 + x12 + y12) > 0:
        researchers = researchers - 1
    if (x2 + y2) > 0:
        researchers = researchers - 1
    cycle = 0
    while researchers > 0:
        cycle += 1
        if cycle == 5:
            break
        for researchType in researchTypes:
            mouse_drag(wo/2 - 300, ho/2, wo/2 + 1000, ho/2, d=0.2)
            mouse_drag(wo/2 - 300, ho/2, wo/2 + 1000, ho/2, d=0.2)
            researchTimes = researchQueues[researchType]
            if researchTimes > 0:
                # select right research tab and turn pages
                if (researchType in (researches['econ_p1'] + researches['econ_p2'] + researches['econ_p3'])):
                    x1, y1 = searchIcon(png + '\\research\\economy_tech1.png')
                    x2, y2 = searchIcon(png + '\\research\\economy_tech2.png')
                    if (x1 + y1)>0:
                        mouse_click(x1, y1)
                    elif (x2 + y2)>0:
                        mouse_click(x2, y2)
                if (researchType in (researches['mili_p1'] + researches['mili_p2'] + researches['mili_p3'])):
                    x1, y1 = searchIcon(png + '\\research\\military_tech1.png')
                    x2, y2 = searchIcon(png + '\\research\\military_tech2.png')
                    if (x1 + y1)>0:
                        mouse_click(x1, y1)
                    elif (x2 + y2)>0:
                        mouse_click(x2, y2)
                x1 = researches['turn_page'][0]  + xo
                x2 = researches['turn_page'][2]  + xo
                y  = researches['turn_page'][1]  + yo 
                turn_page = 0
                if (researchType in (researches['econ_p2'] + researches['mili_p2'])):
                    turn_page = 1
                if (researchType in (researches['econ_p3'] + researches['mili_p3'])):
                    turn_page = 2
                if (researchType in (researches['econ_p4'] + researches['mili_p4'])):
                    turn_page = 3 
                if turn_page>0:
                    for i in range(turn_page):
                        mouse_drag(x1, y, x2, y)
                        time.sleep(1)
                # find research icon and click research
                x, y = searchIcon(png + f'\\research\\{researchType}.png')
                if (x + y)>0:
                    mouse_click(x, y)
                    x, y = searchIcon(png + '\\research\\researchButton.png')
                    if (x + y)>0:   
                        mouse_click(x, y)
                        x, y = searchIcon(png + '\\misc\\back.png')
                        mouse_click(x, y)
                        x, y = searchIcon(png + '\\misc\\need_help.png')
                        mouse_click(x, y)
                        researchQueues[researchType] = researchTimes - 1
                        print(researchQueues)
                    else:
                        x, y = misc['background']
                        mouse_click(x, y)
                else:
                    x, y = searchIcon(png + '\\misc\\back.png')
                    mouse_click(x, y)
                x, y = misc['background']
                mouse_click(x, y)
    x, y = searchIcon(png + '\\misc\\back.png')
    mouse_click(x, y)
    x, y = misc['background']
    mouse_click(x, y)

def enact(policyQueues):
    reconnect()
    policyTypes = list(policyQueues.keys())
    x, y = buildings['notice_board']
    mouse_click(x, y, 2)
    x, y = searchIcon(png + '\\policy\\enactIcon.png')
    if (x + y)>0:
        mouse_click(x, y)
        for policyType in policyTypes:
            mouse_drag(wo/2 - 300, ho/2, wo/2 + 1000, ho/2, d=0.2)
            enactTimes = policyQueues[policyType]
            if enactTimes > 0:
                if policyType in policies['p2']:
                    x1 = policies['turn_page'][0]  + xo
                    x2 = policies['turn_page'][2]  + xo
                    y  = policies['turn_page'][1]  + yo
                    mouse_drag(x1, y, x2, y)
                x, y = searchIcon(png + f'\\policy\\{policyType}.png')
                if (x + y) > 0:
                    mouse_click(x, y)
                    x, y = searchIcon(png + '\\policy\\enactButton.png')
                    if (x + y) > 0:
                        mouse_click(x, y)
                        x, y = searchIcon(png + '\\misc\\back.png')
                        mouse_click(x, y)
                        x, y = searchIcon(png + '\\misc\\need_help.png')
                        mouse_click(x, y)
                        x, y = misc['background']
                        mouse_click(x, y)
                        policyQueues[policyType] = enactTimes - 1
                        print(policyQueues)
                    else:
                        x, y = misc['background']
                        mouse_click(x, y)
    x, y = misc['background']
    mouse_click(x, y)

def trainTroops(troopType, troopLevel, upgrade=0):
    reconnect()
    # select troop type to be trained
    x, y = buildings[troopType]
    mouse_click(x, y, 2)
    x1, y1 = searchIcon(png + '\\misc\\speedupIcon.png')
    x2, y2 = searchIcon(png + f'\\train\\train_{troopType[0].upper()}.png')
    if ((x1 + y1)==0) and ((x1+y2)>0):
        mouse_click(x2, y2)
        # select troop level to be trained
        if troopType[0].upper()=='C':
            x, y = troopLV2[str(troopLevel)]
        else:
            x, y = troopLV1[str(troopLevel)]
        mouse_click(x, y)
        if upgrade==1:
            x, y = searchIcon(png + '\\train\\upgradeTroop.png')
            mouse_click(x, y)
        x, y = misc['runButton']
        mouse_click(x, y)
        time.sleep(1)
    else:
        x, y = misc['background']
        mouse_click(x, y)    

def check_legionQueue():
    reconnect()
    availableLegions = []
    x, y = searchIcon(png + '\\rss\\player.png')
    mouse_click(x, y)
    x, y = searchIcon(png + '\\rss\\legion.png')
    mouse_click(x, y)
    x1, y1 = searchIcon(png + '\\rss\\legionQueue_3.png',
                        confidence = 0.95,
                        grayscale = True)
    x2, y2 = searchIcon(png + '\\rss\\legionQueue_4.png',
                        confidence = 0.95,
                        grayscale = True)
    if (x1 + y1 + x2 + y2)>0:
        pass
    else:
        x, y = searchIcon(png + '\\rss\\infield.png')
        if (x + y) > 0:
            mouse_click(x, y)
        x_l1, y_l1 = searchIcon(png + '\\rss\\legion_1.png')
        x_l2, y_l2 = searchIcon(png + '\\rss\\legion_2.png')
        x_l3, y_l3 = searchIcon(png + '\\rss\\legion_3.png')
        x_l4, y_l4 = searchIcon(png + '\\rss\\legion_4.png')
        x_l5, y_l5 = searchIcon(png + '\\rss\\legion_5.png')
        if (x_l1 + y_l1)==0:
            availableLegions.append(1)  
        if (x_l2 + y_l2)==0:
            availableLegions.append(2) 
        if (x_l3 + y_l3)==0:
            availableLegions.append(3) 
        if (x_l4 + y_l4)==0:
            availableLegions.append(4) 
        if (x_l5 + y_l5)==0:
            availableLegions.append(5)
        time.sleep(1)
        mouse_drag(wo/2 + xo, ho/2 + yo + 300, wo/2 + xo, ho/2 + yo + 200, 1)
        x_l1, y_l1 = searchIcon(png + '\\rss\\legion_1.png')
        x_l2, y_l2 = searchIcon(png + '\\rss\\legion_2.png')
        x_l3, y_l3 = searchIcon(png + '\\rss\\legion_3.png')
        x_l4, y_l4 = searchIcon(png + '\\rss\\legion_4.png')
        #x_l5, y_l5 = searchIcon(png + '\\rss\\legion_5.png')
        if (x_l1 + y_l1)==0 and (1 not in availableLegions):
            availableLegions.append(1)    
        if (x_l2 + y_l2)==0 and (2 not in availableLegions):
            availableLegions.append(2) 
        if (x_l3 + y_l3)==0 and (3 not in availableLegions):
            availableLegions.append(3)
        if (x_l4 + y_l4)==0 and (4 not in availableLegions): 
            availableLegions.append(4) 
        if (x_l5 + y_l5)==0 and (5 not in availableLegions):
            availableLegions.append(5)
    x, y = misc['background']
    mouse_click(x, y, 2)   
    return availableLegions

def gatherRSS():
    import random
    reconnect()
    available = check_legionQueue()
    cycle = 0
    while len(available)>0:
        cycle += 1
        if cycle == 10:
            break
        reconnect()
        picked = random.choice(available)
        press_buttons('space', 1)
        options = rssOptions['gather_' + str(picked)]
        rssType = random.choice(options)
        press_buttons('f', 1)
        time.sleep(1)
        x, y = rssTypes[rssType]
        mouse_click(x, y)
        x, y = searchIcon(png + '\\rss\\searchButton.png')
        mouse_click(x, y)
        x, y = rssTypes['center']
        mouse_click(x, y)
        x, y = searchIcon(png + f'\\rss\\{rssType}.png')
        if (x+y)>0:
            x, y = searchIcon(png + '\\rss\\gather.png')  
            if (x+y)>0:
                mouse_click(x, y)
                x, y = searchIcon(png + '\\rss\create_legion.png')
                mouse_click(x, y)    
                x, y = legions['s']
                mouse_click(x, y)
                x, y = legions[str(picked)]
                mouse_click(x, y)
                x, y = misc['runButton']
                mouse_click(x, y)
                print("legion ", picked, " -- ", rssType)
                press_buttons('space', 1)
                available = check_legionQueue()
                
def execution(taskControl):        
    cycle = 0
    while True:
        print(f'cycle: {cycle}')
        if (cycle % reset_cycles)==0 and (cycle>0):
            reset()
        press_buttons('space', 2)
        if taskControl['scoutMap']==1:
            try:
                print("scout")  
                scoutMap()
            except:
                print('cannot perform "scout"') 
        if taskControl['clickHelp']==1:
            clickHelp()  
        if taskControl['build']==1:
            try:
                print("build")
                upgradeBuilding(buildQueues)
            except:
                print('cannot perform "build"')
        if taskControl['research']==1:
            try:
                print("research")
                doResearch(researchQueues)
            except:
                print('cannot perform "research"')
        if taskControl['policy']==1:
            try:
                print("policy")
                enact(policyQueues)
            except:
                print('cannot perform "policy"')
        if taskControl['train']==1:
            try:
                print("train")
                trainTroops('swordsmen_camp'  , trainTroop['train_infantry'][0], trainTroop['train_infantry'][1])
                trainTroops('abbey'           , trainTroop['train_magic'][0], trainTroop['train_infantry'][1])
                trainTroops('knight_camp'     , trainTroop['train_calvary'][0], trainTroop['train_infantry'][1])
                trainTroops('ballista_factory', trainTroop['train_marksman'][0], trainTroop['train_infantry'][1])
                trainTroops('celestial_temple', trainTroop['train_flying'][0], trainTroop['train_infantry'][1])
            except:
                print('cannot perform "train"')
        if taskControl['gather']==1:
            try:
                print("gather")
                gatherRSS()
            except:
                print('cannot perform "gather"')
        cycle += 1 
        time.sleep(60 * cycle_break)
### ---------------------------------------------------------------------------

### Load Params ---------------------------------------------------------------
wdir = "D:\\myClicker"
png  = wdir + '\\png\\res_base'
f = open(wdir + '\\params\\main.txt')
main = json.load(f)
f.close()
start_delay = main[0]["start_delay"]
cycle_break = main[0]["cycle_break"]
reconnect_break = main[0]["reconnect_break"]
reset_cycles =  main[0]["reset_cycles"]

buildQueues     = main[1]
researchQueues  = main[2]
policyQueues    = main[3]
trainTroop      = main[4]
rssOptions      = main[5]
taskControl     = main[6]

f = open(wdir + '\\params\\buildings_xy.txt')
buildings = json.load(f)
f.close()
  
f = open(wdir + '\\params\\troopLevels_xy.txt')      
troopLV = json.load(f)
f.close()
troopLV1 = troopLV[0]
troopLV2 = troopLV[1]

f = open(wdir + '\\params\\rssTypes_xy.txt') 
rssTypes = json.load(f)
f.close()

f = open(wdir + '\\params\\legions_xy.txt')
legions = json.load(f)
f.close()

f = open(wdir + '\\params\\misc_xy.txt')
misc = json.load(f)
f.close()

f = open(wdir + '\\params\\policies.txt')
policies = json.load(f)
f.close()

f = open(wdir + '\\params\\researches.txt')
researches = json.load(f)
f.close()
### --------------------------------------------------------------------------- 


from datetime import datetime
ctime = datetime.now()
edate = datetime(2024, 2, 24)  
passcode = input("Tell me what you think:") 
if ((passcode=='BellyBeo is so handsome !!!') and (ctime < edate)) or (passcode=='sieumeovn'):
    time.sleep(60 * start_delay)
    execution(taskControl)


#time.sleep(60 * start_delay)
#execution(taskControl)  
