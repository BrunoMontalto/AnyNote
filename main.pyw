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

TOOLS = []
for filename in os.listdir("tools"):
    TOOLS.append(pygame.image.load("tools/" + filename).convert_alpha())

def main():
    global wn, w,h, pointer_img
    pointer_in = False
    clock = pygame.time.Clock()

    frame = NoteFrame((0, 32), (500, 500), DEFAULT_FONT, DEFAULT_THEME)
    #files bar
    buttons = [ImageButton(LINE_INDEX_WIDTH//2,FILES_BAR_HEIGHT//2, (LINE_INDEX_WIDTH - 4, FILES_BAR_HEIGHT - 4), colorSum(frame.theme[0], (-5, -5, -5)), TOOLS[frame.tool], 0)]
    button_down = None

    def draw():
        mx, my = pygame.mouse.get_pos()
        w, h = wn.get_size()
        frame.set_size((w, h - 16 - FILES_BAR_HEIGHT))

        pointer_img = frame.listen(events, mx, my)

        if my < 32 or my > frame.y + frame.h:
            pointer_img = 0

        for b in buttons:
            if b.inTouch(mx, my):
                pointer_img = 1
                break

        wn.fill(colorSum(frame.theme[0], (-15, -15, -15)))
        #pygame.draw.rect(wn, colorSum(frame.theme[0], (-15, -15, -15)), (0, h - 16, w, h))

        frame.draw(wn)

        #files bar
        for b in buttons:
            b.draw(wn, b is button_down)

        #bottom bar
        line_col = GUI_FONT.render("Line: " + str(frame.cursor_line) + ", Column: " + str(frame.cursor_col), True, frame.theme[1])
        line_cnt = GUI_FONT.render(str(len(frame.files[frame.file_index])) + " line" + ("s" if len(frame.files[frame.file_index]) > 1 else ""), True, frame.theme[1])
        wn.blit(line_col, (LINE_PAD, wn.get_height() - 8 - line_col.get_height()/2))
        wn.blit(line_cnt, (wn.get_width() - LINE_PAD - line_cnt.get_width(), wn.get_height() - 8 - line_col.get_height()/2))

        pointer = CURSORS[pointer_img]
        if pointer_in:
            wn.blit(pointer, (mx - pointer.get_width()//2, my - pointer.get_height()//2))
            
        
        pygame.display.flip()

    oldWndProc = win32gui.SetWindowLong(win32gui.GetForegroundWindow(), win32con.GWL_WNDPROC, lambda *args: wndProc(oldWndProc, draw, *args))
    while 1:
        mx, my = pygame.mouse.get_pos()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.ACTIVEEVENT:
                if (event.gain == 1):  # mouse enter the window
                    pointer_in = True
                else:  # mouse leave the window
                    pointer_in = False
                    frame.drawing = False
                    frame.prev_mx, frame.prev_my = None, None
            
            elif event.type == pygame.VIDEORESIZE:
                w, h = event.w, event.h
                #pygame.display.set_icon(pygame.image.load("icon.png").convert_alpha())
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.inTouch(mx, my):
                        button_down = b
                        break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if button_down and button_down.inTouch(mx, my):
                    if button_down.tag == 0:
                        frame.tool = (frame.tool + 1) % len(TOOLS)
                        button_down.sprite = TOOLS[frame.tool]
                
                button_down = None

            
            
        #######################
        draw()
        #######################
        
        clock.tick(60)


if __name__ == "__main__":
    main()
    quit()
