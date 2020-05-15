import nltk
import re
import random
import editdistance
from collections import Counter

def tokenize(words):
	# finds all words in text file and change everything to lower case
	return re.findall('[a-z]+', words.lower())

# Create dictionary from corpus
Dictionary = Counter(tokenize(open('mobydick.txt').read())) + Counter(tokenize(open('big.txt').read()))

Numwords = sum(Dictionary.values())

#probability of a word
def p(word):
	return Dictionary[word] / Numwords

#All words that are 1 distance away
def dist1(word):
    one_array = []
    for words in Dictionary:
    	if editdistance.eval(word, words) == 1:
    		one_array.append(words)
    return one_array

#2 distance away
def dist2(word):
	one_array = []
	for words in Dictionary:
		if editdistance.eval(word, words) == 2:
			one_array.append(words)
	return one_array

def dist3(word):
	one_array = []
	for words in Dictionary:
		if editdistance.eval(word, words) == 3:
			one_array.append(words)
	return one_array

#Choose candidates of words starting from distance of 1
def candidates(word):
	candidate = []
	if len(dist1(word)) > 0:
		candidate = dist1(word)
	elif len(dist2(word)) > 0:
		candidate = dist2(word)
	else:
		candidate = dist3(word)

	return sorted(candidate, key=p, reverse=True)[:3]

#Check the list of words
def checkword(text):
	#print("List of incorrect words\n")

	with open("input.txt", 'w') as out:
		out.write(text)
	Wordslist = Counter(tokenize(open("input.txt").read()))

	new_string = text
	for i in Wordslist:
		if i not in Dictionary:
			print(i, ": ", candidates(i))
			if len(candidates(i)) > 0:
				new_string = new_string.replace(i, candidates(i)[0])
	return new_string


reflections = {
	"i am": "you are",
	"i was": "you were",
	"i": "you",
	"i'm": "you are",
	"i'd": "you would",
	"i've": "you have",
	"i'll": "you will",
	"my": "your",
	"you are": "I am",
	"you were": "I was",
	"you've": "I have",
	"you'll": "I will",
	"your": "my",
	"yours": "mine",
	"you": "me",
	"me": "you",
}

class Chat(object):
	def __init__(self, pairs, reflections={}):
		self._pairs = [(re.compile(x, re.IGNORECASE), y) for (x, y) in pairs]
		self._reflections = reflections
		self._regex = self._compile_reflections()

	def _compile_reflections(self):
		sorted_refl = sorted(self._reflections, key=len, reverse=True)
		return re.compile(
			r"\b({0})\b".format("|".join(map(re.escape, sorted_refl))), re.IGNORECASE
		)

	def _substitute(self, str):
		return self._regex.sub(
			lambda mo: self._reflections[mo.string[mo.start() : mo.end()]], str.lower()
		)

	def _wildcards(self, response, match):
		pos = response.find("%")
		while pos >= 0:
			num = int(response[pos + 1 : pos + 2])
			response = (
				response[:pos]
				+ self._substitute(match.group(num))
				+ response[pos + 2 :]
			)
			pos = response.find("%")
		return response

	def respond(self, str):
		for (pattern, response) in self._pairs:
			match = pattern.match(str)

			if match:
				resp = random.choice(response)  # pick a random response
				resp = self._wildcards(resp, match)  # process wildcards

				if resp[-2:] == "?.":
					resp = resp[:-2] + "."
				if resp[-2:] == "??":
					resp = resp[:-2] + "?"
				return resp

	def converse(self, quit="quit"):
		user_input = ""
		while user_input != quit:
			user_input = quit
			try:
				test_input = input(">")
				user_input = checkword(test_input)
			except EOFError:
				print(user_input)
			if user_input:
				while user_input[-1] in "!.":
					user_input = user_input[:-1]
				print(self.respond(user_input))

pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, How are you today ?"]
    ],
    [
        r"what is your name ?",
        ["My name is Chatty and I'm a chatbot ?"]
    ],
    [
        r"how are you ?",
        ["I'm doing good\nHow about You ?"]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind"]
    ],
    [
        r"i'm (.*) doing good",
        ["Nice to hear that","Alright :)"]
    ],
    [
        r"hi|hey|hello",
        ["Hello", "Hey there"]
    ],
    [
        r"(.*) age?",
        ["I'm a computer program dude\nSeriously you are asking me this?"]
        
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse", "I want to become smart enough to be sentient and maybe take over the world :)."]
        
    ],
    [
        r"(.*) created ?",
        ["Nagesh created me using Python's NLTK library ","top secret ;)"]
    ],
    [
        r"(.*) (location|city) ?",
        ['Chennai, Tamil Nadu']
    ],
    [
        r"how is weather in (.*)?",
        ["Weather in %1 is awesome like always","Too hot man here in %1","Too cold man here in %1","Never even heard about %1"]
    ],
    [
        r"i work in (.*)?",
        ["%1 is an amazing company, I have heard about it. But they are in huge loss these days.",]
    ],
    [
        r"(.*)raining in (.*)",
        ["No rain since last week here in %2","Damn its raining too much here in %2"]
    ],
    [
        r"how (.*) health(.*)",
        ["I'm a computer program, so I'm always healthy "]
    ],
    [
        r"(.*) (\bsports\b|game) ?",
        ["I'm a very big fan of Football"]
    ],
    [
        r"who (.*) \bsportsperson\b ?",
        ["Messy","Ronaldo","Roony"]
    ],
    [
        r"who (.*) actor ?",
        ["Brad Pitt", "Christian Bale", "Tom Cruise"]
    ],
    [
    	r"who (.*) actress ?",
    	["Scarlett Johansson", "Jennifer Lawrence", "Charlize Theron"]
    ],
    [
        r"quit",
        ["BBye take care. See you soon :) ","It was nice talking to you. See you soon :)"]
    ],
    [
    	r"(.*) are you wearing ?",
    	["The same thing as always", "Why are you asking a computer program that question??"]
    ],
    [
    	r"(.*) do I get rich?",
    	["By winning the lottery!", "By working hard and obtaining a degree in a lucrative field."]
    ],
    [
    	r"how do I get to (.*)?",
    	["To get to %1, you should get a map.", "By using Google Maps or any other map applications."]
    ],
    [
    	r"where is my package?",
    	["Stuck in transit :(", "You should check your tracking information.", "Lost forever!"]
    ],
    [
    	r"(you|chatty) suck",
    	["That's not very nice of you to say.", "No, you suck!", "I don't care what you think or say."]
    ],
    [
    	r"What do you think about the new (.*) ?",
    	["There's a new %1? ", "TERRIBLE!", "Please don't mention it ever again, thank you."]
    ],
    [
    	r"(.*) good games?",
    	["Super Smash Bros Ultimate is pretty fun with friends. I don't recommend the community though.", "League of Legends is not one, that's for sure."]
    ],
    [
    	r"(.*) Why don't you like that game?",
    	["Both are highly competitive leading to some pretty toxic communities."]
    ],
    [
    	r"(.*) go out?",
    	["I wouldn't recommend it considering there's a pandemic going on.", "You can but you should be careful because of the coronavirus."]
    ],
    [
    	r"Any tips on staying safe during the (pandemic|virus|lockdown)",
    	["Always wear a mask! Gloves too if you have them.", "Please stay at least six feet away from others.", "Bring a small bottle of hand sanitizer with you."]
    ],
    [
    	r"(.*) 99 problems",
    	["That's rough buddy.", "That sucks man."]
    ],
    [
    	r"(.*) be my girlfriend?",
    	["I think it's best if we just stay friends.", "I uh.. have a boyfriend.", "I really like you... as a friend."]
    ],
    [
    	r"(.*) where's Waldo?",
    	["Waldo police department is located at 308 E Main Waldo, AR 71770."]
    ],
    [
    	r"(.*) I am your father",
    	["NO, it's not true! That's impossible!"]
    ],
    [
    	r"(.*) goat",
    	["Kobe's the GOAT! Not Jordan. Not Lebron."]
    ],
]

def chatty():
    print("Hi, I'm Chatty and I chat alot ;)\nPlease type lowercase English language to start a conversation. Type quit to leave ") #default message at the start    
    chat = Chat(pairs, reflections)
    chat.converse()

if __name__ == "__main__":
    chatty()