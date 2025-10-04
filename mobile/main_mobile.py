#!/usr/bin/env python3
"""
Zone-H Mobile Mirror Application
Main application file for mobile version using Kivy
Author: Hadi Ramdhani
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

# Import mobile modules
from src.config import (
    APP_NAME, APP_VERSION, APP_AUTHOR,
    MOBILE_DEFAULT_SETTINGS, MOBILE_USER_AGENTS,
    MOBILE_SUCCESS_MESSAGES, MOBILE_ERROR_MESSAGES, MOBILE_WARNING_MESSAGES
)
from src.utils import (
    ZoneHMobileMirror,
    validate_url_mobile, sanitize_url_mobile,
    save_results_to_json_mobile, save_results_to_csv_mobile,
    calculate_success_rate_mobile, check_network_status
)
from src.ui import (
    MobileAboutDialog, MobileHelpDialog, MobileResultDialog, MobileExportDialog,
    HackerTextInput, HackerButton, MobileProgressBar,
    ResultsList, MobileLogOutput, SettingsPanel
)


class ZoneHMobileMirrorApp(App):
    """Main application class for Zone-H Mobile Mirror"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mirror_thread = None
        self.results = []
        self.is_mirroring = False
        
    def build(self):
        """Build the application UI"""
        # Set window properties
        Window.clearcolor = (0, 0, 0, 1)  # Black background
        Window.softinput_mode = 'below_target'  # Handle keyboard
        
        # Main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Header
        header = self.create_header()
        main_layout.add_widget(header)
        
        # Content area with scroll
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
        
        # URL Input section
        url_section = self.create_url_input_section()
        content_layout.add_widget(url_section)
        
        # Settings section
        settings_section = self.create_settings_section()
        content_layout.add_widget(settings_section)
        
        # Control buttons
        control_section = self.create_control_section()
        content_layout.add_widget(control_section)
        
        # Progress section
        progress_section = self.create_progress_section()
        content_layout.add_widget(progress_section)
        
        # Results section
        results_section = self.create_results_section()
        content_layout.add_widget(results_section)
        
        # Log section
        log_section = self.create_log_section()
        content_layout.add_widget(log_section)
        
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)
        
        # Bottom toolbar
        toolbar = self.create_toolbar()
        main_layout.add_widget(toolbar)
        
        return main_layout
    
    def create_header(self):
        """Create application header"""
        header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=[dp(20), dp(10)]
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
        header.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text=f'v{APP_VERSION} - Elite Mobile Mirror Tool',
            font_size=dp(12),
            color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(20)
        )
        header.add_widget(subtitle)
        
        # Add glow effect
        with header.canvas.before:
            Color(0, 1, 0, 0.1)
            self.header_glow = Rectangle(pos=header.pos, size=header.size)
        
        header.bind(pos=self.update_header_glow, size=self.update_header_glow)
        
        return header
    
    def update_header_glow(self, instance, value):
        """Update header glow effect"""
        self.header_glow.pos = (instance.x - 5, instance.y - 5)
        self.header_glow.size = (instance.width + 10, instance.height + 10)
    
    def create_url_input_section(self):
        """Create URL input section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Section title
        title = Label(
            text='🎯 TARGET URLs',
            font_size=dp(16),
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(25)
        )
        section.add_widget(title)
        
        # URL input
        self.url_input = HackerTextInput(
            hint_text='Enter URLs (one per line)\nExample:\nhttp://site1.com\nhttps://site2.com',
            height=dp(120)
        )
        section.add_widget(self.url_input)
        
        # Background
        with section.canvas.before:
            Color(0.05, 0.05, 0.05, 0.8)
            self.url_bg = Rectangle(pos=section.pos, size=section.size)
        
        section.bind(pos=self.update_url_bg, size=self.update_url_bg)
        
        return section
    
    def update_url_bg(self, instance, value):
        """Update URL section background"""
        self.url_bg.pos = instance.pos
        self.url_bg.size = instance.size
    
    def create_settings_section(self):
        """Create settings section"""
        return SettingsPanel()
    
    def create_control_section(self):
        """Create control buttons section"""
        section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Start button
        self.start_button = HackerButton(
            text='🚀 START MIRROR',
            size_hint_x=0.5
        )
        self.start_button.bind(on_press=self.start_mirror)
        section.add_widget(self.start_button)
        
        # Stop button
        self.stop_button = HackerButton(
            text='⏹️ STOP',
            size_hint_x=0.3,
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_mirror)
        section.add_widget(self.stop_button)
        
        # Clear button
        clear_button = HackerButton(
            text='🗑️ CLEAR',
            size_hint_x=0.2
        )
        clear_button.bind(on_press=self.clear_all)
        section.add_widget(clear_button)
        
        return section
    
    def create_progress_section(self):
        """Create progress section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Progress label
        self.progress_label = Label(
            text='Ready to start',
            font_size=dp(12),
            color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(20)
        )
        section.add_widget(self.progress_label)
        
        # Progress bar
        self.progress_bar = MobileProgressBar()
        section.add_widget(self.progress_bar)
        
        # Statistics
        stats_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(20),
            spacing=dp(10)
        )
        
        self.total_label = Label(
            text='Total: 0',
            font_size=dp(10),
            color=(1, 1, 1, 0.8)
        )
        stats_layout.add_widget(self.total_label)
        
        self.success_label = Label(
            text='Success: 0',
            font_size=dp(10),
            color=(0, 1, 0, 0.8)
        )
        stats_layout.add_widget(self.success_label)
        
        self.failed_label = Label(
            text='Failed: 0',
            font_size=dp(10),
            color=(1, 0, 0, 0.8)
        )
        stats_layout.add_widget(self.failed_label)
        
        section.add_widget(stats_layout)
        
        # Background
        with section.canvas.before:
            Color(0.05, 0.05, 0.05, 0.8)
            self.progress_bg = Rectangle(pos=section.pos, size=section.size)
        
        section.bind(pos=self.update_progress_bg, size=self.update_progress_bg)
        
        return section
    
    def update_progress_bg(self, instance, value):
        """Update progress section background"""
        self.progress_bg.pos = instance.pos
        self.progress_bg.size = instance.size
    
    def create_results_section(self):
        """Create results section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(250),
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Section title and export button
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30)
        )
        
        title = Label(
            text='📊 MIRROR RESULTS',
            font_size=dp(16),
            bold=True,
            color=(0, 1, 0, 1)
        )
        header_layout.add_widget(title)
        
        self.export_button = HackerButton(
            text='💾 EXPORT',
            size_hint_x=0.3,
            height=dp(30),
            font_size=dp(10)
        )
        self.export_button.bind(on_press=self.show_export_dialog)
        self.export_button.disabled = True
        header_layout.add_widget(self.export_button)
        
        section.add_widget(header_layout)
        
        # Results list
        scroll_view = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )
        
        self.results_list = ResultsList()
        scroll_view.add_widget(self.results_list)
        section.add_widget(scroll_view)
        
        # Background
        with section.canvas.before:
            Color(0.05, 0.05, 0.05, 0.8)
            self.results_bg = Rectangle(pos=section.pos, size=section.size)
        
        section.bind(pos=self.update_results_bg, size=self.update_results_bg)
        
        return section
    
    def update_results_bg(self, instance, value):
        """Update results section background"""
        self.results_bg.pos = instance.pos
        self.results_bg.size = instance.size
    
    def create_log_section(self):
        """Create log section"""
        self.log_output = MobileLogOutput()
        return self.log_output
    
    def create_toolbar(self):
        """Create bottom toolbar"""
        toolbar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Network status
        self.network_label = Label(
            text='🌐 Network: Checking...',
            font_size=dp(10),
            color=(1, 1, 1, 0.8)
        )
        toolbar.add_widget(self.network_label)
        
        # Help button
        help_button = HackerButton(
            text='❓ HELP',
            size_hint_x=0.2,
            font_size=dp(10),
            height=dp(35)
        )
        help_button.bind(on_press=self.show_help_dialog)
        toolbar.add_widget(help_button)
        
        # About button
        about_button = HackerButton(
            text='ℹ️ ABOUT',
            size_hint_x=0.2,
            font_size=dp(10),
            height=dp(35)
        )
        about_button.bind(on_press=self.show_about_dialog)
        toolbar.add_widget(about_button)
        
        # Check network status
        Clock.schedule_once(self.check_network, 1)
        
        return toolbar
    
    def check_network(self, dt):
        """Check network status"""
        if check_network_status():
            self.network_label.text = '🌐 Network: Connected'
            self.network_label.color = (0, 1, 0, 0.8)
        else:
            self.network_label.text = '🌐 Network: Offline'
            self.network_label.color = (1, 0, 0, 0.8)
    
    def show_about_dialog(self, instance):
        """Show about dialog"""
        dialog = MobileAboutDialog()
        dialog.open()
    
    def show_help_dialog(self, instance):
        """Show help dialog"""
        dialog = MobileHelpDialog()
        dialog.open()
    
    def show_export_dialog(self, instance):
        """Show export dialog"""
        if not self.results:
            self.log_output.add_log("No results to export!")
            return
        
        dialog = MobileExportDialog(results=self.results)
        dialog.set_callback(self.handle_export)
        dialog.open()
    
    def handle_export(self, export_type, results):
        """Handle export callback"""
        try:
            if export_type == 'json':
                filename = save_results_to_json_mobile(results)
                self.log_output.add_log(f"Results exported to {filename}")
            elif export_type == 'csv':
                filename = save_results_to_csv_mobile(results)
                self.log_output.add_log(f"Results exported to {filename}")
        except Exception as e:
            self.log_output.add_log(f"Export error: {str(e)}")
    
    def start_mirror(self, instance):
        """Start mirror process"""
        # Get URLs from input
        urls_text = self.url_input.text.strip()
        if not urls_text:
            self.log_output.add_log("Please enter at least one URL!")
            return
        
        # Parse URLs
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        if not urls:
            self.log_output.add_log("Please enter valid URLs!")
            return
        
        # Validate URLs
        valid_urls = []
        for url in urls:
            if validate_url_mobile(url):
                valid_urls.append(sanitize_url_mobile(url))
            else:
                self.log_output.add_log(f"Invalid URL: {url}")
        
        if not valid_urls:
            self.log_output.add_log("No valid URLs found!")
            return
        
        # Update UI
        self.is_mirroring = True
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.export_button.disabled = True
        self.progress_bar.value = 0
        self.results.clear()
        self.results_list.clear_results()
        
        # Update labels
        self.progress_label.text = f'Mirroring {len(valid_urls)} URLs...'
        self.log_output.add_log(f"Starting mass mirror for {len(valid_urls)} URLs...")
        
        # Start mirror thread
        self.mirror_thread = ZoneHMobileMirror(
            urls=valid_urls,
            delay=self.get_delay(),
            callback=self.mirror_callback
        )
        self.mirror_thread.start()
    
    def stop_mirror(self, instance):
        """Stop mirror process"""
        if self.mirror_thread and self.mirror_thread.is_alive():
            self.mirror_thread.stop()
            self.log_output.add_log("Stopping mirror process...")
            self.progress_label.text = 'Stopping...'
    
    def mirror_callback(self, event_type, data):
        """Callback untuk mirror thread"""
        if event_type == 'log':
            self.log_output.add_log(data)
        elif event_type == 'result':
            self.results.append(data)
            self.results_list.add_result(data)
            self.update_statistics()
        elif event_type == 'progress':
            self.progress_bar.value = data
        elif event_type == 'completed':
            self.mirror_completed()
    
    def update_statistics(self):
        """Update statistics labels"""
        total = len(self.results)
        success = sum(1 for r in self.results if r['status'] == 'Success')
        failed = total - success
        
        self.total_label.text = f'Total: {total}'
        self.success_label.text = f'Success: {success}'
        self.failed_label.text = f'Failed: {failed}'
    
    def mirror_completed(self):
        """Handle mirror completion"""
        self.is_mirroring = False
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.export_button.disabled = False
        self.progress_label.text = 'Mirror completed!'
        self.log_output.add_log("Mirror process completed!")
        
        # Calculate success rate
        if self.results:
            success_rate = calculate_success_rate_mobile(self.results)
            self.log_output.add_log(f"Success rate: {success_rate:.1f}%")
    
    def clear_all(self, instance):
        """Clear all data"""
        self.url_input.text = ''
        self.results_list.clear_results()
        self.results.clear()
        self.progress_bar.value = 0
        self.progress_label.text = 'Ready to start'
        self.update_statistics()
        self.log_output.clear_log()
        self.log_output.add_log("All data cleared!")
    
    def get_delay(self):
        """Get delay from settings"""
        # For now, use default delay
        # TODO: Get from settings panel
        return 2
    
    def on_stop(self):
        """Handle application stop"""
        if self.mirror_thread and self.mirror_thread.is_alive():
            self.mirror_thread.stop()
            self.mirror_thread.join(timeout=5)


def main():
    """Main function"""
    app = ZoneHMobileMirrorApp()
    app.run()


if __name__ == '__main__':
    main()