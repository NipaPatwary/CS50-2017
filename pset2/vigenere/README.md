# Specification

Design and implement a program that encrypts messages using Vigenère’s cipher.

Implement your program in a file called vigenere.c in a directory called vigenere.

Your program must accept a single command-line argument: a keyword, k, composed entirely of alphabetical characters.

If your program is executed without any command-line arguments, with more than one command-line argument, or with one command-line argument that contains any non-alphabetical character, your program should print an error (of your choice) and exit immediately, with main returning 1 (thereby signifying an error).

Otherwise, your program must proceed to prompt the user for a string of plaintext, p, (as by a prompt for plaintext:) which it must then encrypt according to Vigenère’s cipher with k, ultimately printing the result (prepended with ciphertext: and ending with a newline) and exiting, with main returning 0.

With respect to the characters in k, you must treat A and a as 0, B and b as 1, …? , and Z and z as 25.

Your program must only apply Vigenère’s cipher to a character in p if that character is a letter. All other characters (numbers, symbols, spaces, punctuation marks, etc.) must be outputted unchanged. Moreover, if your code is about to apply the jth character of k to the ith character of p, but the latter proves to be a non-alphabetical character, you must wait to apply that jth character of k to the next alphabetical character in p; you must not yet advance to the next character in k.

Your program must preserve the case of each letter in p.