from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import ButtonBehavior


class ImageButton(ButtonBehavior, Image):
    pass

#cria um label e imagem com comportamento de botão
class LabelButton(ButtonBehavior, Label):
    pass