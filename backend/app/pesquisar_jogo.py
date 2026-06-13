import os
import pyautogui as auto
from time import sleep
from color.cores import *

navegador = "Google Chrome"
mensagem = "Jogos da Copa na data de hoje"

os.system(f"open -a '{navegador}'")
sleep(0.9)
auto.press("enter")

auto.write(f"{mensagem}")
sleep(0.5)
auto.press("enter")

print(f"\n{CinzaClaro}Seguem os Jogos da {Reset}{Verde}Copa do Mundo 🏆{Reset}{CinzaClaro} de Hoje{Reset} {Amarelo}no seu navegador!!{Reset}\n")