#!/usr/bin/env python3
"""
Mobile Dialogs for Zone-H Mobile Mirror Tool
Custom dialogs untuk mobile interface
Author: Hadi Ramdhani
"""

from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.clock import Clock


class MobileAboutDialog(ModalView):
    """About dialog untuk mobile"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.8)
        self.auto_dismiss = True
        self.background_color = (0, 0, 0, 0.9)
        
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Title
        title = Label(
            text='📱 ZONE-H MOBILE MIRROR',
            font_size=dp(24),
            bold=True,
            color=(0, 1, 0, 1),  # Green
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(title)
        
        # Version info
        version_info = Label(
            text='Version 1.0.0\nby Hadi Ramdhani',
            font_size=dp(14),
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(60),
            halign='center'
        )
        main_layout.add_widget(version_info)
        
        # Description
        description = Label(
            text='A mobile application for mass mirroring Zone-H notifications '
                 'with optimized performance for mobile devices.',
            font_size=dp(12),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(80),
            text_size=(dp(250), None),
            halign='center'
        )
        main_layout.add_widget(description)
        
        # Features
        features_label = Label(
            text='✨ FEATURES:',
            font_size=dp(16),
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(features_label)
        
        features_text = Label(
            text='• Mass mirror multiple URLs\n'
                 '• Mobile-optimized interface\n'
                 '• Real-time progress tracking\n'
                 '• Export results (JSON/CSV)\n'
                 '• Network status monitoring\n'
                 '• Battery-aware operation',
            font_size=dp(11),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(120),
            text_size=(dp(250), None),
            halign='left'
        )
        main_layout.add_widget(features_text)
        
        # Close button
        close_btn = Button(
            text='CLOSE',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        close_btn.bind(on_press=self.dismiss)
        main_layout.add_widget(close_btn)
        
        self.add_widget(main_layout)


class MobileHelpDialog(ModalView):
    """Help dialog untuk mobile"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.7)
        self.auto_dismiss = True
        self.background_color = (0, 0, 0, 0.9)
        
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )
        
        # Title
        title = Label(
            text='🛡️ QUICK HELP',
            font_size=dp(22),
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(title)
        
        # Scrollable content
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )
        
        content_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Help content
        help_text = """🔧 HOW TO USE:

1. Enter URLs in the input field
2. Set delay and timeout settings
3. Choose user agent for mobile
4. Tap START MIRROR to begin
5. Monitor progress in real-time
6. View results in the list below

📱 MOBILE FEATURES:
• Touch-optimized interface
• Battery-aware operation
• Network status monitoring
• Export results to storage
• Vibration on completion

⚠️ TIPS:
• Use WiFi for better performance
• Keep device charged during mirror
• Check network status before start
• Use appropriate delay settings

📧 CONTACT:
For support and updates, visit our GitHub repository.
"""
        
        help_label = Label(
            text=help_text,
            font_size=dp(11),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(300),
            text_size=(dp(250), None),
            halign='left'
        )
        content_layout.add_widget(help_label)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        # Close button
        close_btn = Button(
            text='GOT IT',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        close_btn.bind(on_press=self.dismiss)
        main_layout.add_widget(close_btn)
        
        self.add_widget(main_layout)


class MobileResultDialog(ModalView):
    """Dialog untuk menampilkan hasil mirror"""
    
    def __init__(self, result, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.6)
        self.auto_dismiss = True
        self.background_color = (0, 0, 0, 0.9)
        self.result = result
        
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Status
        status_color = (0, 1, 0, 1) if result['status'] == 'Success' else (1, 0, 0, 1)
        status_text = '✅ SUCCESS' if result['status'] == 'Success' else '❌ FAILED'
        
        status_label = Label(
            text=status_text,
            font_size=dp(18),
            bold=True,
            color=status_color,
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(status_label)
        
        # URL
        url_label = Label(
            text=f"URL: {result['url']}",
            font_size=dp(12),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(60),
            text_size=(dp(250), None),
            halign='left'
        )
        main_layout.add_widget(url_label)
        
        # Status code
        status_code_label = Label(
            text=f"Status Code: {result['status_code']}",
            font_size=dp(12),
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(status_code_label)
        
        # Title
        title_label = Label(
            text=f"Title: {result['title']}",
            font_size=dp(12),
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(40),
            text_size=(dp(250), None),
            halign='left'
        )
        main_layout.add_widget(title_label)
        
        # Timestamp
        time_label = Label(
            text=f"Time: {result['timestamp']}",
            font_size=dp(10),
            color=(1, 1, 1, 0.6),
            size_hint_y=None,
            height=dp(25)
        )
        main_layout.add_widget(time_label)
        
        # Close button
        close_btn = Button(
            text='CLOSE',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        close_btn.bind(on_press=self.dismiss)
        main_layout.add_widget(close_btn)
        
        self.add_widget(main_layout)


class MobileExportDialog(ModalView):
    """Dialog untuk export hasil"""
    
    def __init__(self, results, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.5)
        self.auto_dismiss = True
        self.background_color = (0, 0, 0, 0.9)
        self.results = results
        
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Title
        title = Label(
            text='💾 EXPORT RESULTS',
            font_size=dp(20),
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(40)
        )
        main_layout.add_widget(title)
        
        # Info
        info_label = Label(
            text=f'Found {len(results)} results to export',
            font_size=dp(12),
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(30)
        )
        main_layout.add_widget(info_label)
        
        # Export buttons
        json_btn = Button(
            text='EXPORT AS JSON',
            size_hint_y=None,
            height=dp(45),
            background_color=(0, 0.5, 0, 1),
            color=(1, 1, 1, 1)
        )
        json_btn.bind(on_press=self.export_json)
        main_layout.add_widget(json_btn)
        
        csv_btn = Button(
            text='EXPORT AS CSV',
            size_hint_y=None,
            height=dp(45),
            background_color=(0, 0.3, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        csv_btn.bind(on_press=self.export_csv)
        main_layout.add_widget(csv_btn)
        
        # Cancel button
        cancel_btn = Button(
            text='CANCEL',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.5, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        cancel_btn.bind(on_press=self.dismiss)
        main_layout.add_widget(cancel_btn)
        
        self.add_widget(main_layout)
        
    def export_json(self, instance):
        """Export sebagai JSON"""
        if self.callback:
            self.callback('json', self.results)
        self.dismiss()
        
    def export_csv(self, instance):
        """Export sebagai CSV"""
        if self.callback:
            self.callback('csv', self.results)
        self.dismiss()
        
    def set_callback(self, callback):
        """Set callback untuk export"""
        self.callback = callback