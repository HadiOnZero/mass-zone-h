#!/usr/bin/env python3
"""
Mobile Widgets for Zone-H Mobile Mirror Tool
Custom widgets untuk mobile interface
Author: Hadi Ramdhani
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle


class HackerTextInput(TextInput):
    """TextInput dengan tema hacker untuk mobile"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.05, 0.05, 0.05, 1)  # Dark background
        self.foreground_color = (0, 1, 0, 1)  # Green text
        self.cursor_color = (0, 1, 0, 1)  # Green cursor
        self.font_name = 'monospace'
        self.font_size = dp(12)
        self.multiline = True
        self.size_hint_y = None
        self.height = dp(100)
        self.padding = [dp(10), dp(10)]
        
        # Draw border
        with self.canvas.before:
            Color(0, 1, 0, 0.5)  # Green border
            self.border_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_border, size=self.update_border)
    
    def update_border(self, *args):
        """Update border position and size"""
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size


class HackerButton(Button):
    """Button dengan tema hacker untuk mobile"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.1, 0.1, 0.1, 1)  # Dark background
        self.color = (0, 1, 0, 1)  # Green text
        self.font_name = 'monospace'
        self.font_size = dp(14)
        self.bold = True
        self.size_hint_y = None
        self.height = dp(45)
        self.padding = [dp(15), dp(10)]
        
        # Draw glow effect
        with self.canvas.before:
            Color(0, 1, 0, 0.3)  # Green glow
            self.glow_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_glow, size=self.update_glow)
    
    def update_glow(self, *args):
        """Update glow effect"""
        self.glow_rect.pos = (self.x - 2, self.y - 2)
        self.glow_rect.size = (self.width + 4, self.height + 4)


class MobileProgressBar(ProgressBar):
    """ProgressBar kustom untuk mobile"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 100
        self.value = 0
        self.size_hint_y = None
        self.height = dp(25)
        self.background_color = (0.1, 0.1, 0.1, 1)
        self.color = (0, 1, 0, 1)
        
        # Custom styling
        with self.canvas.before:
            Color(0, 0.5, 0, 0.3)  # Dark green background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        """Update background rectangle"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class ResultItem(BoxLayout):
    """Widget untuk menampilkan hasil mirror individual"""
    
    def __init__(self, result, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(10)
        self.spacing = dp(10)
        
        # Status indicator
        status_color = (0, 1, 0, 1) if result['status'] == 'Success' else (1, 0, 0, 1)
        status_symbol = '✅' if result['status'] == 'Success' else '❌'
        
        status_label = Label(
            text=status_symbol,
            font_size=dp(20),
            color=status_color,
            size_hint_x=0.15
        )
        self.add_widget(status_label)
        
        # Content layout
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_x=0.85
        )
        
        # URL
        url_label = Label(
            text=result['url'],
            font_size=dp(11),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(20),
            text_size=(dp(200), None),
            halign='left',
            shorten=True
        )
        content_layout.add_widget(url_label)
        
        # Status and code
        status_text = f"{result['status']} (Code: {result['status_code']})"
        status_info = Label(
            text=status_text,
            font_size=dp(10),
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(15)
        )
        content_layout.add_widget(status_info)
        
        # Title
        title_label = Label(
            text=f"Title: {result['title']}",
            font_size=dp(9),
            color=(1, 1, 1, 0.7),
            size_hint_y=None,
            height=dp(15),
            text_size=(dp(200), None),
            halign='left',
            shorten=True
        )
        content_layout.add_widget(title_label)
        
        # Timestamp
        time_label = Label(
            text=result['timestamp'],
            font_size=dp(8),
            color=(1, 1, 1, 0.6),
            size_hint_y=None,
            height=dp(12)
        )
        content_layout.add_widget(time_label)
        
        self.add_widget(content_layout)
        
        # Background based on status
        with self.canvas.before:
            if result['status'] == 'Success':
                Color(0, 0.3, 0, 0.2)  # Dark green
            else:
                Color(0.3, 0, 0, 0.2)  # Dark red
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        """Update background rectangle"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class ResultsList(GridLayout):
    """Widget untuk menampilkan daftar hasil mirror"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.spacing = dp(5)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.results = []
    
    def add_result(self, result):
        """Tambahkan hasil ke daftar"""
        self.results.append(result)
        result_item = ResultItem(result=result)
        self.add_widget(result_item)
    
    def clear_results(self):
        """Bersihkan daftar hasil"""
        self.results.clear()
        self.clear_widgets()
    
    def get_results(self):
        """Dapatkan semua hasil"""
        return self.results


class MobileLogOutput(BoxLayout):
    """Widget untuk menampilkan log output"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(150)
        self.padding = dp(10)
        
        # Title
        title = Label(
            text='📋 CONSOLE LOG',
            font_size=dp(14),
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(25)
        )
        self.add_widget(title)
        
        # Scrollable log area
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )
        
        self.log_label = Label(
            text='Ready - Zone-H Mobile Mirror\n',
            font_size=dp(9),
            color=(0, 1, 0, 1),
            font_name='monospace',
            size_hint_y=None,
            text_size=(dp(280), None),
            halign='left',
            valign='top'
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll_view.add_widget(self.log_label)
        self.add_widget(scroll_view)
        
        # Background
        with self.canvas.before:
            Color(0, 0, 0, 0.8)  # Dark background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        """Update background"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def add_log(self, message):
        """Tambahkan pesan ke log"""
        current_text = self.log_label.text
        new_text = current_text + message + '\n'
        self.log_label.text = new_text
        
        # Auto-scroll to bottom
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
    
    def scroll_to_bottom(self, dt):
        """Scroll ke bawah"""
        if hasattr(self.parent, 'scroll_y'):
            self.parent.scroll_y = 0
    
    def clear_log(self):
        """Bersihkan log"""
        self.log_label.text = ''


class SettingsPanel(BoxLayout):
    """Panel untuk pengaturan"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = dp(15)
        self.spacing = dp(10)
        self.size_hint_y = None
        self.height = dp(200)
        
        # Title
        title = Label(
            text='⚙️ SETTINGS',
            font_size=dp(16),
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(30)
        )
        self.add_widget(title)
        
        # Delay setting
        delay_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        delay_label = Label(
            text='Delay (sec):',
            font_size=dp(12),
            color=(1, 1, 1, 0.9),
            size_hint_x=0.4
        )
        delay_layout.add_widget(delay_label)
        
        self.delay_input = TextInput(
            text='2',
            multiline=False,
            font_size=dp(12),
            size_hint_x=0.3,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1)
        )
        delay_layout.add_widget(self.delay_input)
        
        self.add_widget(delay_layout)
        
        # Timeout setting
        timeout_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(40)
        )
        
        timeout_label = Label(
            text='Timeout (sec):',
            font_size=dp(12),
            color=(1, 1, 1, 0.9),
            size_hint_x=0.4
        )
        timeout_layout.add_widget(timeout_label)
        
        self.timeout_input = TextInput(
            text='15',
            multiline=False,
            font_size=dp(12),
            size_hint_x=0.3,
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1)
        )
        timeout_layout.add_widget(self.timeout_input)
        
        self.add_widget(timeout_layout)
        
        # Background
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 0.8)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_bg, size=self.update_bg)
    
    def update_bg(self, *args):
        """Update background"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def get_delay(self):
        """Get delay value"""
        try:
            return int(self.delay_input.text)
        except ValueError:
            return 2
    
    def get_timeout(self):
        """Get timeout value"""
        try:
            return int(self.timeout_input.text)
        except ValueError:
            return 15