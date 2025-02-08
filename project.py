from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

# Оновлені товари для демонстрації
products = {
    'Аніме плакат (Mushoku Tensei)': {'price': 2, 'image': 'poster.png'},
    'Аніме фігурка (Kimetsu no Yaiba)': {'price': 7.25, 'image': 'sta.png'},
    'Аніме катана (One Piece)': {'price': 17.90, 'image': 'sw.png'}
}

products2 = {
    'Фанко Поп (Bleach)': {'price': 8, 'image': 'ich.png'},
    'Аніме фігурка (Tower of God)': {'price': 9.5, 'image': 'tv.png'},
    'Аніме брелок (Naruto)': {'price': 2.5, 'image': 'akaz.png'}
}

cart = {}

# Екран авторизації
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.4, 0.0, 0.0, 1)  # Темно-червоний фон
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Image(source='pr.png', size_hint=(1, 0.3)))

        layout.add_widget(Label(text='Ласкаво просимо до аніме магазину!',
                                font_size='16sp',
                                color=(1, 1, 1, 1)))

        self.username_input = TextInput(hint_text='Логін',
                                        multiline=False,
                                        font_size='16sp',
                                        padding_y=(10, 10),
                                        size_hint=(1, None),
                                        height='35dp',
                                        background_color=(0.7, 0.1, 0.1, 1),
                                        foreground_color=(1, 1, 1, 1))

        self.password_input = TextInput(hint_text='Пароль',
                                        multiline=False,
                                        password=True,
                                        font_size='16sp',
                                        padding_y=(10, 10),
                                        size_hint=(1, None),
                                        height='35dp',
                                        background_color=(0.7, 0.1, 0.1, 1),
                                        foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)

        btn = Button(text='Увійти',
                     size_hint=(1, None),
                     height='35dp',
                     background_normal='',
                     background_color=(0.8, 0.0, 0.0, 1),
                     color=(1, 1, 1, 1),
                     font_size='16sp')
        btn.bind(on_release=self.login)
        layout.add_widget(btn)
        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        if username and password:
            self.manager.current = 'main'

# Головний екран
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.3, 0.0, 0.0, 1)  # Темно-червоний фон
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Верхній контейнер з двома кнопками
        top_layout = BoxLayout(size_hint_y=None, height='50dp')

        # Кнопка "Корзина"
        cart_btn = Button(
            text='Корзина',
            size_hint=(None, None),
            size=('80dp', '35dp'),
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        cart_btn.bind(on_release=self.go_to_cart)

        # Кнопка "2 сторінка"
        next_btn = Button(
            text='2 сторінка',
            size_hint=(None, None),
            size=('80dp', '35dp'),
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
            font_size='16sp',
            pos_hint={'right': 1}
        )
        next_btn.bind(on_release=self.go_to_second)

        # Додаємо кнопку "Корзина" зліва
        top_layout.add_widget(cart_btn)
        # Додаємо порожній віджет для заповнення простору
        top_layout.add_widget(BoxLayout())
        # Додаємо кнопку "2 сторінка" справа
        top_layout.add_widget(next_btn)

        layout.add_widget(top_layout)

        for product in products:
            product_layout = BoxLayout(size_hint_y=None, height='120dp', padding=5, spacing=5)

            image = Image(source=products[product]['image'], size_hint=(None, None), size=('80dp', '80dp'))

            info_layout = BoxLayout(orientation='vertical')
            description = Label(text=f"{product} - {products[product]['price']}$", font_size='14sp')
            add_button = Button(
                text='Додати до корзини',
                size_hint=(1, None),
                height='35dp',
                background_normal='',
                background_color=(0.8, 0.0, 0.0, 1),
                color=(1, 1, 1, 1),
                font_size='14sp'
            )
            add_button.bind(on_release=lambda x, p=product: self.add_to_cart(p))

            info_layout.add_widget(description)
            info_layout.add_widget(add_button)

            product_layout.add_widget(image)
            product_layout.add_widget(info_layout)
            layout.add_widget(product_layout)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def add_to_cart(self, product_name):
        if product_name in cart:
            cart[product_name] += 1
        else:
            cart[product_name] = 1
        self.manager.current = 'cart'

    def go_to_cart(self, instance):
        self.manager.current = 'cart'

    def go_to_second(self, instance):
        self.manager.current = 'second'


class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.3, 0.0, 0.0, 1)  # Темно-червоний фон
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Верхній контейнер з двома кнопками
        top_layout = BoxLayout(size_hint_y=None, height='50dp')

        # Кнопка "Корзина"
        cart_btn = Button(
            text='Корзина',
            size_hint=(None, None),
            size=('120dp', '35dp'),
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),  # Червоний колір кнопки
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        cart_btn.bind(on_release=self.go_to_cart)

        # Кнопка "Головна сторінка"
        back_btn = Button(
            text='Головна сторінка',
            size_hint=(None, None),
            size=('120dp', '35dp'),
            background_normal='',
            background_color=(0.7, 0.1, 0.1, 1),  # Червоний колір кнопки
            color=(1, 1, 1, 1),
            font_size='16sp',
            pos_hint={'right': 1}
        )
        back_btn.bind(on_release=self.go_to_main)

        top_layout.add_widget(cart_btn)
        top_layout.add_widget(BoxLayout())
        top_layout.add_widget(back_btn)

        layout.add_widget(top_layout)

        for product in products2:
            product_layout = BoxLayout(size_hint_y=None, height='120dp', padding=5, spacing=5)

            image = Image(source=products2[product]['image'], size_hint=(None, None), size=('80dp', '80dp'))

            info_layout = BoxLayout(orientation='vertical')
            description = Label(text=f"{product} - {products2[product]['price']}$", font_size='14sp', color=(1, 1, 1, 1))
            add_button = Button(
                text='Додати до корзини',
                size_hint=(1, None),
                height='35dp',
                background_normal='',
                background_color=(0.8, 0.0, 0.0, 1),  # Червоний колір кнопки
                color=(1, 1, 1, 1),
                font_size='14sp'
            )
            add_button.bind(on_release=lambda x, p=product: self.add_to_cart(p))

            info_layout.add_widget(description)
            info_layout.add_widget(add_button)

            product_layout.add_widget(image)
            product_layout.add_widget(info_layout)
            layout.add_widget(product_layout)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def add_to_cart(self, product_name):
        if product_name in cart:
            cart[product_name] += 1
        else:
            cart[product_name] = 1
        self.manager.current = 'cart'

    def go_to_cart(self, instance):
        self.manager.current = 'cart'

    def go_to_main(self, instance):
        self.manager.current = 'main'

# Екран корзини
class CartScreen(Screen):
    def __init__(self, **kwargs):
        super(CartScreen, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0.3, 0.0, 0.0, 1)  # Темно-червоний фон
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text='Корзина порожня', font_size='16sp', color=(1, 1, 1, 1))
        layout.add_widget(self.label)

        btn_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)

        # Кнопка "Очистити корзину"
        clear_btn = Button(
            text='Очистити корзину',
            size_hint=(1, None),
            height='35dp',
            background_normal='',
            background_color=(0.8, 0.0, 0.0, 1),  # Червоний колір кнопки
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        clear_btn.bind(on_release=self.clear_cart)  # Прив'язуємо метод до кнопки

        # Кнопка "Назад до покупок"
        back_btn = Button(
            text='Назад до покупок',
            size_hint=(1, None),
            height='35dp',
            background_normal='',
            background_color=(0.8, 0.0, 0.0, 1),  # Червоний колір кнопки
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        back_btn.bind(on_release=self.go_back)

        btn_layout.add_widget(clear_btn)
        btn_layout.add_widget(back_btn)

        layout.add_widget(btn_layout)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def on_pre_enter(self, *args):
        self.update_cart()

    def update_cart(self):
        if cart:
            cart_text = '\n'.join([f"{item} x{quantity}" for item, quantity in cart.items()])
            self.label.text = f"Корзина:\n{cart_text}"
        else:
            self.label.text = "Корзина порожня"

    def clear_cart(self, instance):
        cart.clear()
        self.update_cart()

    def go_back(self, instance):
        self.manager.current = 'main'

class ShoppingApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CartScreen(name='cart'))
        sm.add_widget(SecondScreen(name='second'))
        return sm

if __name__ == '__main__':
    ShoppingApp().run()