import scrapy
from datetime import date
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Ponto:
  # imprime o período selecionado o sistema
  periodo = ''
  batidaHoras = []
  primeiraEntrada = ''
  formato = '%H:%M'

  def __init__(self, driver, dia):
    self.driver = driver
    self.dia = dia

  def abrirPagina(self):    
    print('Abrindo Meu RH')
    self.driver.get("http://meurh.sinqia.com.br:8099/01/#/login")
    
  def efetuarLogin(self):
    print('Efetuando Login')
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='user']"))).send_keys("#")
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))).send_keys("#")
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.po-button-label'))).click()

  def abrirEspelhoPonto(self):    
    self.efetuarLogin()
    print("Abrindo espelho de ponto")
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()=' Ponto ']"))).click()
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='#/timesheet/clockings']"))).click()
    elemPeriodo = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.po-select-button')))
    self.periodo = str(elemPeriodo.text)
    print('Período atual: ' + self.periodo)        
    print('Dia..........: ' + self.dia)

  def obterBatidasDia(self):
    self.abrirEspelhoPonto()
    # Seleciona a tabela com todos os dias do mEs    
    diasTabela = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
    # Varre tabela dos dias até encontrar a data desejada
    for i in range(len(diasTabela)):
      if (str(diasTabela[i].text).startswith(str(self.dia))):
        return diasTabela[i].text.replace('\n', '')
  
  def obterHorasHoje(self):    
    batidasComData = self.obterBatidasDia()
    # Varre registro das batidas para encontrar somente as horas
    for i in range(len(batidasComData)):
      if (batidasComData[i] == ':'):
        self.batidaHoras.append(batidasComData[i-2] + batidasComData[i-1] + ":" + batidasComData[i+1] + batidasComData[i+2]) 
  
  def calcularHorasTrabalhadas(self):       
    self.obterHorasHoje()  
    print('Calculando horas trabalhadas')
    # Calcula horas trabalhadas: (S1-E1) + (S2-E2)
    horasTrabalhadas = datetime.strptime(str((datetime.strptime(self.batidaHoras[2], self.formato) - datetime.strptime(self.batidaHoras[0], self.formato)) + (datetime.strptime(self.batidaHoras[3], self.formato) - datetime.strptime(self.batidaHoras[1], self.formato))), '%H:%M:%S')
    self.primeiraEntrada = self.batidaHoras[0]     
    print('E1: ' + self.batidaHoras[0])
    print('S1: ' + self.batidaHoras[2])
    print('E2: ' + self.batidaHoras[1])
    print('S2: ' + self.batidaHoras[3])
    print('Horas trabalhadas: ' + horasTrabalhadas.strftime(self.formato))
    return horasTrabalhadas.strftime(self.formato)
      
  def obterPrimeiraEntrada(self):
    return str(self.primeiraEntrada)

  def validaPeriodo(self):
    return (str(self.dia[2:5]) in str(self.periodo))