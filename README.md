# volatile-broadside
An automated report builder for the Volatility Memory Forensics Framework. 

There are many commands that will be run in most investigations. This script runs them and saves the output. 

USAGE:

broadside.py [OPTIONS] FILE

broadside.py -v path/to/volatility -f FILE 

-v, --volalility PATH 

	Sets the path to the volatility executable
	
-f, --file FILE 

	Path to memeory image
	
-a, --add COMMAND 

	Adds a command to be run
	
-r, --remove COMMAND 

	Removes a command

TO-DO:

-Make the HTML/CSS report pretty and colorful 

-Add support for Gnu/Linux and Mac OSX memory images 

-Get the list of valid profiles from volatility 
