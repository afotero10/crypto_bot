import telepot
from parametros_bot.conexion import token_telegram,chat_id

bot=telepot.Bot(token_telegram)

bot.sendMessage(chat_id,'mensaje')