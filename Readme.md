## Background
This was implemented as a semester project of my course Blockchain and Cryptocurrency was just intended to create to pass the project NOT FOR PROFESSIONAL OR FINAL PROJECT USE.

## Description:
This is an Identity management system that takes information of a new person as well as take picture of the person upload it on blockchain after securing it with multisignature. To retrieve an information of a person, a piece of information has to be given along with the picture of that person and all the information about that person will be retrieve. There are four scripts: two clients and two servers.

## Pre-requisites

### 1: Install multichain:
#### Windows:
Download https://www.multichain.com/download/multichain-windows-2.3.3.zip and, either\
\
a: Extract its CONTENTS (not the whole folder but all the individual file i.e: multichain-util, etc.) to C:/. But then you can only access multichain tools from cmd in C:/.\
or\
b: Extract it to any folder you like but put the folder in environment variable. Then you can access multichain tools from any folder in cmd.\

#### Linux:
	su
	cd /tmp
	wget https://www.multichain.com/download/multichain-2.3.3.tar.gz
	tar -xvzf multichain-2.3.3.tar.gz\
	cd multichain-2.3.3\
	mv multichaind multichain-cli multichain-util /usr/local/bin #to make easily accessible on the command line
	exit #to return to your regular user

### 2: Run multichain block chain
2.1:  Create ID chain

	multichain-util create IDChain
2.2: Run ID chain

    multichain IDChain -daemon
2.3 create stream

	multichain-cli  IDChain create stream identity_stream true
	multichain-cli IDChain subscribe identity_stream

2.4: Replace IP Adresses in your client script with appropriate Server IP Address

## Working
### Input
Run server-input script, then run client-input script, write appropriate Information, write appropriate location of the person's picture (Make sure picture is clear and front facing)
### Retrieve info
Run server-retrieve script, the run client retrieve script, put right info in it, write location of new picture to match if the person retrieving info is the same.
Enjoy!

