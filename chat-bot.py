nome = 'Norman'
gordinho = 'Pizzaria do Gordinho'
comprimento = f'Olá! Seja bem-vindo à {gordinho}. Meu nome é {nome}, e estou aqui para agilizar seu atendimento.'

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
    '17': {'nome': 'Sprite', 'preco': 5.00}
}

# Função para exibir o cardápio de refrigerantes
def exibir_cardapio_refrigerantes():
    print('\nRefrigerantes:')
    print('1. Coca-Cola - R$ 5.00')
    print('2. Guaraná - R$ 5.00')
    print('3. Sprite - R$ 5.00')

# Comprimentos
print(comprimento)

# Primeira entrada de dados do cliente
nome_user = input('Qual é o seu nome? ')

print(f'Ok, {nome_user}, irei te mandar o nosso cardápio.')
print('Digite o número da opção do menu a seguir para continuarmos:\n')

# Exibir o cardápio de pizzas
print("Pizzas:")
for chave, item in list(cardapio.items())[:14]:  # Exibir apenas pizzas
    print(f'{chave}. {item["nome"]} - R$ {item["preco"]:.2f}')

# Entrada do cliente para selecionar a opção do cardápio
while True:
    opcao_pizza = input('\nEscolha a opção de pizza: ')
    
    if opcao_pizza in cardapio and int(opcao_pizza) <= 14:
        break
    else:
        print('Opção inválida. Por favor, escolha uma opção válida.')

# Exibir a escolha do cliente
item_escolhido = cardapio[opcao_pizza]
print(f'Você escolheu: {item_escolhido["nome"]} - R$ {item_escolhido["preco"]:.2f}')
total = item_escolhido['preco']

# Perguntar se o cliente deseja adicionar uma bebida
while True:
    deseja_bebida = input('Você deseja adicionar uma bebida ao seu pedido? (sim/não): ').strip().lower()
    
    if deseja_bebida == 'sim' or deseja_bebida == 's':
        # Exibir o cardápio de refrigerantes
        exibir_cardapio_refrigerantes()
        
        # Selecionar a bebida
        while True:
            opcao_bebida = input('\nEscolha o refrigerante desejado (1-3): ')
            
            if opcao_bebida in ['1', '2', '3']:  # Mapear as opções para as chaves corretas
                bebida_chave = str(int(opcao_bebida) + 14)
                bebida_escolhida = cardapio[bebida_chave]
                print(f'Você escolheu: {bebida_escolhida["nome"]} - R$ {bebida_escolhida["preco"]:.2f}')
                total += bebida_escolhida['preco']
                break  # Sai do loop ao escolher uma bebida válida
            else:
                print('Opção de refrigerante inválida. Por favor, escolha uma opção de 1 a 3.')
        break  # Sai do loop principal ao adicionar uma bebida ou não
    elif deseja_bebida == 'não' or deseja_bebida == 'nao' or deseja_bebida == 'n':
        print('Sem bebida adicionada.')
        break  # Sai do loop se não deseja bebida
    else:
        print('Não entendi sua resposta. Por favor, responda com "sim" ou "não".')

# Solicitar a localização para entrega
localizacao = input('Por favor, informe sua localização para entrega: ')

# Exibir o valor total e a localização
print(f'O total do seu pedido é R$ {total:.2f}.')
print(f'Seu pedido será entregue em: {localizacao}.')
