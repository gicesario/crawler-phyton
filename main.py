import os
from ponto import Ponto
from jira import Jira
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from datetime import datetime

driver = webdriver.Chrome('C:/Users/Gisela/Desktop/python/robo_alocacao_horas/chromedriver/chromedriver')
driver.maximize_window()
os.system('cls')

# Obtém as datas automaticamente
# Informa as datas manualmente:

print('Dia (DD/MM): ')
dia = str(input())
data = str('2020-' + str(dia)[3:5] + '-' + str(dia)[0:2]) 

p = Ponto(driver, str(dia))
p.abrirPagina()
hrsTotal = p.calcularHorasTrabalhadas()

if (p.validaPeriodo()):
  driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')  
  # Tempo para alocar no Ticket JS-1 (Minutos em outras atividades)
  print('Minutos em JS-1 (Shared): ')
  tempoJS1 = int(input())
  # Tempo para alocar no Ticket JS-117 (Minutos em reuniões)  
  print('Minutos em JS-117 (Reunioes): ')
  tempoJS117 = int(input())  
  # abre a aba do jira
  j = Jira(driver, str(data), p.obterPrimeiraEntrada(), hrsTotal, tempoJS1, tempoJS117)
  j.abrirPagina()
  j.alocarHorasHoje()
else:
  print('Não foi encontrado o período desejado no Meu RH')
