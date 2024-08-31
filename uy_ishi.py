from random import shuffle

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget,
    QPushButton, 
    QGridLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)

class Button(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(100,100)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #F3FF90;
                font-size: 36px;
                padding: 8px;
                border-radius: 16px;
                border: none;
                color: #7C00FE;
            }}
            QPushButton:hover {{
                background-color: #7C00FE;
                font-size: 46px;
                border: 2px solid "#bc8f5b";
                color: #F9E400;
            }}
        """)

class Puzzle(QWidget):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.matrix = list()
        self.setStyleSheet("background-color: #059212")
        numbers = self.create_numbers()
        
        self.movescounter = 0
        self.time_on_off = False
        self.origin_matrix = list(map(str,range(1,self.size**2))) + [' ']

        self.grid = QGridLayout()

        index = 0
        for i in range(self.size):
            row = list()
            for j in range(self.size):
                btn = Button(numbers[index])
                self.grid.addWidget(btn, i,j)
                row.append(btn)
                if numbers[index] == " ":
                    btn.hide()
                index+=1
                btn.clicked.connect(self.change_position)
            self.matrix.append(row)

        self.timer_label = QLabel()
        self.timer_label.setText(f'Time: {0}')
        self.timer_label.setStyleSheet('font-size: 25px')

        self.moves_label = QLabel()
        self.moves_label.setText(f'Moves: {0}')
        self.moves_label.setStyleSheet('font-size: 25px')

        self.h_box_upper = QHBoxLayout()
        self.h_box_upper.addWidget(self.timer_label)
        self.h_box_upper.addStretch(10)
        self.h_box_upper.addWidget(self.moves_label)

        self.restart_btn = QPushButton('Restart')
        self.restart_btn.setFixedSize(100,50)
        self.restart_btn.setStyleSheet("""
            QPushButton {
                font-size: 25px;
                background-color: #7C00FE;
                color: white
            }
            QPushButton:hover {
                font-size: 30px;
                background-color: red;
                color: white
            }
        """)
        
        self.restart_btn.pressed.connect(self.restart_game)

        self.pause_btn = QPushButton('Pause')
        self.pause_btn.setFixedSize(100,50)
        self.pause_btn.setCheckable(True)
        self.pause_btn.setStyleSheet("""
                QPushButton {
                    font-size: 25px;
                    background-color: #7C00FE;
                    color: white
                }
                QPushButton:hover {
                    font-size: 30px;
                    background-color: red;
                    color: white
                }
            """)

        self.set_timer()

        self.pause_btn.clicked.connect(self.pause_screen)

        self.h_box_bottom = QHBoxLayout()
        self.h_box_bottom.addWidget(self.restart_btn)
        self.h_box_bottom.addWidget(self.pause_btn)

        self.v_box = QVBoxLayout()
        self.v_box.addLayout(self.h_box_upper)
        self.v_box.addSpacing(20)
        self.v_box.addLayout(self.grid)
        self.v_box.addSpacing(20)
        self.v_box.addLayout(self.h_box_bottom)

        self.setLayout(self.v_box)

    def create_numbers(self):
        numbres = list(map(str,range(1, self.size**2))) + [" "]
        shuffle(numbres)
        return numbres

    def change_position(self):
        if not self.time_on_off:
            self.set_timer()
            self.time_on_off = True

        btn = self.sender()
        for x in range(self.size):
            for y in range(self.size):
                if btn.text() == self.matrix[x][y].text():
                    if x > 0 and self.matrix[x-1][y].text() == ' ':
                        text = btn.text()
                        btn.hide()
                        self.matrix[x-1][y].setText(text)
                        btn.setText(' ')
                        self.matrix[x-1][y].show()
                        self.updatemoves()
                    elif x+1 < self.size and self.matrix[x+1][y].text() == ' ':
                        text = btn.text()
                        btn.hide()
                        self.matrix[x+1][y].setText(text)
                        btn.setText(' ')
                        self.matrix[x+1][y].show()
                        self.updatemoves()
                    elif y > 0 and self.matrix[x][y-1].text() == ' ':
                        text = btn.text()
                        btn.hide()
                        self.matrix[x][y-1].setText(text)
                        btn.setText(' ')
                        self.matrix[x][y-1].show()
                        self.updatemoves()
                    elif y+1 < self.size and self.matrix[x][y+1].text() == ' ':
                        text = btn.text()
                        btn.hide()
                        self.matrix[x][y+1].setText(text)
                        btn.setText(' ')
                        self.matrix[x][y+1].show()
                        self.updatemoves()
                    self.check_btn_place(x,y)


    def check_btn_place(self,x: int,y: int) -> None:
        if self.matrix[x][y].text() == self.origin_matrix[x*self.size + y]:
            self.matrix[x][y].setStyleSheet('color: orange')

    def set_timer(self):
        self.count = 0
        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_timer)
    
    def update_timer(self):
        self.count+=1
        self.timer_label.setText(f'Time: {self.count}')

    def updatemoves(self):
        self.movescounter+=1
        self.moves_label.setText(f'Move: {self.movescounter}')

    def pause_screen(self):
        if self.pause_btn.isChecked():
            for i in self.matrix:
                for j in i:
                    j.setEnabled(False)
            self.timer.stop()
        else:
            for i in self.matrix:
                for j in i:
                    j.setEnabled(True)
            self.timer.start()

    def restart_game(self):
        self.close()
        self.game = Puzzle(4)
        self.game.show()

def main():
    app = QApplication([])
    puzzle = Puzzle(4)
    puzzle.show()
    app.exec_()

if __name__ == '__main__':
    main()