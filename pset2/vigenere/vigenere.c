#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // check if argument 1 (key) is provided
    if(!argv[1])
    {
        printf("Please, provide ONE key consisting of LETTERS.\n");
        return 1;
    }

    // check if number of arguments is 2
    // iterate through argument 1 to check if every character is a letter
    // if not - return error code 1
    for(int i = 0, l = strlen(argv[1]); i < l; i++)
    {
        if(argc != 2 || !isalpha(argv[1][i]))
        {
            printf("Please, provide ONE key consisting of LETTERS.\n");
            return 1;
        }
    }

    string k = argv[1];

    printf("plaintext: ");
    string p = get_string();

    printf("ciphertext: ");

    // iterate through plaintext and key
    for(int i = 0; i < strlen(p); i++)
    {
        // if key is shorter than plaintext, continue shifting plaintext with the key from the beginning
        int j = i % strlen(k);

        // shift only letters
        // for each letter in both plaintext and key that is lower case, substract 32 from it
        // then add the result of given formula to 97 for lower case, and 65 for upper case letters
        if(isalpha(p[i]))
        {
            if(islower(p[i]))
            {
                if(islower(k[j]))
                {
                    printf("%c", (char) 97 + (p[i] - 32 + k[j] - 32) % 26);
                }
                else if(isupper(k[j]))
                {
                    printf("%c", (char) 97 + (p[i] - 32 + k[j]) % 26);
                }

            }
            else if(isupper(p[i]))
            {
                if(islower(k[j]))
                {
                    printf("%c", (char) 65 + (p[i] + k[j] - 32) % 26);
                }
                else if(isupper(k[j]))
                {
                    printf("%c", (char) 65 + (p[i] + k[j]) % 26);
                }
            }
        }
        else
        {
            printf("%c", p[i]);
        }
    }
    printf("\n");
    return 0;
}