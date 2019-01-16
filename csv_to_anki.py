import genanki
import csv
import PySimpleGUI as sg
import random

CHARS_LIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=~`{}[]|:;<>?/ .,'"


def id_generator(string):
    def seed_preprocessor(arg):
        arg_num_list = []
        for char in arg:
            if char == '"':
                ch = '/'
                num = CHARS_LIST.index(ch)
                arg_num_list.append(str(num))
            elif char == '\\':
                ch = '/'
                num = CHARS_LIST.index(ch)
                arg_num_list.append(str(num))
            else:
                num = CHARS_LIST.index(char)
                arg_num_list.append(str(num))
        pre_num = ''.join(arg_num_list)  # returns a string of digits from arg
        pre_num = int(pre_num)

        # scale final_num down... using random.seed
        random.seed(pre_num)
        final_num = random.randint(0, 999999999)
        return final_num

    random.seed(seed_preprocessor(string))
    res = random.randint(1000000000, 9999999999)
    return res


class Note(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def main():
    def note_generator(question, answer):
        note = Note(
            model=model,
            fields=[question, answer],
            guid=Note.guid
        )
        return note

    with sg.FlexForm('Get filename example') as form:
        layout = [[sg.Text('File to convert:')], [sg.Input(), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
                  [sg.T('Put converted file in folder:')],
                  [sg.Input(), sg.FolderBrowse()],
                  [sg.T('Deck title:')],
                  [sg.InputText()],
                  [sg.SimpleButton('Convert', bind_return_key=True), sg.Cancel()]]

    button, values = form.LayoutAndRead(layout)

    file = values[0]
    dest_folder = values[1]
    deck_title = values[2]
    deck_id = id_generator(deck_title)

    with open(file) as data:
        reader = csv.DictReader(data)
        l_data = []
        for row in reader:
            l_data.append(row)

    model = genanki.Model(
        1607392319,  # The model ID appears to only affect the code, not the ID of output deck files
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
        ])

    deck = genanki.Deck(
        deck_id,
        deck_title)

    for line in l_data:
        deck.add_note(note_generator(line['Term'], line['Definition']))

    # file title doesn't affect the deck title
    genanki.Package(deck).write_to_file(dest_folder + '/' + deck_title + '.apkg')


if __name__ == '__main__':
    main()
