import random
import numpy as np

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.config import Config
Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "400")
Config.set("graphics", "height", "500")

choice = ["X", "O"]
switch = 0


def make_list(matrix, array):
    if array:
        array.clear()  # чтобы не залетел не пустой список
    for lst in matrix:
        for i in range(6):
            array.append(lst[i:i + 5])


def make_diagonal():
    #  Создаем список диагоналей (A->D, C->B) через numpy, где A,B,C,D -это вершины квадрата
    x, y, coordinate_d, a = 10, 10, [], []
    a = np.arange(x * y).reshape(x, y)
    diags = [a[::-1, :].diagonal(i) for i in range(-a.shape[0] + 1, a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1] - 1, -a.shape[0], -1))
    temp = [n.tolist() for n in diags]
    # Сохраняем только те диагонали, длинна которых больше/равна пяти.
    for item in temp:
        if len(item) >= 5:
            coordinate_d.append(item)
    #  Очищаем список temp, создаем в него копию списка coordinate_d и освобождаем переменную под итоговый список
    temp.clear()
    temp = coordinate_d.copy()
    coordinate_d.clear()
    # Создаем итоговый список win диагоналей
    for item in temp:
        if len(item) == 5:
            coordinate_d.append(item)
        else:
            for i in range(len(item) - 4):
                coordinate_d.append(item[i:i + 5])
    return coordinate_d


def make_coordinate_x():
    coordinate_x = []
    make_list(make_matrix(), coordinate_x)
    return coordinate_x


def make_coordinate_y():
    coordinate_y, temp = [], []
    matrix = make_matrix()
    # переворачиваю матрицу для взятия среза, можно переделать через numpy
    for y in range(10):
        for x in range(10):
            coordinate_y.append(matrix[x][y])
    for i in coordinate_y[:10]:
        temp.append(coordinate_y[i:i + 10])
    make_list(temp, coordinate_y)
    return coordinate_y


def make_matrix():
    x, y = 10, 10
    # Создаю матрицу 10*10, для вычисления списков win индексов
    matrix = np.arange(x * y).reshape(x, y)
    matrix = [n.tolist() for n in matrix]
    return matrix


class TickTackToe(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index_list = [i for i in range(100)]
        self.lose = False
        self.loser = ""

        self.matrix = make_matrix()
        self.coordinate_d = make_diagonal()  # win список по оси D
        self.coordinate_x = make_coordinate_x()  # win список по оси X
        self.coordinate_y = make_coordinate_y()  # win список по оси Y

    def get_random_index(self):
        """
        Рекурсивный метод, который возвращает рандомный index свободной кнопки
        """
        index = random.choice(self.index_list)
        if self.button[index].text == "":
            return index
        else:
            self.index_list.pop(self.index_list.index(index))
            return self.get_random_index()

    def tic_tac_toe(self, arg):
        """
        Logic
        """
        global switch

        arg.disabled = True
        arg.text = choice[switch]

        color = [1, 0, 0, 1]  # Red
        coordinate_x = self.coordinate_x
        coordinate_y = self.coordinate_y
        coordinate_d = self.coordinate_d
        all_list = coordinate_x + coordinate_y + coordinate_d
        win_vector = []

        if not switch:
            switch = 1
            index = self.get_random_index()  # случайный элемент
            self.button[index].text = choice[switch]
            self.button[index].disabled = True
            self.index_list.pop(self.index_list.index(index))
            switch = 0

        for i in range(60):
            win_vector.append([self.button[x].text for x in coordinate_x[i]])
        for j in range(60):
            win_vector.append([self.button[y].text for y in coordinate_y[j]])
        for k in range(72):
            win_vector.append([self.button[d].text for d in coordinate_d[k]])

        for index in range(192):
            if win_vector[index].count("X") == 5 \
                    or win_vector[index].count("O") == 5:
                self.lose = True
                for s in all_list[index]:
                    self.button[s].color = color
                    self.loser = self.button[s].text

        if self.lose:
            for index in range(100):
                self.button[index].disabled =True
            self.create_popup()

    def start_button(self, *args):
        self.btn_start.disabled = True
        for index in range(100):
            self.button[index].disabled = False

    def create_popup(self):
        self.popup = Popup(title='Result',
                      content=Label(text=f'Loser is {self.loser}'),
                      size_hint=(.4, .4))
        self.popup.open()

    def build(self):
        self.title = "Tick Tac Toe"
        self.root = BoxLayout(orientation="vertical", padding=[15, 10, 15, 25], spacing=5)
        self.grid_top = GridLayout(orientation="lr-tb", cols=1, spacing=8, size_hint=(1, .1))
        self.btn_start = Button(text="Start", size_hint=(.1, .2), on_press=self.start_button)
        self.grid_top.add_widget(self.btn_start), self.root.add_widget(self.grid_top)
        self.grid_center = GridLayout(orientation="lr-tb", cols=10, rows=10, spacing=2, padding=[0, 15, 0, 0])

        self.button = [0 for _ in range(100)]
        for index in range(100):
            self.button[index] = Button(
                color=[0, 0, 0, 1],
                font_size=20,
                disabled=True,
                text="",
                on_press=self.tic_tac_toe
            )
            self.grid_center.add_widget(self.button[index])
        self.root.add_widget(self.grid_center)
        return self.root


if __name__ == "__main__":
    TickTackToe().run()
