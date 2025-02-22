import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

class ImranGameApp(App):
    def build(self): # Indented this line
        layout = BoxLayout(orientation='vertical')

        self.story_label = Label(text="علی عمران کا مشن شروع!", font_size=24)
        layout.add_widget(self.story_label)

        self.game_image = Image(source='game_scene.png')  # Placeholder image
        layout.add_widget(self.game_image)

        self.next_button = Button(text='اگلا مرحلہ', font_size=20, on_press=self.next_step)
        layout.add_widget(self.next_button)

        return layout

    def next_step(self, instance): # Indented this line
        steps = [
            "جوا کھیل کر رقم جیتی گئی!",
            "ہتھیار خرید لیے گئے!",
            "کمپیوٹر ہیک مکمل!",
            "لیبارٹری کا نقشہ حاصل!",
            "حفاظتی سسٹم بائی پاس ہو چکا!",
            "واپسی کی پلاننگ مکمل!",
            "ٹرانسمیٹر کے ذریعے حکم دیا گیا!",
            "لیبارٹری دھماکے سے تباہ ہو گئی!",
            "مشن مکمل، پاکیشیا سیکرٹ سروس کامیاب!"
        ]

        current_text = self.story_label.text
        if current_text in steps:
            next_index = steps.index(current_text) + 1
            if next_index < len(steps):
                self.story_label.text = steps[next_index]
            else:
                self.story_label.text = "گیم مکمل! 🎮"

if __name__ == '__main__': # Changed name to __name__
    ImranGameApp().run()