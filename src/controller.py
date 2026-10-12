class Controller:
    def __init__(self, io, db, calculator, notifier):
        self.io = io
        self.db = db
        self.calculator = calculator
        self.notifier = notifier

    def run(self):
        a = float(self.io.get_input("Введите сторону a: "))
        b = float(self.io.get_input("Введите сторону b: "))
        c = float(self.io.get_input("Введите сторону c: "))

        cached = self.db.get(a, b, c)
        if cached is not None:
            t_type, err = cached
        else:
            t_type, err = self.calculator.determine_type(a, b, c)
            self.db.add(a, b, c, t_type, err)

        result = err if err else f"Тип: {t_type}"
        self.notifier.send(result)
        return result