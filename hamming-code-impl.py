import numpy as np
import random


G = np.array ([
	[1, 0, 1, 1], 
	[1, 1, 0, 1],
	[0, 0, 0, 1],
	[1, 1, 1, 0],
	[0, 0, 1, 0],
	[0, 1, 0, 0],
	[1, 0, 0, 0]
	])

H = np.array ([
	[0, 0, 0, 1, 1, 1, 1],
	[0, 1, 1, 0, 0, 1, 1],
	[1, 0, 1, 0, 1, 0, 1]
	])


#1 
def block_to_code_word (block):
	
	ans = G.dot(block)
	
	n, m = ans.shape
	for i in range (n):
		ans[i][0] = ans[i][0] % 2
	
	return ans


#2
def code_word_to_checksum_column (code_word):
	
	ans = H.dot(code_word)

	n, m = ans.shape
	for i in range (n):
		ans[i][0] = ans[i][0] % 2

	return ans


#3
def get_wrong (checksum_column, code_word):

	k = ((checksum_column[0] * 2) + checksum_column[1]) * 2 + checksum_column[2]

	if k == 0:
		return code_word

	code_word[k - 1] = 1 - code_word[k - 1]
	return code_word


#4
def string_to_code_string (string):

	ans = []

	for symbol in string:
		k = ord(symbol)

		first_4byte = []
		for i in range (4):
			first_4byte.append([k % 2])
			k //= 2

		second_4byte = []
		for i in range (4):
			second_4byte.append([k % 2])
			k //= 2

		first_4byte.reverse()
		second_4byte.reverse()

		ans.append(np.array(second_4byte))
		ans.append(np.array(first_4byte))


	return ans


#5
def chenge_random_bit (code_word):
	
	rand = random.randint(0, 6)
	code_word[rand] = 1 - code_word[rand]

	return code_word 


def two_blocks_to_char (first_4byte, second_4byte):
	
	k = 0

	for i in (first_4byte):
		k = 2 * k + i[0]

	for i in (second_4byte):
		k = 2 * k + i[0]

	return chr(k)


def code_word_to_block (code_word):
	return [code_word[6], code_word[5], code_word[4], code_word[2]]


#6
def compare_string (string):

	blocks = string_to_code_string (string)

	code_words = []
	for block in blocks:
		code_words.append (block_to_code_word (block))

	change_code_words = []
	for code_word in code_words:
		if (random.randint(1, 100) <= 10):
			change_code_words.append (chenge_random_bit (code_word))
		else:
			change_code_words.append (code_word)


	correct_code_words = []
	for code_word in change_code_words:
		correct_code_words.append (get_wrong (
			code_word_to_checksum_column (code_word), code_word)
		)

	string_ans = ""
	for i in range(0, len(correct_code_words), 2):
		string_ans += two_blocks_to_char (
			code_word_to_block(correct_code_words[i]), 
			code_word_to_block(correct_code_words[i + 1])
			)

	if string != string_ans:
		print ("WRONG!!! (", string, ") not equal (", string_ans, ")")
		exit()
	return string_ans 


print(compare_string ("It's correct program"))
