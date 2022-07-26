import os
import discord
from discord.ext import commands
import requests
from requests.exceptions import RequestException
from coinbase.wallet.client import Client
from keep_running import keep_running


# discord bot prefix
client_bot = commands.Bot(command_prefix='$')

# coinbase api access
client = Client(os.environ['COINBASE_KEY'], os.environ['COINBASE_ACCESS'])

# list of some of the cryptocurrencies from https://www.coinbase.com/browse
coins = [
    'BTC', 'ETH', 'ETH2', 'USDT', 'USDC', 'BUSD', 
    'XRP', 'ADA', 'SOL', 'DOGE', 'DAI', 'DOT', 
    'MATIC', 'AVAX', 'SHIB', 'UNI', 'WBTC', 'LTC', 
    'ETC', 'LINK', 'CRO', 'XLM', 'ATOM', 'BCH', 
    'THETA', 'AXS', 'BSV', 'SAND', 'ALGO', 'MANA', 
    'MKR', 'ZEC', 'APE', 'FLOW', 'ICP', 'FIL', 
    'QNT', 'PAX', 'GRT', 'CHZ', 'AMP', 'SNX', 
    'EOS', 'ENS', 'STX', 'DASH', 'CGLD'
]


@client_bot.event
async def on_ready():
    print('Logged in as Coins Info Bot')
    print('------')
  

@client_bot.command()
async def hello(ctx):
    embed = discord.Embed(
        title="Hello! Welcome to Coins Info Bot where you can view different information on cryptocurrencies.",
        url=
        "https://discord.com/api/oauth2/authorize?client_id=1000366270413287484&permissions=274877974528&scope=bot",
        description="Type '$help' to see list of commands.",
        color=0xeee657)
    embed.set_thumbnail(
        url=
      "https://cdn.discordapp.com/attachments/1001125337570230292/1001343672853475398/coinsinfobot.png"
    )

    await ctx.send(embed=embed)
  
  
@client_bot.command()
async def list(ctx):
    value = ', '.join(coins)
    embed = discord.Embed(title=value,
                         color=349888
                         )
    embed.set_author(name="From Coinbase:")
    embed.set_thumbnail(
                url=
                "https://logosarchive.com/wp-content/uploads/2021/12/Coinbase-logo-square-1.png"
            )
    await ctx.send(embed=embed)


@client_bot.command()
async def prices(ctx, coin):
    try:
        coin = coin.upper()
        buy = client.get_buy_price(currency_pair='{}-USD'.format(coin))
        sell = client.get_sell_price(currency_pair='{}-USD'.format(coin))
        spot = client.get_spot_price(currency_pair='{}-USD'.format(coin))
        buyAmount = buy.get('amount')
        sellAmount = sell.get('amount')
        spotAmount = spot.get('amount')
        value = 'Buy: ${0}, Sell: ${1}, Spot: ${2}'.format(
            buyAmount, sellAmount, spotAmount)
        embed = discord.Embed(title=value)

    except:
        embed = discord.Embed(title='Please check your syntax and try again',
                              color=0xff0000)

    await ctx.send(embed=embed)


@client_bot.command()
async def exchange(ctx, coin_one, coin_two):

    try:
        coin_one = coin_one.upper()
        coin_two = coin_two.upper()
        getRates = client.get_exchange_rates(currency=coin_one)
        rate = getRates.get('rates').get(coin_two)
        try:
            float(rate)
            value = '1 {0} is worth {1} {2}'.format(coin_one, rate, coin_two)
            embed = discord.Embed(title=value)
        except ValueError:
            embed = discord.Embed(title='Cannot process this exhange.')
    except:
        embed = discord.Embed(title='Exchange data not available.',
                              color=0xff0000)

    await ctx.send(embed=embed)


@client_bot.command()
async def history(ctx, coin, period):

    try:
        coin = coin.upper()
        period = period.lower()
        his = client.get_historic_prices(currency_pair=coin + '-USD',
                                         period=period)
        previous = his.get('prices')[-1].get('price')
        current = client.get_spot_price(
            currency_pair='{}-USD'.format(coin)).get('amount')
        previous = float(previous)
        current = float(current)
        if previous == current:
            embed = discord.Embed(title=coin + ': 0% change')
        else:
            if current - previous < 0:
                sign = 0
            elif current - previous > 0:
                sign = 1
            value = abs(current - previous) / previous * 100
        if sign == 1:
            embed = discord.Embed(title=coin + ': UP {0:.2f}%'.format(value),
                                  color=0x008000)
        elif sign == 0:
            embed = discord.Embed(title=coin + ': DOWN {0:.2f}%'.format(value),
                                  color=0xff0000)
    except:
        embed = discord.Embed(title='Please check your syntax and try again, or history data not available.',
                              color=0xff0000)

    await ctx.send(embed=embed)


@client_bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Authors: Karl Dimaculangan, Vincent Lopez, Stephanie Managbanag",
        url=
        "https://mail.google.com/mail/u/0/?fs=1&to=karl.dimaculangan@obf.ateneo.edu&su=Coins+Info+Bot+Feedback&body=[type+your+feedback]&cc=charles.lopez@obf.ateneo.edu+stephanie.managbanag@obf.ateneo.edu&&tf=cm",
        description="This Discord bot is an ITMGT 25.03 Capstone Project",
        color=349888)
    embed.set_thumbnail(
        url=
        "https://1000logos.net/wp-content/uploads/2018/05/Gmail-Logo-2013.png"
    )
    embed.add_field(name="Powered by:", value="Python", inline=True)
    embed.set_footer(text="Let us know if you have any feedback! :)")

    await ctx.send(embed=embed)


client_bot.remove_command('help')


@client_bot.command()
async def help(ctx):
    embed = discord.Embed(title='Welcome to Coins Info Bot!',
                          description='Need help? Here are the commands!',
                          color=0xeee657)
    embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/1001125337570230292/1001343672853475398/coinsinfobot.png"
        )
    embed.add_field(name='$hello',
                    value="Display the bot's greeting message.",
                    inline=False)
    embed.add_field(name='$list',
                    value='Show list of the supported cryptocurrencies.',
                    inline=False)
    embed.add_field(name='$prices',
                    value='Show coin price. \nExample: "$prices ETH"',
                    inline=False)
    embed.add_field(name='$exchange',
                    value='Show exchange rate from one coin to another. \nExample: "$exchange USDC BTC"',
                    inline=False)
    embed.add_field(name='$history',
                    value='Show percentage of change in coin value over a period. \nExample: "$history BTC year" \nAvailable periods to check: "hour", "day", "week", "month", "year"',
                    inline=False)
    embed.add_field(
        name='$info',
        value='Who developed this bot? Find out with this command!',
        inline=False)
    embed.add_field(name='$help',
                    value='Open this help menu again.',
                    inline=False)

    await ctx.send(embed=embed)


keep_running()
client_bot.run(os.environ['DISCORD_TOKEN'])

