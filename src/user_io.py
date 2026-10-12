from abc import ABC, abstractmethod

class UserIO(ABC):
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        ...

class ConsoleUserIO(UserIO):
    def get_input(self, prompt: str) -> str:
        return input(prompt)