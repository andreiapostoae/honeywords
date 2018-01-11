import cPickle
import time
import sys

def attack(username, run_mode):
	db_name = 'users_tail.db' if run_mode == 'take-a-tail' else 'users_chaffing.db'

	with open(db_name, 'rb') as input_db:
		db = cPickle.load(input_db)

	(_, honeywords, hashes, tough_nuts) = db[username]
	print tough_nuts
	possible_passwords = []

	print "Found %d MD5 hashes: " % len(honeywords), hashes, "\n"
	for i in range(len(honeywords)):
		print "Trying to find a match for the hash number %d... " % (i+1)
		time.sleep(0.5)

		if tough_nuts[i]:
			print "Found a tough nut, could not find a matching password in reasonable time."
			possible_passwords.append('?')
		else:
			print "Found possible password: ", honeywords[i]
			possible_passwords.append(honeywords[i])
		print ""

	print possible_passwords


if __name__ == '__main__':
	attack(sys.argv[1], sys.argv[2])