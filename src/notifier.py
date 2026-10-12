from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        ...

class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        # имитация: реально никуда не шлём
        print(f"[EMAIL] {message}")