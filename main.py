from flask import Flask, request, jsonify
from discord.ext import commands
import asyncio
import threading

app = Flask(__name__)

def run_bot(token):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    client = commands.Bot(command_prefix='!', self_bot=True)

    @client.event
    async def on_ready():
        print(f"Logged in as: {client.user} (ID: {client.user.id})")

    @client.command()
    async def spam(ctx, num: int):
        for i in range(num):
            await ctx.send("SPAM")

    client.run(token, bot=False)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        # Here you could start the bot using the URL or do other processing
        return jsonify({'message': f'URL received: {url}'})
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submit URL</title>
    </head>
    <body>
        <h1>Enter URL to Process</h1>
        <form method="post" action="/">
            <input type="text" name="url" placeholder="Enter URL here" required>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    '''

@app.route('/start_bot', methods=['POST'])
def start_bot():
    data = request.get_json()
    token = data.get('token')
    if token:
        thread = threading.Thread(target=run_bot, args=(token,))
        thread.daemon = True
        thread.start()
        return jsonify({'message': 'Bot is starting'}), 200
    else:
        return jsonify({'error': 'No token provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25522)
