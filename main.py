import asyncio
from discord.ext import commands
from flask import Flask, request, jsonify
from multiprocessing import Process

# Discord Bot Setup
bot_prefix = '!'
bot = commands.Bot(command_prefix=bot_prefix, self_bot=True)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def write(ctx, word: str, times: int):
    output = (word + '\n') * times
    await ctx.send(output.strip())

# Flask Web Server Setup
app = Flask(__name__)

def run_bot(token):
    asyncio.set_event_loop(asyncio.new_event_loop())  # Create a new event loop for the new process
    bot.run(token, bot=False)

@app.route('/start', methods=['POST'])
def start_bot():
    token = request.json.get('token')
    if token:
        # Start bot in a new process
        process = Process(target=run_bot, args=(token,))
        process.start()
        return jsonify({'message': 'Bot is starting'}), 200
    else:
        return jsonify({'error': 'Token is required'}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Prevent Flask from stopping the bot when reloading
