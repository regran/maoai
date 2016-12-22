import pygame
pygame.init()

fnt = pygame.font.SysFont('texgyreheros', 15)
print(pygame.font.get_fonts())

buttons = []

def wrapline(font, words, rect):
    """Return words of a font formatted to fit in a given rect"""
    words = words.split()
    lines = []
    while words != []:
        finalwords = " " + words[0] + " "
        del words[0]
        while words!= [] and (fnt.size(finalwords + words[0])[0]< rect.width):
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
        pygame.draw.rect(surf, self.lin, self.rect, 2)

   # def is_clicked(self, clickorhov):
    def is_clicked(self, up=True):
        click = pygame.mouse.get_pressed()[0] 
        pos = self.rect.collidepoint(pygame.mouse.get_pos())
        #if clickorhov:
        newclick = pos and self.inf == (175,175,175) and not click
        if pos and not up: #button pressed down
            self.inf = (175, 175, 175)
        elif pos and not click: #mouseover
            self.inf = (220, 220, 220)
        elif (pos and not up) or not (click or pos): #mouse released and not hovering
            self.inf = (210,210,210)
        return newclick  #mouse released on pressed button

    def click(self):
        self.inf = (210, 210, 210)


class Prompt():
    def __init__(self, promp, xcoord, ycoord, w, h):
        self.image = pygame.Surface((w,h))
        self.rect = self.image.get_rect(x=xcoord, y=ycoord)
        self.inf = (200, 200, 200)
        self.lin = (160, 160, 160)
        self.p = wrapline(fnt, promp, self.rect)
        self.image.fill(self.inf)
        lineheight = fnt.size(self.p[0])[1]
        lh=0
        for lines in self.p:
            self.image.blit(fnt.render(lines, True, (0, 0, 0)), (0,lh))
            lh+=lineheight

    def drawP(self, surf):
        pygame.draw.rect(screen, self.lin, self.rect, 2)
        surf.blit(self.image, self.rect)

class ButtonPrompt(Prompt):
    def __init__(self, promp, x, y, w, h, butt):
        global buttons
        super(ButtonPrompt, self).__init__(promp, x, y, w, h)
        self.b = Button(butt, x+w-w/5-10, y+h-(h/5)-10, w/5, h/5)

    def drawP(self, surf):
        super(ButtonPrompt, self).drawP(surf)
        self.b.drawB(surf)
        #return self.b.is_clicked()

class TwoButtonPrompt(ButtonPrompt):
    def __init__(self, promp, x, y, w, h, butt1, butt2):
        global buttons
        super(TwoButtonPrompt, self).__init__(promp, x, y, w, h, butt2)
        self.b2 = Button(butt1, x+10, y+h-(h/5)-10, w/5, h/5)

    def drawP(self, surf):
        b1 = super(TwoButtonPrompt, self).drawP(surf)
        self.b2.drawB(surf)
       # return self.b2.is_clicked() or b1      
        
        

screen = pygame.display.set_mode([500,500])
pygame.display.set_caption("Drawing test")
draw = True

prompttest = TwoButtonPrompt("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z I love writing GUIS that's a lie", 10, 10, 200, 100, "Yes", "No")
butt = Button("Testing", 250, 250, 100, 50)
buttons+=[butt]
print(len(buttons))
clicked = []
while(draw):
    hover = []
    unclick = False
    pos = pygame.mouse.get_pos()
    clicked = [b for b in buttons if b.rect.collidepoint(pos)]  
    mousevent = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            draw = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            for c in clicked:
                print(c.is_clicked(True))
            mousevent = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for c in clicked:
                c.is_clicked(False)
            mousevent = True
        """if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = [b for b in buttons if b.rect.collidepoint(pos)]
            if len(clicked) > 0:
                print ("A button was clicked")
        if event.type == pygame.MOUSEBUTTONUP:
            unclick = True
            print("Unclick time")"""
    screen.fill((0, 255, 0))
    """for b in buttons:
        if b.rect.collidepoint(pos):
            b.is_clicked(False)
        else:
            if not b in clicked:
                b.unclick()
    for b in clicked:
        b.is_clicked(True)
    if unclick:
        for c in clicked:
            b.unclick()
        clicked = []"""
    if not mousevent:
        for b in buttons:
            if(b.is_clicked()):
                exit()
    prompttest.drawP(screen)
    
    butt.drawB(screen)
    pygame.display.flip()

pygame.quit()
