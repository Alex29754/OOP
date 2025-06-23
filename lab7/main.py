from enum import Enum, auto
from typing import Any, Callable, Dict, Optional, Type
from contextlib import contextmanager
import inspect

# Жизненные циклы
class LifeStyle(Enum):
    PerRequest = auto()
    Scoped = auto()
    Singleton = auto()

# DI-контейнер
class Injector:
    def __init__(self):
        self._registrations = {}  # интерфейс -> (класс, lifestyle, params, factory)
        self._singletons = {}
        self._scoped_instances = {}
        self._scope_active = False

    def register(self, interface: Type, implementation: Optional[Type] = None,
                 lifestyle: LifeStyle = LifeStyle.PerRequest,
                 params: Optional[Dict[str, Any]] = None,
                 factory: Optional[Callable[[], Any]] = None):
        self._registrations[interface] = (implementation, lifestyle, params or {}, factory)

    def get_instance(self, interface: Type):
        if interface not in self._registrations:
            raise ValueError(f"Interface {interface} not registered")

        implementation, lifestyle, params, factory = self._registrations[interface]

        if lifestyle == LifeStyle.Singleton:
            if interface not in self._singletons:
                self._singletons[interface] = self._create_instance(interface, implementation, params, factory)
            return self._singletons[interface]

        if lifestyle == LifeStyle.Scoped:
            if not self._scope_active:
                raise RuntimeError("Scoped instance requested outside of scope")
            if interface not in self._scoped_instances:
                self._scoped_instances[interface] = self._create_instance(interface, implementation, params, factory)
            return self._scoped_instances[interface]

        return self._create_instance(interface, implementation, params, factory)

    def _create_instance(self, interface: Type, implementation: Type, params: Dict[str, Any], factory: Optional[Callable]):
        if factory:
            return factory()

        sig = inspect.signature(implementation.__init__)
        kwargs = {}
        for name, param in sig.parameters.items():
            if name == 'self' or param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue

            if name in params:
                kwargs[name] = params[name]
            elif param.annotation in self._registrations:
                kwargs[name] = self.get_instance(param.annotation)
            else:
                raise ValueError(f"Cannot resolve dependency '{name}' of {implementation}")
        return implementation(**kwargs)

    @contextmanager
    def create_scope(self):
        try:
            self._scope_active = True
            self._scoped_instances = {}
            yield self
        finally:
            self._scope_active = False
            self._scoped_instances = {}

# ===== Интерфейсы =====
class Interface1:
    def do(self): pass

class Interface2:
    def run(self): pass

class Interface3:
    def execute(self): pass

class InterfaceWithParams:
    def show(self): pass

class InterfaceWithFactory:
    def create(self): pass

# ===== Реализации =====
class Class1_Debug(Interface1):
    def do(self): print("Debug: Class1 doing something")

class Class2_Debug(Interface2):
    def run(self): print("Debug: Class2 running")

class Class3_Debug(Interface3):
    def __init__(self, dep: Interface1):
        self.dep = dep
    def execute(self):
        print("Debug: Class3 executing with dependency:")
        self.dep.do()

# ===== Реализация с параметрами =====
class ParametrizedClass(InterfaceWithParams):
    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level
    def show(self):
        print(f"ParametrizedClass: name={self.name}, level={self.level}")

# ===== Реализация через фабрику =====
class FactoryClass(InterfaceWithFactory):
    def __init__(self):
        self.created = True
    def create(self):
        print("FactoryClass: instance created via factory!")

# ===== Конфигурации =====
def configure(injector: Injector):
    injector.register(Interface1, Class1_Debug, LifeStyle.Singleton)
    injector.register(Interface2, Class2_Debug)
    injector.register(Interface3, Class3_Debug, LifeStyle.Scoped)

    # Регистрация с параметрами
    injector.register(
        InterfaceWithParams,
        ParametrizedClass,
        lifestyle=LifeStyle.Singleton,
        params={"name": "AdminUser", "level": 5}
    )

    # Регистрация через фабрику
    injector.register(
        InterfaceWithFactory,
        factory=lambda: FactoryClass(),
        lifestyle=LifeStyle.PerRequest
    )

# ===== Демонстрация =====
def main():
    injector = Injector()
    configure(injector)

    with injector.create_scope() as scope:
        print("=== Scoped: Class3_Debug ===")
        i3a = scope.get_instance(Interface3)
        i3a.execute()
        i3b = scope.get_instance(Interface3)
        print("Scoped same object:", i3a is i3b)

    print("\n=== Singleton with parameters ===")
    param_instance = injector.get_instance(InterfaceWithParams)
    param_instance.show()

    print("\n=== Factory instance ===")
    factory_obj = injector.get_instance(InterfaceWithFactory)
    factory_obj.create()

if __name__ == "__main__":
    main()
