import pygame
from pygame import gfxdraw

def colorSum(color,color2):
    res = list(color)
    for i in range(len(res)):
        res[i] = (res[i] + color2[i])%256
    return tuple(res)


def smooth_circle(surface, color,pos, radius,fill = True, border = False, borderColor = (0,0,0)):
    if border:
        gfxdraw.filled_ellipse(surface,*pos,radius+2,radius+2,borderColor)
        gfxdraw.aaellipse(surface,*pos,radius+2,radius+2,borderColor)
    if fill:
        gfxdraw.filled_ellipse(surface,*pos,radius,radius,color)
    gfxdraw.aaellipse(surface,*pos,radius,radius,color)



class ImageButton:
    def __init__(self,x,y,size,color,sprite,tag=0):
        self.x = x
        self.y = y
        self.size = size
        self.tag = tag
        self.color = color
        self.sprite = sprite
        self.disabled = False


    def draw(self,surf, selected = False, selected2 = False):
        color = self.color if not selected2 else ((244,150,78)if self.tag%2 else (245,239,199))
        color = color if not selected else colorSum(color,(10,10,10))
        if self.disabled:
            color = colorSum(self.color,(-10,-10,-10))
        pygame.draw.rect(surf,color,(self.x - self.size[0]/2,self.y-self.size[1]/2,self.size[0],self.size[1]))
        size = self.sprite.get_size()
        surf.blit(self.sprite,(self.x - size[0]/2,self.y-size[1]/2))

    def inTouch(self,mx,my):
        if self.disabled: return False
        return mx > self.x - self.size[0]/2 and mx < self.x + self.size[0]/2 and my > self.y - self.size[1]/2 and my < self.y + self.size[1]/2

    def toggleDisable(self):
        self.disabled = not self.disabled

    def setEnabled(self,b):
        self.disabled = not b


class TextButton:
    def __init__(self,x,y,size,color, textColor, text, font, tag = 0):
        self.font = font
        self.x = x
        self.y = y
        self.size = size
        self.text = text
        self.color = color
        self.textColor = textColor
        self.img = self.font.render(text,True,self.textColor)
        self.selected = False
        self.disabled = False
        self.tag = tag

    def setText(self,text):
        self.text = text
        self.img = self.font.render(text,True,self.textColor)

    def draw(self,surf, selected = False):
        color = self.color if not selected else colorSum(self.color,(10,10,10))
        if self.disabled:
            color = colorSum(self.color,(-10,-10,-10))
        pygame.draw.rect(surf,color,(self.x - self.size[0]/2,self.y-self.size[1]/2,self.size[0],self.size[1]))
        size = self.img.get_size()
        surf.blit(self.img,(self.x - size[0]/2,self.y-size[1]/2))

    def inTouch(self,mx,my):
        if self.disabled: return False
        return mx > self.x - self.size[0]/2 and mx < self.x + self.size[0]/2 and my > self.y - self.size[1]/2 and my < self.y + self.size[1]/2
    
    def toggleDisable(self):
        self.disabled = not self.disabled

    def setEnabled(self,b):
        self.disabled = not b



class Label:
    def __init__(self,x,y,text,color,font):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font

    def draw(self,wn, centered = True):
        render = self.font.render(self.text,True,self.color)
        if centered:
            wn.blit(render,(self.x - render.get_width()/2, self.y - render.get_height()/2))
            return
        wn.blit(render,(self.x,self.y))

    
        

class Slider:
    def __init__(self,x,y,size, minValue=9999999,maxValue=9999999, color = (30,30,30),size2 = (10,15)):
        self.x = x
        self.y = y
        self.size = size
        self.size2 = size2
        if minValue == 9999999: self.minValue = 0
        else: self.minValue = minValue
        if maxValue == 9999999: self.maxValue = size
        else: self.maxValue = maxValue
        self.color = color
        
        self.slider = 0
        self.sliding = False

    @property
    def value(self):
        return self.slider * (self.maxValue-self.minValue)/self.size + self.minValue
        

    def inTouch(self,mx,my):
        return mx >= self.x + self.slider - self.size2[0]/2 and mx <= self.x + self.slider + self.size2[0]/2 and my >= self.y - self.size2[1]/2 and my <= self.y + self.size2[1]/2 or mx >= self.x and mx <= self.x + self.size and self.y - 1<=my<= self.y + 1

    def step(self,events,mx,my):
        if self.sliding:
            self.slider = mx - self.x
            if self.slider < 0: self.slider = 0
            elif self.slider > self.size: self.slider = self.size
        toRet = ""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inTouch(mx,my):
                    self.sliding = True
                    toRet = "down"
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.sliding : toRet = "up"
                self.sliding = False
                
        return toRet


    def draw(self,wn):
        pygame.draw.rect(wn,self.color,(self.x - 1,self.y - 1,self.size,2))
        pygame.draw.rect(wn,colorSum(self.color,((30,30,30) if not self.sliding else (20,20,20))),(self.x + self.slider - self.size2[0]/2,self.y - self.size2[1]/2,*self.size2))


class Input:
    def __init__(self, x, y, size, font, text = "", bg = (20,20,20), fg = (255,255,255)):
        self.x = x
        self.y = y
        self.size = size
        self.font = font
        self.bg = bg
        self.fg = fg

        self.blist = ["AudioMute","MediaSelect","break","return","escape","left shift","right shift","ctrl","/","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","caps lock","numlock","super","right super","up","left","right","down","left alt","left ctrl","right alt","right ctrl","menu",
                 "insert","home","page up","page down","end","delete","print screen","pause","scroll lock","unknown key","tab", "backspace"]

        self.height = self.font.get_height()
        self.text = text
        self.bar = 0
        self.start = 0
        self.focused = False
        self.locked = False

    
    def inTouch(self, mx, my):
        return mx >= self.x and mx <= self.x + self.size  and  my >= self.y and my <= self.y + self.height
    
    
    def step(self, events, mx, my):
        if self.locked: return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.inTouch(mx, my):
                    self.focused = True
                else:
                    self.focused = False

            elif event.type == pygame.KEYDOWN:
                if not self.focused: continue
                if event.key == pygame.K_LEFT:
                    self.bar = (self.bar-1) * int(self.bar > 0)
                    continue
                elif event.key == pygame.K_RIGHT:
                    self.bar = (self.bar+1) * int(self.bar < len(self.text)) + len(self.text)*(self.bar >= len(self.text))
                    continue
                name = pygame.key.name(event.key)
                if not name in self.blist:
                    if name == "space":
                        self.text += " "
                    else:
                        self.text += name
                    self.bar += 1
                elif name == "backspace":
                    if self.start > 0: self.start -= 1
                    self.text = self.text[:self.bar-1] + self.text[self.bar:]
                    self.bar = (self.bar-1) * int(self.bar > 0)
    

    def draw(self, wn):
        pygame.draw.rect(wn,(self.bg if self.focused else colorSum(self.bg,(-20,-20,-20))), (self.x,self.y,self.size,self.height + 1))
        if self.focused:
            text = self.text[self.start:self.bar] + "|" + self.text[self.bar:]
            if self.bar >= self.start:
                if self.font.size(self.text[self.start:self.bar])[0] > self.size:
                    self.start += 1
            else:
                self.start -= 1
        else: text = self.text

        
        render= self.font.render(text, True, self.fg if not self.locked else colorSum(self.fg,(-30,-30,-30)))
        crop = pygame.Surface((self.size,self.height), pygame.SRCALPHA)
        crop.blit(render,(0,0))
        wn.blit(crop,(self.x,self.y))
    
