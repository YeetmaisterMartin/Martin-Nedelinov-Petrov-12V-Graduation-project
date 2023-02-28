import PlayerVsPlayer as PvP
import PlayerVsComputer as PvC
import pygame as p

import SmartMoveFinder



def main():
    p.init()
    menu_screen = p.display.set_mode((PvP.WIDTH, PvP.HEIGHT))
    clock = p.time.Clock()
    menu_screen.fill(p.Color("black"))
    draw_pvp(menu_screen)
    running = True

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.KEYDOWN:  # Key press handling
                if e.key == p.K_1:
                    PvP.player_vs_player_launcher()
                    running = False
                elif e.key == p.K_2:
                    PvC.player_vs_computer_launcher()
                    running = False
                elif e.key == p.K_3:
                    SmartMoveFinder.DEPTH = 2
                    PvC.player_vs_computer_launcher()
                    running = False
                elif e.key == p.K_4:
                    SmartMoveFinder.DEPTH = 3
                    PvC.player_vs_computer_launcher()
                    running = False

        clock.tick(PvP.MAX_FPS)
        p.display.flip()


def draw_pvp(screen):
    text1 = "MENU"
    text2 = "PRESS 1 to play vs HUMAN"
    text3 = "PRESS 2 to play vs EASY AI"
    text4 = "PRESS 3 to play vs MEDIUM AI"
    text5 = "PRESS 4 to play vs HARD AI"
    font1 = p.font.SysFont("Helvetica", 50, True, False)
    font2 = p.font.SysFont("Type1", 50, True, False)

    text_object1 = font1.render(text1, False, p.Color("dark Green"))
    text_object2 = font2.render(text2, False, p.Color("light blue"))
    text_object3 = font2.render(text3, False, p.Color("pink"))
    text_object4 = font2.render(text4, False, p.Color("red"))
    text_object5 = font2.render(text5, False, p.Color("dark red"))

    text_location1 = p.Rect(320, 120, 400, 400)
    text_location2 = p.Rect(150, 300, 400, 400)
    text_location3 = p.Rect(150, 400, 400, 400)
    text_location4 = p.Rect(150, 500, 400, 400)
    text_location5 = p.Rect(150, 600, 400, 400)

    screen.blit(text_object1, text_location1)
    screen.blit(text_object2, text_location2)
    screen.blit(text_object3, text_location3)
    screen.blit(text_object4, text_location4)
    screen.blit(text_object5, text_location5)
    #p.display.flip()





if __name__ == "__main__":
    main()

