from AnyNote import *

size = w,h = 500, 500
wn = pygame.display.set_mode(size, pygame.RESIZABLE)


def main():
    clock = pygame.time.Clock()

    frame = NoteFrame((0,0), (500,500), DEFAULT_FONT, DEFAULT_THEME)
    while 1:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            
            
        #######################
        frame.set_size(wn.get_size())
        frame.listen(events)

        wn.fill((0,0,0))
        frame.draw(wn)
        #######################
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
    quit()
