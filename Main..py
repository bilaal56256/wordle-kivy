# Wordle Kivy App with Real AdMob Integration (Banner Only for Now)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from datetime import datetime
from kivmob import KivMob
import random
import os

Window.clearcolor = (0.1, 0.1, 0.1, 1)
LabelBase.register(name='Roboto', fn_regular='BebasNeue-Regular.ttf')
store = JsonStore("game_data.json")

APP_ID = "ca-app-pub-1644069676777509~2139726918"
BANNER_ID = "ca-app-pub-1644069676777509/9056203649"

class StyledButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = "Roboto"
        self.background_normal = ""
        self.background_color = (0.2, 0.2, 0.2, 1)
        self.color = (1, 1, 1, 1)
        self.size_hint_y = None
        self.height = 50
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = RoundedRectangle(radius=[15], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class SolverScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        layout.add_widget(Image(source="wordle_logo.png", size_hint_y=None, height=100))

        self.correct = TextInput(hint_text="Correct letters (_ for unknown)", multiline=False)
        self.misplaced = TextInput(hint_text="Misplaced letters", multiline=False)
        self.wrong = TextInput(hint_text="Wrong letters", multiline=False)

        layout.add_widget(self.correct)
        layout.add_widget(self.misplaced)
        layout.add_widget(self.wrong)

        btn = StyledButton(text="Get Suggestions")
        btn.bind(on_press=self.get_suggestions)
        layout.add_widget(btn)

        self.result = Label(text="Suggestions will appear here", color=(1, 1, 1, 1))
        layout.add_widget(self.result)

        self.add_widget(layout)

    def get_suggestions(self, instance):
        correct = self.correct.text.lower()
        misplaced = self.misplaced.text.lower()
        wrong = self.wrong.text.lower()
        with open("words.txt", "r") as f:
            words = [w.strip() for w in f if len(w.strip()) == len(correct)]
        filtered = []
        for word in words:
            match = True
            for i in range(len(correct)):
                if correct[i] != '_' and word[i] != correct[i]:
                    match = False
                    break
            if misplaced and not all(c in word for c in misplaced):
                match = False
            if wrong and any(c in word for c in wrong):
                match = False
            if match:
                filtered.append(word)
        self.result.text = "\n".join(filtered[:10]) if filtered else "No matches found."

class DailyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        self.logo = Image(source="wordle_logo.png", size_hint_y=None, height=100)
        self.layout.add_widget(self.logo)

        self.status = Label(text="Play Daily Challenge", color=(1, 1, 1, 1))
        self.layout.add_widget(self.status)

        self.input = TextInput(hint_text="Enter your guess", multiline=False)
        self.layout.add_widget(self.input)

        self.submit = StyledButton(text="Submit Guess")
        self.submit.bind(on_press=self.submit_guess)
        self.layout.add_widget(self.submit)

        self.result = Label(text="Guesses show here", color=(1, 1, 1, 1), markup=True)
        self.layout.add_widget(self.result)

        self.icon = Image(source="", size_hint_y=None, height=80)
        self.layout.add_widget(self.icon)

        self.reset = StyledButton(text="Reset Daily Game")
        self.reset.bind(on_press=self.reset_game)
        self.layout.add_widget(self.reset)

        self.add_widget(self.layout)
        self.load_word()

    def load_word(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.word_key = f"word_{today}"
        self.guess_key = f"guesses_{today}"

        if not store.exists(self.word_key):
            with open("words.txt") as f:
                words = [w.strip() for w in f if len(w.strip()) == 5]
            word = random.choice(words)
            store.put(self.word_key, word=word)

        self.secret = store.get(self.word_key)['word']
        self.guesses = store.get(self.guess_key)['data'] if store.exists(self.guess_key) else []
        self.show_guesses()

    def submit_guess(self, instance):
        guess = self.input.text.strip().lower()
        self.input.text = ""
        if len(guess) != 5:
            self.status.text = "Enter a valid 5-letter word."
            return
        if guess in self.guesses:
            self.status.text = "Already guessed."
            return
        self.guesses.append(guess)
        store.put(self.guess_key, data=self.guesses)
        if guess == self.secret:
            self.status.text = "Correct! You win!"
            self.icon.source = "trophy.png"
        elif len(self.guesses) >= 6:
            self.status.text = f"Out of tries! Word was: {self.secret}"
            self.icon.source = "fail.png"
        else:
            self.status.text = f"Wrong. Tries left: {6 - len(self.guesses)}"
        self.show_guesses()

    def show_guesses(self):
        out = ""
        for g in self.guesses:
            row = ""
            for i, c in enumerate(g):
                if c == self.secret[i]:
                    row += f"[color=#6aaa64]{c.upper()}[/color] "
                elif c in self.secret:
                    row += f"[color=#c9b458]{c.upper()}[/color] "
                else:
                    row += f"[color=#787c7e]{c.upper()}[/color] "
            out += row + "\n"
        self.result.text = out if out else "Guesses show here"

    def reset_game(self, instance):
        store.delete(self.word_key) if store.exists(self.word_key) else None
        store.delete(self.guess_key) if store.exists(self.guess_key) else None
        self.status.text = "Game reset. Try again."
        self.icon.source = "refresh.png"
        self.load_word()

class WordleApp(App):
    def build(self):
        self.ads = KivMob(APP_ID)
        self.ads.new_banner(BANNER_ID, top_pos=False)
        self.ads.request_banner()
        self.ads.show_banner()

        root = BoxLayout(orientation='vertical')
        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(SolverScreen(name='solver'))
        self.sm.add_widget(DailyScreen(name='daily'))

        nav = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        btn1 = StyledButton(text="Solver Mode")
        btn2 = StyledButton(text="Daily Mode")
        btn1.bind(on_press=lambda x: self.sm.switch_to(self.sm.get_screen('solver')))
        btn2.bind(on_press=lambda x: self.sm.switch_to(self.sm.get_screen('daily')))
        nav.add_widget(btn1)
        nav.add_widget(btn2)

        root.add_widget(nav)
        root.add_widget(self.sm)
        return root

if __name__ == '__main__':
    WordleApp().run()
