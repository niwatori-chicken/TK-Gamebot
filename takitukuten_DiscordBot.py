from asyncio import tasks
import discord
import random
from discord.ext import commands

bot = commands.Bot(command_prefix="ttg!", intents=discord.Intents.all())
bot.remove_command("help")

dedicated_channel_id=1085154401091584061

player1 = "none"
player2 = "none"

player1_hp = 50
player2_hp = 50
player1_mp = 25
player2_mp = 30

player1_def = 0
player2_def = 0

player1_card = []
player2_card = []

player1_deck = []
player2_deck = []

player1_card_v = []
player2_card_v = []

player1_pray_c = 0
player2_pray_c = 0

cards = ["00","01","02","03","04","05","06","07"]

game = 0
turn = 0
turns = 0

player1_ok = 0
player2_ok = 0
    

@bot.event
async def on_ready():
    print("起動完了")

@bot.command()
async def play(ctx): #ゲームプレイ開始

    if ctx.channel.id == dedicated_channel_id :
        global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp

        if ctx.author.bot: #botならスルー
            return
        
        if player1 == "none" : #プレイヤー1が参加したとき
            player1 = ctx.author
            await ctx.send(str(player1.name) + "が対戦相手を募集しています。")

        elif player2 == "none" and player1 != ctx.author : #プレイヤー2が参加したとき
            player2 = ctx.author
            await ctx.send(str(player2.name) + "が参加しました。 ゲームが開始します。")
            game = 1
            await player2.send("デッキを選択してください。(ttg!deckはDMで使用できます。)")
            await player1.send("デッキを選択してください。(ttg!deckはDMで使用できます。)")

        elif player2 == "none" and player1 == ctx.author : #プレイヤー1がすでに参加しているとき
            await ctx.send("既にゲームに参加しています。")

        else : #すでにゲームが開始されているとき
            await ctx.send("ゲームが既にプレイされています。")

    else : #専用チャンネル以外
        await ctx.send("専用チャンネルを使用してください。")

@bot.command()
async def exit(ctx): #ゲームプレイから退出

    if ctx.channel.id == dedicated_channel_id :
        global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,player1_ok,player2_ok,player1_mp,player2_mp,turn,player1_def,player2_def,turns,player1_pray_c,player2_pray_c

        if ctx.author.bot: #botならスルー
            return

        if player1 == ctx.author :#プレイヤー1の時
            await ctx.send(str(player1.name) + "が退出しました。")
            player1 = player2
            player2 = "none"
            player1_deck = player2_deck
            player2_deck = []
            
            if game == 1 or game == 2: #残りプレイヤーが居なくなった時
                await ctx.send("プレイヤーが一人になったため、ゲームが終了しました。")
                player1 = "none"
                player1_card = []
                player2_card = []
                player1_hp = 50
                player2_hp = 50
                player1_mp = 25
                player2_mp = 30
                player1_def = 0
                player2_def = 0
                player1_pray_c = 0
                player2_pray_c = 0
                player1_deck = []
                player2_deck = []
                player1_ok = 0
                player2_ok = 0
                turn = 0
                turns = 0
            game = 0
 
        elif player2 == ctx.author : #プレイヤー2の時
            await ctx.send(str(player2.name) + "が退出しました。")
            player2 = "none"
            await ctx.send("プレイヤーが一人になったため、ゲームが終了しました。")
            player1 = "none"
            player1_card = []
            player2_card = []
            player1_hp = 50
            player2_hp = 50
            player1_mp = 25
            player2_mp = 30
            player1_def = 0
            player2_def = 0
            player1_pray_c = 0
            player2_pray_c = 0
            turns = 0
            player1_deck = []
            player2_deck = []
            game = 0
            turn = 0

        else : #そもそも参加していないとき
            await ctx.send(ctx.author.name + "は参加していません。")
 
    else : #専用チャンネル以外
        await ctx.send("専用チャンネルを使用してください。")

@bot.command()
async def ok(ctx):

    if ctx.channel.id == dedicated_channel_id :

        global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,player1_ok,player2_ok,turn,player1_card_v,player2_card_v,player1_mp,turns

        def card_type(card_id) : #カード変換定義

            if card_id == "00" :
                return "ノーマルアタック(00)"

            if card_id == "01" :
                return "癒しの詩(01)"
            
            if card_id == "02" :
                return "テンションビッツ(02)"
            
            if card_id == "03" :
                return "クレイジースロット(03)"
            
            if card_id == "04" :
                return "スキルハンター(04)"
            
            if card_id == "05" :
                return "回避(05)"
            
            if card_id == "06" :
                return "小さな祈り(06)"
            
            if card_id == "07" :
                return "パワーアタック(07)"


        if ctx.author.bot: #botならスルー
            return

        if player1 == ctx.author and player1_deck != []:

            if game == 1 and player1_ok == 0:
                player1_ok = 1
                await ctx.send(str(player1.name) + "が準備を完了しました。")

                if player2_ok == 1 :
                    await ctx.send("両者の準備が完了しました。 戦闘開始！")
                    await ctx.send(str(player1.name)+"のターンです。")
                    turn = 1
                    turns = 1
                    await ctx.send(str(turns)+"ターン目")
                    game = 2
                    player1_mp = player1_mp + 5
                    i = 0

                    while i < 4 :
                        player1_card += [player1_deck[random.randint(0, 7)]]
                        i = i + 1

                    i = 0
                    while i < 4 :
                        player2_card += [player2_deck[random.randint(0, 7)]]
                        i = i + 1

                    await player1.send("自分のHP: "+str(player1_hp)+"\n自分のMP: "+str(player1_mp)+"\n\n相手のHP: "+str(player2_hp)+"\n相手のMP: "+str(player2_mp)+"\n\n自分の手札: ")
                    
                    for v in player1_card :
                        player1_card_v = player1_card_v + [card_type(v)]

                    await player1.send(str(player1_card_v))

            else :
                await ctx.send("ゲームが開始していないまたは既に完了しています。")

        elif player2 == ctx.author and player2_deck != [] :

            if game == 1 and player2_ok == 0:
                player2_ok = 1

                await ctx.send(str(player2.name) + "が準備を完了しました。")

                if player1_ok == 1 :
                    await ctx.send("両者の準備が完了しました。 戦闘開始！")
                    await ctx.send(str(player1.name)+"のターンです。")
                    turn = 1
                    turns = 1
                    await ctx.send(str(turns)+"ターン目")
                    game = 2
                    player1_mp = player1_mp + 5
                    i = 0

                    while i < 4 :
                        player1_card += [player1_deck[random.randint(0, 7)]]
                        i = i + 1
                    i = 0

                    while i < 4 :
                        player2_card += [player2_deck[random.randint(0, 7)]]
                        i = i + 1

                    await player1.send("自分のHP: "+str(player1_hp)+"\n自分のMP: "+str(player1_mp)+"\n\n相手のHP: "+str(player2_hp)+"\n相手のMP: "+str(player2_mp)+"\n\n自分の手札: ")
                    
                    for v in player1_card :
                        player1_card_v = player1_card_v + [card_type(v)]
                    
                    await player1.send(str(player1_card_v))
            
            else :
                await ctx.send("ゲームが開始していないまたは既に完了しています。")
        
        else :
            await ctx.send("ゲームに参加していないまたはデッキを選択していません。")
    
    else :
        await ctx.send("専用チャンネルを使用してください。")

@bot.command()
async def end(ctx):
    global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,player1_ok,player2_ok,player1_mp,player2_mp,turn,player1_card_v,player2_card_v,turns,player1_def,player2_def
    if ctx.channel.id == dedicated_channel_id :
        def card_type(card_id) :
            if card_id == "00" :
                return "ノーマルアタック(00)"
            if card_id == "01" :
                return "癒しの詩(01)"
            if card_id == "02" :
                return "テンションビッツ(02)"
            if card_id == "03" :
                return "クレイジースロット(03)"
            if card_id == "04" :
                return "スキルハンター(04)"
            if card_id == "05" :
                return "回避(05)"
            if card_id == "06" :
                return "小さな祈り(06)"
            if card_id == "07" :
                return "パワーアタック(07)"
        if ctx.author.bot:
            return
        if game == 2 :
            if player1 == ctx.author and turn == 1 :
                player2_mp = player2_mp + 5
                player2_def = 0
                if player2_mp > 49 :
                    player2_mp = 50
                turn = 2
                turns += 1
                await ctx.send(str(turns)+"ターン目")
                player2_card_v = []
                player1_card_v = []
                if len(player2_card) < 8 :
                    player2_card += [player2_deck[random.randint(0, 7)]]
                await ctx.send("ターンが終了しました。 "+str(player2.name)+"のターンです。")
                await player2.send("自分のHP: "+str(player2_hp)+"\n自分のMP: "+str(player2_mp)+"\n\n相手のHP: "+str(player1_hp)+"\n相手のMP: "+str(player1_mp)+"\n\n自分の手札: ")
                for v in player2_card :
                    player2_card_v = player2_card_v + [card_type(v)]
                await player2.send(str(player2_card_v))
            if player2 == ctx.author and turn == 2 :
                player1_mp = player1_mp + 5
                player1_def = 0
                if player1_mp > 49 :
                    player1_mp = 50
                turn = 1
                turns += 1
                await ctx.send(str(turns)+"ターン目")
                player2_card_v = []
                player1_card_v = []
                if len(player1_card) < 8 :
                    player1_card += [player1_deck[random.randint(0, 7)]]
                await ctx.send("ターンが終了しました。 "+str(player1.name)+"のターンです。")
                await player1.send("自分のHP: "+str(player1_hp)+"\n自分のMP: "+str(player1_mp)+"\n\n相手のHP: "+str(player2_hp)+"\n相手のMP: "+str(player2_mp)+"\n\n自分の手札: ")
                for v in player1_card :
                    player1_card_v = player1_card_v + [card_type(v)]
                await player1.send(str(player1_card_v))
    else :
        await ctx.send("専用チャンネルを使用してください。")
@bot.command()
async def card(ctx,arg1):
    global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,player1_ok,player2_ok,player1_mp,player2_mp,turn,player1_card_v,player2_card_v,player1_def,player2_def,turns,player1_pray_c,player2_pray_c
    async def draw(draw,player) :
        global player1_card,player2_card
        await ctx.send(str(player.name)+"が"+str(draw)+"枚ドローしました。")
        if player == player1 :
                i = 0
                while i < draw :
                    if len(player1_card) < 8 :
                        player1_card += [player1_deck[random.randint(0, 7)]]
                    i = i + 1
        if player == player2 :
                i = 0
                while i < draw :
                    if len(player2_card) < 8 :
                        player2_card += [player2_deck[random.randint(0, 7)]]
                    i = i + 1
    async def mp(mp,player) :
        global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,player1_ok,player2_ok,player1_mp,player2_mp,turn,player1_card_v,player2_card_v
        if player == player1 :
            player1_mp += mp
            if player1_mp > 49 :
                    player1_mp = 50
        if player == player2 :
            player2_mp += mp
            if player2_mp > 49 :
                    player2_mp = 50
        if mp < 0 :
                await ctx.send(str(player.name)+"のMPが"+str(mp)+"減った！")
        if mp > 0 :
                await ctx.send(str(player.name)+"のMPが"+str(mp)+"増えた！")
    async def hp(hp,player,armor) :
        global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,player1_ok,player2_ok,player1_mp,player2_mp,turn,player1_card_v,player2_card_v,player1_pray_c,player2_pray_c
        if hp < 0 :
            if armor > 0 :
                await ctx.send(str(armor)+"ダメージ防いだ！")
            if hp+armor < 0 :
                await ctx.send(str(player.name)+"に"+str(hp+armor)+"のダメージ！")
        if hp > 0 :
            await ctx.send(str(player.name)+"のHPが"+str(hp)+"回復！")
        if player == player1 :
            if hp < 0 and hp+armor > 0 :
                await ctx.send("無効！")
            else :
                player1_hp += hp+armor
            if player1_hp > 99 :
                player1_hp = 100
            if player1_hp < 1 :
                await ctx.send(str(player.name)+"のHPが0になった！ "+str(player2.name)+"の勝利！")
                player2 = "none"
                player1 = "none"
                player1_card = []
                player2_card = []
                player1_hp = 50
                player2_hp = 50
                player1_mp = 25
                player2_mp = 30
                player1_pray_c = 0
                player2_pray_c = 0
                player1_deck = []
                player2_deck = []
                player1_ok = 0
                player2_ok = 0
                turn = 0
                game = 0
        if player == player2 :
            if hp < 0 and hp+armor > 0 :
                await ctx.send("無効！")
            else :
                player2_hp += hp+armor
            if player2_hp > 99 :
                player2_hp = 100
            if player2_hp < 1 :
                await ctx.send(str(player.name)+"のHPが0になった！ "+str(player1.name)+"の勝利！")
                player2 = "none"
                player1 = "none"
                player1_card = []
                player2_card = []
                player1_hp = 50
                player2_hp = 50
                player1_mp = 25
                player2_mp = 30
                player1_pray_c = 0
                player2_pray_c = 0
                player1_deck = []
                player2_deck = []
                player1_ok = 0
                player2_ok = 0
                turn = 0
                game = 0
    def card_type(card_id) :
        if card_id == "00" :
            return "ノーマルアタック(00)"
        if card_id == "01" :
            return "癒しの詩(01)"
        if card_id == "02" :
            return "テンションビッツ(02)"
        if card_id == "03" :
            return "クレイジースロット(03)"
        if card_id == "04" :
            return "スキルハンター(04)"
        if card_id == "05" :
            return "回避(05)"
        if card_id == "06" :
            return "小さな祈り(06)"
        if card_id == "07" :
            return "パワーアタック(07)"
    if ctx.channel.id == dedicated_channel_id :
        if ctx.author.bot:
            return
        if player1 == ctx.author and turn == 1 :
            if player1_card[0] in arg1 or player1_card[1] in arg1 or player1_card[2] in arg1 or player1_card[3] in arg1 or player1_card[4] in arg1 or player1_card[5] in arg1 or player1_card[6] in arg1 or player1_card[7] in arg1 :
                await ctx.send(str(player1.name)+"が"+str(card_type(arg1))+"を使用した！")
                if arg1 == "00" :
                    if player1_mp > 4 :
                        await hp(-5,player2,player2_def)
                        await mp(-5,player1)
                        player1_card.remove("00")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "01" :
                    if player1_mp > 9 :
                        await mp(-10,player1)
                        await hp(10,player1,0)
                        player1_card.remove("01")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "02" :
                    await hp(-2,player1,player1_def)
                    await mp(10,player1)
                    player1_card.remove("02")
                if arg1 == "03" :
                    if player1_mp > 9 :
                        await mp(-10,player1)
                        await draw(2,player1)
                        player1_card.remove("03")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "04" :
                    if player1_mp > 9 :
                        await mp(-10,player1)
                        take_card = player2_card[random.randint(0, len(player2_card)-1)]
                        player1_card += [take_card]
                        player1_card.remove("04")
                        player2_card.remove(take_card)
                        await ctx.send(str(player2.name)+"から"+str(card_type(take_card))+"を奪いました。")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "05" :
                    await mp(5,player1)
                    await hp(-3,player1,player1_def)
                    player1_def = 99
                    player1_card.remove("05")
                    await ctx.send("次の"+str(player1.name)+"のターンまでのダメージが無効化されます。")
                if arg1 == "06" :
                    await hp(-2,player1,player1_def)
                    player1_pray_c += 1
                    heal_c = 0
                    await ctx.send("祈った回数の合計: "+str(player1_pray_c))
                    if player1_pray_c > 0 :
                        heal_c += 3
                        if player1_pray_c > 2 :
                            heal_c += 3
                            if player1_pray_c > 4 :
                                heal_c += 3
                                if player1_pray_c > 6 :
                                    heal_c += 3
                                    if player1_pray_c > 8 :
                                        await ctx.send("祈った回数が9回に達した！")
                                        await hp(-14,player2,player2_def)
                    await mp(heal_c,player1)
                    player1_card.remove("06")
                if arg1 == "07" :
                    if player1_mp > 11 :
                        await hp(-10,player2,player2_def)
                        await mp(-12,player1)
                        player1_card.remove("07")
                    else :
                        await ctx.send("MPが足りません。")
        elif player2 == ctx.author and turn == 2 :
            if player2_card[0] in arg1 or player2_card[1] in arg1 or player2_card[2] in arg1 or player2_card[3] in arg1 or player2_card[4] in arg1 or player2_card[5] in arg1 or player2_card[6] in arg1 or player2_card[7] in arg1 :
                await ctx.send(str(player2.name)+"が"+str(card_type(arg1))+"を使用した！")
                if arg1 == "00" :
                    if player2_mp > 4 :
                        await hp(-5,player1,player1_def)
                        await mp(-5,player2)
                        player2_card.remove("00")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "01" :
                    if player2_mp > 9 :
                        await mp(-10,player2)
                        await hp(10,player2,0)
                        player2_card.remove("01")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "02" :
                    await hp(-2,player2,player2_def)
                    await mp(10,player2)
                    player2_card.remove("02")
                if arg1 == "03" :
                    if player2_mp > 9 :
                        await draw(2,player2)
                        await mp(-10,player2)
                        player2_card.remove("03")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "04" :
                    if player2_mp > 9 :
                        await mp(-10,player2)
                        take_card = player1_card[random.randint(0, len(player1_card)-1)]
                        player2_card += [take_card]
                        player2_card.remove("04")
                        player1_card.remove(take_card)
                        await ctx.send(str(player1.name)+"から"+str(card_type(take_card))+"を奪いました。")
                    else :
                        await ctx.send("MPが足りません。")
                if arg1 == "05" :
                    await mp(5,player2)
                    await hp(-3,player2,player2_def)
                    player2_def = 99
                    player2_card.remove("05")
                    await ctx.send("次の"+str(player2.name)+"のターンまでのダメージが無効化されます。")
                if arg1 == "06" :
                    await hp(-2,player2,player2_def)
                    player2_pray_c += 1
                    heal_c = 0
                    await ctx.send("祈った回数の合計: "+str(player2_pray_c))
                    if player2_pray_c > 0 :
                        heal_c += 3
                        if player2_pray_c > 2 :
                            heal_c += 3
                            if player2_pray_c > 4 :
                                heal_c += 3
                                if player2_pray_c > 6 :
                                    heal_c += 3
                                    if player2_pray_c > 8 :
                                        await ctx.send("祈った回数が9回に達した！")
                                        await hp(-14,player1,player1_def)
                    await mp(heal_c,player2)
                    player2_card.remove("06")
                if arg1 == "07" :
                    if player2_mp > 11 :
                        await hp(-10,player1,player1_def)
                        await mp(-12,player2)
                        player2_card.remove("07")
                    else :
                        await ctx.send("MPが足りません。")
@bot.command()
async def stat(ctx):
    global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,player1_ok,player2_ok,turn,player1_mp,player2_mp,player1_card_v,player2_card_v,player1_pray_c,player2_pray_c
    if ctx.author.bot:
        return
    def card_type(card_id) :
        if card_id == "00" :
            return "ノーマルアタック(00)"
        if card_id == "01" :
            return "癒しの詩(01)"
        if card_id == "02" :
            return "テンションビッツ(02)"
        if card_id == "03" :
            return "クレイジースロット(03)"
        if card_id == "04" :
            return "スキルハンター(04)"
        if card_id == "05" :
            return "回避(05)"
        if card_id == "06" :
            return "小さな祈り(06)"
        if card_id == "07" :
            return "パワーアタック(07)"
    if player1 == ctx.author :
        player2_card_v = []
        player1_card_v = []
        await ctx.author.send("自分のHP: "+str(player1_hp)+"\n自分のMP: "+str(player1_mp)+"\n\n相手のHP: "+str(player2_hp)+"\n相手のMP: "+str(player2_mp)+"\n\n自分の手札: ")
        for v in player1_card :
            player1_card_v = player1_card_v + [card_type(v)]
        await player1.send(str(player1_card_v))        
    elif player2 == ctx.author :
        player2_card_v = []
        player1_card_v = []
        await ctx.author.send("自分のHP: "+str(player2_hp)+"\n自分のMP: "+str(player2_mp)+"\n\n相手のHP: "+str(player1_hp)+"\n相手のMP: "+str(player1_mp)+"\n\n自分の手札: ")
        for v in player2_card :
            player2_card_v = player2_card_v + [card_type(v)]
        await player2.send(str(player2_card_v))
@bot.command()
async def deck(ctx,arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8):
    global game,player1,player2,player1_deck,player2_deck,player1_card,player2_card,player1_hp,player2_hp,cards,player1_ok,player2_ok
    if ctx.author.bot:
        return
    def card_type(card_id) :
        if card_id == "00" :
            return "ノーマルアタック(00)"
        if card_id == "01" :
            return "癒しの詩(01)"
        if card_id == "02" :
            return "テンションビッツ(02)"
        if card_id == "03" :
            return "クレイジースロット(03)"
        if card_id == "04" :
            return "スキルハンター(04)"
        if card_id == "05" :
            return "回避(05)"
        if card_id == "06" :
            return "小さな祈り(06)"
        if card_id == "07" :
            return "パワーアタック(07)"
    if ctx.guild == None :
        if player1 == ctx.author :
            if player1_ok == 0 :
                player1_deck = [arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8]
                if player1_deck[0] not in cards or player1_deck[1] not in cards or player1_deck[2] not in cards or player1_deck[3] not in cards or player1_deck[4] not in cards or player1_deck[5] not in cards or player1_deck[6] not in cards or player1_deck[7] not in cards :
                    await ctx.send("無効です。")
                    player1_deck = []
                else :
                    await ctx.send(str(player1.name) + "が選んだカード: " + str(card_type(arg1)) + "、" + str(card_type(arg2)) + "、" + str(card_type(arg3)) + "、" + str(card_type(arg4)) + "、" + str(card_type(arg5)) + "、" + str(card_type(arg6)) + "、" + str(card_type(arg7)) + "、" + str(card_type(arg8)))
        elif player2 == ctx.author :
            if player2_ok == 0 :
                player2_deck = [arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8]
                if player2_deck[0] not in cards or player2_deck[1] not in cards or player2_deck[2] not in cards or player2_deck[3] not in cards or player2_deck[4] not in cards or player2_deck[5] not in cards or player2_deck[6] not in cards or player2_deck[7] not in cards :
                    await ctx.send("無効です。")
                    player2_deck = []
                else :
                    await ctx.send(str(player2.name) + "が選んだカード: " + str(card_type(arg1)) + "、" + str(card_type(arg2)) + "、" + str(card_type(arg3)) + "、" + str(card_type(arg4)) + "、" + str(card_type(arg5)) + "、" + str(card_type(arg6)) + "、" + str(card_type(arg7)) + "、" + str(card_type(arg8)))
        else :
            await ctx.send("あなたがゲームに参加してないまたはゲームが開始していません。")
    else :
        await ctx.send("DMでのみ実行できます。")

bot.run("token") #実行

"""
総括
ifの入れ子多用はやめよう、せめて3階層までに。
"""