from src.robots import RobotABC


class Robot(RobotABC):
    def __init__(self, image, size=50, pos=(0, 0), angle=0):
        super().__init__(image, size, pos, angle)

    def setup(self):
        print("Robo 1 setup")

    def loop(self, sensors):
        if sensors[0] != -1:
            return "left"
        elif sensors[2] != -1:
            return "right"
        else:
            return "front"
