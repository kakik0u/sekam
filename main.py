import discord
from discord import app_commands
import requests
import json
from file import loadjson, loadtxt, savetxt, savejson

TOKEN="PLEASE INSERT TOKEN"
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event#init処理
async def on_ready():
    print("SEKAM起動")
    await tree.sync(
    spamer=loadtxt("spamer.txt")
    await client.change_presence(activity=discord.CustomActivity(name=f"やっつけたスパム:{spamer}人"))

@client.event
async def on_member_join(member):
  if member.bot:
     print("bot")
     return
  url=f"https://discord.com/api/v10/guilds/518371205452005387/members/{member.id}"
  headers = {"Authorization": "PLEASE INSERT USER TOKEN"}
  response = requests.get(url, headers=headers)
  if response.status_code == 404:
    status="spam"
    await client.change_presence(activity=discord.CustomActivity(name=f"迎撃中"))
    try:
        await member.send("参加しようとなさったサーバーは特定のユーザー向けに設定されているため、キックしました。\nもしこの処理が間違いだと思われる場合招待リンクの発行者に問い合わせてください。\nThis server is configured for a specific user.You have been kicked from the server.\nIf you believe this process is in error, please contact the publisher of the invitation link")
    except:
        print("message error")
    await member.kick(reason="専科への所属を確認できませんでした。")
    data=loadjson("logchannel.json")
    logchannelid=find_key(data, str(member.guild.id))
    if logchannelid == "Nothing":
       pass
    else:
       logch=client.get_channel(int(logchannelid))
       await logch.send(f"{member.display_name}(DiscordID:{member.id})は専科にいなかったのでkickしました。")
       print("loggingchok")
    spamer=loadtxt("spamer.txt")
    spamer2=int(spamer)+1
    savetxt("spamer.txt",str(spamer2))
    await client.change_presence(activity=discord.CustomActivity(name=f"やっつけたスパム:{spamer2}人"))
  else:
    status="senka"
    data=loadjson("logchannel.json")
    logchannelid=find_key(data, str(member.guild.id))
    if logchannelid == "Nothing":
       pass
    else:
       logch=client.get_channel(int(logchannelid))
       await logch.send(f"{member.display_name}(DiscordID:{member.id})は専科にいます！やったー！")
    spamer=loadtxt("spamer.txt")
    await client.change_presence(activity=discord.CustomActivity(name=f"やっつけたスパム:{spamer}人"))
  f = open('log.txt', 'a')
  f.write(f"{member}:{status}\n")
  f.close()
  print(status)

@client.event
async def on_guild_join(guild):
    owner = guild.owner
    greeting_message = f"こんにちは、SEKAMです。\nサーバーへの採用ありがとうございます。\n説明が必要な機能が一つあるので説明させてください。"
    embed=discord.Embed(title="検出ログ機能", description="サーバーの入室者が専科民かどうかを逐一報告する機能です。")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/963413133463027725/1240544634233421855/image.png?ex=6646f2b9&is=6645a139&hm=ffd5e2b6c570fc68d216f9e5c661a71f167d5148391688e25b6adf7dd87cbcc6&")
    embed.add_field(name="設定方法", value="/log コマンドをサーバー内で実行し、ログを送信するチャンネルを選択します。(ユーザーに見られないところで実行したほうがいいかも？)", inline=True)
    try:
        await owner.send(content=greeting_message,embed=embed)
        await owner.send("また、Sekamの制限を外したいときは私をキックしてください。\n私のアイコンをクリックしたら下くらいにある「アプリを追加」から簡単に再追加できます。\n[プライバシーポリシー](https://death.kakikou.app/sekam/privacy/ )を一応書いてますが個人情報を集める機能がそもそも備わってないので気にしなくて大丈夫だと思います。気にする必要が出てきたら場合また連絡します。\n最後に、お問い合わせとか機能の要望はこのDMに送られても気づけないので開発者(DiscordID:@kakik0u)に連絡して下さい。")
        print(f"サーバー {guild.name} のオーナー {owner.name} にDMを送信しました。")
    except discord.HTTPException:
        print(f"サーバー {guild.name} のオーナー {owner.name} にDMを送信できませんでした。")

@tree.command(name="log",description="ログチャンネルを指定できます")
@app_commands.default_permissions(administrator=True)
async def logid(ctx:discord.Interaction,channel: discord.TextChannel):
  data = dict(loadjson("logchannel.json"))
  key = str(ctx.guild.id)
  keydata=list(data.keys())
  chid=str(channel.id)
  if key in keydata:
    del data[key]
    data[key] = chid
    savejson("logchannel.json",data)
    await ctx.response.send_message("設定を変更しました。",ephemeral=True)
  else:
    data[key] = chid
    savejson("logchannel.json",data)
    await ctx.response.send_message("設定されました。",ephemeral=True)


def find_key(json_data,logid):
    data = json_data
    def search_keys(obj, keys=[]):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if str(logid) in key:
                    return value
                keys.append(key)
                result = search_keys(value, keys)
                if result is not None:
                    return result
                keys.pop()
        elif isinstance(obj, list):
            for item in obj:
                result = search_keys(item, keys)
                if result is not None:
                    return result
        return None
    result = search_keys(data)
    if result is not None:
        return str(result)
    else:
        return "Nothing"
    
client.run(TOKEN)
