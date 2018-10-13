import time
import sys									#usado para gerar a palavra aleatória
import random
import os

def m_a():
	text = str(input('\nWrite the code, or write "b" to go back\n'))
	if text == "b": default()
	text = text.split(" / ")
	global word
	word = ""
	
	for x in range (0, len(text)):
		text[x] = text[x].split(" ")
		
		for y in range (0, len(text[x])):
			letter = text[x][y]
			codes = {".-":"a", ".":"e", "..-.":"f",	"....":"h", "..":"i", ".---":"j", ".-..":"l", ".--.":"p", ".-.":"r", "...":"s", "..-":"u", "...-":"v", ".--":"w", ".----":"1", "..---":"2", "...--":"3", "....-":"4", ".....":"5", ".-.-.-":".", "..--..":"?", ".----.":"'", ".-...":"&", "..--.-":"_", ".-..-.":'"', "...-..-":"$", ".--.-.":"@", ".-.-":"a", ".--.-":"a", "..--.":"o", ".-..-":"e", "..-..":"e", ".---.":"j", "...-.":"s", ".--..":"p", "..--":"u"}
			codes2 = {"-...":"b", "-.-.":"c", "-..":"d", "--.":"g", "-.-":"k", "--":"m", "-.":"n", "---":"o", "--.-":"q", "-":"t", "-..-":"x", "-.--":"y", "--..":"z", "-....":"6", "--...":"7", "---..":"8", "----.":"9", "-----":"0", "--..--":",", "-.-.--":"!", "-..-.":"/", "-.--.":"(", "-.--.-":")", "---...":":", "-.-.-.":";", "-...-":"=", "-....-":"-", "-.-..":"c", "--.-.":"g", "-.--.":"h", "--.--":"n", "---.":"o"}

			if letter not in codes and letter not in codes2: 
				print ("\nUNAVAILABLE CODE", end = '')
				sys.exit()
			
			else:
				if letter[0] == ".":
					word = word + (codes[letter])					
				else:
					word = word + (codes2[letter])
		
		word = word + " "	
	return(word)

def default():
	global word, l
	clear()
	print("a) Random word")
	print("b) Write text for your friend")
	op = input("c) Back\n")
	clear()
	
	if op == "c": menu()
	
	elif op == "b":
		print("a) Text in morse")
		print("b) Normal text")
		op = input("c) Back\n")
		
		if op == "a": m_a()
		elif op == "b":
			word = input("\nWrite the word/sentence:\n")
		else: default()
		l = len(word)
		
	else: 
		text = open("wordss.txt").readlines()	#conjunto de mais de 3 mil palavras		
		word = text[random.randint(0, 2998)]							#sorteia uma palavra
		l = (len(word)-1)
		
	starting()	

def menu():
	global name
	clear()
	name = input("Hello! Let's play Hangman! What's your name?\n")
	print('\nWelcome, ', name, '. While playing, you can write "exit" to leave the game or "menu" to come here!\n', sep = '') 
	print("a) Start")
	op = input("b) Exit\n")
		
	if op == "b": sys.exit()
	else: default()							#aparentemente na palavra aleatória tem um a mais de len :/

def starting():		
	clear()										#limpa o cmd
	global chances, guesses, n, letters, l
	letters = ["_"]*l							#usado para para imprimir no cmd como se fosse a palavra, conforme vai acertando vai subtituindo os '_' pelas letras
	chances = 10								#contador das chances
	guesses = [""]*26							#vetor que armazena as letras já foram usadas
	n = 0										#usado para definir a posição de 'guesses'

	print("")
	for x in range(0, len(letters)):			#loop que imprime a palavra, por enquanto ainda com underlines
		if word[x] == " ":						#se ouver espaços na palavra, irá substituir o underline por ' '
			print(" ", end = ' ')
			letters[x] = " "
		else:
			print("_", end = ' ')				#imprime os underlines
			
	print("\n\nGood Luck, ", name, "!", end = ' ', sep = '')

	print("\n\nLetters used: ", end = '')				#imprime as letras usadas
	for x in range(0, 27):
		if guesses[x] != "":
			print(guesses[x], ", ", end = '', sep = '')
		else: break
	game()
	print("\nWould you like to play again?")
	print("a) Yes, please")
	op = input("b) No, thank you\n")
	
	if op == "a": 
		menu()
		z = 1
		
def game():
	global chances, guesses, n, letters
	while chances > 0:
			
		print("\n\nChances:", chances)
		guess = input("\nGuess a character:\n") 	#adivinhar caractere
			
		if guess == "exit": 
			print("Word:", word)
			sys.exit()
		
		elif guess == "menu": 
			print("\nWord:", word)
			time.sleep(2)
			menu()
				
		clear()
		print("")
		
		if guess == " " or len(guess) > 1 or guess == "": 
			for z in range(0, len(letters)):
				print(letters[z], end = ' ')
			print("\n\nUnavailable character(s)", end = '')
		
		elif guess in guesses:					#se o caractere já foi usado anteriormente
			for z in range(0, len(letters)):	#imprime os underlines e depois a mensagem
				print(letters[z], end = ' ')
			print("\n\nYou already guessed this letter", end = '')
		
		else:
			guesses[n] = guess					#caso seja a primeira vez do caratere, ele será armazenado
			n+=1								#posição da lista de caracteres sobe
			
			if guess in word:					#se o caractere estiver correto
				for z in range(0, len(letters)):
					if word[z] == guess:		
						letters[z] = word[z]	#substitui o underline pela letra
			else:
				chances-=1						#se o caractere não estiver correto, o nº de chances diminui 
			
			for z in range(0, len(letters)):
					if letters[z] == " ": print(" ", end = ' ')  #imprime novamente os underlines e/ou com a letras já adivinhadas
					else: print(letters[z], end = ' ')	
					
			if guess in word: print("\n\nYey! You got one!", end = '')  #imprime diferentes mensagens se o caractere estiver correto ou não
			else: print("\n\nWrong guess", end = '')
			
			if "_" not in letters:								#se não houver mais underlines, o jogador ganhou
				print("\n\nCongratulations ", name, "! You win!", sep = '')
				break									#sai do jogo	
		
		print("\n\nLetters used: ", end = '')				#imprime as letras usadas
		for x in range(0, 27):
			if guesses[x] != "":
				print(guesses[x], ", ", end = '', sep = '')
			else: break
		
	if chances == 0: print("\n\nOh no, you lose...", "\nWord:", word)	#se as chances acabarem e sair do loop, mensagem de fim
	return()

if __name__ == "__main__":
	clear = lambda: os.system('cls')			#usado para limpar o cmd
	menu()	
