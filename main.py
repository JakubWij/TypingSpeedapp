from sqlalchemy import create_engine, Column, Integer, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import tkinter
import tkinter as tk
import random
import ctypes
from tkinter.constants import E, W, N, S, CENTER

# Create a connection to the SQLite database, echo=True prints all sql statements
engine = create_engine('sqlite:///score.db', echo=True)
# Create a session factory for interacting with the database
Session = sessionmaker(bind=engine)
# Create a base class for declarative models
Base = declarative_base()


# Define a simple model for a Score
class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    score = Column(Integer)

    def __repr__(self):
        return f"<Score {self.score}"


# # Create the users table in the database
# Base.metadata.create_all(engine)


class SpeedTyping:
    def __init__(self, root):
        self.root = root
        self.root.title('Type Speed Test')
        self.root.geometry("800x600")
        self.mistakes = 0
        self.text = None
        self.WPM = 0
        self.session = Session()
        self.high_score = self.get_high_score()
        self.root.option_add('*Label.Font', ('Helvetica', 30))
        self.root.option_add('*Button.Font', ('Helvetica', 20))
        self.start_test()

    def add_new_score(self):
        score = Score(score=self.WPM)
        self.session.add(score)
        self.session.commit()

    def get_high_score(self):
        high_score = self.session.query(func.max(Score.score)).scalar()
        return high_score

    def start_test(self):
        self.high_score = self.get_high_score()
        self.random_texts()
        self.root.bind('<Key>', self.key_press)
        split_point = 0
        self.test_on = True
        self.passed_seconds = 0

        self.root.after(60000, self.stop_text)
        self.root.after(1000, self.add_second)

        self.left_label = tk.Label(self.root, text=self.text[0:split_point], fg='grey')
        self.left_label.place(relx=0.5, rely=0.5, anchor=E)

        self.right_label = tk.Label(self.root, text=self.text[split_point:])
        self.right_label.place(relx=0.5, rely=0.5, anchor=W)

        self.current_letter_label = tk.Label(self.root, text=self.text[split_point], fg='grey')
        self.current_letter_label.place(relx=0.5, rely=0.6, anchor=N)

        self.time_label = tk.Label(self.root, text=f'0 Seconds', fg='grey')
        self.time_label.place(relx=0.5, rely=0.4, anchor=S)

        self.high_score_label = tk.Label(self.root, text=f'High Score 💪: {self.high_score}', font=('Helvetica', 20))
        self.high_score_label.place(relx=0.8, rely=0.1, anchor=S)

    def random_texts(self):
        texts = ['Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live '
                 'the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large '
                 'language ocean. A small river named Duden flows by their place and supplies it with the necessary '
                 'regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. '
                 'Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic '
                 'life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for '
                 'the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands',
                 'A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring '
                 'which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which '
                 'was created for the bliss of souls like mine. I am so happy, my dear friend, so absorbed in the '
                 'exquisite sense of mere tranquil existence, that I neglect my talents. I should be incapable of '
                 'drawing a single stroke at the present moment; and yet I feel that I never was a greater artist '
                 'than now. When, while the lovely valley teems with vapour around me, and the meridian sun strikes '
                 'the upper surface of the impenetrable foliage of my trees, and but',
                 'One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed '
                 'into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could '
                 'see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly '
                 'able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared '
                 'with the size of the rest of him, waved about helplessly as he looked. "What\'s happened to me?" he '
                 'thought. It wasn\'t a dream. His room, a proper human room although a little too small, lay '
                 'peacefully between its four familiar walls. A collection of textile samples lay spread']
        self.text = random.choice(texts).lower()

    def stop_text(self):
        self.test_on = False

        self.WPM = len(self.left_label.cget('text').split(' '))
        CPM = len(''.join([char for char in self.left_label.cget('text') if char != ' ']))

        self.time_label.destroy()
        self.current_letter_label.destroy()
        self.left_label.destroy()
        self.right_label.destroy()

        self.words_per_minute = tk.Label(self.root, text=f'Words per minute: {self.WPM}', fg='black')
        self.words_per_minute.place(relx=0.5, rely=0.4, anchor=CENTER)

        self.characters_per_minute = tk.Label(self.root, text=f'Characters per minute: {CPM}', fg='black')
        self.characters_per_minute.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.mistakes_label = tk.Label(self.root, text=f'Mistakes made: {self.mistakes}', fg='black')
        self.mistakes_label.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.restart_button = tk.Button(self.root, text='Retry', command=self.restart)
        self.restart_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.add_new_score()

    def restart(self):
        self.words_per_minute.destroy()
        self.restart_button.destroy()
        self.characters_per_minute.destroy()
        self.mistakes_label.destroy()

        self.start_test()

    def add_second(self):
        self.passed_seconds += 1
        self.time_label.configure(text=f'{self.passed_seconds} Seconds')

        if self.test_on:
            self.root.after(1000, self.add_second)

    def key_press(self, event=None):
        try:
            if event.char.lower() == self.right_label.cget('text')[0].lower():
                # delete one from right side
                self.right_label.configure(text=self.right_label.cget('text')[1:])
                # add one from left side
                self.left_label.configure(text=self.left_label.cget('text') + event.char.lower())
                # set the next letter label
                self.current_letter_label.configure(text=self.right_label.cget('text')[0])
            else:
                self.mistakes += 1
        except tkinter.TclError:
            pass


root = tk.Tk()

app = SpeedTyping(root)

root.mainloop()
