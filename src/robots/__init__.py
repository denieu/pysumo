from abc import *
import pygame


class RobotABC(ABC):
    def __init__(self, image, size=50, pos=(0, 0), angle=0):
        super().__init__()
        self.setup()

        # Attribute Points
        self.__max_points = 5

        # Attributes
        self.__attributes_seted = 0
        self.__attributes = {
            "name": "",
            "vel": 0,
            "strengh": 0,
            "sd": 0,
            "sa": 0
        }

        # Position
        self.__angle = angle
        self.__pos = [pos[0], pos[1]]

        # Graph
        self.__image = pygame.image.load(image)
        self.__image = pygame.transform.scale(self.__image, (size, size))
        self.__image = pygame.transform.rotate(self.__image, angle)

    def get_attributes(self):
        return self.__attributes

    def set_attributes(self, vel, strengh, sd, sa):
        if self.__attributes_seted == 0:
            if (vel + strengh + sd + sa) > self.__max_points:
                raise Exception("Attribute points exceeded")
            else:
                self.__attributes["vel"] = vel
                self.__attributes["strengh"] = strengh
                self.__attributes["sd"] = sd
                self.__attributes["sa"] = sa
                self.__attributes_seted = 1

    def get_angle(self):
        return self.__angle

    def rotate(self, angle):
        self.__angle += angle

        if self.__angle >= 360:
            self.__angle = 360 - self.__angle
            self.__angle = 360 - self.__angle

        elif self.__angle < 0:
            self.__angle = 360 + self.__angle

        self.__image = pygame.transform.rotate(self.__image, angle)

    def get_pos(self):
        return self.__pos

    def move(self, pos):
        self.__pos = [pos[0], pos[1]]

    def get_image(self):
        return self.__image

    @classmethod
    @abstractmethod
    def setup(cls):
        pass

    @classmethod
    @abstractmethod
    def loop(cls, sensors):
        pass
