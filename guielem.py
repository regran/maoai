import pygame
pygame.init()

fnt = pygame.font.SysFont('texgyreheros', 30)


def wrapline(font, words, rect):
    """Return words of a font formatted to fit in a given rect"""
    words = words.split()
    lines = []
    while words != []:
        finalwords = " " + words[0] + " "
        del words[0]
        while words!= [] and (fnt.size(finalwords + words[0])[0]< rect.width-20):
            finalwords += words[0] + " "
            del words[0]
        lines+=[finalwords]
    return lines

class Button(pygame.sprite.Sprite):
    def __init__(self, word, xcoord, ycoord, wid, hei):
        """word is a string, xcoord/ycoord are coordinates of top left, wid hei are width and height"""
        self.image = pygame.Surface((wid, hei))
        self.rect = self.image.get_rect(x=xcoord, y=ycoord)
        self.words = wrapline(fnt, word, self.rect) 
        self.lin = (185, 185, 185)
        self.inf = (210, 210, 210)

    def drawB(self, surf):
        """Draw the button on a given surface"""
        self.image.fill(self.inf)
        self.image.blit(fnt.render(self.words[0], True, (0, 0, 0)), (0,0))
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, self.lin, self.rect, 3)

   # def is_clicked(self, clickorhov):
    def is_clicked(self, up=True):
        click = pygame.mouse.get_pressed()[0] 
        pos = self.rect.collidepoint(pygame.mouse.get_pos())
        newclick = pos and self.inf == (175,175,175) and not click
        if pos and not up: #button pressed down
            self.inf = (175, 175, 175)
        elif pos and not click: #mouseover
            self.inf = (220, 220, 220)
        elif not (click or pos): #mouse released and not hovering
            self.inf = (210,210,210)
        return newclick  #mouse released on pressed button

class Arrow(pygame.sprite.Sprite):
    def __init__(self, xycoord, upa=True):
        if upa:
            self.normal = pygame.image.load("uparrow.png").convert()
            self.hover = pygame.image.load("uparrowhover.png").convert()
            self.click = pygame.image.load("uparrowclick.png").convert()
        else:
            self.normal = pygame.image.load("downarrow.png").convert()
            self.hover  = pygame.image.load("downarrowhover.png").convert()
            self.click = pygame.image.load("downarrowclick.png").convert()
        self.image = self.normal
        self.rect = self.image.get_rect(x=xycoord[0], y=xycoord[1])
        self.clicked = False

    def drawA(self, surf):
        return surf.blit(self.image, self.rect)

    def is_clicked(self, up=True):
        click = pygame.mouse.get_pressed()[0]
        pos = self.rect.collidepoint(pygame.mouse.get_pos())
        clicked = pos and self.clicked and not click
        if pos and not up:
            self.clicked = True
            self.image = self.click
        elif pos and not click:
            self.image = self.hover
            self.clicked = False
        elif not (click or pos):
            self.image = self.normal
            self.clicked = False
        return clicked


class Prompt():
    def __init__(self, promp, xcoord, ycoord, w, h):
        self.image = pygame.Surface((w,h))
        self.rect = self.image.get_rect(x=xcoord-w/2, y=ycoord-h/2)
        self.inf = (200, 200, 200)
        self.lin = (160, 160, 160)
        self.p = wrapline(fnt, promp, self.rect)
        self.image.fill(self.inf)
        lineheight = fnt.size(self.p[0])[1]
        lh=10
        for lines in self.p:
            self.image.blit(fnt.render(lines, True, (0, 0, 0)), (10,lh))
            lh+=lineheight

    def drawP(self, surf):
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, self.lin, self.rect, 5)

class ButtonPrompt(Prompt):
    def __init__(self, promp, x, y, w, h, butt):
        global buttons
        super(ButtonPrompt, self).__init__(promp, x, y, w, h)
        self.b = Button(butt, x+w*4/5-10-w/2, y+h*4/5-10-h/2, w/5, h/5)

    def drawP(self, surf, events):
        super(ButtonPrompt, self).drawP(surf)
        self.b.drawB(surf)
        b1 = False
        for e in events:
            b1 = mousecheck(e, [self.b])
            if b1:
                break
        return b1    


class TwoButtonPrompt(ButtonPrompt):
    def __init__(self, promp, x, y, w, h, butt1, butt2):
        global buttons
        super(TwoButtonPrompt, self).__init__(promp, x, y, w, h, butt2)
        self.b2 = Button(butt1, x+10-w/2, y+h-(h/5)-10-h/2, w/5, h/5)

    def drawP(self, surf, events):
        b1 = super(TwoButtonPrompt, self).drawP(surf, events)
        self.b2.drawB(surf)
        b2 = False
        if b1:
            return b1, False
        for e in events:
            b2=mousecheck(e, [self.b2])
            if b2:
                break
        return b1, b2    
        
def mousecheck(event, buttons):
    for c in buttons:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return  c.is_clicked(False)
        else:
            return c.is_clicked() 
"""
print(pygame.font.get_fonts())

buttons = []
events = []

screen = pygame.display.set_mode([1000,800])
pygame.display.set_caption("Drawing test")
draw = True

prompttest = ButtonPrompt("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z I love writing GUIS that's a lie", 10, 10, 500, 250,  "No")
butt = Button("Testing", 250, 250, 100, 50)
buttons+=[butt]
print(len(buttons))
clicked = []
while(draw):
    pos = pygame.mouse.get_pos()
    clicked = [b for b in buttons if b.rect.collidepoint(pos)]  
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            draw = False
            break
        mousecheck(event, clicked)
    screen.fill((0, 255, 0))
    if prompttest.drawP(screen, events):
        exit()
    butt.drawB(screen)
    pygame.display.flip()

pygame.quit()
"""
