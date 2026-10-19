from abc import ABC, abstractmethod

class Notifier(ABC):#абстрактный интерфейс
    @abstractmethod
    def send(self, message: str) -> None:
        ...

class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[EMAIL] {message}")