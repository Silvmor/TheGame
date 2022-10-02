from datetime import datetime
class Fps():
    def __init__(self):
        self.FC=60
        self.FPS=60
        self.previous_time = datetime.now()
        self.current_time = datetime.now()
        self.font_path = "Fonts/Courier.ttf"
        self.font_size = 20
        self.font_color= (255,255,255)
        self.font = pygame.font.Font(self.font_path,self.font_size)
        self.view = self.font.render(str(self.FPS),True,self.font_color)
        self.rect = self.view.get_rect()
        self.rect.topleft =[0,0]

    def show(self):
        self.view.fill((0,0,0))
        display_surface.blit(self.view,self.rect)
        if self.FC==0 :
            self.FC=60
            self.current_time = datetime.now()
            difference = self.current_time-self.previous_time
            difference/=60
            time = datetime.strptime(str(difference),"%H:%M:%S.%f")
            self.FPS = int((1/int(time.microsecond))*10**6)
            self.previous_time=self.current_time
            del difference,time
        else :
            self.FC-=1
        self.view = self.font.render(str(self.FPS),True,self.font_color)
        display_surface.blit(self.view,self.rect)
        pygame.display.update(self.rect)