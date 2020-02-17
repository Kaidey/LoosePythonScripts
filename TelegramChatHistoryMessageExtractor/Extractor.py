import regex as re
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup

messages = list()

# Say user A types different messages in a row (uninterrupted). His first message 'lives' in an html div with class
# 'message default clearfix' but the rest of them have class 'message default clearfix joined'
# When user B stops the continuous messaging from user A, user B's message is again stored in an html div with class
# 'message default clearfix'

# 1 - User A: Hello -> 'message default clearfix'
# 2 - User A: How rea you? -> 'message default clearfix joined'
# 3 - User A: *are -> 'message default clearfix joined'
# 4 - User B: Fine you? -> 'message default clearfix'
# 5 - User A: Me too -> 'message default clearfix'

# When div 1 is passed to this function, it will recursively retrieve divs 2 and 3 and return their text in a list
# When div 4 is passed, nothing happens because there are no joined messages, since User B is immediately 'interrupted'
def findJoinedMessages(htmlDiv, messagesList):
    message = htmlDiv.findNextSibling('div')

    if message is not None:

        htmlClass = ''

        for atr in message.attrs['class']:

            htmlClass += atr + ' '

        if htmlClass == 'message default clearfix joined ':
            body = message.find('div', class_='body')
            messageText = body.find('div', class_='text')
            if messageText is None:
                pass
            else:
                messagesList.append(messageText.text)
                findJoinedMessages(message, messagesList)
            return

        else:
            return
    else:
        return

def processDivData(messageDiv):

    joinedMessages = list()

    findJoinedMessages(messageDiv, joinedMessages)

    textDiv = messageDiv.find('div', class_='text')

    if textDiv is not None:
        firstMsg = textDiv.text
        firstMsg = firstMsg.replace('\n', '').strip()

        user = messageDiv.find('div', class_='from_name').text
        user = user.replace('\n', '').strip()

        return firstMsg, user, joinedMessages
    else:
        return None, None, None


def extractMessages(outputFile, path):

    files = [f for f in listdir(path) if isfile(join(path, f))]

    for file in files:

        regex = re.compile(r'.*.html', re.IGNORECASE)

        if re.match(regex, file) is not None:

            with open(join(path, file), errors='replace', encoding='utf8') as fd:

                data = BeautifulSoup(fd, 'html.parser')

                firstMessageFromUser = data.findAll('div', class_='message default clearfix')

                for div in firstMessageFromUser:

                    firstMsg, user, joinedMessages = processDivData(div)

                    if firstMsg is not None and user is not None and joinedMessages is not None:

                        with open(outputFile, 'a', encoding='utf8') as out:

                            out.write('%s: %s\n' % (user, firstMsg))
                            for msg in joinedMessages:
                                out.write('%s: %s\n' % (user, msg.replace('\n', '').strip()))

def main():

    path = input('Provide the complete path for the folder that contains your html file/files: \n')
    output = input('Provide the output file name: \n')

    extractMessages(output, path)

if __name__ == '__main__':
    main()