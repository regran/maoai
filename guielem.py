import pygame
pygame.init()

fnt = pygame.font.SysFont('texgyreheros', 15)
print(pygame.font.get_fonts())

def wrapline(font, words, rect):
    """Return words of a font formatted to fit in a given rect"""
    words = words.split()
    lines = []
    while words != []:
        finalwords = words[0] + " "
        del words[0]
        while words!= [] and (fnt.size(finalwords + words[0])[0]< rect.width):
            print(rect.width)
            print(finalwords)
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
        self.lin = (150, 150, 150)
        self.inf = (210, 210, 210)
        self.image.fill(self.inf)
        self.image.blit(fnt.render(self.words[0], True, (0, 0, 0)), (2,2))

    def drawB(self, surf):
        """Draw the button on a given surface"""
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, self.lin, self.rect, 2)

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
        super(ButtonPrompt, self).__init__(promp, x, y, w, h)
        self.b = Button(butt, w-w/5-10, h-(h/5)-10, w/5, h/5)
        self.b.drawB(self.image)

    def drawP(self, surf):
        super(ButtonPrompt, self).drawP(surf)

class TwoButtonPrompt(ButtonPrompt):
    def __init__(self, promp, x, y, w, h, butt1, butt2):
        super(TwoButtonPrompt, self).__init__(promp, x, y, w, h, butt2)
        self.b2 = Button(butt1, 10, h-(h/5)-10, w/5, h/5)
        self.b2.drawB(self.image)
    
    def drawP(self, surf):
        super(TwoButtonPrompt, self).drawP(surf)

screen = pygame.display.set_mode([500,500])
pygame.display.set_caption("Drawing test")
draw = True

while(draw):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            draw = False
    screen.fill((0, 255, 0))
    prompttest = TwoButtonPrompt("A B C D E F G H I J K L M N O P Q R S T", 10, 10, 200, 100, "Yes", "No")
    prompttest.drawP(screen)
    butt = Button("Testing", 250, 250, 100, 50)
    butt.drawB(screen)
    pygame.display.flip()

pygame.quit()
