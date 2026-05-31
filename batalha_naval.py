import os
from random import randint
from time import sleep

tabuleiroFeedbackJogador = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

tabuleiroFeedbackComputador = [
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0]
]

tabuleiroJogador = [
    ['@',1,2,3,4,5,6,7,8,9,10],
    ['A',0,0,0,0,0,0,0,0,0,0],
    ['B',0,0,0,0,0,0,0,0,0,0],
    ['C',0,0,0,0,0,0,0,0,0,0],
    ['D',0,0,0,0,0,0,0,0,0,0],
    ['E',0,0,0,0,0,0,0,0,0,0],
    ['F',0,0,0,0,0,0,0,0,0,0],
    ['G',0,0,0,0,0,0,0,0,0,0],
    ['H',0,0,0,0,0,0,0,0,0,0],
    ['I',0,0,0,0,0,0,0,0,0,0],
    ['J',0,0,0,0,0,0,0,0,0,0]
]

tabuleiroComputador = [
    ['@',1,2,3,4,5,6,7,8,9,10],
    ['A',0,0,0,0,0,0,0,0,0,0],
    ['B',0,0,0,0,0,0,0,0,0,0],
    ['C',0,0,0,0,0,0,0,0,0,0],
    ['D',0,0,0,0,0,0,0,0,0,0],
    ['E',0,0,0,0,0,0,0,0,0,0],
    ['F',0,0,0,0,0,0,0,0,0,0],
    ['G',0,0,0,0,0,0,0,0,0,0],
    ['H',0,0,0,0,0,0,0,0,0,0],
    ['I',0,0,0,0,0,0,0,0,0,0],
    ['J',0,0,0,0,0,0,0,0,0,0]
]

tamanhoBarco = 5
letrasLinhas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

for i in range (5):
    for c in range (11):
        print (tabuleiroJogador[c])

    letraRow = input(f"Digite a linha de onde quer colocar o barco de tamanho {tamanhoBarco}: ")
    if letraRow in letrasLinhas:
        rowBarco = letrasLinhas.index(letraRow) + 1

    columBarco = int(input(f"Digite a coluna de onde quer colocar o barco de tamanho {tamanhoBarco}: "))
    orientacaoBarco = input(f"Digite a orientação do barco V ou H: ")
    for j in range(tamanhoBarco):
        tabuleiroJogador[rowBarco] [columBarco] = '■'
        if orientacaoBarco == 'V':
            rowBarco += 1
        else:
            columBarcoBarco += 1
    tamanhoBarco -= 1

os.system('cls' if os.name == 'nt' else 'clear')