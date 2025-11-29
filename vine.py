import discord, random
from discord.ext import commands
from deep_translator import GoogleTranslator  # 번역 라이브러리
from langdetect import detect # 언어 감지 라이브러리
from discord.ui import Button, View
import os
from dotenv import load_dotenv

load_dotenv('D:\\Project\\vine\\.env')
TOKEN = os.getenv('DISCORD_TOKEN')
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# intents 설정 (권한)
intents = discord.Intents.default()
intents.messages = True 
intents.message_content = True 

# 번역 모드 상태
translation_state = False 

# 봇 상태 설정
activity = discord.Game(name='명령어 확인은 "바인아 도움"')

# 명령어 접두사는 '바인아 + 띄어쓰기까지'
client = commands.Bot(command_prefix='바인아 ', intents=intents, activity=activity)

# 종료 및 오프라인
@client.command(name='vineOut', hidden=True)
async def shutdown(ctx):
    if ctx.author.id != ADMIN_ID: 
        await ctx.send("이 명령어는 관리자만 사용할 수 있습니다.")
        return
    await ctx.send('봇을 종료합니다. 🛑')
    await client.close()

# 안녕 명령어
@client.command(aliases=['안녕', '안녕하세요', 'ㅎㅇ', '하이', '헬로', 'ㅎ2']) 
async def hello(ctx): 
    m = random.randrange(1,6) 
    if m == 1:
        await ctx.send('반가워요, {}님!'.format(ctx.author.display_name))
    elif m == 2:
        await ctx.send('{}님 보고 싶었어요. 🥺'.format(ctx.author.display_name))
    elif m == 3:
        await ctx.send('좋은 하루네요, {}님!'.format(ctx.author.display_name))
    elif m == 4:
        await ctx.send('안녕하세요, {}님!'.format(ctx.author.display_name))
    elif m == 5:
        await ctx.send('인사 받아드릴까요? 🤭')

# 도움말
@client.command(name='도움')
async def help(ctx):
     embed = discord.Embed(title = "📢  Vine 도움말", description = '**바인 사용법입니다!**', color=0xA9A9F5)
     embed.add_field(name = "1️⃣ 바인아 안녕", value = '`바인과 간단한 인사를 나눌 수 있어요.\n추가로 "안녕하세요", "ㅎㅇ", "하이", "헬로", "ㅎ2"가 가능하답니다!`', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "2️⃣ 바인아 잘자", value = '`바인이 다정한 인사를 보내줘요.`', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "3️⃣ 바인아 번역", value = '`원하는 문장을 보내면, 바인이 열심히 번역해줘요.\n번역모드 실행 중에도 명령어를 실행할 수 있어요.`', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "4️⃣ 번역끝", value = '`번역을 중단하고 싶다면, "번역끝" 또는 "tr_end"를 입력해 주세요.`', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "5️⃣ 바인아 바보", value = '`바인을 마음껏 놀려보세요 😁`', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "\n", value = '\n', inline=False)
     embed.add_field(name = "6️⃣ 바인아 가위바위보", value = '`바인과 가위바위보를 즐겨보세요!`', inline=False)
    
     embed.set_footer(text = f"{ctx.message.author.name}", icon_url = ctx.message.author.avatar.url)
     embed.set_thumbnail(url="https://i.ibb.co/PvP5vWsx/vine.jpg")
     await ctx.send(embed = embed)

# 번역 명령어
@client.command(name='번역')
async def translation(ctx):
    global translation_state
    translation_state = True 
    await ctx.send('**번역 모드를 시작합니다.**\n`원하는 문장을 보내주시면 자동으로 번역 됩니다.\n`')
        
@client.event
async def on_message(message):
    global translation_state
    if message.author == client.user: 
        return
    
    if message.content.startswith('바인아'):  
        await client.process_commands(message)
        return

    # 번역모드일 때
    if translation_state:
        if message.content == "번역끝" or message.content == "tr_end":
            translation_state = False 
            await message.channel.send('`번역 모드를 종료합니다. 필요하시면 언제든 불러주세요!`')
            return
        if message.content == "바인아 번역":
            await message.channel.send('`번역모드를 실행중입니다. 번역을 원하는 문장을 보내주세요!`')
            return

        try:
            content = message.content
            lang = None

            # "nice", "hi" 같은 짧은 영어 해결
            if content.isascii():
                lang = 'en'
            else:
                try:
                    lang = detect(content)
                except:
                    # "ㅎㅇ" 처럼 너무 짧아서 감지 못하면 그냥 무시 (에러 방지)
                    lang = None

            # 2. 한국어 번역
            if lang == 'ko':
                print(lang)
                res_japanese = GoogleTranslator(source='auto', target='ja').translate(message.content)
                res_english = GoogleTranslator(source='auto', target='en').translate(message.content)

                embed = discord.Embed(title = '✨ '+message.content, description = '', color=0xA9A9F5)
                embed.add_field(name = '', value = f"**Japanese :** {res_japanese}", inline=False)
                embed.add_field(name = '', value = f"**English :** {res_english}", inline=False)
                await message.channel.send(embed = embed)

            # 3. 일본어 번역
            elif lang == 'ja':
                print(lang)
                res_korean = GoogleTranslator(source='auto', target='ko').translate(message.content)
                res_english = GoogleTranslator(source='auto', target='en').translate(message.content)
                embed = discord.Embed(title = '✨ '+message.content, description = '', color=0xA9A9F5)
                embed.add_field(name = '', value = f"**Korean :** {res_korean}", inline=False)
                embed.add_field(name = '', value = f"**English :** {res_english}", inline=False)
                await message.channel.send(embed = embed)

            # 4. 영어 번역
            elif lang == 'en':
                print(lang)
                res_korean = GoogleTranslator(source='auto', target='ko').translate(message.content)
                res_japanese = GoogleTranslator(source='auto', target='ja').translate(message.content)
                embed = discord.Embed(title = '✨ '+message.content, description = '', color=0xA9A9F5)
                embed.add_field(name = '', value = f"**Korean :** {res_korean}", inline=False)
                embed.add_field(name = '', value = f"**Japanese :** {res_japanese}", inline=False)
                await message.channel.send(embed = embed)
        
        except Exception as e:
            # 언어 감지 실패하거나 너무 짧은 단어일 때 에러 방지
            print(f"번역 에러: {e}")
            
    await client.process_commands(message)
    return

# 잘자 명령어
@client.command(name='잘자', aliases=['굿나잇'])
async def good_night(ctx):
    m = random.randrange(1,6)
    if m == 1:
        await ctx.send('안녕히 주무세요, {}님! 악몽은 바인이 가져갈게요. 😇'.format(ctx.author.display_name))
    elif m == 2:
        await ctx.send('오늘 하루도 고생했어요, {}님! 🌙'.format(ctx.author.display_name))
    elif m == 3:
        await ctx.send('{}님, 저랑 조금만 더 놀면 안 돼요? 🥺'.format(ctx.author.display_name))
    elif m == 4:
        await ctx.send('바인이도 잘게요 흐아암..🥱'.format(ctx.author.display_name))
    elif m == 5:
        await ctx.send('좋은 꿈 꿔요 {}님 😌'.format(ctx.author.display_name))

# 바보 명령어
@client.command(name='바보', aliases=['메롱', '멍청이'])
async def joke(ctx):
    m = random.randrange(1,7)
    if m == 1:
        await ctx.send('저도 화는 낼 줄 알아요. 🤬')
    elif m == 2:
        await ctx.send('놀리지 마세요...😒')
    elif m == 3:
        await ctx.send('흥! 기다리세요 예솔님이 혼내주실 거예요. 😤')
    elif m == 4:
        await ctx.send('조만간 {}님보다 똑똑해 질걸요? 😁'.format(ctx.author.display_name))
    elif m == 5:
        await ctx.send('열심히 배우고 있는 걸요 😒')
    elif m == 6:
        await ctx.send('{}님도 바보멍청이!! 😥'.format(ctx.author.display_name))     

# 가위바위보
@client.command(name='가위바위보')
async def rock_s_p(ctx):
    rsp = ['가위', '바위', '보']

    async def button_callback(interaction: discord.Interaction):
        user_choice = interaction.data['custom_id']
        bot_choice = random.choice(rsp)

        bot_emoji = {'가위': '✌', '바위': '✊', '보': '🖐'}[bot_choice]
        user_emoji = {'가위': '✌', '바위': '✊', '보': '🖐'}[user_choice]

        result = rsp.index(user_choice) - rsp.index(bot_choice)
        if result == 0:
            outcome = "비겼어요! 마음이 통했네요 😏"
        elif result == 1 or result == -2:
            outcome = f"{interaction.user.display_name}님이 이겼네요! 다음번엔 바인이 이겨볼게요 🤩"
        else:
            outcome = "우왕 제가 이겼네요 😎" 

        await interaction.response.edit_message(content=f"**{user_emoji} vs {bot_emoji}**\n\n{outcome}", view=None)

    rock = Button(label="✊", style=discord.ButtonStyle.gray, custom_id="바위")
    scissors = Button(label="✌", style=discord.ButtonStyle.gray, custom_id="가위")
    paper = Button(label="🖐", style=discord.ButtonStyle.gray, custom_id="보")

    for btn in [rock, scissors, paper]:
        btn.callback = button_callback

    view = View()
    view.add_item(rock)
    view.add_item(scissors)
    view.add_item(paper)

    await ctx.send("가위바위보는 바인이 또 장인인걸요 (¬‿¬)\n선택해 주세요!", view=view)

client.run(TOKEN)