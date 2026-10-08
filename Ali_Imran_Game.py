import os
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

# Urdu shaping and RTL libraries
import arabic_reshaper
from bidi.algorithm import get_display

def fix_urdu(text):
    """Urdu text ko sahi tarah se jodne aur RTL karne ka function"""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

class ImranGameApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Standard Windows Font
        urdu_font = 'arial.ttf'

        # Game Steps Data (Storyline Text + Matching Image Files)
        self.game_data = [
            {
                "text": "علی عمران کا مشن شروع!", 
                "image": "scene0.png"
            },
            {
                "text": "سین 1: مشن کو مکمل کرنے کے لیے جوا کھیل کر رقم جیتی گئی سڈنی جوا بار سے،", 
                "image": "scene1.png"
            },
            {
                "text": "سین 2: جوئے کی جیتی گئی رقم سے ہتھیار اور کمپیوٹر ہیک کرنے کی مشینیں خریدی گئیں۔", 
                "image": "scene2.png"
            },
            {
                "text": "کمپیوٹر ہیک مکمل!", 
                "image": "scene3.png"
            },
            {
                "text": "لیبارٹری کا نقشہ حاصل!", 
                "image": "scene4.png"
            },
            {
                "text": "حفاظتی سسٹم بائی پاس ہو چکا!", 
                "image": "scene5.png"
            },
            {
                "text": "واپسی کی پلاننگ مکمل!", 
                "image": "scene6.png"
            },
            {
                "text": "ٹرانسمیٹر کے ذریعے حکم دیا گیا!", 
                "image": "scene7.png"
            },
            {
                "text": "لیبارٹری دھماکے سے تباہ ہو گئی!", 
                "image": "scene8.png"
            },
            {
                "text": "مشن مکمل، پاکیشیا سیکرٹ سروس کامیاب!", 
                "image": "scene9.png"
            }
        ]
        
        self.current_index = 0

        # Story Label
        self.story_label = Label(
            text=fix_urdu(self.game_data[0]["text"]), 
            font_size=24,
            font_name=urdu_font,
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.story_label)

        # Image Control
        initial_img = self.game_data[0]["image"]
        if not os.path.exists(initial_img):
            initial_img = 'game_scene.png' # Fallback if specific image missing

        self.game_image = Image(source=initial_img, size_hint=(1, 0.6))
        layout.add_widget(self.game_image)

        # Next Button
        self.next_button = Button(
            text=fix_urdu("اگلا مرحلہ"), 
            font_size=22, 
            font_name=urdu_font,
            size_hint=(1, 0.2),
            on_press=self.next_step
        )
        layout.add_widget(self.next_button)

        return layout

    def next_step(self, instance):
        if self.current_index + 1 < len(self.game_data):
            self.current_index += 1
            step_info = self.game_data[self.current_index]
            
            # Update Text
            self.story_label.text = fix_urdu(step_info["text"])
            
            # Update Image dynamically
            img_path = step_info["image"]
            if os.path.exists(img_path):
                self.game_image.source = img_path
                self.game_image.reload()
        else:
            self.story_label.text = fix_urdu("گیم مکمل! 🎮")

if __name__ == '__main__':
    ImranGameApp().run()