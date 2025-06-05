from dataclasses import dataclass, field
from typing import Optional, Protocol, TypeVar, Generic, Sequence
import json
import os

T = TypeVar("T")


@dataclass(order=True)
class User:
    sort_index: str = field(init=False, repr=False)
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    email: Optional[str] = None
    address: Optional[str] = None

    def __post_init__(self):
        self.sort_index = self.name


class IDataRepository(Protocol, Generic[T]):
    def get_all(self) -> Sequence[T]: ...
    def get_by_id(self, id: int) -> Optional[T]: ...
    def add(self, item: T) -> None: ...
    def update(self, item: T) -> None: ...
    def delete(self, item: T) -> None: ...


class IUserRepository(IDataRepository[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]: ...


class DataRepository(Generic[T], IDataRepository[T]):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._data: list[T] = []
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                self._data = [self._deserialize(item) for item in raw_data]

    def _save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([self._serialize(item) for item in self._data], f, ensure_ascii=False, indent=2)

    def _serialize(self, item: T) -> dict:
        return item.__dict__

    def _deserialize(self, data: dict) -> T:
        raise NotImplementedError

    def get_all(self) -> Sequence[T]:
        return self._data

    def get_by_id(self, id: int) -> Optional[T]:
        return next((item for item in self._data if item.id == id), None)

    def add(self, item: T) -> None:
        self._data.append(item)
        self._save()

    def update(self, item: T) -> None:
        index = next((i for i, x in enumerate(self._data) if x.id == item.id), -1)
        if index != -1:
            self._data[index] = item
            self._save()

    def delete(self, item: T) -> None:
        self._data = [x for x in self._data if x.id != item.id]
        self._save()


class UserRepository(DataRepository[User], IUserRepository):
    def _deserialize(self, data: dict) -> User:
        data = dict(data)
        data.pop("sort_index", None)
        return User(**data)

    def get_by_login(self, login: str) -> Optional[User]:
        return next((u for u in self._data if u.login == login), None)


class IAuthService(Protocol):
    def sign_in(self, user: User) -> None: ...
    def sign_out(self) -> None: ...
    @property
    def is_authorized(self) -> bool: ...
    @property
    def current_user(self) -> Optional[User]: ...


class AuthService(IAuthService):
    def __init__(self, auth_file: str):
        self.auth_file = auth_file
        self._current_user: Optional[User] = None
        self._load()

    def _load(self):
        if os.path.exists(self.auth_file):
            with open(self.auth_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.pop("sort_index", None)
                self._current_user = User(**data)

    def _save(self):
        if self._current_user:
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(self._current_user.__dict__, f, ensure_ascii=False, indent=2)
        else:
            if os.path.exists(self.auth_file):
                os.remove(self.auth_file)

    def sign_in(self, user: User) -> None:
        self._current_user = user
        self._save()

    def sign_out(self) -> None:
        self._current_user = None
        self._save()

    @property
    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> Optional[User]:
        return self._current_user


if __name__ == "__main__":
    repo = UserRepository("users.json")
    auth = AuthService("auth.json")

    user = User(id=1, name="Alice", login="alice", password="pass123", email="alice@mail.com")
    if not repo.get_by_id(user.id):
        repo.add(user)

    user.email = "alice_new@mail.com"
    repo.update(user)

    user_from_repo = repo.get_by_login("alice")
    if user_from_repo and user_from_repo.password == "pass123":
        auth.sign_in(user_from_repo)

    print("Авторизован:", auth.is_authorized)
    print("Пользователь:", auth.current_user)

    auth.sign_out()

    auth2 = AuthService("auth.json")
    print("Автоавторизация:", auth2.is_authorized)
    print("Пользователь:", auth2.current_user)
