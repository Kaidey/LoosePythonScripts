import regex as re

def readLogFile(fileName, outputFileName):

    messages = list()
    regex = re.compile(r'^[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9], [a-zA-Z0-9]+', re.IGNORECASE)
    checkMediaOmitted = re.compile(r'.*<Media omitted>$', re.IGNORECASE)

    with open(fileName, errors='replace', encoding='utf8') as file:

        for line in file:

            if re.match(checkMediaOmitted, line) is not None:
                pass
            else:
                if re.match(regex, line) is not None:

                    line = re.sub(r'[0-9][0-9]:[0-9][0-9]', r'splitMarker', line)

                    message = line.split('splitMarker - ')[1]
                    message = re.sub(r'<Media omitted>', r'', message)

                    messages.append(message)
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
