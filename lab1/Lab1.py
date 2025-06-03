from math import sqrt

SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768

class Point2d:
    def __init__(self, x: int, y: int)-> None:
        self.x, self.y = x, y

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'Point2D({self.x}, {self.y})'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point2d):
            return False
        return self.x == other.x and self.y == other.y

    # Properties
    @property #getter x
    def x(self):
        return self._x

    @x.setter #setter x
    def x(self, x) -> None:
        if x<0 or x>SCREEN_WIDTH:
            raise ValueError("x out of bounds")
        self._x = x

    @property #getter y
    def y(self):
        return self._y

    @y.setter #setter y
    def y(self, y) -> None:
        if y<0 or y>SCREEN_HEIGHT:
            raise ValueError("y out of bounds")
        self._y = y

class Vector2d:
    def __init__(self, x: int, y: int)-> None:
        self.x, self.y = x, y

    # Properties
    @property #getter x
    def x(self):
        return self._x

    @x.setter #setter x
    def x(self, x) -> None:
        self._x = x

    @property #getter y
    def y(self):
        return self._y

    @y.setter #setter y
    def y(self, y) -> None:
        self._y = y

    @classmethod
    def fromPoints(cls, start: Point2d, end: Point2d)-> None:
        return Vector2d(end.x-start.x, end.y-start.y)

    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    def __repr__(self) -> str:
        return f'Vector2d({self.x}, {self.y})'

    def __abs__(self) -> int:
        return sqrt(self.x * self.x) + (self.y * self.y)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2d):
            return False
        return self.x == other.x and self.y == other.y

    def __getitem__(self, index: int):
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise IndexError("Invaild index")

    def __setitem__(self, index: int, value: int):
        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case _:
                raise IndexError("Invaild index")

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __add__(self, other):
        if not isinstance(other, Vector2d):
            raise TypeError("Vector2d can only be added to Vector2d")
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector2d):
            raise TypeError("Vector2d can only be subtracted from Vector2d")
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError("Vector2d can only be multiplied by int")
        return Vector2d(self.x * other, self.y * other)

    def __rmul__(self, other):
        if not isinstance(other, int):
            raise TypeError("Vector2d can only be multiplied by int")
        return Vector2d(self.x * other, self.y * other)

    def __truediv__(self, other):
        if not isinstance(other, int):
            raise TypeError("Vector2d can only be divided by int")
        if other == 0:
            raise ZeroDivisionError("Division by zero")
        return Vector2d(int(self.x / other), int(self.y / other))

    def scalarMultiply(self, other):
        if not isinstance(other, Vector2d):
            raise TypeError("Vector2d can only be scalar multiplied by Vector2d")
        return self.x * other.x + self.y * other.y

    @classmethod
    def getScalarMultiply(cls,vector1, vector2):
        if not isinstance(vector1, Vector2d) or not isinstance(vector2, Vector2d):
            raise TypeError("Vector2d can only be scalar multiplied by Vector2d")
        return vector1.scalarMultiply(vector2)

    def vectorMultiply(self, other):
        if not isinstance(other, Vector2d):
            raise TypeError("Vector2d can only be vector multiplied by Vector2d")
        return self.x * other.y - self.y * other.x

    @classmethod
    def getVectorMultiply(cls, vector1, vector2):
        if not isinstance(vector1, Vector2d) or not isinstance(vector2, Vector2d):
            raise TypeError("Vector2d can only be vector multiplied by Vector2d")
        return vector1.vectorMultiply(vector2)

    def combineMultimply(self, other1, other2):
        if not isinstance(other1, Vector2d) or not isinstance(other2, Vector2d):
            raise TypeError("Vector2d can only be combine multiplied by two Vector2d")
        return 0

    @classmethod
    def getCombineMultiply(cls, vector1, vector2, vector3):
        if not isinstance(vector1, Vector2d) or not isinstance(vector2, Vector2d) or not isinstance(vector3, Vector2d):
            raise TypeError("Vector2d can only be combine multiplied by two Vector2d")
        return 0

#actual test
p1 = Point2d (69,420)
p2 = Point2d (300, 500)
p3 = Point2d (1, 3)
v1 = Vector2d (35, 100)
v2 = Vector2d.fromPoints(p1, p2)
v3 = Vector2d.fromPoints(p1, p3)

print(f'Пример точки: {repr(p1)}')
print(f'Пример вектор: {repr(v1)}')
print(f'Пример вектора заданного по точкам: {repr(v2)}')

print(f'p1==p2: {p1==p2}')
print(f'v1==v2: {v1==v2}')
print(v1==v1)
print(p2 == p2)

print(f'Модуль вектора v1: {abs(v1)}')
print(f'v1+v2: {v1+v2}')
print(f'v1-v2: {v1-v2}')
print(f'v1*5: {v1*5}')
print(f'5*v1: {5*v1}')
print(f'v1/5: {v1/5}')
print(f'Скалярное произведение: {v1.scalarMultiply(v2)}')
print(f'Векторное произведение: {Vector2d.getVectorMultiply(v1, v2)}')
print(f'Смешанное произведение: {Vector2d.getCombineMultiply(v1, v2, v3)}')