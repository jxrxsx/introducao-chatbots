#importando bibliotecas
import requests
import json
import os

class TelegramBot:

  def __init__(self):
    self.botToken = '1682477468:AAHJROORxslHpcTUrwpKSquiVlJZyo8Cyfk'
    self.url_base = f'https://api.telegram.org/bot{self.botToken}'
    
  def Start(self):
    update_id = None
    while True:
      atualizacao = self.newMessages(update_id)
      dados = atualizacao["result"]
      if dados:
        for dado in dados:
          update_id = dado["update_id"]
          mensagem = str(dado["message"]["text"])
          chat_id = dado["message"]["from"]["id"]
          primeira_mensagem = int(dado["message"]["message_id"]) == 1
          resposta = self.criarRespostas(mensagem, primeira_mensagem)
          self.responder(resposta, chat_id)

  #receber mensagens
  def newMessages(self, update_id):
    link_requisicao = f'{self.url_base}/getUpdates?timeout=1000'
    if update_id:
      link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
    result = requests.get(link_requisicao)
    return json.loads(result.content)
  
  #criar as respostas das mensagens
  def criarRespostas(self, mensagem, primeira_mensagem):
    if primeira_mensagem == True or mensagem in('menu', 'Menu'):
      return f'Salve quebrada! Cardápio do dia tem: {os.linesep}1 - Mac de 10 {os.linesep}2 - Shake de 5'

    if mensagem == '1':
      return f'O valor do Mac de 10 é: R$ 10{os.linesep}\n Confirmar pedido? (s/n)'
    elif mensagem == '2':
      return f'O valor do Shake de 5 é: R$ 5{os.linesep}\n Confirmar pedido? (s/n)'

    elif mensagem.lower() in ('s', 'sim', 'Sim'):
      return 'Pedido confirmado com sucesso! Já já chega aí '
    elif mensagem.lower() in ('n', 'não', 'Não'):
      return 'Dmr então, vacilão! Sei onde vc mora... Digite "menu" para retornar ao Menu'

    else:
      return 'Gostaria de acessar o Menu? Digite "menu" para retornar ao Menu'



  #responder pessoas
  def responder(self, resposta, chat_id):
    link_requisicao = f'{self.url_base}/sendMessage?chat_id={chat_id}&text={resposta}'
    requests.get(link_requisicao)


bot = TelegramBot()
bot.Start()
