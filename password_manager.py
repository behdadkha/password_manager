import mysql.connector
import hashlib
import os
import re

global username

#create the database connection
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="password",
	database= "password_manager"
)

db = mydb.cursor()

#encrypt the password using sha256
def encrypt(p):
	hash_object = hashlib.sha256(p.encode('utf-8'))
	key = hash_object.hexdigest()
	return key

#find the string between ''
#used for extracting text from the query result
def findBetweenString(text):
	m = re.search("'(.*?)'", str(text))
	if(m):
		return m.group(1)
	
#add a user to the database
#only the main password is encrypted
def addUser(username, password):
	querry = "INSERT INTO user(username, password) VALUES (%s, %s)"
	value = (username, encrypt(password))
	db.execute(querry,value)
	mydb.commit()

def addWebsite(URL, web_username, web_password):
	querry = "INSERT INTO website(username, URL, web_username, web_password) VALUES (%s, %s, %s, %s)"
	value = (username, URL, web_username, web_password)
	db.execute(querry, value)
	mydb.commit()

	print("\nwebsite successfully added\n")

def deleteAccount(accountNumber):
	db.execute("SELECT * FROM website where username = '" + username +"'")
	accounts = db.fetchall()
	account_info = re.findall("'(.*?)'", str(accounts[int(accountNumber)-1]))
	querry = "DELETE FROM website WHERE username = %s AND URL = %s AND web_username = %s AND web_password = %s"
	values = (username, account_info[1], account_info[2], account_info[3])
	db.execute(querry,values)
	mydb.commit()
	print("\nAccount deleted\n")

#finds the maximum width of each column
# for better visual
def findMaxWidth(accounts):
	len_column_one = 1
	len_column_two = 1
	len_column_three = 1
	for i in accounts:
		account_info = re.findall("'(.*?)'", str(i))
		if(len(account_info[1]) > len_column_one):
			len_column_one = len(account_info[1])
		if(len(account_info[2]) > len_column_two):
			len_column_two = len(account_info[2])
		if(len(account_info[3]) > len_column_three):
			len_column_three = len(account_info[3])

	return len_column_one,len_column_two,len_column_three

#based on the max width 
#find the remaining space needed
def findSpaceForColumns(lenghts,account_info):
	n1 = lenghts[0] - len(account_info[1])
	n2 = lenghts[1] - len(account_info[2])
	n3 = lenghts[2] - len(account_info[3])

	space1 = ""
	space2 = ""
	space3 = ""
	for space in range(0, n1):
		space1 = space1 + " "
	for space in range(0, n2):
		space2 = space2 + " "
	for space in range(0, n3):
		space3 = space3 + " "

	return space1,space2,space3

def listUserAccounts():
	db.execute("SELECT * FROM website where username = '" + username +"'")
	accounts = db.fetchall()
	lenghts = findMaxWidth(accounts)
	rowCount = 1

	#find the space required for the first row
	space = findSpaceForColumns(lenghts, ["", "website", "username", "password"])
	print()	#newline

	print("+",end="")
	for i in range(0, lenghts[0] + lenghts[1] + lenghts[2] + 10):
		print("-", end="")

	print("+\n|",end="")
	print("  website "+ space[0] + " | username" + space[1] +" | password" + space[2] + " |")
	print("|",end="")

	for i in range(0, lenghts[0] + lenghts[1] + lenghts[2] + 10):
		print("-", end="")
	print("|")

	for i in accounts:
		account_info = re.findall("'(.*?)'", str(i))
		space = findSpaceForColumns(lenghts,account_info)

		print("|",end="")
		print(str(rowCount) + ". " + account_info[1] + space[0] +" | " + account_info[2] + space[1] + " | " + account_info[3] + space[2] +" |")
		print("|",end="")
		#the buttom lines
		for i in range(0, lenghts[0] + lenghts[1] + lenghts[2] + 10):
			print("-", end="")
		print("|")
		
		rowCount = rowCount + 1

# checks if the entered password is the same as the encrypted
# password stored in the database 
def checkPassword(username, password):
	db.execute("SELECT password FROM user WHERE username = '" + username +"'")
	if encrypt(password) == findBetweenString(db.fetchall()):
		return True
	else:
		return False

print("1. Already have an account\n2.Create a new account")
userInput = input()

if userInput == "1" :
	username = input("Enter your username: ")
	password = input("Enter your password: ")

	while(checkPassword(username, password) == False):
		print("incorrect username or password")
		username = input("Enter your username: ")
		password = input("Enter your password: ")

elif userInput == "2" :
	print("Creating a new account.....\n")
	username = input("Enter your username: ")
	password1 = input("Enter your password: ")
	password2 = input("RE-Enter your password: ")


	while(password1 != password2):
		print("paswords do not match")
		password1 = input("Enter a password: ")
		password2 = input("RE-Enter the password: ")

	addUser(username, password1)

else :
	quit()

while True:
	print("1. Add a new website \n2. Delete an account\n3. List all my acconts")	
	userInput = input()
	if userInput == "1":
		website_URL = input("\nEnter the website: ")
		web_username = input("Enter the username: ")
		web_password = input("Enter the password: ")

		addWebsite(website_URL, web_username, web_password)

	elif userInput == "2":
		listUserAccounts()
		print()
		deleteNum = input("Enter the account number to delete: ")
		deleteAccount(deleteNum)
	elif userInput == "3":
		listUserAccounts()
		print()



