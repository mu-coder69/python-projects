from pygame import transform, mouse

class button():
    screen = None
    def __init__(self, x, y, image, scale, show=True):
        width = image.get_width()
        height = image.get_height()
        self.image = transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.show = show

    def drawButton(self):        
        self.screen.blit(self.image, (self.rect.x, self.rect.y)) 

    def trigger(self):
        triggered = False
        #get mouse position
        pos = mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                triggered = True

        if mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return triggered