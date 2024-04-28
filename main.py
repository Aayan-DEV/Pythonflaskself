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
        print(f"Selfbot {client.user} is ready to be used.")

    @client.command()
    async def spam(ctx, num: int):
        for i in range(num):
            await ctx.send("SPAM")

    client.run(token, bot=False)

@app.route('/start_bot', methods=['POST'])
def start_bot():
    data = request.get_json()
    token = data.get('token')
    if token:
        thread = threading.Thread(target=run_bot, args=(token,))
        thread.start()
        return jsonify({'message': 'Bot is starting'}), 200
    else:
        return jsonify({'error': 'No token provided'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
