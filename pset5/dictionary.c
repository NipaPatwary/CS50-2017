/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// create node structures for linked lists
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// create hashtable with 50 buckets
#define HASHSIZE 50
node *hashtable[HASHSIZE];

// djb2 hash function (by Daniel J. Bernstein)
unsigned long hash(const char *str)
{
    unsigned long hash = 5381;
    int c = 0;

    while (c == *str++)
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }

    return hash % HASHSIZE;
}

// keep track of number of words in dictionary
int wordCount = 0;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // find in which bucket word should be
    int i = hash(word);

    // define first node of linked list (head) and cursor
    node *head = hashtable[i];
    node *cursor = head;

    // iterate through linked list and compare strings
    while(cursor != NULL)
    {
        if(strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // try to open dictionary
    FILE *dct = fopen(dictionary, "r");
    if(dct == NULL)
    {
        return false;
    }

    // declare variable to store words from dictionary
    char dctWord[LENGTH + 1];

    // scan dictionary word by word
    while(fscanf(dct, "%s", dctWord) != EOF)
    {
        // get memory for node to store words into
        node *new_node = malloc(sizeof(node));

        // if returns NULL, quit the speller, else set dctWord as new_node value
        if(new_node == NULL)
        {
            unload();
            return false;
        }
        // else copy word from dictionary to node, find its position in hashtable,
        // link it to first node in that linked list, and move head to that node. increment word count
        else
        {
            strcpy(new_node->word, dctWord);
            int head = hash(dctWord);
            new_node->next = hashtable[head];
            hashtable[head] = new_node;
            wordCount++;
        }
    }
    fclose(dct);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return wordCount;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // iterate through hashtable and free all nodes in each bucket (linked list)
    for(int i = 0; i < HASHSIZE; i++)
    {
        node *cursor = hashtable[i];

        while(cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
