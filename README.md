# Honeywords
Password-cracking detection using honeywords
Inspired from **Honeywords: Making Password-Cracking Detectable** by Ari Juels and Ronald L. Rivest - [link](http://people.csail.mit.edu/rivest/honeywords/)

## Overview
This project provides additional security for a login system in the case of password hashes leaking. For each user, k-1 additional passwords are generated and their hashes are stored. By doing this, an attacker who can reverse the hashes for those generated passwords can not distinguish the correct password (*sugarword*) from the others (*honeywords*).

A *honeychecker* (secure server) is used to supervise the authentications and report incidents in case of attacks. The key idea in this method is to be able to generate passwords that look real in order to achieve honeypot *flatness*.

For the simplicity of the project, only the webserver is used here, but the honeychecker behavior is simulated correctly.

Two methods from the paper are implemented:

- take-a-tail
- chaffing-with-a-password-model (uses first 10k passwords from the RockYou dataset)

## Project structure
    .
    ├── static               # stylesheets for the webserver
    ├── templates            # HTML files for flask
    ├── attack.py            # attacker script
    ├── honeywords.py        # honeyword generation module
    ├── rockyou_10000.txt    # first 10k passwords from the RockYou dataset, used in chaffing
    ├── users_chaffing.db    # chaffing database
    ├── users_tail.db        # take-a-tail database
    └── Proiect IC.pdf       # Romanian description of this implementation


## How to run
  1. Install flask for Python 2.7: 
```
pip install flask
```

  2. Run the webserver with the generation method given as argument: 
```
python webserver.py [take-a-tail|chaffing]
```

  3. Register an user [here](127.0.0.1:5000/register) and memorize the credentials.

  4. Run the attacker script to see the information an attacker who reverses hashes would get: 
```
python attacker.py username [take-a-tail|chaffing]
```

  5. (optional) Login with one of the passwords [here](127.0.0.1:5000/) obtained by the attacker to simulate a real scenario.