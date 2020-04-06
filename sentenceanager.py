
class SentenceManager:
    def __init__(self):
        self.__sentences = []

    def setscript(self, script):
        sentences = script.split("\n\r")
        for sentence in sentences:
            self.__sentences.append(sentence)

        for sentence in self.__sentences:
            print(sentence)



    @property
    def sentences(self):
        return '\n'.join(self.__sentences)


        # for sentence in script:
        #     sentence = sentence.replace('\n', '', len(sentence)).replace('\r', '', len(sentence))
        #     self.sentences.append(sentence)



