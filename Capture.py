import cv2
import numpy as np
import os
from tensorflow.keras.models import model_from_json
from Chopsticks.game_logic import GameLogic
import random


class Capture:
    def __init__(self):
        self.states = [1, 1, 1, 1]
        self.categories = [1, 2, 3, 4]
        self.turn_flag = random.choice([0, 1])
        self.div_flag = 0  # indicates that player chose to divide
        self.player_inputs = []  # save the images to be predicted one at a time
        self.player_preds1 = []  # save the predicted values of num fingers during division as well as not div
        self.player_preds2 = []  # used for saving the predicted values of num fingers during division
        self.pos = []  # list to indicate the position of hand during players turn
        self.r50_model, self.r18_model = self.load_models()
        self.display_message = "It's your turn!" if self.turn_flag else "It's CPU's turn!"

    def load_models(self):
        # load json and create model
        r50_json_file = open(os.path.join('models', 'R50_model.json'), 'r')
        loaded_r50_model_json = r50_json_file.read()
        r50_json_file.close()
        r50_model = model_from_json(loaded_r50_model_json)
        # load weights into new model
        r50_model.load_weights(os.path.join('models', "Resnet50.h5"))

        # load json and create model
        r18_json_file = open(os.path.join('models', 'R18_model.json'), 'r')
        loaded_r18_model_json = r18_json_file.read()
        r18_json_file.close()
        r18_model = model_from_json(loaded_r18_model_json)
        # load weights into new model
        r18_model.load_weights(os.path.join('models', "Resnet18.h5"))

        return r50_model, r18_model

    def run_game_logic(self):
        while True:
            if self.div_flag and self.turn_flag:
                self.display_message = "It's your turn!"
                if len(self.player_preds1) <= 2 and len(self.player_inputs) > 1:
                    input_plr = self.player_inputs.pop()
                    input_pll = self.player_inputs.pop()
                    self.player_preds1.append(self.categories[int(np.argmax(self.r50_model.predict(input_plr)[0]))])
                    self.player_preds2.append(self.categories[int(np.argmax(self.r50_model.predict(input_pll)[0]))])
                    if len(self.player_preds2) == 2:
                        num_fingers_l = max(set(self.player_preds1), key=self.player_preds1.count)
                        num_fingers_r = max(set(self.player_preds2), key=self.player_preds2.count)

                        if GameLogic().div_validate(self.states, num_fingers_l, num_fingers_r, self.turn_flag):
                            self.states, self.turn_flag = GameLogic().player_turn_div(self.states, num_fingers_l,
                                                                                      num_fingers_r)
                            self.div_flag = 0

                        else:
                            self.display_message = "Invalid division!"

                        self.player_preds1.clear()
                        self.player_preds2.clear()
                        self.player_inputs.clear()

            elif not self.div_flag and self.turn_flag:
                self.display_message = "It's your turn!"
                if len(self.player_preds1) <= 2 and len(self.player_inputs) > 0:
                    popped_image = self.player_inputs.pop()
                    self.player_preds1.append(self.categories[int(np.argmax(self.r50_model.predict(popped_image)[0]))])
                    if len(self.player_preds1) == 2:
                        num_fingers = max(set(self.player_preds1), key=self.player_preds1.count)
                        pos = max(set(self.pos), key=self.pos.count)

                        # ask again if num fingers could not be determined
                        if GameLogic().validate(self.states, num_fingers, pos, self.turn_flag):
                            self.states, self.turn_flag = GameLogic().player_turn(self.states, num_fingers, pos)
                            self.pos.clear()

                        else:
                            self.display_message = "Invalid move!"

                        self.player_preds1.clear()
                        self.player_inputs.clear()

            # turn flag is 0 for cpu turn
            elif not self.turn_flag:
                self.display_message = "It's CPU's turn!"
                self.states, self.turn_flag = GameLogic().cpu_turn(self.states)

    def hand_detect_pred(self, img):
        output = np.squeeze(self.r18_model.predict(img))
        if output[0] < output[1]:
            return True
        else:
            return False

    def detect_hand(self, frame):

        X1 = [20, 340, 20, 340]
        Y1 = [20, 20, 260, 260]
        X2 = [300, 620, 300, 620]
        Y2 = [220, 220, 460, 460]

        cpul = frame[Y1[0]: Y2[0], X1[0]: X2[0]]
        cpur = frame[Y1[1]: Y2[1], X1[1]: X2[1]]

        pll = frame[Y1[2]: Y2[2], X1[2]: X2[2]]
        plr = frame[Y1[3]: Y2[3], X1[3]: X2[3]]

        img1 = np.expand_dims(np.asarray(cv2.resize(cpul, (224, 224))), axis=0)
        img2 = np.expand_dims(np.asarray(cv2.resize(cpur, (224, 224))), axis=0)
        img3 = np.expand_dims(np.asarray(cv2.resize(pll, (224, 224))), axis=0)
        img4 = np.expand_dims(np.asarray(cv2.resize(plr, (224, 224))), axis=0)

        if self.turn_flag:

            c_l = self.hand_detect_pred(img1)
            c_r = self.hand_detect_pred(img2)
            p_l = self.hand_detect_pred(img3)
            p_r = self.hand_detect_pred(img4)

            # Single hand detected at player left cell as well as player right
            if p_l and p_r:
                self.div_flag = 1  # to indicate that division action might take place
                self.player_inputs.append(img3)
                self.player_inputs.append(img4)

            # Single hand detected at cpu left cell
            elif c_l:
                self.pos.append(0)  # append the position of the cell where hand is
                self.player_inputs.append(img1)

            # Single hand detected at cpu right cell
            elif c_r:
                self.pos.append(1)  # append the position of the cell where hand is
                self.player_inputs.append(img2)
