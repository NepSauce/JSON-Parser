Author: Zawad Atif
ID: B00947033

Program parses a stream of tokens that are either handwritten or
generated via JSON Scanner.

The token stream is then checked for semantic and syntactic errors.
Whenever an exception is encountered the program halts and prints 
out the error message into a file and the terminal.

Usage:

The program allows for <TOKEN_TYPE, TOKEN_VALUE> format.

Run the program via terminal using the command:

python JSONSemantic.py 

Assumptions:

JSON object must be of the specified tokenized format and must
be written into a text file with each line containing just one
token.

The output is seperately created for each input file. Program can 
catch both semantic and syntactic errors but only shows the error type 
for just the semantic errors.
