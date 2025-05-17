#!/usr/bin/env python
#		Apply a wpgtk/pywal color scheme to Firefox and Thunderbird.
#		Copyright (C) 2025	Suyooo
#
#		This program is free software: you can redistribute it and/or modify
#		it under the terms of the GNU General Public License as published by
#		the Free Software Foundation, either version 3 of the License, or
#		(at your option) any later version.
#
#		This program is distributed in the hope that it will be useful,
#		but WITHOUT ANY WARRANTY; without even the implied warranty of
#		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
#		GNU General Public License for more details.
#
#		You should have received a copy of the GNU General Public License
#		along with this program.	If not, see <https://www.gnu.org/licenses/>.

import sys, os
import configparser, json
import msgpack, lzma, base64
import webbrowser, email.generator, email.mime.multipart, email.mime.text, tempfile, time
from os.path import expanduser

def json_url_encode(theme):
	packed = msgpack.packb(theme)
	compressed = lzma.compress(packed, format=lzma.FORMAT_ALONE)
	return base64.urlsafe_b64encode(compressed).decode("utf-8")

def json_url_decode(b64):
	compressed = base64.urlsafe_b64decode((b64 + "==").encode("utf-8"))
	packed = lzma.decompress(compressed, format=lzma.FORMAT_ALONE)
	return msgpack.unpackb(packed)

def hex_to_rgb(h):
	 return {
			"r": int(h[1:3], 16),
			"g": int(h[3:5], 16),
			"b": int(h[5:7], 16)
	 }

def create_theme():
	keywords_config = configparser.ConfigParser()
	keywords_config.read(expanduser("~/.config/wpg/keyworfddfds.conf"))
	keywords = {} if len(keywords_config.sections()) == 0 else { k: keywords_config["default"][k] for k in keywords_config["default"] }
	colors = json.load(open(expanduser("~/.cache/wal/colors.json"), "r"))

	theme = json.load(open(os.path.join(sys.path[0], "theme.json"), "r"))
	for k in theme["colors"]:
		v = theme["colors"][k]
		if type(v) is not dict:
			if v in colors["colors"]: theme["colors"][k] = hex_to_rgb(colors["colors"][v])
			elif v in colors["special"]: theme["colors"][k] = hex_to_rgb(colors["special"][v])
			elif v in keywords: theme["colors"][k] = hex_to_rgb(keywords[v])
			elif v.startswith("#"): theme["colors"][k] = hex_to_rgb(v)
			else: raise Exception("Property " + k + " in theme has unexpected value " + v)
	
	return theme

cmd_opt = "url" if len(sys.argv)==1 else sys.argv[1]
if cmd_opt == "-h" or cmd_opt == "--help" or cmd_opt == "h" or cmd_opt == "help":
	print("Usage: wpgtk-firefox-themer.py [mode or Firefox Color URL]")
	print("")
	print("Modes:")
	print("  url     Default. Output the Firefox Color URL to stdout")
	print("  ff      Open the Firefox Color URL in default browser (probably Firefox)")
	print("  tb      Open a message containing the URL in Thunderbird (thunderbird must be in PATH, and should already be open)")
	print()
	print("If a Firefox Color URL is passed as the argument, it will be decoded into JSON as a base for your own theme config.")
	exit()
elif cmd_opt.startswith("https://color.firefox.com/?theme="):
	print(cmd_opt[33:])
	print(json.dumps(json_url_decode(cmd_opt[33:]), indent="\t"))
else:
	url = "https://color.firefox.com/?theme=" + json_url_encode(create_theme())
	if cmd_opt == "url":
		print(url)
	elif cmd_opt == "ff":
		webbrowser.open(url)
	elif cmd_opt == "tb":
		msg = email.mime.multipart.MIMEMultipart()
		msg["To"] = "you@computer"
		msg["From"] = "wpgtk-firefox-themer@computer"
		msg["Subject"] = "Here's your Firefox Color theme!"
		msg.attach(email.mime.text.MIMEText(url, "plain"))
		
		with tempfile.NamedTemporaryFile("w", suffix=".eml", delete_on_close=False) as tmp:
			emlGenerator = email.generator.Generator(tmp)
			emlGenerator.flatten(msg)
			tmp.flush()
			os.system("thunderbird -file " + tmp.name)
			time.sleep(5)
	else:
		raise Exception("Unknown mode. Check --help for allowed modes")
