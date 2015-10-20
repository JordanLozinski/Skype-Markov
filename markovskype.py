#markovskype.py

#markov

import re, random, sqlite3

databangs = "C:\\Users\\Jordan\\AppData\\Roaming\\Skype\\ultimamax12\\main.db"


chainlength = 2
stopword = "\x02"
maxwords = 30
markov = {}

def xml_check(message):
	if message:
		return message[0] == "<"
	else:
		return True

def sanitize_message(message): #removes quotes from message and converts it all to lower case
    return re.sub('[\"\']', '', message.lower())

def parse_sentence(msg):
	try:
		print("PARSING " + msg)
	except UnicodeEncodeError:
		pass
	msg = sanitize_message(msg)
	for w1, w2, w3 in split_message(msg):
		key = (w1, w2)
		if key in markov:
			markov[key].append(w3)
		else:
			markov[key] = [w3]

def split_message(msg):
	words = msg.split()

	if len(words) > chainlength:
		words.append(stopword)
		for i in range(len(words)-chainlength):
			yield words[i:i+chainlength+1]


def generate_message():
	key = random.choice(list(markov.keys()))
	seenwords = []
	for i in range(maxwords):
		seenwords.append(key[0])
		print(markov[key])
		nextword = random.choice(markov[key])

		if nextword == stopword:
			if random.random() > .333:
				break
			else:
				seenwords
		key = (key[1], nextword)
	return ' '.join(seenwords)

def main():
	database = sqlite3.connect(databangs)
	cursor = database.cursor()
	author = input("skype username of desired target? ")
	cursor.execute("SELECT * FROM Messages WHERE author=\'" + author + "\'")
	for row in cursor:
		if xml_check(row[17]) == False:
			parse_sentence(row[17])
	print(generate_message())
	while True:
		eval(input("eval: "))

main()