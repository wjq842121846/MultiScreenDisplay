import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTextEdit, QComboBox, QFileDialog, QScrollArea, 
                             QFrame, QGridLayout, QGroupBox, QLineEdit, QSplitter, QMenu, QAction, 
                             QInputDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QIcon
from screen_manager import ScreenManager
from content_window import ContentWindow
from view_config_manager import ViewConfigManager
from ui_styles import *

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.screen_manager = ScreenManager()
        self.content_windows = {}
        self.view_config_manager = ViewConfigManager()
        self.selected_screen_index = -1  # 当前选中的屏幕
        self.init_ui()
        self.setup_screens()
        self.connect_signals()
        
        # 延迟加载上次会话配置
        QTimer.singleShot(1500, self.load_last_session_config)
        
    def init_ui(self):
        self.setWindowTitle("🖥️ 多屏幕内容管理器")
        self.setGeometry(200, 100, 1600, 1000)
        
        # 设置全局样式，包括消息框修复
        global_style = """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                color: #ffffff;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(52, 152, 219, 0.1),
                                          stop:1 rgba(52, 152, 219, 0.05));
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background: #3498db;
                border-radius: 6px;
                color: white;
            }
            /* 修复消息框样式 */
            QMessageBox {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 8px;
                font-size: 12px;
            }
            QMessageBox QLabel {
                color: #ecf0f1;
                font-size: 12px;
                padding: 10px;
                margin: 5px;
                background: transparent;
                min-height: 40px;
                max-width: 400px;
                word-wrap: true;
            }
            QMessageBox QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
                min-height: 30px;
                margin: 5px;
            }
            QMessageBox QPushButton:hover {
                background: #2980b9;
            }
            QMessageBox QPushButton:pressed {
                background: #21618c;
            }
            /* 修复输入对话框样式 */
            QInputDialog {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 8px;
            }
            QInputDialog QLabel {
                color: #ecf0f1;
                font-size: 12px;
                padding: 8px;
                background: transparent;
            }
            QInputDialog QLineEdit {
                background: #34495e;
                border: 1px solid #3498db;
                border-radius: 4px;
                padding: 8px;
                color: #ecf0f1;
                font-size: 12px;
                min-height: 20px;
            }
        """
        
        # 应用现代化主窗口样式
        self.setStyleSheet(global_style)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 使用更现代的布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 顶部标题区域
        self.create_header_section(main_layout)
        
        # 主内容区域
        content_splitter = QSplitter(Qt.Horizontal)
        content_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #34495e;
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QSplitter::handle:hover {
                background: #3498db;
            }
        """)
        
        # 左侧控制面板
        left_panel = self.create_left_panel()
        
        # 右侧预览面板
        right_panel = self.create_right_panel()
        
        content_splitter.addWidget(left_panel)
        content_splitter.addWidget(right_panel)
        content_splitter.setSizes([650, 950])  # 设置初始比例
        
        main_layout.addWidget(content_splitter)
        
    def create_header_section(self, parent_layout):
        """创建顶部标题区域"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 rgba(52, 152, 219, 0.8),
                                          stop:0.5 rgba(155, 89, 182, 0.8),
                                          stop:1 rgba(52, 152, 219, 0.8));
                border-radius: 15px;
                padding: 15px;
                margin: 5px;
            }
        """)
        header_frame.setMaximumHeight(100)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # 左侧图标和标题
        title_layout = QVBoxLayout()
        
        title_label = QLabel("🖥️ 多屏幕内容管理器")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
        """)
        
        subtitle_label = QLabel("专业的多显示器内容投放解决方案")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                margin-top: 5px;
            }
        """)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        header_layout.addLayout(title_layout)
        
        header_layout.addStretch()
        
        # 右侧快速操作按钮
        quick_actions_layout = QHBoxLayout()
        
        # 快速配置按钮
        quick_config_btn = QPushButton("⚡ 快速配置")
        quick_config_btn.setStyleSheet(self.get_modern_button_style("#e74c3c"))
        quick_config_btn.clicked.connect(self.show_quick_config_menu)
        
        # 保存配置按钮
        save_config_btn = QPushButton("💾 保存配置")
        save_config_btn.setStyleSheet(self.get_modern_button_style("#27ae60"))
        save_config_btn.clicked.connect(self.quick_save_config)
        
        quick_actions_layout.addWidget(quick_config_btn)
        quick_actions_layout.addWidget(save_config_btn)
        header_layout.addLayout(quick_actions_layout)
        
        parent_layout.addWidget(header_frame)
        
    def get_modern_button_style(self, color):
        """获取现代化按钮样式"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 {color}, stop:1 rgba(0,0,0,0.2));
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: rgba(0,0,0,0.3);
                transform: translateY(0px);
            }}
        """
        
    def create_left_panel(self):
        """创建左侧控制面板"""
        left_widget = QWidget()
        left_widget.setStyleSheet("""
            QWidget {
                background: rgba(44, 62, 80, 0.3);
                border-radius: 12px;
            }
        """)
        
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(15, 15, 15, 15)
        left_layout.setSpacing(15)
        
        # 屏幕控制区域
        self.create_modern_screen_controls(left_layout)
        
        # 操作控制区域
        self.create_modern_control_buttons(left_layout)
        
        return left_widget
        
    def create_right_panel(self):
        """创建右侧预览面板"""
        right_widget = QWidget()
        right_widget.setStyleSheet("""
            QWidget {
                background: rgba(52, 73, 94, 0.3);
                border-radius: 12px;
            }
        """)
        
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(15, 15, 15, 15)
        
        # 视图配置标题
        config_title = QLabel("🎮 视图配置中心")
        config_title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ecf0f1;
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 rgba(155, 89, 182, 0.8),
                                          stop:1 rgba(52, 152, 219, 0.8));
                border-radius: 8px;
                margin-bottom: 10px;
            }
        """)
        config_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(config_title)
        
        # 视图配置管理器
        right_layout.addWidget(self.view_config_manager)
        
        return right_widget
        
    def create_modern_screen_controls(self, parent_layout):
        """创建现代化屏幕控制区域"""
        controls_group = QGroupBox("🖥️ 屏幕控制中心")
        controls_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #27ae60;
                border-radius: 15px;
                margin-top: 20px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(39, 174, 96, 0.15),
                                          stop:1 rgba(39, 174, 96, 0.05));
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 5px 12px 5px 12px;
                background: #27ae60;
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }
        """)
        
        controls_layout = QVBoxLayout(controls_group)
        controls_layout.setSpacing(15)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(52, 73, 94, 0.3);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #2980b9;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")
        self.screens_layout = QVBoxLayout(scroll_widget)
        self.screens_layout.setSpacing(20)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(400)
        
        controls_layout.addWidget(scroll_area)
        parent_layout.addWidget(controls_group)
        
    def create_modern_control_buttons(self, parent_layout):
        """创建现代化操作按钮区域"""
        button_group = QGroupBox("🎮 快速操作")
        button_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #e67e22;
                border-radius: 15px;
                margin-top: 20px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(230, 126, 34, 0.15),
                                          stop:1 rgba(230, 126, 34, 0.05));
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 5px 12px 5px 12px;
                background: #e67e22;
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }
        """)
        button_group.setMaximumHeight(120)
        
        button_layout = QVBoxLayout(button_group)
        button_layout.setSpacing(12)
        
        # 操作按钮行
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新屏幕")
        refresh_btn.setStyleSheet(self.get_control_button_style("#3498db"))
        refresh_btn.clicked.connect(self.refresh_screens)
        
        # 显示所有按钮
        show_all_btn = QPushButton("👁️ 显示所有")
        show_all_btn.setStyleSheet(self.get_control_button_style("#27ae60"))
        show_all_btn.clicked.connect(self.show_all_windows)
        
        # 隐藏所有按钮
        hide_all_btn = QPushButton("🚫 隐藏所有")
        hide_all_btn.setStyleSheet(self.get_control_button_style("#e74c3c"))
        hide_all_btn.clicked.connect(self.hide_all_windows)
        
        actions_layout.addWidget(refresh_btn)
        actions_layout.addWidget(show_all_btn)
        actions_layout.addWidget(hide_all_btn)
        
        button_layout.addLayout(actions_layout)
        parent_layout.addWidget(button_group)
        
    def get_control_button_style(self, color):
        """获取控制按钮样式"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 {color}, stop:1 rgba(0,0,0,0.2));
                border: 1px solid rgba(255,255,255,0.3);
            }}
            QPushButton:pressed {{
                background: rgba(0,0,0,0.3);
                border: 1px solid rgba(255,255,255,0.5);
            }}
        """
        
    def setup_screens(self):
        screens = self.screen_manager.get_screens()
        
        for i, screen in enumerate(screens):
            self.create_screen_control_panel(i, screen)
            
    def create_screen_control_panel(self, screen_index, screen_info):
        primary_text = " (主屏幕)" if screen_info['is_primary'] else ""
        
        # 创建现代化的屏幕控制面板
        group_box = QGroupBox(f"🖥️ 屏幕 {screen_index + 1}{primary_text}")
        group_box.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(155, 89, 182, 0.1),
                                          stop:1 rgba(155, 89, 182, 0.03));
                color: #ecf0f1;
                min-height: 200px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 4px 10px 4px 10px;
                background: #9b59b6;
                border-radius: 6px;
                color: white;
                font-size: 12px;
            }
        """)
        
        group_layout = QVBoxLayout(group_box)
        group_layout.setSpacing(12)
        group_layout.setContentsMargins(15, 20, 15, 15)
        
        # 屏幕信息区域
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: rgba(52, 73, 94, 0.3);
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(5)
        
        # 分辨率信息
        resolution_label = QLabel(f"📐 分辨率: {screen_info['width']} × {screen_info['height']}")
        resolution_label.setStyleSheet("""
            QLabel {
                color: #74b9ff;
                font-size: 11px;
                font-weight: normal;
                background: transparent;
                padding: 2px;
            }
        """)
        
        # 位置信息
        position_label = QLabel(f"📍 位置: ({screen_info['x']}, {screen_info['y']})")
        position_label.setStyleSheet("""
            QLabel {
                color: #a29bfe;
                font-size: 11px;
                font-weight: normal;
                background: transparent;
                padding: 2px;
            }
        """)
        
        info_layout.addWidget(resolution_label)
        info_layout.addWidget(position_label)
        group_layout.addWidget(info_frame)
        
        # 内容配置区域
        config_frame = QFrame()
        config_frame.setStyleSheet("""
            QFrame {
                background: rgba(46, 204, 113, 0.1);
                border-radius: 8px;
                padding: 10px;
                margin: 2px;
            }
        """)
        config_layout = QVBoxLayout(config_frame)
        config_layout.setSpacing(10)
        
        # 内容类型选择
        type_layout = QHBoxLayout()
        content_type_label = QLabel("📝 内容类型:")
        content_type_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
                min-width: 80px;
            }
        """)
        
        content_type_combo = QComboBox()
        content_type_combo.setStyleSheet("""
            QComboBox {
                background: #34495e;
                border: 2px solid #3498db;
                border-radius: 6px;
                padding: 6px 10px;
                color: #ecf0f1;
                font-size: 11px;
                min-height: 25px;
            }
            QComboBox:hover {
                border-color: #2980b9;
                background: #2c3e50;
            }
            QComboBox::drop-down {
                border: none;
                background: #3498db;
                width: 20px;
                border-radius: 3px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                background: white;
            }
            QComboBox QAbstractItemView {
                background: #2c3e50;
                border: 1px solid #3498db;
                selection-background-color: #3498db;
                color: #ecf0f1;
            }
        """)
        content_type_combo.addItems(["文本", "图片", "视频", "网页"])
        
        type_layout.addWidget(content_type_label)
        type_layout.addWidget(content_type_combo)
        config_layout.addLayout(type_layout)
        
        # 内容输入区域
        content_label = QLabel("📄 内容:")
        content_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
            }
        """)
        config_layout.addWidget(content_label)
        
        content_input = QTextEdit()
        content_input.setStyleSheet("""
            QTextEdit {
                background: #2c3e50;
                border: 2px solid #16a085;
                border-radius: 6px;
                padding: 8px;
                color: #ecf0f1;
                font-size: 11px;
                max-height: 60px;
                min-height: 60px;
            }
            QTextEdit:focus {
                border-color: #1abc9c;
                background: #34495e;
            }
        """)
        content_input.setPlaceholderText("输入文本内容或文件路径...")
        config_layout.addWidget(content_input)
        
        group_layout.addWidget(config_frame)
        
        # 操作按钮区域
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background: rgba(52, 152, 219, 0.1);
                border-radius: 8px;
                padding: 8px;
                margin: 2px;
            }
        """)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(8)
        
        # 选择文件按钮
        file_btn = QPushButton("📁 选择文件")
        file_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: #2980b9;
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:pressed {
                background: #21618c;
            }
        """)
        file_btn.clicked.connect(lambda: self.select_file(content_input))
        
        # 应用按钮
        apply_btn = QPushButton("✅ 应用到屏幕")
        apply_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 10px;
                min-height: 30px;
            }
            QPushButton:hover {
                background: #229954;
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:pressed {
                background: #1e8449;
            }
        """)
        apply_btn.clicked.connect(lambda: self.apply_content(screen_index, content_type_combo.currentText(), content_input.toPlainText()))
        
        button_layout.addWidget(file_btn)
        button_layout.addWidget(apply_btn)
        group_layout.addWidget(button_frame)
        
        self.screens_layout.addWidget(group_box)
        
        # 创建内容窗口和预览
        if screen_index not in self.content_windows:
            self.content_windows[screen_index] = ContentWindow(screen_index, screen_info)
            
        # 添加到视图配置管理器
        self.view_config_manager.add_screen(screen_index, screen_info)
            
    def select_file(self, text_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            text_edit.setText(file_path)
            
    def apply_content(self, screen_index, content_type, content):
        if screen_index in self.content_windows:
            window = self.content_windows[screen_index]
            window.set_content(content_type, content)
            window.show()
            
            # 更新视图配置
            self.view_config_manager.update_screen_content(screen_index, content_type, content)
            
    def apply_saved_config(self, screens_config):
        """应用保存的配置"""
        for screen_index_str, config in screens_config.items():
            try:
                screen_index = int(screen_index_str)
                content_type = config.get('content_type', '无内容')
                content = config.get('content', '')
                
                if content_type != '无内容' and content:
                    self.apply_content(screen_index, content_type, content)
                    
            except (ValueError, KeyError) as e:
                print(f"应用配置失败 - 屏幕 {screen_index_str}: {e}")
            
    def refresh_screens(self):
        # 清空现有控件
        for i in reversed(range(self.screens_layout.count())):
            self.screens_layout.itemAt(i).widget().setParent(None)
            
        # 清空视图配置
        self.view_config_manager.clear_screens()
        
        # 重新获取屏幕信息
        self.screen_manager.refresh()
        self.setup_screens()
        
    def show_all_windows(self):
        for window in self.content_windows.values():
            window.show()
            
    def hide_all_windows(self):
        for window in self.content_windows.values():
            window.hide()
            
    def connect_signals(self):
        """连接信号"""
        # 连接视图配置管理器的屏幕选择信号
        self.view_config_manager.screen_layout_view.screen_selected.connect(self.on_screen_selected_from_view)
        
        # 连接配置应用请求信号
        self.view_config_manager.apply_config_requested.connect(self.apply_saved_config)
        
    def on_screen_selected_from_view(self, screen_index):
        """从视图配置中选择屏幕的处理"""
        self.selected_screen_index = screen_index
        print(f"从视图中选择了屏幕 {screen_index + 1}")
        
        # 可以在这里添加额外的处理逻辑，比如:
        # - 高亮对应的控制面板
        # - 滚动到对应的控制区域
        # - 自动设置焦点到对应的输入控件
        
    def get_selected_screen_info(self):
        """获取当前选中屏幕的信息"""
        if self.selected_screen_index >= 0:
            screens = self.screen_manager.get_screens()
            if self.selected_screen_index < len(screens):
                return screens[self.selected_screen_index]
        return None
        
    def apply_content_to_selected(self, content_type, content):
        """应用内容到当前选中的屏幕"""
        if self.selected_screen_index >= 0:
            self.apply_content(self.selected_screen_index, content_type, content)
        
    def show_quick_config_menu(self):
        """显示快速配置菜单"""
        config_dir = "view_configs"
        if not os.path.exists(config_dir):
            QMessageBox.information(self, "提示", "暂无保存的配置！")
            return
            
        # 获取所有配置文件
        config_files = [f for f in os.listdir(config_dir) if f.endswith('.json') and not f.startswith('_')]
        
        if not config_files:
            QMessageBox.information(self, "提示", "暂无保存的配置！")
            return
        
        # 创建菜单
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #2c3e50;
                border: 1px solid #3498db;
                border-radius: 5px;
                color: #ecf0f1;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 3px;
            }
            QMenu::item:selected {
                background: #3498db;
            }
        """)
        
        # 添加配置项到菜单
        for config_file in sorted(config_files):
            try:
                config_path = os.path.join(config_dir, config_file)
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                config_name = config_data.get('name', os.path.splitext(config_file)[0])
                screen_count = len(config_data.get('screens', {}))
                
                action_text = f"📝 {config_name} ({screen_count}个屏幕)"
                action = QAction(action_text, self)
                action.triggered.connect(lambda checked, path=config_path: self.quick_apply_config(path))
                menu.addAction(action)
                
            except Exception as e:
                print(f"读取配置文件 {config_file} 失败: {e}")
        
        if menu.actions():
            # 显示菜单
            button = self.sender()
            menu.exec_(button.mapToGlobal(button.rect().bottomLeft()))
        else:
            QMessageBox.information(self, "提示", "没有可用的配置！")
    
    def quick_apply_config(self, config_path):
        """快速应用指定配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            screens_config = config_data.get('screens', {})
            config_name = config_data.get('name', '未命名')
            
            if not screens_config:
                QMessageBox.warning(self, "警告", "该配置没有屏幕设置！")
                return
            
            # 应用配置
            self.apply_saved_config(screens_config)
            
            # 显示成功信息
            screen_count = len(screens_config)
            QMessageBox.information(self, "成功", f"已应用配置 '{config_name}'\n包含 {screen_count} 个屏幕设置")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"应用配置失败：{str(e)}")
    
    def quick_save_config(self):
        """快速保存当前配置"""
        current_config = self.view_config_manager.get_current_config()
        
        if not current_config:
            QMessageBox.information(self, "提示", "当前没有需要保存的配置！")
            return
        
        # 输入配置名称
        config_name, ok = QInputDialog.getText(
            self, "保存配置", "请输入配置名称:",
            text=f"配置_{datetime.now().strftime('%m%d_%H%M')}"
        )
        
        if not ok or not config_name.strip():
            return
            
        config_name = config_name.strip()
        
        # 检查配置是否已存在
        config_dir = "view_configs"
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            
        config_file = os.path.join(config_dir, f"{config_name}.json")
        if os.path.exists(config_file):
            reply = QMessageBox.question(
                self, "确认覆盖", 
                f"配置 '{config_name}' 已存在，是否覆盖？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # 保存配置
        config_data = {
            "name": config_name,
            "description": f"快速保存于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "created_time": datetime.now().isoformat(),
            "screens": current_config
        }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            screen_count = len(current_config)
            QMessageBox.information(self, "成功", f"配置 '{config_name}' 已保存！\n包含 {screen_count} 个屏幕设置")
            
            # 刷新视图配置管理器的列表
            self.view_config_manager.refresh_config_list()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置失败：{str(e)}")
        
    def closeEvent(self, event):
        # 保存当前配置为默认配置
        try:
            current_config = self.view_config_manager.get_current_config()
            if current_config:
                config_data = {
                    "name": "默认配置",
                    "description": "程序关闭时自动保存的配置",
                    "created_time": datetime.now().isoformat(),
                    "screens": current_config
                }
                
                # 确保配置目录存在
                config_dir = "view_configs"
                if not os.path.exists(config_dir):
                    os.makedirs(config_dir)
                
                # 保存默认配置
                default_config_path = os.path.join(config_dir, "_last_session.json")
                with open(default_config_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
                    
        except Exception as e:
            print(f"保存默认配置失败: {e}")
        
        # 关闭所有内容窗口
        for window in self.content_windows.values():
            window.close()
        event.accept()
        
    def load_last_session_config(self):
        """加载上次会话的配置"""
        try:
            config_path = os.path.join("view_configs", "_last_session.json")
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                screens_config = config_data.get('screens', {})
                if screens_config:
                    # 延迟应用配置，确保界面完全初始化
                    QTimer.singleShot(1000, lambda: self.apply_saved_config(screens_config))
                    
        except Exception as e:
            print(f"加载上次会话配置失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("多屏幕内容管理器")
    app.setApplicationVersion("2.0")
    
    # 设置应用图标（如果存在）
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    # 设置高DPI支持
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    main_window = MainController()
    main_window.show()
    
    sys.exit(app.exec_())