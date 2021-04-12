#!/usr/bin/python3
## Chris Sikes
## 4/1/2021

import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

domainfile = open("allowed_domains.txt", "r")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='domainsearch')
async def image(ctx):
    # Clear domains.txt
    cmd = "echo > domains.txt"
    os.system(cmd)
    for line in domainfile:
        cmd = "curl -s https://crt.sh/?cn=%." + line.rstrip() + "\&output=json |jq -r \'.[].name_value\' | sed \'s/\*\.//g\' | sort -u >> domains.txt"
        os.system(cmd)
        cmd = "/<path to sublister>/sublist3r.py -d " + line.rstrip() + "| tail -n +24 >> domains.txt"
        os.system(cmd)
    await ctx.send('Finished searching. Now formatting and Diff')
    # remove html colored urls
    cmd = "sed -i 's/\\x1b\[[0-9;]*m//g' domains.txt"
    os.system(cmd)
    # sort and remove duplicates
    cmd = "sort -u domains.txt -o domains.txt"
    os.system(cmd)

@bot.command(name='httprobe')
async def image(ctx):
    cmd = "cat domaindiff.txt | httprobe > valid.txt"
    os.system(cmd)
    cmd = "sort -u valid.txt -o valid.txt"
    os.system(cmd)
    with open('valid.txt', 'rb') as fp:
        await ctx.send(file=discord.File(fp, 'valid.txt'))

@bot.command(name='domainsnew')
async def image(ctx):
    # Clear domains.txt
    cmd = "echo > domainsnew.txt"
    os.system(cmd)
    for line in domainfile:
        cmd = "curl -s https://crt.sh/?cn=%." + line.rstrip() + "\&output=json |jq -r \'.[].name_value\' | sed \'s/\*\.//g\' | sort -u >> domainsnew.txt"
        os.system(cmd)
        cmd = "/<path to sublister>/sublist3r.py -d " + line.rstrip() + "| tail -n +24 >> domainsnew.txt"
        os.system(cmd)
    await ctx.send('Finished searching. Now formatting and Diff')
    # remove html colored urls
    cmd = "sed -i 's/\\x1b\[[0-9;]*m//g' domainsnew.txt"
    os.system(cmd)
    # sort and remove duplicates
    cmd = "sort -u domainsnew.txt -o domainsnew.txt"
    os.system(cmd)
    # find anything new in 
    cmd = "diff master_domains.txt domainsnew.txt|grep '>'|cut -c 3- > domains.txt"
    os.system(cmd)
    cmd = "rm domainsnew.txt"
    os.system(cmd)

    with open('domains.txt', 'rb') as fp:
        await ctx.send(file=discord.File(fp, 'domains.txt'))
    cmd = "mv domains.txt domaindiff.txt"
    os.system(cmd)

bot.run(TOKEN)

















