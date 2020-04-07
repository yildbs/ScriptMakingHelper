import time


class SentenceManager:
    def __init__(self):
        self.__sentences = []
        self.__current_line = 0

    def set_script(self, script):
        sentences = script.split("\n")
        sentences_temp = []
        for sentence in sentences:
            sentence = sentence.replace('\n', '', len(sentence)).replace('\r', '', len(sentence))
            if sentence != '':
                sentences_temp.append(sentence)
        self.__sentences = sentences_temp

    def set_current_line(self, n):
        for index, sentence in enumerate(self.__sentences):
            n -= len(sentence) + 1
            if n < 0:
                self.__current_line = index
                self.current_line_changed(self.__current_line)
                break

    @staticmethod
    def clean_sentence(s):
        while True:
            if '[' in s:
                if ']' in s:
                    s = s[: s.find('[')] + s[s.find(']') + 1:]
                else:
                    s = s.replace('[', '')
            elif ']' in s:
                s = s.replace(']', '')
            else:
                break

        while True:
            if s.startswith(' '):
                s = s[1:]
            else:
                break

        for _ in range(10):
            s = s.replace('  ', ' ', len(s))
        return s

    @property
    def sentences(self):
        return '\n'.join(self.__sentences)

    @property
    def len(self):
        return len(self.__sentences)

    ###############################
    # commands
    ###############################
    def increment(self):
        self.__current_line = min(self.__current_line+1, len(self.__sentences)-1)
        self.current_line_changed(self.__current_line)

    def decrement(self):
        self.__current_line = max(self.__current_line - 1, 0)
        self.current_line_changed(self.__current_line)

    def erase_current_line(self):
        del self.__sentences[self.__current_line]
        self.sentence_changed()

    def set_who_is_saying(self, name):
        if name != '':
            name = name.replace('\n', '', len(name)).replace('\r', '', len(name))
            self.__sentences[self.__current_line] = '[%s] ' % name + self.clean_sentence(self.__sentences[self.__current_line])
            self.sentence_changed()
            time.sleep(0.01)
            self.increment()

    def make_paragraph(self):
        self.__sentences.insert(self.__current_line, '------------------------')
        self.sentence_changed()

    def join(self):
        self.__sentences[self.__current_line] += ' '
        self.__sentences[self.__current_line] += self.clean_sentence(self.__sentences[self.__current_line+1])
        del self.__sentences[self.__current_line+1]
        self.sentence_changed()

    def clean(self):
        self.__sentences[self.__current_line] =  self.clean_sentence(self.__sentences[self.__current_line])
        self.sentence_changed()

    ############################
    def sentence_changed(self):
        pass
    def current_line_changed(self, n):
        pass



