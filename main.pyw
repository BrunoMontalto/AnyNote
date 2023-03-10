from AnyNote import *

size = w,h = 500, 500
wn = pygame.display.set_mode(size, pygame.RESIZABLE)

pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
CURSORS = []
for filename in os.listdir("cursors"):
    CURSORS.append(pygame.image.load("cursors/" + filename).convert_alpha())
cursor_img = 0

pygame.display.set_caption("AnyNote")
pygame.display.set_icon(pygame.image.load("icon.png").convert_alpha())

def main():
    global w,h, cursor_img
    cursor_in = False
    clock = pygame.time.Clock()

    frame = NoteFrame((0,0), (500,500), DEFAULT_FONT, DEFAULT_THEME)
    while 1:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return

            if (event.type == pygame.ACTIVEEVENT):
                if (event.gain == 1):  # mouse enter the window
                    cursor_in = True
                else:  # mouse leave the window
                    cursor_in = False

            
            
        #######################
        mx, my = pygame.mouse.get_pos()
        frame.set_size(wn.get_size())
        cursor_img = frame.listen(events, mx, my)

        wn.fill((0,0,0))
        frame.draw(wn)

        cursor = CURSORS[cursor_img]
        if cursor_in:
            wn.blit(cursor, (mx - cursor.get_width()//2, my - cursor.get_height()//2))
        #######################
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
    quit()
