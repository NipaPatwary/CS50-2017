import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # create set for positive words and add all words from positive-words.txt
        self.positives = set()

        file = open(positives, "r")
        for line in file:
            if not line.startswith(";"):
                self.positives.add(line.rstrip("\n"))
        file.close()

        # create set for negative words and add all words from negative-words.txt
        self.negatives = set()

        file = open(negatives, "r")
        for line in file:
            if not line.startswith(";"):
                self.negatives.add(line.rstrip("\n"))
        file.close()


    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        if text.lower() in self.positives:
            return 1
        if text.lower() in self.negatives:
            return -1
        return 0
