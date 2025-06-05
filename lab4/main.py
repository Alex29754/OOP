from typing import Protocol, TypeVar, Generic

# Универсальный тип
T = TypeVar("T")


# --- Интерфейс слушателя изменений ---
class PropertyChangedListenerProtocol(Protocol[T]):
    def on_property_changed(self, obj: T, property_name: str) -> None:
        ...


# --- Интерфейс для классов, которые оповещают об изменениях ---
class DataChangedProtocol(Protocol[T]):
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol[T]) -> None:
        ...
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol[T]) -> None:
        ...


# --- Интерфейс слушателя ПЕРЕД изменением (валидация) ---
class PropertyChangingListenerProtocol(Protocol[T]):
    def on_property_changing(self, obj: T, property_name: str, old_value, new_value) -> bool:
        ...


# --- Интерфейс для классов, поддерживающих валидацию изменений ---
class DataChangingProtocol(Protocol[T]):
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol[T]) -> None:
        ...
    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol[T]) -> None:
        ...


# --- Класс, реализующий все протоколы ---
class Person(DataChangedProtocol["Person"], DataChangingProtocol["Person"]):
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age
        self._change_listeners: list[PropertyChangedListenerProtocol] = []
        self._changing_listeners: list[PropertyChangingListenerProtocol] = []

    # Добавление/удаление слушателей изменений
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._change_listeners.append(listener)

    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._change_listeners.remove(listener)

    # Добавление/удаление слушателей валидации
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.append(listener)

    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.remove(listener)

    # Уведомление: перед изменением
    def _notify_property_changing(self, property_name: str, old_value, new_value) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True

    # Уведомление: после изменения
    def _notify_property_changed(self, property_name: str) -> None:
        for listener in self._change_listeners:
            listener.on_property_changed(self, property_name)

    # --- Свойство name ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if self._notify_property_changing("name", self._name, value):
            self._name = value
            self._notify_property_changed("name")

    # --- Свойство age ---
    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if self._notify_property_changing("age", self._age, value):
            self._age = value
            self._notify_property_changed("age")

    def __str__(self):
        return f"Person(name={self._name}, age={self._age})"


# --- Пример слушателя изменений ---
class PrintListener(PropertyChangedListenerProtocol[Person]):
    def on_property_changed(self, obj: Person, property_name: str) -> None:
        print(f"[Изменение] {property_name} изменено у {obj}")


# --- Пример валидатора ---
class AgeValidator(PropertyChangingListenerProtocol[Person]):
    def on_property_changing(self, obj: Person, property_name: str, old_value, new_value) -> bool:
        if property_name == "age":
            if not (0 <= new_value <= 120):
                print(f"[Ошибка] Неверный возраст: {new_value}")
                return False
        return True


# --- Ещё один валидатор ---
class NameValidator(PropertyChangingListenerProtocol[Person]):
    def on_property_changing(self, obj: Person, property_name: str, old_value, new_value) -> bool:
        if property_name == "name" and len(new_value.strip()) == 0:
            print(f"[Ошибка] Имя не может быть пустым!")
            return False
        return True


# --- Тестирование ---
if __name__ == "__main__":
    p = Person("Alice", 30)

    # Добавляем слушателей
    p.add_property_changed_listener(PrintListener())
    p.add_property_changing_listener(AgeValidator())
    p.add_property_changing_listener(NameValidator())

    print("Попытка изменить возраст на 40:")
    p.age = 40  # проходит

    print("\nПопытка изменить возраст на -5:")
    p.age = -5  # не проходит

    print("\nПопытка изменить имя на 'Bob':")
    p.name = "Bob"  # проходит

    print("\nПопытка изменить имя на '   ':")
    p.name = "   "  # не проходит
