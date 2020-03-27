import math
import random
import pygame
import time
import threading

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color


    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)




class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()

def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)

def main():
    pygame.init()
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True


#####################     DISPLAY 1 SETUP     #####################
    screen = pygame.display.set_mode((width, width))
    font = pygame.font.Font(None, 32)
    titlefont = pygame.font.Font(None,48)
    t1font = pygame.font.Font(None,32)
    t2font = pygame.font.Font(None,32)
    errorfont = pygame.font.Font(None,32)
    input_box = pygame.Rect(300, 200, 140, 32)
    input_box2 = pygame.Rect(300, 250, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    error_color = pygame.Color("red")
    color = color_inactive
    activebox1 = False
    activebox2 = False
    text1 = ''
    text2 = ''
    t1 = "16 digit card number"
    t2 = "3 digit CVV code"
    error = "Code must be 16 digits CVV must be 3 digits"
    titletext = font.render("Enter your debit card information to continue!!!",True,color_active,None)
    titlerect = titletext.get_rect()
    titlerect.center = (width//2, 25)
    t1text = font.render(t1,True,color_active,None)
    t1rect = t1text.get_rect()
    t1rect.center = (125,215)
    t2text = font.render(t2,True,color_active,None)
    t2rect = t2text.get_rect()
    t2rect.center = (125,265)
    errortext = font.render(error,True,error_color,None)
    errorrect = errortext.get_rect()
    errorrect.center = (width//2,400)
    errorflg = False
    done = False

#####################     DISPLAY 2 SETUP     #####################
    bankscreen = pygame.display.set_mode((width, width))
    bankfont = pygame.font.Font(None, 32)
    banktitlefont = pygame.font.Font(None,48)
    bankt1font = pygame.font.Font(None,32)
    bankt2font = pygame.font.Font(None,32)
    bankerrorfont = pygame.font.Font(None,32)
    bankinput_box = pygame.Rect(300, 200, 140, 32)
    bankinput_box2 = pygame.Rect(300, 250, 140, 32)
    bankcolor_inactive = pygame.Color('lightskyblue3')
    bankcolor_active = pygame.Color('dodgerblue2')
    bankerror_color = pygame.Color("red")
    bankcolor = color_inactive
    bankactivebox1 = False
    bankactivebox2 = False
    banktext1 = ''
    banktext2 = ''
    bankt1 = "Username"
    bankt2 = "Password"
    bankerror = "you must enter something into every field"
    banktitletext = font.render("Enter your online bank information to continue!!!",True,color_active,None)
    banktitlerect = titletext.get_rect()
    banktitlerect.center = (width//2, 25)
    bankt1text = font.render(bankt1,True,color_active,None)
    bankt1rect = bankt1text.get_rect()
    bankt1rect.center = (125,215)
    bankt2text = font.render(bankt2,True,color_active,None)
    bankt2rect = bankt2text.get_rect()
    bankt2rect.center = (125,265)
    bankerrortext = font.render(bankerror,True,bankerror_color,None)
    bankerrorrect = bankerrortext.get_rect()
    bankerrorrect.center = (width//2,400)
    bankerrorflg = False
    bankdone = False

#####################     DISPLAY 3 SETUP     #####################
    ssnscreen = pygame.display.set_mode((width, width))
    ssnfont = pygame.font.Font(None, 32)
    ssntitlefont = pygame.font.Font(None,48)
    ssnt1font = pygame.font.Font(None,32)
    ssnerrorfont = pygame.font.Font(None,32)
    ssninput_box = pygame.Rect(300, 200, 140, 32)
    ssncolor_inactive = pygame.Color('lightskyblue3')
    ssncolor_active = pygame.Color('dodgerblue2')
    ssnerror_color = pygame.Color("red")
    ssncolor = color_inactive
    ssnactivebox1 = False
    ssntext1 = ''
    ssnt1 = "Social Security Number"
    ssnerror = "your social security number should be 9 digits"
    ssntitletext = font.render("Enter your social security number to continue!!!",True,color_active,None)
    ssntitlerect = titletext.get_rect()
    ssntitlerect.center = (width//2, 25)
    ssnt1text = font.render(ssnt1,True,color_active,None)
    ssnt1rect = ssnt1text.get_rect()
    ssnt1rect.center = (125,215)
    ssnerrortext = font.render(ssnerror,True,ssnerror_color,None)
    ssnerrorrect = ssnerrortext.get_rect()
    ssnerrorrect.center = (width//2,400)
    ssnerrorflg = False
    ssndone = False

#####################     DISPLAY 4 SETUP     #####################
    vscreen = pygame.display.set_mode((width, width))
    vfont = pygame.font.Font(None, 32)
    vtitlefont = pygame.font.Font(None,40)
    vt1font = pygame.font.Font(None,56)
    vt2font = pygame.font.Font(None,30)
    vcolor_inactive = pygame.Color('lightskyblue3')
    vcolor_active = pygame.Color('dodgerblue2')
    verror_color = pygame.Color("red")
    vcolor = color_inactive
    vt1 = "@Nicholas-Wachter-2"
    vt2 = "the press enter to coninue"
    vtitletext = vtitlefont.render("Venmo me $500 to continue!!!!!",True,color_active,None)
    vtitlerect = titletext.get_rect()
    vtitlerect.center = (width//2+50,200)
    vt1text = vt1font.render(vt1,True,color_active,None)
    vt1rect = vt1text.get_rect()
    vt1rect.center = (width//2,width//2)
    vt2text = vt2font.render(vt2,True,color_active,None)
    vt2rect = vt2text.get_rect()
    vt2rect.center = (width//2,450)
    vdone = False

    clock = pygame.time.Clock()
    check = 0
    turn = 1
    paused = False
    while flag:
        if paused == True and turn == 1:
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # If the user clicked on the input_box rect.
                        if input_box.collidepoint(event.pos):
                            # Toggle the active variable.
                            activebox1 = not activebox1
                        else:
                            activebox1 = False
                        if input_box2.collidepoint(event.pos):
                            activebox2 = not activebox2
                            activebox1 = False
                        else:
                            activebox2 = False
                        # Change the current color of the input box.
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if len(text2)==3 and len(text1)==16:
                                paused = False
                                turn = 2
                            else:
                                errorflg = True
                            text1 = ''
                            text2 = ''
                        if activebox1:
                            if event.key == pygame.K_BACKSPACE:
                                text1 = text1[:-1]
                            else:
                                text1 += event.unicode
                        elif activebox2:
                            if activebox2:
                                if event.key == pygame.K_BACKSPACE:
                                    text2 = text2[:-1]
                                else:
                                    text2 += event.unicode
                if paused == False:
                    break
                screen.fill((30, 30, 30))
                # Render the current text.
                txt_surface = font.render(text1, True, color)
                txt_surface2 = font.render(text2,True,color)
                # Resize the box if the text is too long.
                width = max(200, txt_surface.get_width()+10)
                width2 = max(200,txt_surface2.get_width()+10)
                input_box.w = width
                input_box2.w = width2
                # Blit the text.
                screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                screen.blit(txt_surface2, (input_box2.x+5, input_box2.y+5))
                screen.blit(titletext,titlerect)
                screen.blit(t1text,t1rect)
                screen.blit(t2text,t2rect)
                if errorflg:
                    screen.blit(errortext,errorrect)
                # Blit the input_box rect.
                pygame.draw.rect(screen, color, input_box, 2)
                pygame.draw.rect(screen, color, input_box2, 2)

                pygame.display.flip()
                clock.tick(30)
        elif paused == True and turn == 2:
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # If the user clicked on the input_box rect.
                        if bankinput_box.collidepoint(event.pos):
                            # Toggle the active variable.
                            bankactivebox1 = not bankactivebox1
                            activebox2 = False
                        else:
                            bankactivebox1 = False
                        if bankinput_box2.collidepoint(event.pos):
                            bankactivebox2 = not activebox2
                            bankactivebox1 = False
                        else:
                            bankactivebox2 = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if len(banktext2)>0 and len(banktext1)>0:
                                paused = False
                                turn = 3
                            else:
                                bankerrorflg = True
                            banktext1 = ''
                            banktext2 = ''
                        if bankactivebox1:
                            if event.key == pygame.K_BACKSPACE:
                                banktext1 = banktext1[:-1]
                            else:
                                banktext1 += event.unicode
                        elif bankactivebox2:
                            if bankactivebox2:
                                if event.key == pygame.K_BACKSPACE:
                                    banktext2 = banktext2[:-1]
                                else:
                                    banktext2 += event.unicode
                if paused == False:
                    break
                screen.fill((30, 30, 30))
                # Render the current text.
                banktxt_surface = font.render(banktext1, True, color)
                banktxt_surface2 = font.render(banktext2,True,color)
                # Resize the box if the text is too long.
                bankwidth = max(200, banktxt_surface.get_width()+10)
                bankwidth2 = max(200,banktxt_surface2.get_width()+10)
                bankinput_box.w = bankwidth
                bankinput_box2.w = bankwidth2
                # Blit the text.
                screen.blit(banktxt_surface, (bankinput_box.x+5, bankinput_box.y+5))
                screen.blit(banktxt_surface2, (bankinput_box2.x+5, bankinput_box2.y+5))
                screen.blit(banktitletext,banktitlerect)
                screen.blit(bankt1text,bankt1rect)
                screen.blit(bankt2text,bankt2rect)
                if bankerrorflg:
                    screen.blit(bankerrortext,bankerrorrect)
                # Blit the input_box rect.
                pygame.draw.rect(bankscreen, color, bankinput_box, 2)
                pygame.draw.rect(bankscreen, color, bankinput_box2, 2)

                pygame.display.flip()
                clock.tick(30)
        elif paused == True and turn == 3:
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # If the user clicked on the input_box rect.
                        if ssninput_box.collidepoint(event.pos):
                            # Toggle the active variable.
                            ssnactivebox1 = not ssnactivebox1
                        else:
                            ssnactivebox1 = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if len(ssntext1)==9:
                                paused = False
                                turn = 4
                            else:
                                ssnerrorflg = True
                            ssntext1 = ''
                        if ssnactivebox1:
                            if event.key == pygame.K_BACKSPACE:
                                ssntext1 = ssntext1[:-1]
                            else:
                                ssntext1 += event.unicode
                if paused == False:
                    break
                screen.fill((30, 30, 30))
                # Render the current text.
                ssntxt_surface = font.render(ssntext1, True, color)
                # Resize the box if the text is too long.
                ssnwidth = max(200, ssntxt_surface.get_width()+10)
                ssninput_box.w = ssnwidth
                # Blit the text.
                screen.blit(ssntxt_surface, (ssninput_box.x+5, ssninput_box.y+5))
                screen.blit(ssntitletext,ssntitlerect)
                screen.blit(ssnt1text,ssnt1rect)
                if ssnerrorflg:
                    screen.blit(ssnerrortext,ssnerrorrect)
                # Blit the input_box rect.
                pygame.draw.rect(ssnscreen, color, ssninput_box, 2)
                pygame.display.flip()
                clock.tick(30)
        elif paused == True and turn == 4:
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            paused = False
                if paused == False:
                    break
                screen.fill((30, 30, 30))
                # Render the current text.
                screen.blit(vtitletext,vtitlerect)
                screen.blit(vt1text,vt1rect)
                screen.blit(vt2text,vt2rect)
                pygame.display.flip()
                clock.tick(30)
        else:
            if (len(s.body)+1)%2 == 0 and check == 0 and len(s.body)+1 != 2:
                paused = True
                check = 1
            else:
                if (len(s.body)+1)%2!=0 and len(s.body)+1 != 2:
                    check = 0
            pygame.time.delay(50)
            clock.tick(10)
            s.move()
            if s.body[0].pos == snack.pos:
                s.addCube()
                snack = cube(randomSnack(rows, s), color=(0,255,0))

            for x in range(len(s.body)):
                if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                    print('Score: ', len(s.body))
                    s.reset((10,10))
                    break
        redrawWindow(win)
    pass



main()
