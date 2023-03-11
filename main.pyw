from AnyNote import *

import win32gui #for refresh during resize
import win32con #

def wndProc(oldWndProc, draw_callback, hWnd, message, wParam, lParam):
    if message == win32con.WM_SIZE:
        draw_callback()
        win32gui.RedrawWindow(hWnd, None, None, win32con.RDW_INVALIDATE | win32con.RDW_ERASE)
    return win32gui.CallWindowProc(oldWndProc, hWnd, message, wParam, lParam)

size = w,h = 500, 500
wn = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
pygame.display.set_caption("AnyNote")
pygame.display.set_icon(pygame.image.load("icon.png").convert_alpha())



pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
CURSORS = []
for filename in os.listdir("cursors"):
    CURSORS.append(pygame.image.load("cursors/" + filename).convert_alpha())
pointer_img = 0


def main():
    global wn, w,h, cursor_img
    pointer_in = False
    clock = pygame.time.Clock()

    frame = NoteFrame((0,0), (500,500), DEFAULT_FONT, DEFAULT_THEME)

    def draw():
        mx, my = pygame.mouse.get_pos()
        frame.set_size((wn.get_width(), wn.get_height() - 16))
        pointer_img = frame.listen(events, mx, my)
        if my > frame.y + frame.h:
            pointer_img = 0

        wn.fill(colorSum(frame.theme[0], (-15, -15, -15)))
        frame.draw(wn)

        line_col = GUI_FONT.render("Line: " + str(frame.cursor_line) + ", Column: " + str(frame.cursor_col), True, frame.theme[1])
        line_cnt = GUI_FONT.render(str(len(frame.lines)) + " line" + ("s" if len(frame.lines) > 1 else ""), True, frame.theme[1])
        wn.blit(line_col, (LINE_PAD, wn.get_height() - 8 - line_col.get_height()/2))
        wn.blit(line_cnt, (wn.get_width() - LINE_PAD - line_cnt.get_width(), wn.get_height() - 8 - line_col.get_height()/2))

        pointer = CURSORS[pointer_img]
        if pointer_in:
            wn.blit(pointer, (mx - pointer.get_width()//2, my - pointer.get_height()//2))
        
        pygame.display.flip()

    oldWndProc = win32gui.SetWindowLong(win32gui.GetForegroundWindow(), win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, draw, *args))
    while 1:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.ACTIVEEVENT:
                if (event.gain == 1):  # mouse enter the window
                    pointer_in = True
                else:  # mouse leave the window
                    pointer_in = False
            
            elif event.type == pygame.VIDEORESIZE:
                w, h = event.w, event.h
                #pygame.display.set_icon(pygame.image.load("icon.png").convert_alpha())

            
            
        #######################
        draw()
        #######################
        
        clock.tick(60)


if __name__ == "__main__":
    main()
    quit()
