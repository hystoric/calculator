import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from functools import partial

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.title('Калькулятор')
        self.geometry('300x340+1000+500')
        self.resizable(False, False)

        self.grid_params = {
            'sticky': 'wens',
            'padx': 5, 'pady': 5
        }

        self.btn_params = {
            'fg_color': '#333333',
            'hover_color': '#262626',
            'font': ('Arial', 13)
        }

        self.create_ui()
        self.configure_grid()

    def create_ui(self):
        self.entry = ctk.CTkEntry(
            self, justify='right',
            font=('Arial', 30), height=50
        )
        self.entry.insert(0, '0')
        self.entry.grid(
            row=0, column=0,
            columnspan=4,
            stick='we', padx=5
        )
        self.entry.bind('<Key>', self.calculate)

        button_data = [
            ('0', 4, 0), ('1', 1, 0), ('2', 1, 1), ('3', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('7', 3, 0),
            ('8', 3, 1), ('9', 3, 2), ('+', 1, 3), ('-', 2, 3),
            ('*', 3, 3), ('/', 4, 3), ('C', 4, 1), ('=', 4, 2)
        ]

        for text, row, column in button_data:
            command = partial(self.calculate, text)

            button = ctk.CTkButton(
                self,
                **self.btn_params,
                text=text,
                command=command
            )
            button.grid(
                row=row,
                column=column,
                **self.grid_params
            )

    def configure_grid(self):
        for column in range(4):
            self.grid_columnconfigure(column, weight=1)

        for row in range(1, 5):
            self.grid_rowconfigure(row, weight=1)

    def calculate(self, action):
        is_keyboard = hasattr(action, 'char')

        if is_keyboard:
            event = action
            action = event.char

            if event.keysym == 'Backspace' or action == '\x08':
                value = self.entry.get()
                self.entry.delete(0, 'end')

                if len(value) <= 1:
                    self.entry.insert(0, '0')
                else:
                    self.entry.insert(0, value[:-1])
                return 'break'

            if action == '\r':
                action = '='

            if action not in '0123456789+-*/=':
                return 'break'

        value = self.entry.get()

        if action == 'C':
            self.entry.delete(0, 'end')
            self.entry.insert(0,0)
            return 'break' if is_keyboard else None

        if action == '=':
            if not value:
                return 'break' if is_keyboard else None

            if value [-1] in '+-*/':
                value += value [:-1]
            self.entry.delete(0, 'end')

            try:
                result = str(eval(value))
                self.entry.insert(0, result)
            except (NameError, SyntaxError):
                CTkMessagebox(
                    self,
                    title='Внимание!',
                    message='Нужны только цифры. Вы ввели другие символы!'
                )
                self.entry.insert(0,0)
            except ZeroDivisionError:
                CTkMessagebox(
                    self,
                    title='Внимание!',
                    message='На ноль делить нельзя!'
                )
                self.entry.insert(0,0)
            return 'break' if is_keyboard else None

        if action in '+-*/':
            if not value:
                return 'break' if is_keyboard else None
            if value[-1] in '+-*/':
                value = value[:-1]
            elif any(op in value for op in '+-*/'):
                self.entry.delete(0, 'end')
                try:
                    value = str(eval(value))
                except ZeroDivisionError:
                    CTkMessagebox(
                        self,
                        title='Внимание!',
                        message='На ноль делить нельзя!'
                    )
                    value = '0'
                except Exception:
                    value = '0'
            self.entry.delete(0, 'end')
            self.entry.insert(0, value + action)
            return 'break' if is_keyboard else None

        if value == '0':
            value = ''
        self.entry.delete(0, 'end')
        self.entry.insert(0, value + str(action))

        if is_keyboard:
            return 'break'


if __name__ == '__main__':
    app = CalculatorApp()
    app.mainloop()