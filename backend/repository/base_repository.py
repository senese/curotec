from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')
TModel = TypeVar('TModel')


class BaseRepository(ABC, Generic[T, TModel]):
    @abstractmethod
    def insert(self, entity: T) -> TModel: ...

    @abstractmethod
    def update(self, entity: T) -> None: ...

    @abstractmethod
    def find(self, id: str) -> TModel: ...

    @abstractmethod
    def find_all(self) -> list[TModel]: ...

    @abstractmethod
    def delete(self, model: TModel) -> None: ...
