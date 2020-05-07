from pyrogram import *
import requests , json
app = Client("instagram")

sudo = 989484046

@app.on_message()
def echo(client, message):
	text = message.text
	chat_id = message.chat.id
	user_name = message.from_user.first_name
	user_id = message.from_user.id
	g = open("data/users.txt", "r")
	users = str(user_id) in g.read()
	f = open("data/ban.txt", "r")
	banned_users = str(user_id) in f.read()
	if banned_users == False:
		if users == False and user_id != sudo:
			g = open("data/users.txt", "a")
			g.write("{}\n".format(user_id))
		if text == "/start":
			message.reply_text("Please Send Instagram username\nLike This : \n**@th3_developer**")
		elif "@" in text:
			text = text.replace("@","")
			api = requests.get("https://www.instagram.com/{}/?__a=1".format(text))
			api = api.text
			try:
				api = json.loads(api)
				photo = api["graphql"]["user"]["profile_pic_url_hd"]
				name = api["graphql"]["user"]["full_name"]
				bio = api["graphql"]["user"]["biography"]
				follow = api["graphql"]["user"]["edge_follow"]["count"]
				followed = api["graphql"]["user"]["edge_followed_by"]["count"]
				id = api["graphql"]["user"]["id"]
				message.reply_photo(photo,caption = "- Name : `{}`\n- Bio : \n`{}`\n- Follow : `{}`\n- Followed : `{}`\n- User Id : `{}`\n\n.".format(name,bio,follow,followed,id))
			except:
				message.reply_text("**There is an error in username**")
		elif "/block" in text and user_id == sudo:
			text = text.replace("/block ","")
			f = open("data/ban.txt", "a")
			f.write("{}\n".format(text))
			message.reply_text("[{}](tg://user?id={}) was banned".format(user_name,user_id),disable_web_page_preview = True)
		elif "/bc" in text and user_id == sudo:
			text = text.replace("/bc ","")
			ulist = open("data/users.txt", "r")
			for user in ulist:
				app.send_message(user,"{}".format(text))
			message.reply_text("Message was sent to all bot users")
	else:
		message.reply_text("You are Banned")
		


app.run()  # Automatically start() and idle()
