import random
import customtkinter
import sqlite3


class LabelAndEntryFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label_hand = customtkinter.CTkLabel(self, text="Введите название автомобиля,\n" 
                                                            " стоимость и отметьте его параметры")
        self.label_name = customtkinter.CTkLabel(self, text="Название автомобиля")
        self.label_cost = customtkinter.CTkLabel(self, text="Стоимость нового автомобиля (руб)")

        self.entry_name = customtkinter.CTkEntry(self, placeholder_text="Введите название")
        self.entry_cost = customtkinter.CTkEntry(self, placeholder_text="Введите стоимость")

        self.label_hand.grid(row=0, column=0, padx=10, sticky="ew")
        self.label_name.grid(row=1, column=0, padx=10, sticky="ew")
        self.entry_name.grid(row=2, column=0, padx=10, sticky="ew")
        self.label_cost.grid(row=3, column=0, padx=10, sticky="ew")
        self.entry_cost.grid(row=4, column=0, padx=10, sticky="ew")

    def get(self):
        return tuple([self.entry_name.get(), self.entry_cost.get()])

    def set(self, name=None, cost=None):
        if name is not None:
            self.entry_name.delete("0", "end")
            self.entry_name.insert("0", name)
        if cost is not None:
            self.entry_cost.delete("0", "end")
            self.entry_cost.insert("0", cost)


class CheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_age = customtkinter.CTkCheckBox(self, text="Старше 10 лет")
        self.checkbox_accident = customtkinter.CTkCheckBox(self, text="Аварийная")
        self.checkbox_customs = customtkinter.CTkCheckBox(self, text="Таможня")
        self.checkbox_mileage = customtkinter.CTkCheckBox(self, text="Пробег по РФ")
        self.checkboxes = [self.checkbox_age, self.checkbox_accident, self.checkbox_customs, self.checkbox_mileage]

        self.checkbox_age.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_accident.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_customs.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_mileage.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            checked_checkboxes.append(checkbox.get())
        return tuple(checked_checkboxes)

    def set(self, parameters=(0, 0, 0, 0)):
        for index in range(len(self.checkboxes)):
            if parameters[index]:
                self.checkboxes[index].select()
            else:
                self.checkboxes[index].deselect()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.database = sqlite3.connect('data.db')
        self.cursor = self.database.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS list_of_car(
                car_id INTEGER,
                name TEXT,
                cost INTEGER,
                age INTEGER,
                accident INTEGER,
                customs INTEGER,
                milage INTEGER
                )
            """)

        self.title("Стоимость автомобиля")
        self.geometry("530x420")
        self.resizable(False, False)

        self.label_and_entry_frame = LabelAndEntryFrame(self)
        self.checkbox_frame = CheckboxFrame(self)

        self.button_calculate = customtkinter.CTkButton(self, text="Подсчитать", command=self.calculate)
        self.button_add = customtkinter.CTkButton(self, text="Добавить", width=90, command=self.add_object)
        self.button_check = customtkinter.CTkButton(self, text="Проверить", width=90, command=self.check_object)
        self.button_delete = customtkinter.CTkButton(self, text="Удалить", width=90, command=self.delete_object)
        self.textbox_list_of_cars = customtkinter.CTkTextbox(self, width=200, corner_radius=15, wrap="word")
        self.entry_result = customtkinter.CTkEntry(self, height=20, font=("Areal", 30), placeholder_text="")

        self.label_and_entry_frame.grid(row=0, column=0, padx=(5, 0), pady=(5, 0))
        self.checkbox_frame.grid(row=1, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
        self.button_calculate.grid(row=2, column=0,  padx=20, pady=5, sticky="ew")
        self.textbox_list_of_cars.grid(row=0, column=1, rowspan=2, columnspan=3, padx=(5, 0), pady=(5, 0),
                                       sticky="nsew")
        self.button_add.grid(row=2, column=1, sticky="ew")
        self.button_check.grid(row=2, column=2, sticky="ew")
        self.button_delete.grid(row=2, column=3, sticky="ew")
        self.entry_result.grid(row=3, column=0, columnspan=4, padx=30, pady=10, sticky="ew")

        self.update_textbox_list_of_car()

    def calculate(self):
        cost = self.label_and_entry_frame.get()[1]
        try:
            cost = int(cost)
            result = cost
            parameters = self.checkbox_frame.get()

            if parameters[0] == 1:
                result -= cost*0.1
            if parameters[1] == 1:
                result -= cost*0.3
            if parameters[2] == 1:
                result -= cost*0.1
            if parameters[3] == 1:
                result -= cost*0.05

            if result % 1 == 0:
                self.entry_result.delete("0", "end")
                self.entry_result.insert("0", round(result))
            else:
                self.entry_result.delete("0", "end")
                self.entry_result.insert("0", round(result, 2))
        except ValueError:
            self.entry_massage("Введите корректную стоимость")
            self.label_and_entry_frame.entry_cost.focus()

    def add_object(self):
        name, cost = self.label_and_entry_frame.get()
        parameters = self.checkbox_frame.get()
        if name and cost:
            self.cursor.execute("INSERT INTO list_of_car VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (self.random_id(), name, cost, *parameters))
            self.database.commit()
            self.update_textbox_list_of_car()
            self.entry_massage("Запись добавлена")
        else:
            self.entry_massage("Введите название и стоимость")
            self.label_and_entry_frame.entry_name.focus()

    def check_object(self):
        try:
            car_id = int(self.entry_result.get())
            if self.check_id(car_id):
                self.cursor.execute(f"SELECT * FROM list_of_car WHERE car_id = {car_id}")
                car_object = self.cursor.fetchall()[0]
                name, cost = car_object[1:3]
                parameters = car_object[3:]
                self.label_and_entry_frame.set(name, cost)
                self.checkbox_frame.set(parameters)
                self.calculate()
            else:
                self.entry_massage("Введите id из базы данных")
        except ValueError:
            self.entry_massage("Введите id")

    def delete_object(self):
        car_id = self.entry_result.get()
        if car_id == "<all>":
            self.cursor.execute(f"DELETE FROM list_of_car")
            self.database.commit()
            self.update_textbox_list_of_car()
            self.entry_massage("Записи удалены")
            return None
        try:
            if self.check_id(int(car_id)):
                self.cursor.execute(f"DELETE FROM list_of_car WHERE car_id = {car_id}")
                self.database.commit()
                self.update_textbox_list_of_car()
                self.entry_massage("Запись удалена")
            else:
                self.entry_massage("Введите id из базы данных")
        except ValueError:
            self.entry_massage("Введите id")

    def check_id(self, car_id):
        self.cursor.execute("SELECT car_id FROM list_of_car")
        if car_id in [el[0] for el in self.cursor.fetchall()]:
            return True
        else:
            self.entry_massage("Индекс не найден")
            return False

    def random_id(self):
        while True:
            car_id = round(random.triangular(0.1)*10**6)
            self.cursor.execute("SELECT car_id FROM list_of_car")
            if car_id in [el[0] for el in self.cursor.fetchall()]:
                continue
            else:
                return car_id

    def update_textbox_list_of_car(self):
        self.textbox_list_of_cars.configure(state="normal")
        self.textbox_list_of_cars.delete("0.0", "end")
        self.cursor.execute("SELECT * FROM list_of_car")
        for car_object in self.cursor.fetchall():
            self.textbox_list_of_cars.insert("end", "(id {0}) {1} {2}руб\n".format(*car_object[:3]))
        self.textbox_list_of_cars.configure(state="disabled")

    def entry_massage(self, text):
        self.entry_result.delete("0", "end")
        self.entry_result.configure(placeholder_text=text)
        self.textbox_list_of_cars.focus()


app = App()
app.mainloop()
