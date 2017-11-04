/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // define start, end and middle point of array to search
    int start = 0;
    int end = n - 1;
    int middle = (start + end) / 2;

    // while startpoint is less or equal to endpoint
    while(start <= end)
    {
        // if value found at middle, return true
        if(values[middle] == value)
        {
            return true;
        }
        // if middle is less than value, move startpoint to middle + 1, eliminating left side of array
        else if(values[middle] < value)
        {
            start = middle + 1;
        }
        // if middle is bigger than value, move endpoint to middle - 1, eliminating right side of array
        else if(values[middle] > value)
        {
            end = middle - 1;
        }

        // calculate middle before starting new loop
        middle = (start + end) / 2;
    }

    // if value not found, return false
    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // iterate through values array
    for(int i = 0; i < n; i++)
    {
        // define current value, minimal value, and position of minimal value
        int current = values[i];
        int min = values[i];
        int minPosition = i;

        // for each iteration, compare current value with every other value on right to find minimal value and its position
        for(int j = i; j < n; j++)
        {
            if(values[j] < min)
            {
                min = values[j];
                minPosition = j;
            }
        }

        // swap places of current and minimal values
        values[i] = min;
        values[minPosition] = current;
    }
    return;
}
