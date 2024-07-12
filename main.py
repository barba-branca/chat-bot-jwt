from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # Obtenha a mensagem receboida
    incoming_msg = request.form.get('Body')
    
    # Crie uma resposta TwiML
    resp = MessagingResponse()
    msg = resp.message()
    
    # Defina a mensagem de responta
    response_text = 'Obrigado pela sua mensagem no whatsApp! Você disse:' + incoming_msg
    msg.bory(response_text)
    
    return str(resp)
    
if __name__ == "__main__":
    app.run(debug=True)