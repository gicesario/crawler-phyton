from datetime import date
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Jira:

  # Descrição do ticket JS-117
  descJS_117 = 'Atividade alocada através de robô:'
  # Descrição do ticket JS-1
  descJS_1 = 'Atividade alocada através de robô' 
  # Descrição do chamado
  descChamado = 'Atividade alocada através de robô' 
  # Ticket para alocar as reuniões
  ticketReunioes = "'JS-117'"
  # Ticket para alocar horas ociosas (descompressão, café, etc)
  ticketShared = "'JS-12'"
  # Ticket para alocar horas no chamado
  ticketChamado = "''"  

  # Formatação das horas 
  formato = '%H:%M'
    
  def __init__(self, driver, data, entrada1, hrsTrabalhadas, tempoJS1, tempoJS117):
    self.driver = driver    
    self.data = data
    self.entrada1 = entrada1 # primeira entrada do dia
    self.hrsTrabalhadas = hrsTrabalhadas # horas trabalhadas obtidas o sistema de pontos       
    self.tempoJS1 = tempoJS1 # Tempo para alocar no Ticket JS-1 (Minutos em outras atividades)
    self.tempoJS117 = tempoJS117 # Tempo para alocar no Ticket JS-117 (Minutos em reuniões)  

  def abrirPagina(self):    
    print('Abrindo Jira')  
    self.driver.get("https://jira.sinqia.com.br/secure/Tempo.jspa#/my-work/week?type=LIST")
    self.efetuarLogin()

  def efetuarLogin(self):
    print('Efetuando Login')
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "login-form-username"))).send_keys("#")
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, "login-form-password"))).send_keys("#")
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'login-form-submit'))).click()
    
  def abrirMeuTempo(self):      
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'tempo_menu'))).click()
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'timesheet-mlink_lnk'))).click()

  def abrirLogTime(self):    
    self.abrirMeuTempo()          
    elemCardHoje = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, str(self.data))))
    elemLogTime = elemCardHoje.find_elements_by_xpath(".//div[@class='sc-jhaWeW KIewe']")
    for elem in elemLogTime:
      self.driver.execute_script("arguments[0].click();", elem)

  def enviarDadosLogTime(self, nomeTicket, descricao, inicio, duracao):
    print('Abre form para alocar ticket: ' + str(nomeTicket))
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'issuePickerInput'))).send_keys(str(nomeTicket))
    # pega os inputs 
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sc-kfGgVZ gWpuUj']"))).click()
    elemHrIni = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'from'))) # From   
    elemHrDuracao = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'timeSpentSeconds'))) # Worked
    # adiciona descrição da atividade
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.ID, 'comment'))).send_keys(str(descricao)) #    
    # adiciona hora inicial
    elemHrIni.click
    elemHrIni.send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    elemHrIni.send_keys(str(inicio) + Keys.TAB)     
    # adiciona tempo decorrido
    elemHrDuracao.click
    elemHrDuracao.send_keys(Keys.CONTROL + "a" + Keys.DELETE)
    elemHrDuracao.send_keys(str(duracao)+ Keys.TAB)    
    # faz o envio dos dados
    WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//button[@name='submitWorklogButton']"))).click()

  def alocarTicketJS117(self):   
    self.abrirLogTime()  
    self.enviarDadosLogTime(self.ticketReunioes, self.descJS_117, self.entrada1, str(self.tempoJS117)+'m')
    
  def alocarTicketJS1(self):   
    self.abrirLogTime()  
    # As horas no ticket JS-1 são alocadas após o JS-117
    inicioJS1 = (datetime.strptime(self.entrada1, self.formato) + timedelta(minutes=int(self.tempoJS117))).strftime(self.formato) 
    self.enviarDadosLogTime(self.ticketShared, self.descJS_1, inicioJS1, str(self.tempoJS1)+'m')

  def alocarTicketChamado(self):
    self.abrirLogTime()  
    # As horas no chamado são alocadas logo após os JS-1
    inicioChamado = ((datetime.strptime(self.entrada1, self.formato)) + (timedelta(minutes=int(self.tempoJS1) + int(self.tempoJS117)))).strftime(self.formato) 
    duracaoDesconto = datetime.strptime(str(timedelta(minutes=int(self.tempoJS1)) + timedelta(minutes=int(self.tempoJS117))), '%H:%M:%S' )
    duracaoChamado = datetime.strptime(str((datetime.strptime(self.hrsTrabalhadas, self.formato) - duracaoDesconto)), '%H:%M:%S')
    self.enviarDadosLogTime(self.ticketChamado, self.descChamado, str(inicioChamado), (duracaoChamado.strftime(self.formato)).replace(":", "h")+'m')

  def alocarHorasHoje(self):   
    self.alocarTicketJS117()
    self.alocarTicketJS1()
    self.alocarTicketChamado()
 

