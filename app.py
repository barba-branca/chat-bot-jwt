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

# Cardápio de complementos com preços
complementos = {
    '1': {'nome': 'Calabresa extra', 'preco': 3.00},
    '2': {'nome': 'Pepperoni extra', 'preco': 4.00},
    '3': {'nome': 'Azeitona extra', 'preco': 2.00}
}

# Função para exibir o cardápio de refrigerantes
def exibir_cardapio_refrigerantes():
    return '\n'.join([
        'Escolha um refrigerante:\n',
        '1. Coca-Cola - R$ 5.00',
        '2. Guaraná - R$ 5.00',
        '3. Sprite - R$ 5.00'
    ])

# Função para exibir o cardápio de sucos
def exibir_cardapio_suco():
    return '\n'.join([
        'Escolha um suco:\n',
        '1. Laranja - R$ 5.00',
        '2. Maracujá - R$ 5.00',
        '3. Uva - R$ 5.00'
    ])

# Função para exibir o cardápio de complementos
def exibir_cardapio_complementos():
    return '\n'.join([
        'Deseja adicionar algum complemento à sua pizza?\n',
        '1. Calabresa extra - R$ 3.00',
        '2. Pepperoni extra - R$ 4.00',
        '3. Azeitona extra - R$ 2.00',
        '4. Não adicionar complementos'
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
            'total': 0,
            'address': {
                'rua_av': '',
                'nome_rua_av': '',
                'lote': '',
                'quadra': '',
                'residence_type': '',
                'house_number': '',
                'setor_bairro': ''
            },
            'payment_method': '',
            'contact_number': '',
            'delivery_instructions': ''
        }

    user = user_state[from_number]
    logging.debug(f"Estado do usuário: {user}")

    if user['step'] == 'welcome':
        user['step'] = 'get_name'
        msg.body(f'Olá! Seja bem-vindo à Pizzaria do Gordinho. Meu nome é Norman, e estou aqui para agilizar seu atendimento. Qual é o seu nome?')
        
    elif user['step'] == 'get_name':
        user['name'] = incoming_msg
        user['step'] = 'menu'
        msg.body(f'Ok, {user["name"]}, irei te mandar o nosso cardápio. Digite o número da opção do menu a seguir para continuarmos:\n\n' +
                 '\n'.join([f'{chave}. {item["nome"]} - R$ {item["preco"]:.2f}' for chave, item in list(cardapio.items())[:14]]))
        
    elif user['step'] == 'menu':
        if incoming_msg in cardapio and int(incoming_msg) <= 14:
            item_escolhido = cardapio[incoming_msg]
            user['order'].append(item_escolhido)
            user['total'] += item_escolhido['preco']
            user['step'] = 'ask_more_pizza'
            msg.body(f'Você escolheu: {item_escolhido["nome"]} - R$ {item_escolhido["preco"]:.2f}\nVocê deseja adicionar mais pizzas ao seu pedido? Digite "1" para sim ou "2" para não.')
        else:
            msg.body('Opção inválida. Por favor, escolha uma opção válida do cardápio.')
            
    elif user['step'] == 'ask_more_pizza':
        if incoming_msg == '1':
            user['step'] = 'menu'
            msg.body('Digite o número da opção do menu a seguir para continuar adicionando pizzas:\n\n' +
                     '\n'.join([f'{chave}. {item["nome"]} - R$ {item["preco"]:.2f}' for chave, item in list(cardapio.items())[:14]]))
        elif incoming_msg == '2':
            user['step'] = 'ask_complement'
            msg.body(exibir_cardapio_complementos())
        else:
            msg.body('Não entendi sua resposta. Por favor, responda com "1" para sim ou "2" para não.')
    
    elif user['step'] == 'ask_complement':
        if incoming_msg in complementos:
            complemento_escolhido = complementos[incoming_msg]
            user['order'].append(complemento_escolhido)
            user['total'] += complemento_escolhido['preco']
            msg.body(f'Você adicionou: {complemento_escolhido["nome"]} - R$ {complemento_escolhido["preco"]:.2f}\n{exibir_cardapio_complementos()}')
        elif incoming_msg == '4':
            user['step'] = 'ask_drink'
            msg.body('Você deseja adicionar uma bebida ao seu pedido? Digite "1" para refrigerante, "2" para suco e "3" para não quero.')
        else:
            msg.body('Opção de complemento inválida. Por favor, escolha uma opção válida.')
            
    elif user['step'] == 'ask_drink':
        if incoming_msg == '1':
            user['step'] = 'soda_menu'
            msg.body(exibir_cardapio_refrigerantes())
        elif incoming_msg == '2':
            user['step'] = 'juice_menu'
            msg.body(exibir_cardapio_suco())
        elif incoming_msg == '3':
            user['step'] = 'ask_nome_rua_av'
            msg.body('Por favor, informe o nome da sua rua/avenida.')
        else:
            msg.body('Opção inválida. Por favor, escolha uma opção válida.')
    
    elif user['step'] == 'soda_menu':
        if incoming_msg in ['1', '2', '3']:
            refri_escolhido = cardapio[str(int(incoming_msg) + 14)]  # Adicionando 14 para acessar a chave correta
            user['order'].append(refri_escolhido)
            user['total'] += refri_escolhido['preco']
            user['step'] = 'ask_more_drink'
            msg.body(f'Você escolheu: {refri_escolhido["nome"]} - R$ {refri_escolhido["preco"]:.2f}\nVocê deseja adicionar mais bebidas ao seu pedido? Digite "1" para sim ou "2" para não.')
        else:
            msg.body('Opção de refrigerante inválida. Por favor, escolha uma opção válida.')
            
    elif user['step'] == 'juice_menu':
        if incoming_msg in ['1', '2', '3']:
            suco_escolhido = cardapio[str(int(incoming_msg) + 17)]  # Adicionando 17 para acessar a chave correta
            user['order'].append(suco_escolhido)
            user['total'] += suco_escolhido['preco']
            user['step'] = 'ask_more_drink'
            msg.body(f'Você escolheu: {suco_escolhido["nome"]} - R$ {suco_escolhido["preco"]:.2f}\nVocê deseja adicionar mais bebidas ao seu pedido? Digite "1" para sim ou "2" para não.')
        else:
            msg.body('Opção de suco inválida. Por favor, escolha uma opção válida.')
    
    elif user['step'] == 'ask_more_drink':
        if incoming_msg == '1':
            user['step'] = 'ask_drink'
            msg.body('Você deseja adicionar uma bebida ao seu pedido? Digite "1" para refrigerante, "2" para suco e "3" para não quero.')
        elif incoming_msg == '2':
            user['step'] = 'ask_nome_rua_av'
            msg.body('Por favor, informe o nome da sua rua/avenida.')
        else:
            msg.body('Não entendi sua resposta. Por favor, responda com "1" para sim ou "2" para não.')
            
    elif user['step'] == 'ask_nome_rua_av':
        user['address']['nome_rua_av'] = incoming_msg
        user['step'] = 'ask_lote'
        msg.body('Por favor, informe o número do seu lote.')

    elif user['step'] == 'ask_lote':
        user['address']['lote'] = incoming_msg
        user['step'] = 'ask_quadra'
        msg.body('Por favor, informe o número da sua quadra.')

    elif user['step'] == 'ask_quadra':
        user['address']['quadra'] = incoming_msg
        user['step'] = 'ask_residence_type'
        msg.body('É uma casa ou apartamento? Digite "1" para casa e "2" para apartamento.')

    elif user['step'] == 'ask_residence_type':
        if incoming_msg == '1':
            user['address']['residence_type'] = 'casa'
            user['step'] = 'ask_house_number'
            msg.body('Qual o número da casa?')
        elif incoming_msg == '2':
            user['address']['residence_type'] = 'apartamento'
            user['step'] = 'ask_apartment_number'
            msg.body('Qual o número do apartamento?')
        else:
            msg.body('Opção inválida. Por favor, digite "1" para casa e "2" para apartamento.')

    elif user['step'] == 'ask_house_number':
        user['address']['house_number'] = incoming_msg
        user['step'] = 'ask_setor_bairro'
        msg.body('Por favor, informe o setor ou bairro.')

    elif user['step'] == 'ask_apartment_number':
        user['address']['house_number'] = incoming_msg
        user['step'] = 'ask_setor_bairro'
        msg.body('Por favor, informe o setor ou bairro.')

    elif user['step'] == 'ask_setor_bairro':
        user['address']['setor_bairro'] = incoming_msg
        user['step'] = 'ask_payment_method'
        msg.body('Qual a forma de pagamento? Digite "1" para Pix, "2" para dinheiro ou "3" para cartão.')

    elif user['step'] == 'ask_payment_method':
        if incoming_msg == '1':
            user['payment_method'] = 'Pix'
            user['step'] = 'ask_contact_number'
            msg.body('Por favor, informe um número de contato.')
        elif incoming_msg == '2':
            user['payment_method'] = 'Dinheiro'
            user['step'] = 'ask_contact_number'
            msg.body('Por favor, informe um número de contato.')
        elif incoming_msg == '3':
            user['payment_method'] = 'Cartão'
            user['step'] = 'ask_card_type'
            msg.body('Você escolheu pagamento com cartão. Digite "1" para débito ou "2" para crédito.')
        else:
            msg.body('Opção inválida. Por favor, digite "1" para Pix, "2" para dinheiro ou "3" para cartão.')

    elif user['step'] == 'ask_card_type':
        if incoming_msg == '1':
            user['payment_method'] = 'Cartão de Débito'
            user['step'] = 'ask_contact_number'
            msg.body('Por favor, informe um número de contato.')
        elif incoming_msg == '2':
            user['payment_method'] = 'Cartão de Crédito'
            user['step'] = 'ask_contact_number'
            msg.body('Por favor, informe um número de contato.')
        else:
            msg.body('Opção inválida. Por favor, digite "1" para débito ou "2" para crédito.')

    elif user['step'] == 'ask_contact_number':
        user['contact_number'] = incoming_msg
        user['step'] = 'ask_delivery_instructions'
        msg.body('Você tem alguma instrução especial para a entrega? Por exemplo, "pedir para o motoqueiro buzinar" ou "esperar na porta".')

    elif user['step'] == 'ask_delivery_instructions':
        user['delivery_instructions'] = incoming_msg
        user['step'] = 'order_summary'
        order_summary = '\n'.join([f'{item["nome"]} - R$ {item["preco"]:.2f}' for item in user['order']])
        msg.body(f'Pedido resumido:\n{order_summary}\nTotal: R$ {user["total"]:.2f}\nEndereço: {user["address"]["nome_rua_av"]}, Lote {user["address"]["lote"]}, Quadra {user["address"]["quadra"]}, {user["address"]["residence_type"]} {user["address"]["house_number"]}, Setor/Bairro: {user["address"]["setor_bairro"]}\nForma de Pagamento: {user["payment_method"]}\nNúmero de Contato: {user["contact_number"]}\nInstruções de Entrega: {user["delivery_instructions"]}\n\nSe tudo estiver correto, digite "1" para confirmar, "2" para cancelar ou "3" para corrigir.')

    elif user['step'] == 'order_summary':
        if incoming_msg == '1':
            msg.body('Seu pedido foi confirmado! Em breve, você receberá a confirmação do tempo de entrega. Obrigado por escolher a Pizzaria do Gordinho!')
            user_state.pop(from_number)
        elif incoming_msg == '2':
            msg.body('Seu pedido foi cancelado. Se precisar de mais alguma coisa, estou aqui para ajudar!')
            user_state.pop(from_number)
        elif incoming_msg == '3':
            user['step'] = 'menu'
            user['order'] = []
            user['total'] = 0
            msg.body('Vamos começar novamente. Digite o número da opção do menu a seguir para continuarmos:\n\n' +
                     '\n'.join([f'{chave}. {item["nome"]} - R$ {item["preco"]:.2f}' for chave, item in list(cardapio.items())[:14]]))
        else:
            msg.body('Resposta inválida. Por favor, digite "1" para confirmar, "2" para cancelar ou "3" para corrigir.')

    logging.debug(f"Resposta enviada: {msg.body}")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
