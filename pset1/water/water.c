#include <cs50.h>
#include <stdio.h>

int main(void)
{
    printf("Minutes: ");
    int minutes = get_int();

    int bottles = minutes * 1.5 * 128 / 16;
    printf("Bottles: %i\n", bottles);
}