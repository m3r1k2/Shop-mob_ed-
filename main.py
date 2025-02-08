from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.core.window import Window
# Деякі товари для демонстрації
pink = (0.1, 0.1, 0.3, 1)
Window.clearcolor = pink
products = {
    'a': {'price': 120, 'image': 'image.jpg'},
    'b': {'price': 110, 'image': 'image1.jpg'},
    'c': {'price': 100, 'image': 'image2.jpg'}
}
cart = []

# Екран авторизації
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        layout.add_widget(Label(text="Ласкаво просимо до магазину!", font_size='24sp'))
        layout.add_widget(Image(source='pr.png'))
        self.username_input = TextInput(hint_text='Логін', multiline=False, font_size='18sp', padding_y=(10, 10),
                                        size_hint=(1, None), height='40dp')
        self.password_input = TextInput(hint_text='Пароль', multiline=False, password=True, font_size='18sp',
                                        padding_y=(10, 10), size_hint=(1, None), height='40dp')
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        btn = Button(
            text='Увійти',
            size_hint=(1, None),
            height='40dp',
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        btn.bind(on_release=self.login)
        layout.add_widget(btn)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        # Тут можна додати перевірку логіну та паролю
        if username and password:
            self.manager.current = 'main'


# Головний екран
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Додавання кнопки корзини у верхній частині
        top_layout = BoxLayout(size_hint_y=None, height='50dp')
        cart_btn = Button(
            text='Корзина',
            size_hint=(None, None),
            size=('100dp', '40dp'),
            background_normal='',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        cart_btn.bind(on_release=self.go_to_cart)
        top_layout.add_widget(cart_btn)
        layout.add_widget(top_layout)

        # Додавання списку товарів
        for product in products:
            product_layout = BoxLayout(size_hint_y=None, height='150dp', padding=10, spacing=10)

            # Зображення товару
            image = Image(source=products[product]['image'], size_hint=(None, None), size=('100dp', '100dp'))

            # Опис товару і кнопка додавання до корзини
            info_layout = BoxLayout(orientation='vertical')
            description = Label(text=f"{product} - {products[product]['price']}$", font_size='18sp')
            add_button = Button(
                text='Додати до корзини',
                size_hint=(1, None),
                height ='40dp',
                background_normal='',
                background_color=(0.2, 0.6, 0.86, 1),
                color=(1, 1, 1, 1),
                font_size='18sp'
            )
            add_button.bind(on_release=lambda x, p=product: self.add_to_cart(p))

            info_layout.add_widget(description)
            info_layout.add_widget(add_button)

            product_layout.add_widget(image)
            product_layout.add_widget(info_layout)
            layout.add_widget(product_layout)

        self.add_widget(layout)

    def add_to_cart(self, product_name):
        cart.append(product_name)
        self.manager.current = 'cart'

    def go_to_cart(self, instance):
        self.manager.current = 'cart'

# Екран корзини
class CartScreen(Screen):
    def __init__(self, **kvargs):
        super(CartScreen,self).__init__(**kvargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label = Label(text='', font_size='24sp')
        self.back_btn = Button(
            text='Назад',
            size_hint=(1,None),
            height='40dp',
            background_normal='',
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        self.back_btn.bind(on_release=self.go_back)
        layout.add_widget(self.label)
        layout.add_widget(self.back_btn)
        self.add_widget(layout)

    def on_pre_enter(self,):
        self.update_cart()

    def update_cart(self):
        if cart:
            cart_text = '\n'.join(cart)
            self.label.text = f"Корзина:\n{cart_text}"
        else:
            self.label.text = "Корзина порожня"

    def go_back(self, instance):
        self.manager.current = 'main'
# Клас додатку
class ShopApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CartScreen(name='cart'))
        return sm

if __name__ == '__main__':
    ShopApp().run()