import regex as re

def readLogFile(fileName, outputFileName):

    messages = list()
    regex = re.compile(r'^[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9], [a-zA-Z0-9]+', re.IGNORECASE)

    with open(fileName, errors='replace', encoding='utf8') as file:

        for line in file:

            if re.match(regex, line) is not None:

                line = re.sub(r'[0-9][0-9]:[0-9][0-9]', r'splitMarker', line)

                messages.append(line.split('splitMarker - ')[1])
            else:
                messages[messages.__len__() - 1] += line
    file.close()

    writeCleanedMessages(messages, outputFileName)

def writeCleanedMessages(messages, outputFileName):

    with open(outputFileName, 'w', encoding='utf8') as file:

        for message in messages:
            file.write(message)

    file.close()

def main():
    print('hi')
    inputFile = input('Provide the chat log file name: \n')
    outputFile = input('Provide the output file name: \n')

    readLogFile(inputFile, outputFile)

if __name__ == '__main__':

    main()
