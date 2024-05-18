import discord
from discord import app_commands
import requests
import json
from file import loadjson, loadtxt, savetxt, savejson

TOKEN="Please Insert TOKEN!!!"
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event#init処理
async def on_ready():
    print("起動したンゴねぇ")
    await tree.sync()#スラッシュコマンドを同期

@client.event
async def on_member_join(member):
  url=f"https://discord.com/api/v10/guilds/518371205452005387/members/{member.id}"
  headers = {"Authorization": "専科に入ってるアカウントのトークン"}
  response = requests.get(url, headers=headers)
  if response.status_code == 404:
    status="spam"
    await member.send("参加しようとなさったサーバーは特定のユーザー向けに設定されているため、キックしました。\nもしこの処理が間違いだと思われる場合招待リンクの発行者に問い合わせてください。\nThis server is configured for a specific user.You have been kicked from the server.\nIf you believe this process is in error, please contact the publisher of the invitation link")
    await member.kick(reason="専科への所属を確認できませんでした。")
    data=loadjson("logchannel.json")
    logchannelid=find_key(data, str(member.guild.id))
    print(str(logchannelid))
    if logchannelid == "Nothing":
       print("notlogch")
    else:
       logch=client.get_channel(int(logchannelid))
       await logch.send(f"{member.display_name}(DiscordID:{member.id}は専科にいなかったのでkickしました。)")
  else:
    status="senka"
    data=loadjson("logchannel.json")
    logchannelid=find_key(data, str(member.guild.id))
    if logchannelid == "Nothing":
       print("notlogch")
    else:
       logch=client.get_channel(int(logchannelid))
       await logch.send(f"{member.display_name}(DiscordID:f{member.id}は専科にいます！やったー！")
  f = open('log.txt', 'a')
  f.write(f"{member}:{status}\n")
  f.close()

@tree.command(name="log",description="ログチャンネルを指定できます")
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
