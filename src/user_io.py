from abc import ABC, abstractmethod 

class UserIO(ABC): #это интерфейс
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        ...

class ConsoleUserIO(UserIO):
    def get_input(self, prompt: str) -> str:
        return input(prompt)