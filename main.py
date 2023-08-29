from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle, Color

import time

class Board(RelativeLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.size_hint = (1, 0.8)
        self.pos_hint ={'x':0.025, 'y':0.15}

class MyApp(App):
    def build(self):
        self.num_rows = 6
        self.num_cols = 6
        self.num_plays = 0
        self.num_elem = self.num_cols*self.num_rows
        self.player = 'X'
        self.red = (1, 0.1, 0.1)
        self.yellow = (0.9, 0.8, 0.1)
        self.purple = (0.9, 0.1, 0.8)

        self.player_color = self.red # X is red

        self.sigue_juego = True
        self.winner = ''

        screen = RelativeLayout()
        self.col_buttons = []
        
        b1 = Button(text='1', pos_hint= {'x':0.05,'y': 0.05}, size_hint=(0.1,0.1), background_color=self.red )
        b2 = Button(text='2', pos_hint= {'x':0.21,'y': 0.05}, size_hint=(0.1,0.1), background_color=self.red )
        b3 = Button(text='3', pos_hint= {'x':0.37,'y': 0.05}, size_hint=(0.1,0.1), background_color=self.red )
        b4 = Button(text='4', pos_hint= {'x':0.53,'y': 0.05}, size_hint=(0.1,0.1), background_color=self.red )
        b5 = Button(text='5', pos_hint= {'x':0.69,'y': 0.05}, size_hint=(0.1,0.1), background_color=self.red )
        b6 = Button(text='6', pos_hint= {'x':0.85,'y': 0.05}, size_hint=(0.1,0.1), background_color=self.red )

        self.col_buttons.append(b1)
        self.col_buttons.append(b2)
        self.col_buttons.append(b3)
        self.col_buttons.append(b4)
        self.col_buttons.append(b5)
        self.col_buttons.append(b6)

        screen.add_widget(b1)
        screen.add_widget(b2)
        screen.add_widget(b3)
        screen.add_widget(b4)
        screen.add_widget(b5)
        screen.add_widget(b6)

        b1.bind(on_press=lambda *args: self.juego(1-1, *args))
        b2.bind(on_press=lambda *args: self.juego(2-1, *args))
        b3.bind(on_press=lambda *args: self.juego(3-1, *args))
        b4.bind(on_press=lambda *args: self.juego(4-1, *args))
        b5.bind(on_press=lambda *args: self.juego(5-1, *args))
        b6.bind(on_press=lambda *args: self.juego(6-1, *args))
        
        self.tiles = []
        self.t_color =(0, 1, 0.5)
        board = Board()
        for j in range(6):
            for i in range(6):
                b = Button(text='', background_color=self.t_color, pos_hint= {'x': i*0.16,'y': j*0.16}, size_hint=(0.16,0.16), disabled= 'True')
                self.tiles.append(b)   

        for t in self.tiles:        
            board.add_widget(t)
        
        screen.add_widget(board)

        return screen        

    def juego(self, col, event):
        
        # ver si columna esta llena y mete ficha si lo esta
        llena = self.meter_ficha(col)
        self.num_plays += 1
        if llena:
            pass
        else:
            #cambiar_turno
            self.player = 'O' if self.player == 'X' else 'X'
            self.player_color = self.red if self.player == 'X' else self.yellow
            for b in self.col_buttons:
                b.background_color = self.player_color
            if self.winner != '':
                time.sleep(1)
                self.resetar()
            self.hay_ganador()
                
        ### fin juego ###

    def meter_ficha(self, col):
        isFull =True
        i = 0
        while i < self.num_rows and isFull:
            pos = i*self.num_cols+col
            if self.tiles[pos].text == '':
                self.tiles[pos].color = self.player_color
                self.tiles[pos].text = self.player
                isFull = False
            i +=1
        return isFull
            

    def resetar(self):
        self.player = 'X'
        self.player_color = self.red # X is red
        self.num_plays = 0
        self.sigue_juego = True
        self.winner = ''
        for t in self.tiles:
            t.text = ''
            t.background_color = self.t_color

    def hay_empate(self):
        empate = True
        i = 0
        while not empate and i < self.num_cols:
            pos = (self.num_rows-1)*self.num_cols+i
            if self.tiles[pos] == '':
                empate = False
            i+=1
        return empate


    def hay_ganador(self):
        self.sigue_juego = self.fcolumns() or self.frows() or self.fdiag()
        empate =False
        if self.num_plays >= self.num_elem:
            empate = self.hay_empate()
        if self.sigue_juego or empate:
            self.player = 'O' if self.player == 'X' else 'X'
            self.player_color = self.red if self.player == 'X' else self.yellow
            self.winner = self.player
            if empate:
                content = Button(text='Hubo un Empate !!')
            else:
                content = Button(text=f'{self.winner} gana !!')
            
            content.background_color = (1, 0, 0, 0.5)
            self.pop = Popup(title='Fin de Juego', content=content)
            self.pop.size_hint = (0.5,0.5)
            self.pop.pos_hint = {'x':0.25, 'y':0.25} 
            
            self.pop.open()
            content.bind(on_press=self.pop.dismiss)

    
    def fcolumns(self):
        # fija si hay 4 en vertical
        hay4fila = False
        i = 0
        while i <self.num_cols and not hay4fila:
            j = 0
            while j <= self.num_rows- 4 and not hay4fila:
                pos = j*self.num_cols+i
                if self.tiles[pos].text != '':
                    hay4fila = self.tiles[pos].text == self.tiles[pos+self.num_cols].text and  self.tiles[pos].text == self.tiles[pos+2*self.num_cols].text and  self.tiles[pos].text == self.tiles[pos+3*self.num_cols].text
                    if hay4fila:
                        for i in range(4):
                            self.tiles[pos+self.num_cols*i].background_color = self.purple
                j+=1
            i+=1    
        
        
        return hay4fila

    def frows(self):
        # fija si hay 4 en fila
        hay4fila = False
        i = 0
        while i <= self.num_cols-4 and not hay4fila:
            j = 0
            while j < self.num_rows and not hay4fila:
                pos = j*self.num_cols+i
                if self.tiles[pos].text != '':
                    hay4fila = self.tiles[pos].text == self.tiles[pos+1].text and  self.tiles[pos].text == self.tiles[pos+2].text and  self.tiles[pos].text == self.tiles[pos+3].text
                    if hay4fila:
                        for i in range(4):
                            self.tiles[pos+i].background_color = self.purple
                j+=1
            i+=1    
        return hay4fila
        

    def fdiag(self):
        return self.diag1() or self.diag2()
    
    def diag1(self):
        # fija si hay 4 en diagonal positiva
        hay4fila = False
        i = 0
        while i <= self.num_cols-4 and not hay4fila:
            j = 0
            while j <= self.num_rows-4 and not hay4fila:
                pos = j*self.num_cols+i
                if self.tiles[pos].text != '':
                    hay4fila = self.tiles[pos].text == self.tiles[pos+self.num_cols+1].text and  self.tiles[pos].text == self.tiles[pos+2*(self.num_cols+1)].text and  self.tiles[pos].text == self.tiles[pos+3*(self.num_cols+1)].text
                    if hay4fila:
                        for i in range(4):
                            self.tiles[pos+(self.num_cols+1)*i].background_color = self.purple
                j+=1
            i+=1
        return hay4fila
    
    def diag2(self):
        # fija si hay 4 en diagonal negativa
        hay4fila = False
        i = 0
        while i <= self.num_cols-4 and not hay4fila:
            j = 3 ## start at 4th row
            while j < self.num_rows and not hay4fila:
                pos = j*self.num_cols+i
                if self.tiles[pos].text != '':
                    hay4fila = self.tiles[pos].text == self.tiles[pos-self.num_cols+1].text and  self.tiles[pos].text == self.tiles[pos-2*(self.num_cols-1)].text and  self.tiles[pos].text == self.tiles[pos-3*(self.num_cols-1)].text
                    if hay4fila:
                        for i in range(4):
                            self.tiles[pos-(self.num_cols-1)*i].background_color = self.purple
                j+=1
            i+=1
        return hay4fila

if __name__ == '__main__':
    MyApp().run()
