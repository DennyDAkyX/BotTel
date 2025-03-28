#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic troll calc(Echobot) example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging


from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes, MessageHandler, filters
import random

import os
from dotenv import load_dotenv
load_dotenv()#crea le variabili da un file .env


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



#funzioni per fa calcoli sbagliati
#qui definisco funzione che  genera risultato sbagliato
def wrongCalc(correctResult):
    return correctResult + random.randint(-10,10)

#questa è la funzione per i calcoli
async def calcola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.startswith("/calcola"):
        try:
            expression = " ".join(context.args)
            if not expression:
                await update.message.reply_text("Devi scrivere un'operazione dopo /calcola, es: /calcola 2+2")
                return
            correctResult = eval(expression)
            wrongResult = wrongCalc(correctResult)
            await update.message.reply_text(f"Il risultato di {expression} è: {wrongResult}")
        except:
            await update.message.reply_text("Operazione matematica non riconosciuta, ripeti...")

'''async def calcola(update:Update, contex: CallbackContext)-> None:

    try:
        espressione = update.message.text #qui scrivo i numeri
        correctResult = eval(espressione)
        wrongResult = wrongCalc(correctResult)
        await update.message.reply_text(f"il risultato di {espressione} e :{wrongResult}")
    except:
        await update.message.reply_text("operazione matematica non riconosciuta ripeti....")
    
     # on non command i.e message -calculate (echo) the message on Telegram     
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,calcola))
#------------------------------------------
'''
#funzione consigli sbagliati--------------------------
def bad_advice(category):
    advice_dict = {
        "amore": ["Ignorala per mesi, così capirà che la vuoi!", "Se ti piace qualcuno, insultalo un po' per attirare attenzione."],
        "soldi": ["Metti tutti i tuoi risparmi in criptovalute sconosciute!", "Compra biglietti della lotteria, è un investimento sicuro.", "vuoi dei numeri vincenti?......chiedi a Padre Pio"],
        "salute": ["Mangia solo cibo fritto, così avrai più energia!", "Dormi solo 2 ore a notte, il resto è tempo sprecato!"],
    }
    return random.choice(advice_dict.get(category.lower(), ["Non ho consigli per questa categoria, ma fidati di me lo stesso! 😂"]))

async def consiglio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    category = " ".join(context.args)
    if not category:
        await update.message.reply_text("Dimmi una categoria! Es: /consiglio amore, /consiglio soldi o /consiglio salute")
        return
    
    advice = bad_advice(category)
    await update.message.reply_text(f"Ecco un consiglio per {category}: {advice}")
#------------------------------------------------


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    #parla
    await update.message.reply_text("Ciao sono un bot semplice e intelligente faccio i calcoli e do consigli.....provare per credere [coamndo /calcola o /consiglio]")
    #await update.message.reply_tex("se si desidera la finzione calcoli digitare /calcola, se vuoi consigli /consigli")
    


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

#funzioni per echobot
'''
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)
'''

def main() -> None:
    #Tocken telegram
    TOCKEN_TELEGRAM = os.getenv("TOCKEN_TELEGRAM")
    if TOCKEN_TELEGRAM is None:
        raise EnvironmentError("TOCKEN NON VALIDO")

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOCKEN_TELEGRAM).build()

    

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message -calculate e consigli (echo) the message on Telegram 
    application.add_handler(CommandHandler("calcola", calcola))

    application.add_handler(CommandHandler("consiglio", consiglio))
 
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    #application.run_webhook

    #per caricare su docker -H ssh://161.35.31.29 compose up --build



if __name__ == "__main__":
    main()
