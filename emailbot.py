import discord
import os
import smtplib
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

token = os.environ['TOKEN']
botUser = os.environ['BOTUSER']
botPass = os.environ['BOTPASS']

client = discord.Client()


async def checkEmail(email):
    return re.match(regex, email)


@client.event
async def on_ready():
    print('Logged in')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('*help') and message.author != client.user:
        await message.channel.send(
            'Current commands are as follows: \n\n*help: Shows all the bot commands. \n*email: Sends anonymous email from discord. \n*autoapply: WIP Sends you audio file of youtube video. ')

    if message.content.startswith('*email') and message.author != client.user:
        await message.channel.send('Email address to send to: ')

        if message.author != client.user:
            inputEmail = await client.wait_for('message')

            if checkEmail(inputEmail.content):
                email = inputEmail.content
                await message.channel.send(email + ' registered email.')

            else:
                await message.channel.send('Please restart command and enter a valid email! ')
                return

        else:
            return

        await message.channel.send('Email subject line: ')

        if message.author != client.user:
            inputSubject = await client.wait_for('message')
            subject = inputSubject.content
            await message.channel.send(subject + ' registered subject.')
        else:
            return

        await message.channel.send('Email body: ')

        if message.author != client.user:
            inputBody = await client.wait_for('message')
            body = inputBody.content
            await message.channel.send(body + ' registered body.')
        else:
            return

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(botUser, botPass)

            emailFormat = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(botUser, email, emailFormat)

            await message.channel.send('Sent email to ' + email + '.')
            return

    if message.content.startswith('*ytmp3') and message.author != client.user:
        await message.channel.send('Hello!')

client.run(token)