import requests
from time import sleep
from deep_translator import GoogleTranslator

URL = "https://api.adviceslip.com/advice"
ARQUIVO_CONSELHOS = 'conselhos.txt'

def buscar_conselhos(quantidade):
    conselhos = []
    for i in range(quantidade):
        try:
            print(f'Buscando conselho {i + 1}...')
            resposta = requests.get(URL)
            if resposta.status_code == 200:
                dados = resposta.json()
                id_conselho = dados['slip']['id']
                conselho = dados['slip']['advice']
                conselhos.append((id_conselho, conselho))
                print(f'Conselho recebido: {conselho}')
            else:
                print('Erro ao acessar a API.')
            sleep(1)
        except Exception as e:
            print(f'Erro: {e}')
            break
    return conselhos

def salvar_conselhos(conselhos):
    try:
        try:
            with open(ARQUIVO_CONSELHOS, 'r') as arquivo:
                conselhos_existentes = arquivo.readlines()
        except FileNotFoundError:
            conselhos_existentes = []

        for id_conselho, conselho in conselhos:
            conselhos_existentes.append(f'{id_conselho} - {conselho}\n')

        with open(ARQUIVO_CONSELHOS, 'w') as arquivo:
            arquivo.writelines(conselhos_existentes)

        print('Conselhos salvos com sucesso!')
    except Exception as e:
        print(f'Erro ao salvar os conselhos: {e}')

def mostrar_conselhos_guardados():
    try:
        with open(ARQUIVO_CONSELHOS, 'r') as arquivo:
            print('Conselhos guardados:')
            print(arquivo.read())
    except FileNotFoundError:
        print('Nenhum conselho guardado ainda.')

def traduzir_conselho(conselho):
    try:
        traducao = GoogleTranslator(source='english', target='portuguese').translate(conselho)
        return traducao
    except Exception as e:
        print(f'Erro na tradução: {e}')
        return conselho

def menu():
    conselhos = []
    while True:
        print('\n1. Receber conselhos')
        print('2. Mostrar os Conselhos')
        print('3. Salvar conselhos')
        print('4. Mostrar conselhos guardados')
        print('5. Traduzir conselhos recebidos')
        print('6. Sair')
        print()

        escolha = input('Escolha uma opção: ')

        if escolha == '1':
            quantidade = int(input('Quantos conselhos deseja receber? '))
            conselhos = buscar_conselhos(quantidade)
        elif escolha == '2':
            if conselhos:
                for id_conselho, conselho in conselhos:
                    print(f'{id_conselho}: {conselho}')
            else:
                print('Nenhum conselho recebido ainda.')
        elif escolha == '3':
            if conselhos:
                salvar_conselhos(conselhos)
            else:
                print('Nenhum conselho para salvar.')
        elif escolha == '4':
            mostrar_conselhos_guardados()
        elif escolha == '5':
            if conselhos:
                for id_conselho, conselho in conselhos:
                    traducao = traduzir_conselho(conselho)
                    print(f'{id_conselho}: {conselho} - Tradução: {traducao}')
            else:
                print('Nenhum conselho para traduzir.')
        elif escolha == '6':
            print('Saindo...')
            break

menu()
