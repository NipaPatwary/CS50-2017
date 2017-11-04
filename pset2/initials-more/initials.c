#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    // prompt name from the user
    string s = get_string();

    // if first character isn't blank space, print it in upper case
    if(s[0] != ' ')
    {
        printf("%c", toupper(s[0]));
    }

    // iterate through string provided by user
    for(int i = 0, l = strlen(s); i < l; i++)
    {

        // if current character isn't blank space but character before it - is, print the current character in upper case
        if(s[i] != ' ' && s[i - 1] == ' ')
        {
            printf("%c", toupper(s[i]));
        }
    }

    printf("\n");
}