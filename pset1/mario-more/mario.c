#include <cs50.h>
#include <stdio.h>

int main(void)
{

    int height;

    //check if entered height is in range of 0-23
    do
    {
    printf("Height: ");
    height = get_int();
    }
    while(height < 0 || height > 23);

    //first loop for each row
    for(int i = 0; i < height; i++) {

    //second for blanks
        for(int j = 1; j < height - i; j++) {
            printf(" ");
        }

    //...and third for bricks
        for(int k = 0; k <= i; k++) {
            printf("#");
        }

    //gap
        printf("  ");

    //other side of pyramid
        for(int k = 0; k <= i; k++) {
            printf("#");
        }

    //end of the row
        printf("\n");
    }

}