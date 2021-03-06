"""Robot class"""

import random

class Robot:
    """Defines how a Robot object is created"""

    def __init__(self, name, pos, kind, world=None):
        assert isinstance(name, str)
        assert isinstance(pos, tuple)
        assert len(pos) == 2

        self.name = name
        self.pos = pos
        self.width, self.height = 5, 5
        self.map = [[0 for i in range(self.width)] for j in range(self.height)]
        self.points = 0
        self.kind = kind
        self.myworld = world

    def get_position(self):
        """Get the position of a robot"""

        return self.pos

    def set_position(self, i, j):
        """Set the position of a robot"""

        self.pos = (i, j)
        self.myworld.change(i, j, self.name)

    def map_print(self):
        """Print the map"""

        for i in range(self.height):
            print('\t'.join(str(v) for v in self.map[i]))

    def step(self):
        """This is one step of the robot's life"""

        self.sense()
        self.act(self.think())

    def sense(self):
        """Analyze what's around the robot"""

        self.perception(self.myworld.get_around(self.get_position()))

    def __str__(self):
        return self.name + "@" + str(self.pos)

    def perception(self, sensors):
        """Build an internal model of the world given current sensor values"""

        self.map[2][2] = self.name
        for sensor in sensors:
            if sensor[0] == 'N':
                self.map[1][2] = sensor[1]
            if sensor[0] == 'S':
                self.map[3][2] = sensor[1]
            if sensor[0] == 'W':
                self.map[2][1] = sensor[1]
            if sensor[0] == 'E':
                self.map[2][3] = sensor[1]

        self.map_print()

    def think(self):
        """
        Analize his own map and decide where he can move
        :return N S E W or Blocked:
        """
        out = []
        if self.kind == "dumb":
            if self.map[1][2] in [0, 'o']:
                out.append('N')
            if self.map[3][2] in [0, 'o']:
                out.append('S')
            if self.map[2][1] in [0, 'o']:
                out.append('W')
            if self.map[2][3] in [0, 'o']:
                out.append('E')
        elif self.kind == "smart":
            if self.map[1][2] in ['o']:
                return('N')
            if self.map[3][2] in ['o']:
                return('S')
            if self.map[2][1] in ['o']:
                return('W')
            if self.map[2][3] in ['o']:
                return('E')
            if self.map[1][2] in [0]:
                out.append('N')
            if self.map[3][2] in [0]:
                out.append('S')
            if self.map[2][1] in [0]:
                out.append('W')
            if self.map[2][3] in [0]:
                out.append('E')

        if not out:
            out.append('X')

        return out[random.randint(0, len(out)-1)]

    def act(self, move):
        """
        Moves the robot into the map
        :param move: the position (N,S,E,W) or the Blocked status(X)
        :return: none
        """

        print(self.name)
        print(move)
        if move == 'N':
            if self.map[1][2] == 'o':
                self.points += 1
                self.myworld.food_list -= 1
            self.myworld.change(self.pos[0], self.pos[1], 0)
            self.set_position(self.pos[0]-1, self.pos[1])
        elif move == 'S':
            if self.map[3][2] == 'o':
                self.points += 1
                self.myworld.food_list -= 1
            self.myworld.change(self.pos[0], self.pos[1], 0)
            self.set_position(self.pos[0]+1, self.pos[1])
        elif move == 'W':
            if self.map[2][1] == 'o':
                self.points += 1
                self.myworld.food_list -= 1
            self.myworld.change(self.pos[0], self.pos[1], 0)
            self.set_position(self.pos[0], self.pos[1]-1)
        elif move == 'E':
            if self.map[2][3] == 'o':
                self.points += 1
                self.myworld.food_list -= 1
            self.myworld.change(self.pos[0], self.pos[1], 0)
            self.set_position(self.pos[0], self.pos[1]+1)
        elif move == 'X':
            print("Non posso muovermi")
