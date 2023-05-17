from upload import uploadData
from checkIndex import checkdata
from getDataS import getdata
from getDataID import getdataisbnUid
from dataCluster import clusterData

#MENU

def menu():
	options = {
		1: option_1,
		2: option_2,
		3: option_3,
		4: option_4,
		5: quit
	}
    
	while True:
		print("Menu:")
		print("1. Upload a File to ElasticSearch")
		print("2. Check via index")
		print("3. Retrieve Data from ElasticSearch")
		print("4. Data Cluster")
		print("5. Quit")
		choice = int(input("Enter your choice: "))
		if choice in options:
			options[choice]()
		else:
			print("Invalid choice.")

def option_1():
	fname=input("Give the name of File: ")
	iname=input("Give the index of File: ")
	uploadData(fname, iname)
	print(75 * "=")
	print("Upload Completed!".center(75))
	print(75 * "=")

def option_2():
	iname=input("Give the index of File you are searching: ")
	checkdata(iname)

def option_3():
	keyword = input("Give the keyword: ")
	print("1. Search with simply metric")
	print("2. Search with uid metric")
	choice = int(input("Choice: "))
	if choice == 1:
		books = getdata('books', keyword)
		print('MATCH QUERY METRIC'.center(75, '='))
		print(books.loc[:, ['book_title', 'book_author', 'score']])
		print(75 * "=")
	elif choice == 2:
		user = int(input("Give user id: "))
		ch = input("Use neural network? [Y/n]: ").lower().strip()
		if ch == 'y':
			state = True
		else:
			state = False
		books = getdataisbnUid(keyword, user, activate_nn=state)
		print('MATCH QUERY METRIC THROUGH USER ID'.center(75, '='))
		print(books.loc[:, ['book_title', 'book_author', 'score']])
		print(75 * "=")

def option_4():
	print('1. Euclidean Distance')
	print('2. Cosine Similarity')
	ch = int(input('Choice: '))
	dist = 'cosine_similarity'
	if ch == 1:
		dist = 'euclidean_distance'
	clusterData(dist)


def quit():
	print("Quitting.")
	exit()

menu()