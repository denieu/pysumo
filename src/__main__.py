import pygame
from pygame.locals import *
from sys import exit

from src.robots.robot1 import Robot as Robot1
from src.robots.robot2 import Robot as Robot2


class PySumo:
    SCREN_SIZE = 1000
    ROBOT_SIZE = 50
    CLOCK_TIME = 500

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PySumo")

        self.screen = pygame.display.set_mode((self.SCREN_SIZE, self.SCREN_SIZE))
        self.clock = pygame.time.Clock()

        self.robots = {
            "robots": [],
            "distance": [],
            "floor": [],
            "action": []
        }

        self.instance_robots()

    def instance_robots(self):
        self.robots["robots"].append(Robot1("./image/robo1.png", self.ROBOT_SIZE, (100, 100), 180))
        self.robots["distance"].append([-1] * 3)
        self.robots["floor"].append([-1] * 4)
        self.robots["action"].append("None")

        self.robots["robots"].append(Robot2("./image/robo2.png", self.ROBOT_SIZE, (500, 500), 0))
        self.robots["distance"].append([-1] * 3)
        self.robots["floor"].append([-1] * 4)
        self.robots["action"].append("None")

    def read_distance_sensors(self, reference, oponent):
        _sensors = [-1] * 4

        if oponent.get_pos()[0] == reference.get_pos()[0]:
            if oponent.get_pos()[1] < reference.get_pos()[1]:
                # Cima
                _sensors[0] = abs(oponent.get_pos()[1] - reference.get_pos()[1]) - self.ROBOT_SIZE
                _sensors[1] = -1
            else:
                # Baixo
                _sensors[0] = -1
                _sensors[1] = abs(reference.get_pos()[1] - oponent.get_pos()[1]) - self.ROBOT_SIZE

        if oponent.get_pos()[1] == reference.get_pos()[1]:
            if oponent.get_pos()[0] < reference.get_pos()[0]:
                # Esquerda
                _sensors[2] = abs(oponent.get_pos()[0] - reference.get_pos()[0]) - self.ROBOT_SIZE
                _sensors[3] = -1
            else:
                # Direita
                _sensors[2] = -1
                _sensors[3] = abs(reference.get_pos()[0] - oponent.get_pos()[0]) - self.ROBOT_SIZE

        # Remove sensor traseiro do robo, e ajusta para (esquerda, frente, direita)
        if reference.get_angle() == 0:
            _sensors = [_sensors[2], _sensors[0], _sensors[3]]
        elif reference.get_angle() == 90:
            _sensors = [_sensors[1], _sensors[2], _sensors[0]]
        elif reference.get_angle() == 180:
            _sensors = [_sensors[3], _sensors[1], _sensors[2]]
        elif reference.get_angle() == 270:
            _sensors = [_sensors[0], _sensors[3], _sensors[1]]

        return _sensors

    @staticmethod
    def read_floor_sensors(reference):
        return [-1] * 4

    def move(self, robot, action, oponent):
        posold = robot.get_pos()

        # Rotate
        if action == "left":
            robot.rotate(90)
        elif action == "right":
            robot.rotate(-90)

        # Front/Back
        elif robot.get_angle() == 0 and action == "front" or robot.get_angle() == 180 and action == "back":
            robot.move((posold[0], posold[1] - 1))
        elif robot.get_angle() == 90 and action == "front" or robot.get_angle() == 270 and action == "back":
            robot.move((posold[0] - 1, posold[1]))
        elif robot.get_angle() == 180 and action == "front" or robot.get_angle() == 0 and action == "back":
            robot.move((posold[0], posold[1] + 1))
        elif robot.get_angle() == 270 and action == "front" or robot.get_angle() == 90 and action == "back":
            robot.move((posold[0] + 1, posold[1]))

        # Colision
        if oponent.get_pos()[0] - self.ROBOT_SIZE - 1 <= robot.get_pos()[0] <= \
                oponent.get_pos()[0] + self.ROBOT_SIZE - 1:
            if robot.get_angle() == 0 and robot.get_pos()[1] == oponent.get_pos()[1] + self.ROBOT_SIZE:
                robot.move(posold)
                oponent.move((oponent.get_pos()[0], oponent.get_pos()[1] - 1))
            elif robot.get_angle() == 180 and robot.get_pos()[1] + self.ROBOT_SIZE == oponent.get_pos()[1]:
                robot.move(posold)
                oponent.move((oponent.get_pos()[0], oponent.get_pos()[1] + 1))

        elif oponent.get_pos()[1] - self.ROBOT_SIZE - 1 <= robot.get_pos()[1] <= \
                oponent.get_pos()[1] + self.ROBOT_SIZE - 1:
            if robot.get_angle() == 90 and robot.get_pos()[0] == oponent.get_pos()[0] + self.ROBOT_SIZE:
                robot.move(posold)
                oponent.move((oponent.get_pos()[0] - 1, oponent.get_pos()[1]))
            elif robot.get_angle() == 270 and robot.get_pos()[0] + self.ROBOT_SIZE == oponent.get_pos()[0]:
                robot.move(posold)
                oponent.move((oponent.get_pos()[0] + 1, oponent.get_pos()[1]))

        return robot, oponent

    @staticmethod
    def pygame_events():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

    def pygame_update(self):
        self.clock.tick(self.CLOCK_TIME)
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.robots["robots"][0].get_image(), self.robots["robots"][0].get_pos())
        self.screen.blit(self.robots["robots"][1].get_image(), self.robots["robots"][1].get_pos())

        pygame.display.update()

    def loop(self):
        while True:
            self.pygame_events()

            self.robots["distance"][0] = self.read_distance_sensors(self.robots["robots"][0], self.robots["robots"][1])
            self.robots["distance"][1] = self.read_distance_sensors(self.robots["robots"][1], self.robots["robots"][0])

            self.robots["floor"][0] = self.read_floor_sensors(self.robots["robots"][0])
            self.robots["floor"][1] = self.read_floor_sensors(self.robots["robots"][1])

            self.robots["action"][0] = self.robots["robots"][0].loop(self.robots["distance"][0])
            self.robots["action"][1] = self.robots["robots"][1].loop(self.robots["distance"][1])

            self.robots["robots"][0], self.robots["robots"][1] = self.move(
                self.robots["robots"][0], self.robots["action"][0], self.robots["robots"][1])

            self.robots["robots"][1], self.robots["robots"][0] = self.move(
                self.robots["robots"][1], self.robots["action"][1], self.robots["robots"][0])

            self.pygame_update()


if __name__ == "__main__":
    PySumo().loop()
