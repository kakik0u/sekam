import discord
from discord import app_commands
import requests
import json
from file import loadjson, loadtxt, savetxt, savejson
from discord.ext import commands
from discord.app_commands import default_permissions
from datetime import datetime

TOKEN="BOTTOKEN"
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event#init処理
async def on_ready():
    print("SEKAM起動したンゴねぇ")
    await tree.sync()#スラッシュコマンドを同期
    spamer=loadtxt("spamer.txt")
    await client.change_presence(activity=discord.CustomActivity(name=f"やっつけたスパム:{spamer}人"))

@client.event
async def on_member_join(member):
  if member.bot:
     print("bot")
     return
  url=f"https://discord.com/api/v10/guilds/518371205452005387/members/{member.id}"
  headers = {"Authorization": "専科に加入しているTOKEN"}
  response = requests.get(url, headers=headers)
  if response.status_code == 404:
    status="spam"
    await spamban(member,status)
  
  data=loadjson("configblack.json")
  configblack=find_key(data, str(member.guild.id))
  if configblack == "off":
      pass
  else:
       print("blackliststart")
       data = dict(loadjson("blacklist.json"))
       key = str(member.id)
       keydata=list(data.keys())
       if key in keydata:
         print("blacklist!!!")
         status="blacklist"
         await spamban(member,status)
         f = open('log.txt', 'a')
         now = datetime.now()
         desired_format = "%Y/%m/%d %H:%M:%S"
         formatted_time = now.strftime(desired_format)
         f.write(f"{formatted_time}:{member}:{member.id}:{status}:{member.guild}\n")
         f.close()
         return
         
       else:
         pass
  status="senka"
  data=loadjson("logchannel.json")
  logchannelid=find_key(data, str(member.guild.id))
  if logchannelid == "Nothing":
       pass
  else:
       logch=client.get_channel(int(logchannelid))
       try:
          await logch.send(f"{member.display_name}(DiscordID:{member.id})は専科にいます！やったー！")
       except:
          pass
  spamer=loadtxt("spamer.txt")
  await client.change_presence(activity=discord.CustomActivity(name=f"やっつけたスパム:{spamer}人"))
  f = open('log.txt', 'a')
  now = datetime.now()
  desired_format = "%Y/%m/%d %H:%M:%S"
  formatted_time = now.strftime(desired_format)
  f.write(f"{formatted_time}:{member}:{member.id}:{status}:{member.guild}\n")
  f.close()
  print(status)


async def spamban(member,status):
    await client.change_presence(activity=discord.CustomActivity(name=f"迎撃中"))
    try:
       await member.send("参加しようとなさったサーバーは特定のユーザー向けに設定されているため、キックしました。\nもしこの処理が間違いだと思われる場合招待リンクの発行者に問い合わせてください。\nThis server is configured for a specific user.You have been kicked from the server.\nIf you believe this process is in error, please contact the publisher of the invitation link.\n------------\n注意！Discord海賊団は__特定指定スパム軍団__になっています！SEKAMに海賊団が理由で拒否された場合、__ブラックリスト入り__します！\n自分が専科民なのに遊びで入ってしまった場合は専科にてその旨を書いてください。")
    except:
       print("message send error")
    await member.kick(reason="専科への所属を確認できませんでした。")
    kaizoku="kick"
    bandata=loadjson("ban.json")
    bansetting=find_key(bandata, str(member.guild.id))
    print("bansetting")
    if bansetting == "Nothing":
       pass
    else:
       if bansetting=="on":
          try:
            await member.ban(reason="専科にいなかったことは罪。")
            kaizoku="ban"
            print("banok")
          except:
            print("Banerror")
    data=loadjson("logchannel.json")
    logchannelid=find_key(data, str(member.guild.id))
    if logchannelid == "Nothing":
       pass
    else:
       logch=client.get_channel(int(logchannelid))
       try:
          await logch.send(f"{member.display_name}(DiscordID:{member.id})は専科にいなかったので{kaizoku}しました。コード:{status}")
          print("loggingchok")
       except:
          print("message send error")
    data = dict(loadjson("blacklist.json"))
    key = str(member.id)
    keydata=list(data.keys())
    if key in keydata:
       #del data[key]
       #data[key] = status
       #savejson("blacklist.json",data)
       pass
    else:
        data[key] = status
        savejson("blacklist.json",data)
    spamer=loadtxt("spamer.txt")
    spamer2=int(spamer)+1
    savetxt("spamer.txt",str(spamer2))
    await client.change_presence(activity=discord.CustomActivity(name=f"やっつけたスパム:{spamer2}人"))

@client.event
async def on_guild_join(guild):
    owner = guild.owner
    greeting_message = f"こんにちは、SEKAMです。\nサーバーへの採用ありがとうございます。\n説明が必要な機能が3つあるので説明させてください。"
    embed=discord.Embed(title="検出ログ機能", description="サーバーの入室者が専科民かどうかを逐一報告する機能です。")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/963413133463027725/1240544634233421855/image.png?ex=6646f2b9&is=6645a139&hm=ffd5e2b6c570fc68d216f9e5c661a71f167d5148391688e25b6adf7dd87cbcc6&")
    embed.add_field(name="設定方法", value="/setting log コマンドをサーバー内で実行し、ログを送信するチャンネルを選択します。(ユーザーに見られないところで実行したほうがいいかも？)", inline=True)
    embed2=discord.Embed(title="BAN機能", description="スパムの処し方を選べます。")
    embed2.add_field(name="設定方法", value="/setting ban コマンドをサーバー内で実行し、処理を選びます(キックかBANか)。", inline=True)
    embed3=discord.Embed(title="ブラックリスト機能", description="国際指名手配機能をオフにできます")
    embed3.add_field(name="設定方法", value="/setting blacklist コマンドをサーバー内で実行し、ONかOFFを選びます(初期設定ではオン)。", inline=True)
    try:
        await owner.send(content=greeting_message,embeds=[embed,embed2,embed3])
        await owner.send("よくある勘違いとして「すでにいるメンバーも専科から抜けると自動でキックされる」というものがありますがそのような機能はありません(50人規模のサーバーでないと現実的ではない)\nまた、Sekamの制限を外したいときは私をキックしてください。\n私のアイコンをクリックしたら下くらいにある「アプリを追加」から簡単に再追加できます。\n[プライバシーポリシー](https://death.kakikou.app/sekam/privacy/ )を一応書いてますが個人情報を集める機能がそもそも備わってないので気にしなくて大丈夫だと思います。気にする必要が出てきたら場合また連絡します。\n最後に、お問い合わせとか機能の要望はこのDMに送られても気づけないので開発者(DiscordID:@kakik0u)に連絡して下さい。")
        print(f"サーバー {guild.name} のオーナー {owner.name} にDMを送信しました。")
    except discord.HTTPException:
        print(f"サーバー {guild.name} のオーナー {owner.name} にDMを送信できませんでした。")


class setting(discord.app_commands.Group):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="log",description="ログチャンネルを指定できます。")
    @discord.app_commands.describe(channel="ログを送信するチャンネル(Botが見えている必要があります。)")
    async def logchsetting(self,ctx:discord.Interaction,channel:discord.TextChannel):
       if not ctx.user.guild_permissions.administrator:
        await ctx.response.send_message("管理者権限がないのに設定変更しようだなんて、貴様もしやスパムか！？？！？！？", ephemeral=True)
        return
       data = dict(loadjson("logchannel.json"))
       key = str(ctx.guild.id)
       keydata=list(data.keys())
       chid=str(channel.id)
       view = discord.ui.View()
       button = discord.ui.Button(style=discord.ButtonStyle.danger, label="ログ送信をテストする", custom_id="logtest")
       view.add_item(button)
       if key in keydata:
         del data[key]
         data[key] = chid
         savejson("logchannel.json",data)
         await ctx.response.send_message("設定を変更しました。",view=view,ephemeral=True)
       else:
         data[key] = chid
         savejson("logchannel.json",data)
         await ctx.response.send_message("設定されました。",view=view,ephemeral=True)
            
    @app_commands.command(name="ban",description="BANするかしないか")
    @discord.app_commands.describe(
    setting="初期設定ではキックになっています。"
    )
    @discord.app_commands.choices(
    setting=[
        discord.app_commands.Choice(name="BANする",value="on"),
        discord.app_commands.Choice(name="キックで許す(BANしない)",value="off"),
    ]
    )
    async def bansetting(self,ctx: discord.Interaction,setting:str):
       if not ctx.user.guild_permissions.administrator:
        await ctx.response.send_message("管理者権限がないのに設定変更しようだなんて、貴様もしやスパムか！？？！？！？", ephemeral=True)
        return
       data = dict(loadjson("ban.json"))
       key = str(ctx.guild.id)
       keydata=list(data.keys())
       chid=str(setting)
       if key in keydata:
         del data[key]
         data[key] = chid
         savejson("ban.json",data)
         message1="設定を変更しました。"
       else:
         data[key] = chid
         savejson("ban.json",data)
         message1="設定されました。"
       if chid=="on":
          message1=message1+"BANには追加権限が必要なことがあります。初回の場合は[このボタン](https://discord.com/oauth2/authorize?client_id=1240458222121259030&permissions=2054&scope=bot)から追加権限を付与してください。"
       await ctx.response.send_message(message1,ephemeral=True)
    @app_commands.command(name="blacklist",description="ブラックリストを設定できます。")
    @discord.app_commands.describe(setting="初期設定ではオンになっています。")
    @discord.app_commands.choices(
    setting=[
        discord.app_commands.Choice(name="ブラックリストに参加します",value="on"),
        discord.app_commands.Choice(name="ブラックリストに参加しません",value="off"),
    ]
    )
    async def blacklist(self,ctx:discord.Interaction,setting:str):
       if not ctx.user.guild_permissions.administrator:
        await ctx.response.send_message("管理者権限がないのに設定変更しようだなんて、貴様もしやスパムか！？？！？！？", ephemeral=True)
        return
       data = dict(loadjson("configblack.json"))
       key = str(ctx.guild.id)
       keydata=list(data.keys())
       chid=str(setting)
       if key in keydata:
         del data[key]
         data[key] = chid
         savejson("configblack.json",data)
         await ctx.response.send_message("設定を変更しました。",ephemeral=True)
       else:
         data[key] = chid
         savejson("configblack.json",data)
         await ctx.response.send_message("設定されました。",ephemeral=True)
       
    
bot=discord.ext.commands.Bot
tree.add_command(setting(bot))
     
@client.event
async def on_interaction(inter:discord.Interaction):
    try:
        if inter.data['component_type'] == 2:
            await on_button_click(inter)
    except KeyError:
        pass
async def on_button_click(inter:discord.Interaction):
  custom_id = inter.data["custom_id"]
  if custom_id == "logtest":
    data=loadjson("logchannel.json")
    logchannelid=find_key(data, str(inter.guild.id))
    logch=client.get_channel(int(logchannelid))
    try:
        await logch.send("テスト送信")
        await inter.response.send_message("ちゃんと動きました",ephemeral=True)
    except:
        await inter.response.send_message("エラーが発生しました。SEKAMがそのチャンネルを見ること/送信することができるかご確認ください。",ephemeral=True)
  


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
