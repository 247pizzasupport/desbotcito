#! /usr/bin/python3
import discord, math, random, sqlite3, datetime
import requests, json, re, os

TOKEN = os.environ.get('BOT_TOKEN')

ball = ["It is certain.","It is decidedly so.","Without a doubt.","Yes - definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful."]

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msg_chk = message.content.lower();

    if(msg_chk.find("alexa") !=-1 and msg_chk.find("play") != -1 and msg_chk.find("despacito") != -1):
        msg = 'https://www.youtube.com/watch?v=kJQP7kiw5Fk'
        await client.send_message(message.channel, msg)

    if(msg_chk.find("september") != -1 or msg_chk.find("do you remember") != -1):
        msg = 'https://www.youtube.com/watch?v=LI2hcbUf6TQ'
        await client.send_message(message.channel, msg)

    if(msg_chk == "!bigdickenergy"):
        rng = random.randint(0,100)
        msg = message.author.mention+' has '+str(rng)+'% Big Dick Energy,'
        await client.send_message(message.channel, msg)

    if(msg_chk.find("its been") != -1):
        await client.send_file(message.channel, os.environ.get('WORKING_PATH')+'assets/its_been.mp3')

    if(msg_chk.find("how valid is ") == 0):
        subject = ""
        end = msg_chk.rfind("?")
        if(end != -1):
            subject = message.content[len("how valid is "):end]
        else:
            subject = message.content[len("how valid is "):]
        validity = random.Random(hash(subject+str(datetime.datetime.now()))).randint(0,100)
        msg = subject + " is " + str(validity) + "% valid."
        await client.send_message(message.channel, msg)

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
        embed.add_field(name="Valid", value="If you ask 'How valid is ___', the bot will tell you how valid it is. (With new and improved pseudo-randomness!)")
        embed.add_field(name="!8ball", value="Ask the 8ball a question and you will receive an answer.")
        embed.add_field(name="!fmk x,y,z", value="Provide the bot with three options and she will select which ones to bed, wed, and behead.")
        await client.send_message(message.channel, embed=embed)

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
        if(not math.isnan(d) and not math.isnan(n)):
            list = []
            sum = 0
            for i in range(0,n):
                rng = random.randint(1,d)
                list.append(rng)
                sum = sum + rng
            msg = message.author.mention+' rolled a ' + str(list) + '. Total is ' + str(sum)
            if(len(msg) > 2000):
                for i in range(0,len(msg),2000):
                    await client.send_message(message.channel, msg[i:i+2000])
            else:
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

    if("vore" in msg_chk.split(" ") or "vored" in msg_chk.split(" ") or "vores" in msg_chk.split(" ") or "voring" in msg_chk.split(" ")):
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

client.run(TOKEN)
