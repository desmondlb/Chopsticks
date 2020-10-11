import os
from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import random
import cv2
import sys
from threading import Thread
from Chopsticks import Capture

BUTTON_HEIGHT = 60
BUTTON_WIDTH = 200
HAND_SPRITE_SIZE = 200
DEMO_SIZE = 640
SLIDING_SPEED = 80  # Select from a common factor of 640 and 480
PLAYER_WINDOW_COLOUR = (100, 255, 100)
CPU_WINDOW_COLOUR = (255, 255, 255)
BACKGROUND_COLOUR = (204, 255, 246)
DISPLAY_DIMS = [1152, 640]
FONT_COLOUR = (0, 153, 153)


class Play:
    def __init__(self):
        super().__init__()
        self.camera = cv2.VideoCapture(1)
        self.screen = pygame.display.set_mode(DISPLAY_DIMS)
        self.bg_color = BACKGROUND_COLOUR
        pygame.init()
        pygame.display.set_caption("Chopsticks")
        self.isGame = False
        self.demo_index = 0
        self.slide_left = False
        self.slide_right = False
        self.slide_count = 0
        self.frame_array = list()
        self.sprite_dict = dict()
        self.sprites()
        self.cap_obj = Capture.Capture()
        self.game_init()

    def sprites(self):
        self.sprite_dict['play'] = pygame.transform.scale(
            pygame.image.load(os.path.join("sprites", "play.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.sprite_dict['exit'] = pygame.transform.scale(
            pygame.image.load(os.path.join("sprites", "exit.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.sprite_dict['restart'] = pygame.transform.scale(
            pygame.image.load(os.path.join("sprites", "restart.png")), (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.sprite_dict['left'] = pygame.transform.scale(
            pygame.image.load(os.path.join("sprites", "left.png")), (80, 150))
        self.sprite_dict['right'] = pygame.transform.scale(
            pygame.image.load(os.path.join("sprites", "right.png")), (80, 150))
        self.sprite_dict['howto'] = pygame.transform.scale(
            pygame.image.load(os.path.join("sprites", "howto.png")), (180, 32))
        for i in range(5):
            self.sprite_dict[str(i)+'_r'] = pygame.transform.scale(
                pygame.image.load(os.path.join("sprites", str(i)+"r.png")), (HAND_SPRITE_SIZE, HAND_SPRITE_SIZE))
            self.sprite_dict[str(i)+'_l'] = pygame.transform.scale(
                pygame.image.load(os.path.join("sprites", str(i)+"l.png")), (HAND_SPRITE_SIZE, HAND_SPRITE_SIZE))
            self.sprite_dict['demo' + str(i)] = pygame.transform.scale(
                pygame.image.load(os.path.join("sprites", "demo"+str(i)+".jfif")), (DEMO_SIZE, int(DEMO_SIZE*0.75)))

    def process_frame(self):
        while True:
            if self.isGame and len(self.frame_array) > 0:
                frame = self.frame_array.pop()
                self.cap_obj.detect_hand(frame)
                self.frame_array.clear()

    def message_display(self, string, x, y, size):
        fonts = pygame.font.Font('freesansbold.ttf', size)
        textSurface = fonts.render(string, True, FONT_COLOUR)
        textRect = textSurface.get_rect()
        textRect.center = (x, y)
        self.screen.blit(textSurface, textRect)

    def draw_sprite(self):
        self.screen.blit(self.sprite_dict[str(self.cap_obj.states[0])+'_l'], (180, 100))
        self.screen.blit(self.sprite_dict[str(self.cap_obj.states[1])+'_r'], (500, 100))
        self.screen.blit(self.sprite_dict[str(self.cap_obj.states[2])+'_l'], (180, 340))
        self.screen.blit(self.sprite_dict[str(self.cap_obj.states[3])+'_r'], (500, 340))

    def draw_text(self):
        self.message_display(str(self.cap_obj.display_message), 950, 250, 45)

    def draw_rects(self):
        pygame.draw.rect(self.screen, CPU_WINDOW_COLOUR, (120, 100, 280, 200), 2)
        pygame.draw.rect(self.screen, CPU_WINDOW_COLOUR, (440, 100, 280, 200), 2)
        pygame.draw.rect(self.screen, PLAYER_WINDOW_COLOUR, (120, 340, 280, 200), 2)
        pygame.draw.rect(self.screen, PLAYER_WINDOW_COLOUR, (440, 340, 280, 200), 2)

    def demo_slide_left(self):
        if self.slide_count == 640:
            self.slide_left = False
            self.slide_count = 0
            self.demo_index = (self.demo_index + 1) % 5
            self.screen.blit(self.sprite_dict["demo" + str(self.demo_index)], (100, 80))

        else:
            prev_img = self.sprite_dict["demo" + str(self.demo_index)]
            new_img = self.sprite_dict["demo" + str((self.demo_index + 1) % 5)]
            self.screen.blit(prev_img, (100, 80), (self.slide_count, 0, 640, 480))
            self.screen.blit(new_img, (100 + (640 - self.slide_count), 80), (0, 0, self.slide_count, 480))
            self.slide_count = self.slide_count + SLIDING_SPEED

    def demo_slide_right(self):
        if self.slide_count == 640:
            self.slide_right = False
            self.slide_count = 0
            self.demo_index = (self.demo_index - 1) % 5
            self.screen.blit(self.sprite_dict["demo" + str(self.demo_index)], (100, 80))

        else:
            prev_img = self.sprite_dict["demo" + str(self.demo_index)]
            new_img = self.sprite_dict["demo" + str((self.demo_index - 1) % 5)]
            self.screen.blit(prev_img, (100 + self.slide_count, 80), (0, 0, 640 - self.slide_count, 480))
            self.screen.blit(new_img, (100, 80), (640 - self.slide_count, 0, 640, 480))
            self.slide_count = self.slide_count + SLIDING_SPEED

    def redraw(self):
        self.screen.fill(self.bg_color)

        if self.isGame:
            ret, frame = self.camera.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1, frame)

            self.screen.blit(pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1],
                                                     "RGB"), (100, 80))
            self.frame_array.append(frame)
            self.draw_rects()
            self.draw_text()
            self.draw_sprite()

            self.restart_button_pos = self.screen.blit(self.sprite_dict['restart'], (840, 400))
            self.exit_button_pos = self.screen.blit(self.sprite_dict['exit'], (840, 480))

        else:
            # self.message_display("How to play", 200, 60, 35)
            if self.slide_left:
                self.demo_slide_left()
            elif self.slide_right:
                self.demo_slide_right()
            else:
                self.screen.blit(self.sprite_dict["demo" + str(self.demo_index)], (100, 80))

            self.screen.blit(self.sprite_dict['howto'], (100, 40))
            self.left_arrow_pos = self.screen.blit(self.sprite_dict['left'], (100, 240))
            self.right_arrow_pos = self.screen.blit(self.sprite_dict['right'], (660, 240))
            self.play_button_pos = self.screen.blit(self.sprite_dict['play'], (840, 400))
            self.exit_button_pos = self.screen.blit(self.sprite_dict['exit'], (840, 480))

        pygame.display.update()

    def game_init(self):
        try:
            Thread(target=self.process_frame).start()
            Thread(target=self.cap_obj.run_game_logic).start()
            while True:
                self.redraw()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE or event.key == K_q:
                            sys.exit(0)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if not self.isGame:
                            if self.right_arrow_pos.collidepoint(pygame.mouse.get_pos()):
                                self.slide_left = True
                            elif self.left_arrow_pos.collidepoint(pygame.mouse.get_pos()):
                                self.slide_right = True
                            elif self.play_button_pos.collidepoint(pygame.mouse.get_pos()):
                                self.isGame = True
                            elif self.exit_button_pos.collidepoint(pygame.mouse.get_pos()):
                                sys.exit(0)
                        else:
                            if self.restart_button_pos.collidepoint(pygame.mouse.get_pos()):
                                self.cap_obj.states = [1, 1, 1, 1]
                                self.cap_obj.turn_flag = random.choice([0, 1])
                            elif self.exit_button_pos.collidepoint(pygame.mouse.get_pos()):
                                sys.exit(0)

        except (KeyboardInterrupt, SystemExit):
            pygame.quit()
            cv2.destroyAllWindows()


obj = Play()
