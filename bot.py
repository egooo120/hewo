from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import telnetlib

# --- Configuración ---
AUTHORIZED_USERS = [7279435741]  # Reemplaza con tus IDs de Telegram autorizados
BOT_TOKEN = '7888426082:AAEXYCA5nLXliYys6vcursz1qNHlSJ3cRs0'

AMI_HOST = '127.0.0.1'
AMI_PORT = 5038
AMI_USER = 'TCxPqbeXB9uw'
AMI_PASS = 'S/3zf+V37xGT'

# --- Funciones AMI ---
def create_extension_ami(ext, password):
    try:
        tn = telnetlib.Telnet(AMI_HOST, AMI_PORT, timeout=5)
        tn.write(f"Action: Login\r\nUsername: {AMI_USER}\r\nSecret: {AMI_PASS}\r\n\r\n".encode())

        # Aquí puedes usar comandos personalizados; esto es un ejemplo:
        tn.write(f"Action: Command\r\nCommand: database put SIP/{ext}/secret {password}\r\n\r\n".encode())

        # Opcional: añadir más configuración si es necesario
        # tn.write(f"Action: Command\r\nCommand: database put SIP/{ext}/callerid \"Usuario\" <{ext}>\r\n\r\n".encode())

        tn.write(b"Action: Logoff\r\n\r\n")
        output = tn.read_all().decode()
        return "✅ Extensión creada." if "Response: Success" in output else f"❌ Error:\n{output}"
    except Exception as e:
        return f"❌ Error conectando a AMI: {e}"

# --- Autenticación ---
def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

# --- Comandos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    await update.message.reply_text("✅ ¡Bot activo! Usa /extension <número> <clave> para crear una extensión.")

async def extension(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("❌ No estás autorizado.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("Uso: /extension <número> <clave>")
        return

    ext, password = context.args
    resultado = create_extension_ami(ext, password)
    await update.message.reply_text(resultado)

# --- Main ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("extension", extension))
    app.run_polling()
