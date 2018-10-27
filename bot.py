#! /usr/bin/python3
import discord, math, random, sqlite3, datetime
import requests, json, re, os, shutil, asyncio
from PIL import Image,ImageDraw
from ctypes.util import find_library

TOKEN = os.environ.get('BOT_TOKEN')

ball = ["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]

client = discord.Client()

players = {}
song_queue = {}

async def playNextSong(server, voice_channel):
    discord.opus.load_opus(find_library("opus"))
    try:
        vc = await client.join_voice_channel(voice_channel)
    except:
        if(client.is_voice_connected(server)):
            vc = client.voice_client_in(server)
    if(str(vc.session_id) in song_queue and len(song_queue[str(vc.session_id)]) > 0):
        try:
            player = players[str(vc.session_id)]
            if(not player.is_playing() or player.is_done()):
                player = await vc.create_ytdl_player(song_queue[str(vc.session_id)].pop(0))
                players[str(vc.session_id)] = player
                player.start()
                await asyncio.sleep(player.duration)
                await playNextSong(server, voice_channel)
        except:
            player = await vc.create_ytdl_player(song_queue[str(vc.session_id)].pop(0))
            players[str(vc.session_id)] = player
            player.start()
            await asyncio.sleep(player.duration)
            await playNextSong(message.server, voice_channel)

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Commands are not case sensitive, so we make the whole message lowercase
    msg_chk = message.content.lower();

    if(msg_chk == "!help"):
        embed = discord.Embed(title='Help',description="Below is a list of commands/functions the bot has:")
        embed.add_field(name="Despacito",value="Messages asking Alexa to play Despacito will link to the youtube video for Despacito")
        embed.add_field(name="September",value="Messages alluding to September will link to the youtube video for September (Bass Boosted)")
        embed.add_field(name="its_been",value="Messages in which it has been will send a copy of its_been.mp3")
        embed.add_field(name="VORE",value="Messages containing the forbidden v-word will reset the counter and announce how long it has been since the word was used as well has how many times that user has used the word")
        embed.add_field(name="!bigdickenergy", value="Tells you what percentage Big Dick Energy you have today.")
        embed.add_field(name="!roll XdY",value="Rolls X Y-sided dice and sends back the result")
        embed.add_field(name="!shrug (@ user)",value="Sends back the shrug emoji and optionally mentions another user in the message (Does not work with @ everyone and @ here)")
        embed.add_field(name="!anime",value="Selects a random anime from MyAnimeList (In testing)")
        embed.add_field(name="(Formerly) Valid, now How _ is _", value="If you ask 'How ___ is ___' or 'How ___ am I', the bot will tell you how ___ it is. (With new and improved word selection!)")
        embed.add_field(name="!8ball (question)", value="Ask the 8ball a question and you will receive an answer.")
        embed.add_field(name="!fmk x,y,z", value="Provide the bot with three options and she will select which ones to bed, wed, and behead.")
        embed.add_field(name="!pixel", value="Messages containing an image along with this command will get a 16x16 version of that image returned back. (BETA)")
        embed.add_field(name="Alexa", value="If you ask Alexa to play a youtube link for you while you're connected to a voice channel, she will play it for you!")
        await client.send_message(message.channel, embed=embed)

    if(msg_chk.find("!resetplayer") == 0):
        discord.opus.load_opus(find_library("opus"))
        voice_channel = message.author.voice_channel
        try:
            vc = await client.join_voice_channel(voice_channel)
        except:
            if(client.is_voice_connected(message.server)):
                vc = client.voice_client_in(message.server)
        try:
            player = players[str(vc.session_id)]
            player.stop()
            players[str(vc.session_id)] = None
        except:
            pass
        await vc.disconnect()

    if(msg_chk.find("alexa play ") == 0):
        discord.opus.load_opus(find_library("opus"))
        url = message.content[len("alexa play "):]
        voice_channel = message.author.voice_channel
        try:
            vc = await client.join_voice_channel(voice_channel)
        except:
            if(client.is_voice_connected(message.server)):
                vc = client.voice_client_in(message.server)
        try:
            player = players[str(vc.session_id)]
            if(not player.is_playing()):
                player = await vc.create_ytdl_player(url)
                players[str(vc.session_id)] = player
                player.start()
                await asyncio.sleep(player.duration)
                await playNextSong(message.server, voice_channel)
                t.start()
            elif(player.is_done()):
                player = await vc.create_ytdl_player(url)
                players[str(vc.session_id)] = player
                player.start()
                await asyncio.sleep(player.duration)
                await playNextSong(message.server, voice_channel)
            else:
                msg = "Theres already a song playing, added to queue."
                q = []
                if(str(vc.session_id) in song_queue):
                    q = song_queue[str(vc.session_id)]
                q.append(url)
                song_queue[str(vc.session_id)] = q
                msg = msg + " Current queue is: " + str(q)
                await client.send_message(message.channel, msg)
                return
        except:
            player = await vc.create_ytdl_player(url)
            players[str(vc.session_id)] = player
            player.start()
            await asyncio.sleep(player.duration)
            await playNextSong(message.server, voice_channel)

    if(msg_chk.find("alexa") !=-1 and msg_chk.find("play") != -1 and msg_chk.find("despacito") != -1):
        msg = 'https://www.youtube.com/watch?v=kJQP7kiw5Fk'
        await client.send_message(message.channel, msg)

    if(msg_chk.find("september") != -1 or msg_chk.find("do you remember") != -1):
        msg = 'https://www.youtube.com/watch?v=LI2hcbUf6TQ'
        await client.send_message(message.channel, msg)

    if(msg_chk == "!bigdickenergy"):
        rng = random.randint(0,100)
        msg = message.author.mention+' has '+str(rng)+'% Big Dick Energy.'
        await client.send_message(message.channel, msg)

    if(msg_chk.find("its been") != -1):
        await client.send_file(message.channel, os.environ.get('WORKING_PATH')+'assets/its_been.mp3')

    if(msg_chk.split(" ")[0] == "how" and msg_chk.split(" ")[2] == "is"):
         subject = ""
         adjective = msg_chk.split(" ")[1]
         end = msg_chk.rfind("?")
         if(end != -1):
             subject = message.content[len("how "+adjective+" is "):end]
         else:
             subject = message.content[len("how "+adjective+" is "):]
         percent = random.Random(hash(subject+adjective+str(datetime.datetime.now()))).randint(0,100)
         msg = subject + " is " + str(percent) + "% " + adjective + "."
         await client.send_message(message.channel, msg)

    if(msg_chk.split(" ")[0] == "how" and msg_chk.split(" ")[2] == "am" and msg_chk.split(" ")[3].find("i") == 0):
         adjective = msg_chk.split(" ")[1]
         percent = random.Random(hash(adjective+str(datetime.datetime.now()))).randint(0,100)
         msg = "You are " + str(percent) + "% " + adjective + "."
         await client.send_message(message.channel, msg)

    if(msg_chk.find("!shrug") == 0):
        msg = "¯\_(ツ)_/¯"
        prepend = ""
        if(len(message.mentions) != 0):
            for member in message.mentions:
               prepend = prepend + member.mention + " "
        msg = prepend + msg
        await client.send_message(message.channel, msg)

    if(msg_chk.find("!roll ") == 0):
        params = msg_chk[6:]
        n = int(params.split("d")[0])
        d = int(params.split("d")[1])
        if(not math.isnan(d) and not math.isnan(n) and d>0 and n>0 and d<10001 and n<10001):
            mylist = []
            sum = 0
            for i in range(0,n):
                rng = random.randint(1,d)
                mylist.append(rng)
                sum = sum + rng
            msg = message.author.mention+' rolled a ' + str(mylist) + '. Total is ' + str(sum)
            if(len(msg) > 2000):
                msg = message.author.mention+' rolled a ' + str(sum) + ' on ' +str(n) + ' d' + str(d) + 's'*(n>1) + '.'
                await client.send_message(message.channel, msg)
            else:
                await client.send_message(message.channel, msg)
        else:
            msg = "Parameters are not valid! Please try with more reasonable numbers."
            await client.send_message(message.channel, msg)

    if(msg_chk.find("!8ball ") == 0):
        result = 21 - random.randint(1,20)
        msg = message.author.mention + ' ' + ball[result]
        await client.send_message(message.channel, msg)

    if(msg_chk.find("!fmk ") == 0):
        msg = ""
        params = msg_chk[5:]
        params = params.split(",")
        clean_params = []
        for p in params:
            temp_p = p.lstrip()
            temp_p = temp_p.rstrip()
            clean_params.append(temp_p)
        if(len(clean_params) != 3):
            msg = "Not enough arguments. Command is '!fmk x,y,z"
        else:
            random.shuffle(clean_params)
            msg = "Fuck " + str(clean_params[0]) + ", marry " + str(clean_params[1]) + ", kill " + str(clean_params[2])
        await client.send_message(message.channel, msg)

    if(msg_chk.find("!anime") == 0):
        url = "https://api.jikan.moe/v3/anime/"
        id = random.randint(0,40000)
        r = requests.get(url=url+str(id))
        response = json.loads(r.text)
        while("error" in response):
            id = random.randint(0,32768)
            r = requests.get(url=url+str(id))
            response = json.loads(r.text)
        msg = "Randomly selected anime: " + response["title"]
        await client.send_message(message.channel, msg)

    msg_clean = re.sub("[^A-z0-9 ]","",msg_chk)
    print(msg_clean)
    if("vore" in msg_clean.split(" ") or "vored" in msg_clean.split(" ") or "vores" in msg_clean.split(" ") or "voring" in msg_clean.split(" ")):
        conn = sqlite3.connect(os.environ.get('WORKING_PATH')+'assets/desbotcito_db')
        c = conn.cursor()
        msg = ""
        elapsed_time = 0
        current_time = datetime.datetime.now().timestamp()
        prev_time = 0
        c.execute('SELECT * FROM vore WHERE channel=?', (str(message.channel.id),))
        data = c.fetchall()
        if(len(data) == 0):
            msg = "This is the first time someone has used the v-word."
            c.execute('INSERT INTO vore VALUES (?,?)', (str(message.channel.id), str(current_time)))
        else:
            prev_time = float(data[0][1])
            elapsed_time = datetime.timedelta(seconds = current_time - prev_time)
            days = elapsed_time.days
            hours = int(elapsed_time.seconds/3600)
            minutes = int((elapsed_time.seconds/60)%60)
            seconds = elapsed_time.seconds%60
            msg = message.author.mention+' used the v-word. We went ' + str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' + str(seconds) + ' seconds without mentioning it.';
            c.execute('UPDATE vore SET datetime=? WHERE channel=?', (str(current_time), str(message.channel.id)))
        count = 0
        c.execute('SELECT * FROM voreusage where userid=? AND server=?', (str(message.author),str(message.server)))
        data = c.fetchall()
        if(len(data) == 0):
            count = 1
            c.execute('INSERT INTO voreusage VALUES (?,?,?)', (str(message.author), count, str(message.server)))
        else:
            count = int(data[0][1]) + 1
            c.execute('UPDATE voreusage SET count=? WHERE userid=? AND server=?', (count, str(message.author), str(message.server)))
        mention = message.author.mention+' has used the v-word ' + str(count) + ' time' + 's'*(1 if count>0 else 0) + "."
        await client.send_message(message.channel, msg)
        await client.send_message(message.channel, mention)
        conn.commit()
        conn.close()

    if(message.content == "!pixel"):
        if(len(message.attachments) != 0):
            file = message.attachments[0]
            r = requests.get(file["url"], stream=True, headers={'User-agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                with open(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"], 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

        im = Image.open(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"])
        output_size = 16
        pps = -1
        width = im.size[0]
        height = im.size[1]
        if(width > 1080 or height > 1080):
            msg = "Image is too large! Please try a smaller image."
            await client.send_message(message.channel, msg)
            return
        if(width > height):
            pps = math.ceil(width/output_size)
        else:
            pps = math.ceil(height/output_size)
        data = list(im.getdata())
        im_arr = []
        for i in range(0,len(data),width):
            im_arr.append(data[i:i+width])
        temp_pixel_avg = (0,0,0)
        out_arr = []
        for j in range(0,height,pps):
            for i in range(0,width,pps):
               for y in range(j,j+pps):
                    for x in range(i,i+pps):
                        try:
                            temp0 = temp_pixel_avg[0] + im_arr[y][x][0]
                            temp1 = temp_pixel_avg[1] + im_arr[y][x][1]
                            temp2 = temp_pixel_avg[2] + im_arr[y][x][2]
                            temp_pixel_avg = (temp0,temp1,temp2)
                        except:
                            pass
               avg0 = int(temp_pixel_avg[0]/(pps**2))
               avg1 = int(temp_pixel_avg[1]/(pps**2))
               avg2 = int(temp_pixel_avg[2]/(pps**2))
               temp_pixel_avg = (avg0,avg1,avg2)
               out_arr.append(temp_pixel_avg)
        square_im_arr = []
        for i in range(0,len(out_arr),output_size):
            square_im_arr.append(out_arr[i:i+output_size])
        new_im = Image.new('RGB',(len(square_im_arr[0]),len(square_im_arr)))
        draw = ImageDraw.Draw(new_im)
        for x in range(0,len(square_im_arr[0])):
            for y in range(0,len(square_im_arr)):
                try:
                    draw.point((x,y),fill=square_im_arr[y][x])
                except:
                    pass
        savefile,ext = os.path.splitext(file["filename"])
        new_im.save(os.environ.get("WORKING_PATH")+"pixel/"+savefile+"_icon"+ext)
        await client.send_file(message.channel, os.environ.get("WORKING_PATH")+"pixel/"+savefile+"_icon"+ext)
        os.remove(os.environ.get("WORKING_PATH")+"pixel/"+file["filename"])
        os.remove(os.environ.get("WORKING_PATH")+"pixel/"+savefile+"_icon"+ext)

client.run(TOKEN)
