from random import randint


class Field:
    """
    This is assistant class for minesweeper game.
    The class creates a matrix (type: list, x_size*y_size) with number(mines) of mines (bombs) and
    several additional variables.
    In result matrix mines positions define as number 9 and other numbers mean quantity
    of nearly mines (0-8)
    """
    def __init__(self, x_size: int, y_size: int, mines: int):
        """
        Class constructor
        :param x_size: size x of mine matrix
        :param y_size: size y of mine matrix
        :param mines: number of mines in matrix
        """
        self.size = (x_size, y_size)
        self.bombs = self.get_bombs(mines, x_size, y_size)  # mines coordinates
        self.field = [[0 for i in range(x_size)] for _ in range(y_size)]  # field initialization
        self.fill_field_list()

    @staticmethod
    def get_bombs(n: int, x_size: int, y_size: int):
        """
        This method creates a set with n coordinates of mines.
        The method have not be static.
        :param n: number of mines in matrix
        :param x_size: size x of mine matrix
        :param y_size: size y of mine matrix
        :return: set of tuples (int, int)
        """
        bombs = set()
        while len(bombs) < n:
            bombs.add((randint(0, x_size - 1), randint(0, y_size - 1)))
        return bombs

    @staticmethod
    def bomb_mapper(x: int, y: int, field_size: tuple, bombs: set):
        """
        This method returns a list of tuples with coordinates positions located around
         requested point.
         The method have to be static for call it without an instance.
        :param x: current x coordinate
        :param y: current y coordinate
        :param field_size: tuples (int, int) where ints are field borders
        :param bombs: mines coordinates
        :return: list of tuples (int, int) with interested coordinates
        """
        mapper = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if not (i == x and j == y) and i > -1 and j > -1 \
                        and i < field_size[0] and j < field_size[1] \
                        and (i, j) not in bombs:
                    mapper.append((i, j))
        return mapper

    def fill_field_list(self):
        """
        This method run through coordinates of mines and add 1 to every cell around every mine
        :return: None. The method works directly with  self.field attribute
        """
        for i, j in self.bombs:
            self.field[i][j] = 9
            for k, m in self.bomb_mapper(i, j, self.size, self.bombs):
                self.field[k][m] += 1

    def __repr__(self):
        """
        Silly string representation of class
        :return: String for print
        """
        return '\n'.join([repr(x) for x in self.field])


if __name__ == '__main__':
    game = Field(10, 10, 10)
    print(game)
