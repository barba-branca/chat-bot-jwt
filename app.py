from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# Cardápio com preços
cardapio = {
    '1': {'nome': 'Margherita: molho de tomate, mozarela, tomate e manjericão fresco', 'preco': 25.00},
    '2': {'nome': 'Pepperoni: molho de tomate, mozarela e pepperoni fatiado', 'preco': 30.00},
    '3': {'nome': 'Quatro Queijos: molho de tomate, mozarela, parmesão, gorgonzola e provolone', 'preco': 35.00},
    '4': {'nome': 'Calabresa: molho de tomate, mozarela, calabresa fatiada e cebola', 'preco': 28.00},
    '5': {'nome': 'Frango com Catupiry: molho de tomate, frango desfiado, catupiry e mozarela', 'preco': 32.00},
    '6': {'nome': 'Portuguesa: molho de tomate, mozarela, presunto, ovos, cebola, pimentão e azeitonas', 'preco': 33.00},
    '7': {'nome': 'Pizza Vegetariana: molho de tomate, mozarela, abobrinha, berinjela, pimentão, cebola e tomate', 'preco': 29.00},
    '8': {'nome': 'Pizza de Rúcula com Tomate Seco: molho de tomate, mozarela, rúcula, tomate seco e parmesão', 'preco': 34.00},
    '9': {'nome': 'Pizza Carbonara: molho branco, mozarela, bacon, ovos e parmesão', 'preco': 36.00},
    '10': {'nome': 'Pizza de Camarão: molho de tomate, mozarela, camarão, catupiry e cebola', 'preco': 40.00},
    '11': {'nome': 'Pizza Caprese: molho de tomate, mozarela de búfala, tomate fresco, manjericão e azeitonas pretas', 'preco': 35.00},
    '12': {'nome': 'Pizza de Chocolate com Morango: chocolate derretido, morangos fatiados e leite condensado', 'preco': 28.00},
    '13': {'nome': 'Pizza de Banana com Canela: bananas fatiadas, açúcar e canela', 'preco': 26.00},
    '14': {'nome': 'Pizza Romeu e Julieta: goiabada derretida com queijo mozarela', 'preco': 27.00},
    '15': {'nome': 'Coca-Cola', 'preco': 5.00},
    '16': {'nome': 'Guaraná', 'preco': 5.00},
    '17': {'nome': 'Sprite', 'preco': 5.00},
    '18': {'nome': 'Laranja', 'preco': 5.00},
    '19': {'nome': 'Maracujá', 'preco': 5.00},
    '20': {'nome': 'Uva', 'preco': 5.00}
}

# Função para exibir o cardápio de refrigerantes
def exibir_cardapio_refrigerantes():
    return '\n'.join([
        '\nRefrigerantes:',
        '15. Coca-Cola - R$ 5.00',
        '16. Guaraná - R$ 5.00',
        '17. Sprite - R$ 5.00'
    ])

# Função para exibir o cardápio de sucos
def exibir_cardapio_suco():
    return '\n'.join([
        '\nSucos:',
        '18. Laranja - R$ 5.00',
        '19. Maracujá - R$ 5.00',
        '20. Uva - R$ 5.00'
    ])

# Variáveis globais para armazenar o estado da conversa
user_state = {}

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Responder a mensagens SMS com um chatbot."""
    logging.debug("Recebido uma mensagem")
    logging.debug(f"Dados da requisição: {request.form}")

    incoming_msg = request.form.get('Body', '').strip().lower()
    from_number = request.form.get('From')
    logging.debug(f"Mensagem recebida: {incoming_msg} de {from_number}")

    resp = MessagingResponse()
    msg = resp.message()

    if from_number not in user_state:
        user_state[from_number] = {
            'step': 'welcome',
            'name': '',
            'order': [],
            'total': 0
        }

    user = user_state[from_number]
    logging.debug(f"Estado do usuário: {user}")

    if user['step'] == 'welcome':
        user['step'] = 'get_name'
        msg.body(f'Olá! Seja bem-vindo à Pizzaria do Gordinho. Meu nome é Norman, e estou aqui para agilizar seu atendimento. Qual é o seu nome?')
    elif user['step'] == 'get_name':
        user['name'] = incoming_msg
        user['step'] = 'menu'
        msg.body(f'Ok, {user["name"]}, irei te mandar o nosso cardápio. Digite o número da opção do menu a seguir para continuarmos:\n\n' + '\n'.join([f'{chave}. {item["nome"]} - R$ {item["preco"]:.2f}' for chave, item in list(cardapio.items())[:14]]))
    elif user['step'] == 'menu':
        if incoming_msg in cardapio and int(incoming_msg) <= 14:
            item_escolhido = cardapio[incoming_msg]
            user['order'].append(item_escolhido)
            user['total'] += item_escolhido['preco']
            user['step'] = 'ask_drink'
            msg.body(f'Você escolheu: {item_escolhido["nome"]} - R$ {item_escolhido["preco"]:.2f}\nVocê deseja adicionar uma bebida ao seu pedido? (sim/não)')
        else:
            msg.body('Opção inválida. Por favor, escolha uma opção válida do cardápio.')
    elif user['step'] == 'ask_drink':
        if incoming_msg in ['sim', 's']:
            user['step'] = 'drink_type'
            msg.body('Você gostaria de adicionar refrigerante ou suco? Digite "refrigerante" ou "suco".')
        elif incoming_msg in ['não', 'nao', 'n']:
            user['step'] = 'get_location'
            msg.body('Sem bebida adicionada. Por favor, informe sua localização para entrega:')
        else:
            msg.body('Não entendi sua resposta. Por favor, responda com "sim" ou "não".')
    elif user['step'] == 'drink_type':
        if incoming_msg == 'refrigerante':
            user['step'] = 'drink_menu'
            msg.body(exibir_cardapio_refrigerantes())
        elif incoming_msg == 'suco':
            user['step'] = 'juice_menu'
            msg.body(exibir_cardapio_suco())
        else:
            msg.body('Não entendi sua resposta. Por favor, escolha "refrigerante" ou "suco".')
    elif user['step'] == 'drink_menu':
        if incoming_msg in ['15', '16', '17']:
            bebida_escolhida = cardapio[incoming_msg]
            user['order'].append(bebida_escolhida)
            user['total'] += bebida_escolhida['preco']
            user['step'] = 'get_location'
            msg.body(f'Você escolheu: {bebida_escolhida["nome"]} - R$ {bebida_escolhida["preco"]:.2f}\nPor favor, informe sua localização para entrega:')
        else:
            msg.body('Opção de refrigerante inválida. Por favor, escolha uma opção válida.')
    elif user['step'] == 'juice_menu':
        if incoming_msg in ['18', '19', '20']:
            suco_escolhido = cardapio[incoming_msg]
            user['order'].append(suco_escolhido)
            user['total'] += suco_escolhido['preco']
            user['step'] = 'get_location'
            msg.body(f'Você escolheu: {suco_escolhido["nome"]} - R$ {suco_escolhido["preco"]:.2f}\nPor favor, informe sua localização para entrega:')
        else:
            msg.body('Opção de suco inválida. Por favor, escolha uma opção válida.')
    elif user['step'] == 'get_location':
        user['location'] = incoming_msg
        msg.body(f'O total do seu pedido é R$ {user["total"]:.2f}.\nSeu pedido será entregue em: {user["location"]}.\nObrigado por pedir na Pizzaria do Gordinho!')
        del user_state[from_number]

    logging.debug(f"Resposta: {msg.body}")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
