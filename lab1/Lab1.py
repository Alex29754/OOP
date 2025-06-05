# Ограничения по координатам
MAX_WIDTH = 800
MAX_HEIGHT = 600

class Point2D:
    def __init__(self, x: int, y: int):
        if not (0 <= x <= MAX_WIDTH):
            raise ValueError(f"x должен быть в диапазоне [0, {MAX_WIDTH}]")
        if not (0 <= y <= MAX_HEIGHT):
            raise ValueError(f"y должен быть в диапазоне [0, {MAX_HEIGHT}]")
        self._x = x
        self._y = y

    @property
    def x(self): return self._x

    @property
    def y(self): return self._y

    def __eq__(self, other): return isinstance(other, Point2D) and self.x == other.x and self.y == other.y

    def __str__(self): return f"Point2D({self.x}, {self.y})"

    def __repr__(self): return str(self)


class Vector2D:
    def __init__(self, a, b=None):
        if isinstance(a, Point2D) and isinstance(b, Point2D):
            self._x = b.x - a.x
            self._y = b.y - a.y
        else:
            self._x = int(a)
            self._y = int(b)

    @property
    def x(self): return self._x

    @x.setter
    def x(self, value): self._x = int(value)

    @property
    def y(self): return self._y

    @y.setter
    def y(self, value): self._y = int(value)

    def __getitem__(self, i):
        if i == 0: return self._x
        if i == 1: return self._y
        raise IndexError("Индекс должен быть 0 или 1")

    def __setitem__(self, i, value):
        if i == 0: self._x = int(value)
        elif i == 1: self._y = int(value)
        else: raise IndexError("Индекс должен быть 0 или 1")

    def __iter__(self): return iter((self._x, self._y))

    def __len__(self): return 2

    def __eq__(self, other): return isinstance(other, Vector2D) and self.x == other.x and self.y == other.y

    def __str__(self): return f"Vector2D({self.x}, {self.y})"

    def __repr__(self): return str(self)

    def __abs__(self): return (self.x**2 + self.y**2) ** 0.5

    def __add__(self, other): return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other): return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar): return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar): return Vector2D(self.x / scalar, self.y / scalar)

    def dot(self, other): return self.x * other.x + self.y * other.y

    @staticmethod
    def dot_product(v1, v2): return v1.x * v2.x + v1.y * v2.y

    def cross(self, other): return self.x * other.y - self.y * other.x

    @staticmethod
    def cross_product(v1, v2): return v1.x * v2.y - v1.y * v2.x

    def mixed_product(self, *_): return 0  # В 2D всегда 0


# Пример использования
if __name__ == "__main__":
    a = Point2D(100, 150)
    b = Point2D(300, 400)

    print("Точка A:", a)
    print("Точка B:", b)

    v1 = Vector2D(3, 4)
    v2 = Vector2D(a, b)

    print("Вектор v1:", v1)
    print("Вектор v2 (из A в B):", v2)

    print("Длина v1:", abs(v1))
    print("Сумма векторов:", v1 + v2)
    print("Разность векторов:", v2 - v1)
    print("Умножение на число:", v1 * 2)
    print("Деление на число:", v1 / 2)

    print("Скалярное произведение (метод):", v1.dot(v2))
    print("Скалярное произведение (статич. метод):", Vector2D.dot_product(v1, v2))

    print("Векторное произведение (метод):", v1.cross(v2))
    print("Векторное произведение (статич. метод):", Vector2D.cross_product(v1, v2))

    print("Смешанное произведение:", v1.mixed_product(v1, v2))

    print(f"Индексация v1: x = {v1[0]}, y = {v1[1]}")
    v1[0] = 7
    print("После изменения v1:", v1)
