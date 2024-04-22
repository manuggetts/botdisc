import discord
import os
import random

# Definindo as constantes
REGRAS = f'1 - Não torcer para o Corinthians.{os.linesep}2 - Não desrespeitar os membros.'
MENSAGEM_BOAS_VINDAS = 'acabou de entrar no'
COMANDO_REGRAS = '!regras'
COMANDO_NIVEL = '!nivel'
COMANDO_JOGO = '!jogo'
NUMERO_MINIMO = 1
NUMERO_MAXIMO = 10

# Configurando os intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializando o estado do jogo
        self.guessing_game_active = False
        self.number_to_guess = 0

    async def on_ready(self):
        # Imprime uma mensagem quando o bot está pronto
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        # Imprime todas as mensagens recebidas
        print('Message from {0.author}: {0.content}'.format(message))

        # Ignora as mensagens enviadas pelo próprio bot
        if message.author.bot:
            return

        # Responde aos comandos do usuário
        if message.content == COMANDO_REGRAS:
            await message.channel.send(f'{message.author.name}, as regras do servidor são:{os.linesep}{REGRAS}')
        elif message.content == COMANDO_NIVEL:
            await message.author.send('Nível 1')
        elif message.content == COMANDO_JOGO:
            self.guessing_game_active = True
            self.number_to_guess = random.randint(NUMERO_MINIMO, NUMERO_MAXIMO)
            await message.channel.send('Jogo iniciado! Estou pensando em um número de 1 a 10. Tente adivinhar!')
        elif self.guessing_game_active:
            try:
                # Verifica se o palpite do usuário está dentro do intervalo permitido
                guess = int(message.content)
                if NUMERO_MINIMO <= guess <= NUMERO_MAXIMO:
                    if guess == self.number_to_guess:
                        await message.channel.send('Parabéns, você acertou!')
                        self.guessing_game_active = False
                    else:
                        await message.channel.send('Desculpe, tente novamente!')
                else:
                    await message.channel.send(f'Por favor, insira um número entre {NUMERO_MINIMO} e {NUMERO_MAXIMO}.')
            except ValueError:
                await message.channel.send('Por favor, insira um número.')

    async def on_member_join(self,member):
        # Envia uma mensagem de boas-vindas quando um novo membro entra no servidor
        guild = member.guild
        if guild.system_channel is not None:
            mensagem = f'{member.mention} {MENSAGEM_BOAS_VINDAS} {guild.name}'
            await guild.system_channel.send(mensagem)

client = MyClient(intents=intents)
client.run('MTIzMjAyNzEyMTgyOTAxOTY3MQ.GylzNS.3vd7MNtcMtA8wJOwo2w6QTXRSEq7ODf-dyzD1o')