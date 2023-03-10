import pygame
from pygameGUI import *
import tkinter as tk #for clipboard
import os

pygame.init()
pygame.font.init()

root = tk.Tk()
# keep the window from showing
root.withdraw()

# Constants
DEFAULT_FONT = pygame.font.SysFont("Consolas", 16)
GUI_FONT = pygame.font.SysFont("Consolas", 12)
#                bg             fg
DEFAULT_THEME = [(60, 60, 60), (250, 250, 250)]

CURSOR_COLOR_SWAP_TIMER = 30
REPEAT_TIMER = 30

LINE_INDEX_WIDTH = 50
LINE_PAD = 5



class NoteFrame:
    def __init__(self, position, size, font, theme):
        self.x, self.y = position
        self.w, self.h = size
        self.font = font
        self.theme = theme

        self.lines = [""]

        self.tab_size = 4

        self.cursor_col = 0
        self.cursor_line = 0
        self.cursor_color = self.theme[1]
        self.cursor_color_swap_timer = CURSOR_COLOR_SWAP_TIMER

        self.selecting = False
        self.selection_start = None
        self.selection_end = None

        self.repeat_timer = REPEAT_TIMER
        self.input_hold = None
        self.prev_input_hold = None

        self.scroll = 0

        self.surf = pygame.Surface(size)
    

    def print(self):
        for i in range(len(self.lines)):
            print(self.lines[i])

    def set_size(self, size):
        if size[0] < 0 or size[1] < 0:
            return
        self.w, self.h = size
        self.surf = pygame.Surface(size)

    def new_line(self):
        if self.cursor_col < len(self.lines[self.cursor_line]):
            new_line_content = self.lines[self.cursor_line][self.cursor_col:]
            self.lines[self.cursor_line] = self.lines[self.cursor_line][:self.cursor_col]
        else:
            new_line_content = ""
        
        p = None
        if self.cursor_col > 0 and self.lines[self.cursor_line][self.cursor_col - 1] in ('(', '[', '{'):
            for par in ('(', '[', '{'):
                if self.lines[self.cursor_line][self.cursor_col - 1] == par:
                    new_line_content = (' ' * self.tab_size) + new_line_content
                    self.cursor_col = self.tab_size
                    p = par
                    break
            

        else:
            self.cursor_col = 0
        self.cursor_line += 1
        self.lines.insert(self.cursor_line, new_line_content)
        if p and self.cursor_col < len(self.lines[self.cursor_line]):
            if self.lines[self.cursor_line][self.cursor_col] == chr(ord(p) + 1 + int(p in ('[', '{'))):
                temp_line, temp_col = self.cursor_line, self.cursor_col
                self.new_line()
                self.cursor_line, self.cursor_col = temp_line, temp_col

    def delete_selection(self):
        selection_start = self.selection_start
        selection_end = self.selection_end
        #compare selection positions
        selection_start_pos = 0
        for i in range(selection_start[0]):
            selection_start_pos += len(self.lines[i])
        selection_start_pos += selection_start[1]

        selection_end_pos = 0
        for i in range(selection_end[0]):
            selection_end_pos += len(self.lines[i])
        selection_end_pos += selection_end[1]

        #put start and end in the correct order
        if selection_start_pos > selection_end_pos:
            selection_start, selection_end = selection_end, selection_start

        iter = selection_end[0] - selection_start[0]
        if iter == 0:
            start = selection_start[1]
            end = selection_end[1]
            self.lines[selection_start[0]] = self.lines[selection_start[0]][:start] + self.lines[selection_start[0]][end:]
            #TODO vedere se la linea adesso ?? vuota
            self.selection_start = None
            self.selection_end = None
            self.cursor_col = start
        else:
            self.lines[selection_start[0]] = self.lines[selection_start[0]][:selection_start[1]] + self.lines[selection_end[0]][selection_end[1]:]

            for i in range(iter ):
                self.lines.pop(selection_start[0] + 1)
            
            self.cursor_line = selection_start[0]
            self.cursor_col = selection_start[1]

        self.selection_start = None
        self.selection_end = None
        
        #self.print()


    def handle_input(self, event, mx, my, font_h):
        if event.type == pygame.KEYDOWN:
            print("unicode:", event.unicode)
            print("event key:", event.key)

        
            self.input_hold = (event.key, event.mod, event.unicode)

            if event.key == pygame.K_RETURN:
                self.new_line()

            elif event.key == pygame.K_BACKSPACE: #backspace
                selection_start = self.selection_start
                selection_end = self.selection_end
                if selection_start != selection_end and (selection_start and selection_end): #delete selection
                    self.delete_selection()

                elif self.cursor_col == 0:
                    if self.cursor_line > 0:
                        removed_line = self.lines[self.cursor_line]
                        self.lines.pop(self.cursor_line)
                        self.cursor_line -= 1
                        self.cursor_col = len(self.lines[self.cursor_line])
                        self.lines[self.cursor_line] = self.lines[self.cursor_line] + removed_line
                else:
                    if event.mod & pygame.KMOD_CTRL:
                        
                        if self.cursor_col > 0:
                            self.selection_start = [self.cursor_line, self.cursor_col]
                            self.selection_end = (self.cursor_line, self.cursor_col)
                            c = self.lines[self.selection_start[0]][self.selection_start[1] - 1]
                            if c == " ":
                                self.selection_start[1] -= 1
                            else:
                                while c != " " and self.selection_start[1] > 0:
                                    self.selection_start[1] -= 1
                                    c = self.lines[self.selection_start[0]][self.selection_start[1] - 1]
                            self.cursor_col = self.selection_start[1]
                            self.delete_selection()
                    else:
                        self.lines[self.cursor_line] = self.lines[self.cursor_line][:self.cursor_col - 1] + self.lines[self.cursor_line][self.cursor_col:]
                        self.cursor_col -= 1

                #scroll to cursor
                if self.cursor_line < self.scroll//font_h or self.cursor_line > self.scroll//font_h + self.h/font_h:
                    self.scroll = self.cursor_line * font_h
            
            elif event.key == pygame.K_DELETE:
                selection_start = self.selection_start
                selection_end = self.selection_end
                if selection_start != selection_end and (selection_start and selection_end): #delete selection
                    self.delete_selection()

                elif self.cursor_col == len(self.lines[self.cursor_line]):
                    if self.cursor_line < len(self.lines) - 1:
                        removed_line = self.lines[self.cursor_line + 1]
                        self.lines.pop(self.cursor_line + 1)
                        self.lines[self.cursor_line] = self.lines[self.cursor_line] + removed_line
                else:
                    self.lines[self.cursor_line] = self.lines[self.cursor_line][:self.cursor_col] + self.lines[self.cursor_line][self.cursor_col + 1:]

            
            elif event.key == pygame.K_RIGHT:
                if event.mod & pygame.KMOD_CTRL:
                    if self.cursor_col < len(self.lines[self.cursor_line]):
                        c = self.lines[self.cursor_line][self.cursor_col]
                        if c == " ":
                            self.cursor_col += 1
                        else:
                            while c != " " and self.cursor_col < len(self.lines[self.cursor_line]):
                                self.cursor_col += 1
                                if self.cursor_col < len(self.lines[self.cursor_line]):
                                    c = self.lines[self.cursor_line][self.cursor_col]
                            
                else:
                    self.cursor_col += 1
                    if self.cursor_col > len(self.lines[self.cursor_line]):
                        self.cursor_line += 1
                        if self.cursor_line >= len(self.lines):
                            self.cursor_line = len(self.lines) - 1
                            self.cursor_col = len(self.lines[self.cursor_line])
                            return
                        self.cursor_col = 0

            elif event.key == pygame.K_LEFT:
                if event.mod & pygame.KMOD_CTRL:
                    if self.cursor_col > 0:
                        c = self.lines[self.cursor_line][self.cursor_col - 1]
                        if c == " ":
                            self.cursor_col -= 1
                        else:
                            while c != " " and self.cursor_col > 0:
                                self.cursor_col -= 1
                                c = self.lines[self.cursor_line][self.cursor_col - 1]
                else:
                    self.cursor_col -= 1
                    if self.cursor_col < 0:
                        self.cursor_line -= 1
                        if self.cursor_line < 0:
                            self.cursor_line = 0
                            self.cursor_col = 0
                            return
                        self.cursor_col = len(self.lines[self.cursor_line])


            elif event.key == pygame.K_UP:
                self.cursor_line -= 1
                if self.cursor_line < 0:
                    self.cursor_line = 0
                else:
                    if self.cursor_col > len(self.lines[self.cursor_line]):
                        self.cursor_col = len(self.lines[self.cursor_line])

            elif event.key == pygame.K_DOWN:
                self.cursor_line += 1
                if self.cursor_line > len(self.lines) - 1:
                    self.cursor_line = len(self.lines) - 1
                else:
                    if self.cursor_col > len(self.lines[self.cursor_line]):
                        self.cursor_col = len(self.lines[self.cursor_line])

            
                

            elif (event.key == pygame.K_c) and (event.mod & pygame.KMOD_CTRL): #CTRL C
                #TODO
                pass

            elif (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL): #CTRL V
                print("ctrl V")
                tab = ' ' * self.tab_size
                for c in root.clipboard_get():
                    if c == '\n':
                        self.new_line()
                        continue
                    if c == '\t':
                       self.lines[self.cursor_line] = self.lines[self.cursor_line][:self.cursor_col] + tab + self.lines[self.cursor_line][self.cursor_col:]
                       self.cursor_col += self.tab_size - 1
                    else:
                        self.lines[self.cursor_line] = self.lines[self.cursor_line][:self.cursor_col] + c + self.lines[self.cursor_line][self.cursor_col:]
                    self.cursor_col += 1
                
                #scroll to cursor
                if self.cursor_line < self.scroll//font_h or self.cursor_line > self.scroll//font_h + self.h/font_h:
                    self.scroll = self.cursor_line * font_h

            elif (event.key == pygame.K_a) and (event.mod & pygame.KMOD_CTRL): #CTRL A
                self.selection_start = (0, 0)
                self.selection_end = (len(self.lines) - 1, len(self.lines[-1]))
                self.cursor_line = len(self.lines) - 1
                self.cursor_col = len(self.lines[self.cursor_line])


            elif (event.key == pygame.K_s) and (event.mod & pygame.KMOD_CTRL):
                self.save()

            elif event.key == 9: #tab
                self.lines[self.cursor_line] = self.lines[self.cursor_line][:self.cursor_col] + "    " + self.lines[self.cursor_line][self.cursor_col:]
                self.cursor_col += 4

            else:
                self.cursor_color_swap_timer = CURSOR_COLOR_SWAP_TIMER

                selection_start = self.selection_start
                selection_end = self.selection_end
                if selection_start != selection_end and (selection_start and selection_end): #delete selection
                    self.delete_selection()

                temp = len(self.lines[self.cursor_line])
                new = event.unicode
                for par in ('(', '[', '{'):
                    if new == par:
                        new += chr(ord(par) + 1 + int(par in ('[', '{')))
                        break
                self.lines[self.cursor_line] = self.lines[self.cursor_line][:self.cursor_col] + new + self.lines[self.cursor_line][self.cursor_col:]
                if len(self.lines[self.cursor_line]) > temp:
                    self.cursor_col += 1
        

        elif event.type == pygame.KEYUP:
            self.input_hold = None
            self.repeat_timer = REPEAT_TIMER


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                font_h = self.font.size('|')[1]
                self.cursor_line = my // font_h
                if self.cursor_line >= len(self.lines):
                    self.cursor_line = len(self.lines) - 1
                    self.cursor_col = len(self.lines[self.cursor_line])
                else:    
                    mrow = 0
                    for c in self.lines[self.cursor_line]:
                        mx -= self.font.size(c)[0]
                        if mx < 0:
                            break
                        mrow += 1
                    
                    self.cursor_col = mrow

                self.selecting = True
                self.selection_start = (self.cursor_line, self.cursor_col)
                self.selection_end = None
            
            #TODO fluid scrolling
            elif event.button == 4: #up
                self.scroll -= font_h*3
                if self.scroll < 0:
                    self.scroll = 0
            elif event.button == 5: #down
                self.scroll += font_h*3
            
            

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.selecting = False
                self.selection_end = (self.cursor_line, self.cursor_col)


    def listen(self, events, mx, my):
        #get mouse position relative to the frame
        mx -= self.x
        mx -= LINE_INDEX_WIDTH + LINE_PAD
        my -= self.y
        my += self.scroll

        if mx > 0:
            pointer_img = 1
        else:
            pointer_img = 0

        font_h = self.font.size('|')[1]
        if self.selecting:
            self.cursor_line = my // font_h
            if self.cursor_line >= len(self.lines):
                self.cursor_line = len(self.lines) - 1
                self.cursor_col = len(self.lines[self.cursor_line])
            else:
                mrow = 0
                for c in self.lines[self.cursor_line]:
                    mx -= self.font.size(c)[0]
                    if mx < 0:
                        break
                    mrow += 1
                
                self.cursor_col = mrow
            
            self.selection_end = (self.cursor_line, self.cursor_col)


        if self.prev_input_hold == self.input_hold and self.input_hold:
                self.repeat_timer -= 1
                if self.repeat_timer <= 0:
                    e = pygame.event.Event(pygame.KEYDOWN)

                    e.key, e.mod, e.unicode = self.input_hold
                    self.handle_input(e, mx, my, font_h)
        else:
            self.repeat_timer = REPEAT_TIMER

        self.prev_input_hold = self.input_hold
        
        for event in events:
            self.handle_input(event, mx, my, font_h)

        if self.scroll > font_h * (len(self.lines) - 1):
            self.scroll = font_h * (len(self.lines) - 1)

        #if self.cursor_line < self.scroll//font_h or self.cursor_line > self.scroll//font_h + self.h/:
    
        return pointer_img


    def draw(self, surface):
        self.surf.fill(self.theme[0])
        pygame.draw.rect(self.surf, colorSum(self.theme[0], (-5, -5, -5)), (0, 0, LINE_INDEX_WIDTH, self.h))

        font_h = self.font.size('|')[1]

        #selection
        selection_start = self.selection_start
        selection_end = self.selection_end
        if selection_start != selection_end and (selection_start and selection_end):
            #compare selection positions
            selection_start_pos = 0
            for i in range(selection_start[0]):
                selection_start_pos += len(self.lines[i])
            selection_start_pos += selection_start[1]

            selection_end_pos = 0
            for i in range(selection_end[0]):
                selection_end_pos += len(self.lines[i])
            selection_end_pos += selection_end[1]

            #put start and end in the correct order
            if selection_start_pos > selection_end_pos:
                selection_start, selection_end = selection_end, selection_start

            #draw selection
            iter = selection_end[0] - selection_start[0] + 1
            if iter == 1:
                #find selection start and end in pixels
                start = LINE_INDEX_WIDTH + LINE_PAD + self.font.size(self.lines[selection_start[0]][:selection_start[1]])[0]
                end = LINE_INDEX_WIDTH + LINE_PAD + self.font.size(self.lines[selection_end[0]][:selection_end[1]])[0]
                pygame.draw.rect(self.surf, colorSum(self.theme[0], (100, 100, 100)), (start, selection_start[0] * font_h - self.scroll, max(3, end - start), font_h))
            else:
                for i in range(iter):
                    if i == 0:
                        start = LINE_INDEX_WIDTH + LINE_PAD + self.font.size(self.lines[selection_start[0] + i][:selection_start[1]])[0]
                        end = LINE_INDEX_WIDTH + LINE_PAD + self.font.size(self.lines[selection_start[0] + i])[0]
                        pygame.draw.rect(self.surf, colorSum(self.theme[0], (100, 100, 100)), (start, (selection_start[0] + i) * font_h - self.scroll, max(3, end - start), font_h))
                    elif i == iter - 1:
                        start = LINE_INDEX_WIDTH + LINE_PAD
                        end = LINE_INDEX_WIDTH + LINE_PAD + self.font.size(self.lines[selection_end[0]][:selection_end[1]])[0]
                        pygame.draw.rect(self.surf, colorSum(self.theme[0], (100, 100, 100)), (start, (selection_start[0] + i) * font_h - self.scroll, max(3, end - start), font_h))
                    else:
                        start = LINE_INDEX_WIDTH + LINE_PAD
                        end = LINE_INDEX_WIDTH + LINE_PAD + self.font.size(self.lines[selection_start[0] + i])[0]
                        pygame.draw.rect(self.surf, colorSum(self.theme[0], (100, 100, 100)), (start, (selection_start[0] + i) * font_h - self.scroll, max(3, end - start), font_h))


        
        #text
        #print("range: ", (max(self.scroll//font_h - 1, 0), min(self.scroll//font_h + self.h//font_h + 1 ,len(self.lines))))
        for i in range(max(self.scroll//font_h - 1, 0), min(self.scroll//font_h + self.h//font_h + 1 ,len(self.lines))):
            index = self.font.render(str(i), True, colorSum(self.theme[1], (-50, -50, -50)))
            text = self.font.render(str(self.lines[i]), True, self.theme[1])

            self.surf.blit(index, (LINE_INDEX_WIDTH//2 - index.get_width()//2, font_h * i + font_h//2 - index.get_height()//2 - self.scroll))
            self.surf.blit(text, (LINE_INDEX_WIDTH + LINE_PAD, font_h * i + font_h//2 - text.get_height()//2 - self.scroll))
        

        #cursor
        if self.cursor_color_swap_timer <= 0:
            self.cursor_color_swap_timer = CURSOR_COLOR_SWAP_TIMER
            if self.cursor_color == self.theme[1]:
                self.cursor_color = colorSum(self.cursor_color, (-100, -100, -100))
            else:
                self.cursor_color = colorSum(self.cursor_color, (+100, +100, +100))
        
        self.cursor_color_swap_timer -= 1

        pygame.draw.rect(self.surf, self.cursor_color, (LINE_INDEX_WIDTH + LINE_PAD + self.font.size(self.lines[self.cursor_line][:self.cursor_col])[0], font_h*self.cursor_line -self.scroll,  1, font_h ))
        
        surface.blit(self.surf, (self.x, self.y))


    def save(self):
        with open("save.txt", "w") as f:
            for line in self.lines:
                f.write(line + '\n')
            
            f.close()