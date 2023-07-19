import random
import pandas as pd

OfficialWordList = open('OfficialWordList.txt').read().splitlines()
AnswerList = open('AnswerWordList.txt').read().splitlines()


def playWordle(answer):
    pList = OfficialWordList
    yellows = []
    grays = []
    numGuesses = 0

    for i in range(6):
        guess = random.choice(pList)
        for j in range(5):
            if guess[j] == answer[j]:
                pList = [word for word in pList if word[j] == answer[j]]
            elif (guess[j] in answer) and (yellows.count(guess[j]) < answer.count(guess[j])):
                yellows.append(guess[j])
                pList = [word for word in pList if guess[j] in word]
                pList = [word for word in pList if word[j] != guess[j]]
            else:
                pList = [word for word in pList if word[j] != guess[j]]
                grays.append(guess[j])

            badChars = [char for char in grays if char not in yellows]
            pList = [word for word in pList if not any(char in word for char in badChars)]

        numGuesses += 1
        if answer == guess:
            return [1, numGuesses]

    return [0, 6]


def countVowels(word):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    count = 0
    for char in word:
        if char in vowels:
            count += 1
    return count


# Returns the number of duplicate sets and the highest degree of duplicity among these sets
def countDuplicates(word):
    prevMen = set()  # Set of previously mentioned characters
    dupLets = set()  # Duplicate letters
    count = 1
    for char in word:
        if char in prevMen:
            count += 1
            dupLets.add(char)
        prevMen.add(char)
    return [len(dupLets), count]


def main():
    targetWords = []
    winStatus = []
    NumGuesses = []
    vowels = []
    duplicateSets = []
    duplicateDegree = []
    itr = 100

    for word in AnswerList:
        duplicateData = countDuplicates(word)
        numVowels = countVowels(word)
        for i in range(itr):
            targetWords.append(word)
            result = playWordle(word)
            winStatus.append(result[0])
            NumGuesses.append(result[1])
            duplicateSets.append(duplicateData[0])
            duplicateDegree.append(duplicateData[1])
            vowels.append(numVowels)

    data = {
        'TargetWord': targetWords,
        'WinStatus': winStatus,
        'NumGuesses': NumGuesses,
        'Vowels': vowels,
        'DuplicateSets': duplicateSets,
        'DuplicateDegree': duplicateDegree
    }

    df = pd.DataFrame(data)
    df.to_csv('wordleData.csv', index=False)


if __name__ == "__main__":
    main()