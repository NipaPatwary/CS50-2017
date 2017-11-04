# Specification

Complete the implementation of find by completing the implementation of search and sort in helpers.c.

search
Your implementation must return false immediately if n is non-positive.

Your implementation must return true if value is in values and false if value is not in values.

The running time of your implementation must be in O(log n).

You may not alter the function’s declaration. Its prototype must remain:

bool search(int value, int values[], int n);
sort
Your implemenation must sort, from smallest to largest, the array of numbers that it’s passed.

Assume that each of the array’s numbers will be non-negative and less than 65,536. But the array might contain duplicates.

The running time of your implementation must be in O(n), where n is the array’s size. Yes, linear! Keep in mind that 65,536 is a constant.

You may not alter the function’s declaration. Its prototype must remain:

void sort(int values[], int n);