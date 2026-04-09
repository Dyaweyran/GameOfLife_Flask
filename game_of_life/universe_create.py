import random
import copy
from threading import Lock


class SingletonMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances or args or kwargs:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class GameOfLife(metaclass=SingletonMeta):
    def __init__(self, width=20, height=20):
        self.__width = width
        self.__height = height
        self.world = self.generate_universe()
        self.counter = -1
        self.__old_world = self.world
        self.mistakes = 0

    def __check_condition(self, height, width):
        if 0 <= width < self.__width and 0 <= height < self.__height:
            return True
        return False

    def form_new_generation(self):
        universe = self.world
        self.__old_world = copy.deepcopy(universe)
        new_world = []
        area_check = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1))

        for i in range(self.__height):
            new_row = []
            for j in range(self.__width):
                counter = 0
                for l_height, l_width in area_check:
                    if self.__check_condition(i + l_height, j + l_width):
                        if universe[i + l_height][j + l_width] == 1:
                            counter += 1
                if 2 <= counter <= 3:
                    new_row.append(1)
                else:
                    if self.counter >= 0 and self.__old_world[i][j] == 1:
                        new_row.append(2)
                    else:
                        new_row.append(0)

            new_world.append(new_row)

        self.world = new_world
        self.counter += 1

    def generate_universe(self):
        return [[random.randint(0, 1) for _ in range(self.__width)] for _ in range(self.__height)]

    def check_condition(self, check_line):
        true_line = []

        for elem in self.world:
            for el in elem:
                true_line.append(el)

        counter = 0

        print("User input: ", check_line)
        print()
        print("Correct line: ", true_line)

        if len(true_line) != len(check_line):
            a = len(true_line)
            b = len(check_line)
            raise ValueError(
                f"Разные массивы по длине. Родной: {a} Пользовательский: {b}")

        for i in range(max(len(true_line), len(check_line))):
            if true_line[i] == 1 and check_line[i] == 0 or true_line[i] in (0, 2) and check_line[i] == 1:
                counter += 1

        self.mistakes += counter
