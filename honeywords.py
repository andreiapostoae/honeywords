import sys
import hashlib
from random import shuffle, randint, choice
import string


def apply_md5(pw_list):
	hashed_list = []

	for pw in pw_list:
		m = hashlib.md5()
		m.update(pw)
		hashed_list.append(m.hexdigest())

	return hashed_list


def generate_honeywords_tail(password_plaintext, tail, honeypot_size=5):
	honeywords = []
	honeywords.append(password_plaintext + tail)
	tail_number = int(tail)
	tail_size = len(tail)

	while len(honeywords) != honeypot_size:
		new_random = str(randint(100, 999))
		skip = 0

		for word in honeywords:
			word_tail = word[-tail_size:]
			same_digit = 0

			for i in range(3):
				if word_tail[i] == new_random[i]:
					same_digit += 1

			if same_digit >= 2:
				skip = 1
				break

		if skip == 1:
			continue
		else:
			honeywords.append(password_plaintext + new_random)

	shuffle(honeywords)
	idx = honeywords.index(password_plaintext + tail)

	tough_nuts = [False] * len(honeywords)
	return (idx, honeywords, apply_md5(honeywords), tough_nuts)


def generate_honeywords_chaffing(password_plaintext, honeypot_size):
	with open('rockyou_10000.txt') as f:
		passwords = f.readlines()

	passwords = [x.strip() for x in passwords]
	honeywords = [password_plaintext]

	for i in range(honeypot_size - 1):
		tough_nut_chance = randint(1, 100)
		if tough_nut_chance <= 8:
			honeywords.append(''.join(choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(randint(15, 20))))
			continue
		else:
			starting_pw = choice(passwords)
			length = len(starting_pw)

			new_pw = starting_pw[0]

			for j in range(length - 1):
				rng = randint(1, 10)

				while len(starting_pw) != length:
					starting_pw = choice(passwords)

				if rng == 1:
					starting_pw = choice(passwords)

					while len(starting_pw) != length:
						starting_pw = choice(passwords)

				elif rng >= 2 and rng <= 5:
					starting_pw = choice(passwords)

					while len(starting_pw) != length:
						starting_pw = choice(passwords)

						if len(starting_pw) == length:
							if new_pw[j] != starting_pw[j]:
								continue
							
							break

				new_pw += starting_pw[j + 1]

			honeywords.append(new_pw)

	shuffle(honeywords)
	idx = honeywords.index(password_plaintext)
	return (idx, honeywords, apply_md5(honeywords), [True if len(x) >= 15 else False for x in honeywords])


if __name__ == '__main__':
	# print generate_honeywords_tail('apo1', '590')
	with open('rockyou.txt') as f:
		passwords = f.readlines()


	honeywords = generate_honeywords_chaffing('computer123', 20)
	print honeywords



