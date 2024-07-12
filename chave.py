from twilio import Client

# Adcionando credenciais do teilio
account_sid = 'your_account_sid'
auth_token ='your_auth_token'
client = Client(account_sid, auth_token)

# Enviar mensagem pelo Whatsapp
message = client.mansagem.create(
    drom_='whatsapp : +12513091864', # Número do WhatisApp do twilio
    body = 'Olá, esta é uma mwsagem wnviada pelo Twilio via Whatsapp ',
    to = 'whatsapp:+5562986279544' #numero de destino com o codigo do pais
)

print(message.sid)