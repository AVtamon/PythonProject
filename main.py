

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.mapview import MapView, MapMarker
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.popup import Popup
import geocoder

# Конфигурируем интерфейс
Builder.load_string('''
<TabbedPanel>:
    do_default_tab: False
''')

class GlobalSecurityApp(App):
    def build(self):
        # Главное окно с табами
        panel = TabbedPanel()

        # === Первая вкладка (приветствие) ===
        first_tab = TabbedPanelItem(text='Главная')
        first_layout = BoxLayout(orientation='vertical')
        welcome_img = Image(source='welcome.png')  # Поставьте свое изображение!
        greetings = Label(text='Добро пожаловать в нашу службу глобальной безопасности!', font_size=20)
        first_layout.add_widget(welcome_img)
        first_layout.add_widget(greetings)
        first_tab.add_widget(first_layout)
        panel.add_widget(first_tab)

        # === Вторая вкладка (карта + обновление позиции) ===
        second_tab = TabbedPanelItem(text='Карта')
        second_layout = BoxLayout(orientation='vertical')
        map_view = MapView(zoom=11, lat=55.75, lon=37.62)  # Центр Москвы
        second_layout.add_widget(map_view)
        locate_btn = Button(text='Моё местоположение', size_hint=(1, None), height=50)
        locate_btn.bind(on_press=lambda inst: self.update_map(map_view))
        second_layout.add_widget(locate_btn)
        second_tab.add_widget(second_layout)
        panel.add_widget(second_tab)

        # === Третья вкладка (настройки) ===
        third_tab = TabbedPanelItem(text='Настройки')
        third_layout = BoxLayout(orientation='vertical')
        btn1 = Button(text='Тест 1')
        btn2 = Button(text='Тест 2')
        third_layout.add_widget(btn1)
        third_layout.add_widget(btn2)
        third_tab.add_widget(third_layout)
        panel.add_widget(third_tab)

        # === Четвертая вкладка (помощь) ===
        fourth_tab = TabbedPanelItem(text='Помощь')
        fourth_layout = BoxLayout(orientation='vertical')
        help_label = Label(text='Версия 0.2', font_size=16)
        fourth_layout.add_widget(help_label)
        fourth_tab.add_widget(fourth_layout)
        panel.add_widget(fourth_tab)

        # Определяем опасные точки на карте
        danger_points = [
            {'lat': 55.75, 'lon': 37.62, 'description': 'Опасная точка №1'},
            {'lat': 55.76, 'lon': 37.64, 'description': 'Опасная точка №2'}
        ]

        # Добавляем маркеры на карту
        for point in danger_points:
            marker = MapMarker(lat=point['lat'], lon=point['lon'])
            marker.bind(on_press=lambda inst, desc=point['description']: self.show_popup(desc))
            map_view.add_marker(marker)

        return panel

    def show_popup(self, description):
        """Показываем всплывающее окно с описанием опасности"""
        content = Label(text=description, font_size=20)
        popup = Popup(title='Критическая точка',
                     content=content,
                     size_hint=(None, None),
                     size=(400, 200))
        popup.open()

    def update_map(self, map_view):
        """Обновляет карту в зависимости от местоположения."""
        user_loc = geocoder.ip('me')
        if user_loc.ok:
            lat, lng = user_loc.latlng
        else:
            lat, lng = 55.75, 37.62  # Резервный адрес
        map_view.center_on(lat, lng)

if __name__ == '__main__':
    GlobalSecurityApp().run()
