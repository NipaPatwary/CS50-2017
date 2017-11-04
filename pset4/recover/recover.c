#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>

typedef uint8_t BYTE;

// define BUFFER struct
typedef struct
{
    BYTE buffer[512];
} __attribute__((__packed__))
BUFFER;

int main(int argc, char *argv[])
{

    // ensure proper usage
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // declare file to open and input/output pointers
    char *infile = argv[1];
    FILE *inptr;
    FILE *outptr;

    // open input file
    inptr = fopen(infile, "r");
    if(inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // declare b as BUFFER
    BUFFER b;

    // keep track of number of jpg files
    int jpgCount = 0;

    //keep track if jpg file is already being written
    bool isWriting = false;

    // store jpg files in array
    char filename[50];

    // read through 512 byte blocks to find jpg headers
    while(fread(&b, sizeof(BUFFER), 1, inptr) == 1)
    {
        // when found, check if jpg is already being written
        if(b.buffer[0] == 0xff && b.buffer[1] == 0xd8 && b.buffer[2] == 0xff && (b.buffer[3] & 0xf0) == 0xe0)
        {
            // if yes, close that file and set isWriting to false
            if(isWriting)
            {
                fclose(outptr);
                isWriting = false;
            }

            // save filename with title of current jpg number, open it and write bytes
            sprintf(filename, "%03i.jpg", jpgCount);
            outptr = fopen(filename, "w");
            fwrite(&b, sizeof(BUFFER), 1, outptr);

            // increment jpgCount and set state of isWriting to true
            jpgCount++;
            isWriting = true;
        }
        // if buffer block doesn't contain jpg header, but file is already being written, just continue writing
        else
        {
            if(isWriting)
            {
                fwrite(&b, sizeof(BUFFER), 1, outptr);
            }
        }
    }
    return 0;
}