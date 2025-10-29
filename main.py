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
from threaded_content_window import ThreadedContentWindow
from view_config_manager import ViewConfigManager
from settings_dialog import SettingsDialog
from ui_styles_complete import *

class MainController(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.screen_manager = ScreenManager()
        
        # 线程化内容窗口管理
        self.content_windows = {}
        
        self.view_config_manager = ViewConfigManager()
        # 设置ViewConfigManager的父级引用，以便调用apply_content
        self.view_config_manager.main_controller = self
        self.selected_screen_index = -1  # 当前选中的屏幕
        self.settings_dialog = None
        self.current_settings = {}
        
        self.init_ui()
        self.connect_signals()
        self.load_settings()
        self.restore_window_state()  # 恢复窗口状态（现在被禁用）
        
        # 优化启动顺序，减少初始化时间
        QTimer.singleShot(100, self.center_window)  # 快速居中
        QTimer.singleShot(200, self.setup_screens)  # 快速设置屏幕
        QTimer.singleShot(800, self.load_last_session_config)  # 延迟加载配置
        QTimer.singleShot(500, lambda: self.log_message("✅ 系统初始化完成，准备就绪", "SUCCESS"))
        
        # 定期显示窗口状态（减少频率）
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.log_window_status)
        self.status_timer.start(30000)  # 每30秒显示一次状态
        
    def init_ui(self):
        self.setWindowTitle("🖥️ 多屏幕内容管理器")
        
        # 获取屏幕尺寸并设置合适的窗口大小
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # 使用相对尺寸，适应不同分辨率屏幕
        window_width = int(screen_width * 0.85)  # 屏幕宽度的85%
        window_height = int(screen_height * 0.8)  # 屏幕高度的80%
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = max(50, (screen_height - window_height) // 2)  # 确保不会超出屏幕顶部
        
        # 设置窗口位置和尺寸
        self.setGeometry(x, y, window_width, window_height)
        # 最小尺寸为屏幕的60%
        min_width = int(screen_width * 0.6)
        min_height = int(screen_height * 0.55)
        self.setMinimumSize(min_width, min_height)
        
        # 将窗口信息记录延迟到日志面板创建后
        self.window_info = f"🖥️ 窗口尺寸: {window_width}x{window_height}, 位置: ({x}, {y})"
        
    def center_window(self):
        """强制将窗口居中显示"""
        # 获取当前屏幕尺寸
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        # 获取当前窗口尺寸
        window_width = self.width()
        window_height = self.height()
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = max(100, (screen_height - window_height) // 2)  # 确保距离顶部至少100px
        
        # 移动窗口到居中位置
        self.move(x, y)
        
        # 记录新位置
        if hasattr(self, 'log_message'):
            self.log_message(f"🎯 窗口已居中: 位置({x}, {y}), 尺寸{window_width}x{window_height}", "INFO")
        
        # 应用现代化主窗口样式
        self.setStyleSheet(MAIN_WINDOW_STYLE)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 三段式：标题栏 + 配置中心 + 运行日志
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        main_layout.setSpacing(1)  # 减小间距为1px
        
        # 1. 标题栏（包含快速操作按钮）- 固定比例
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        self.create_enhanced_header_section(header_layout)
        main_layout.addWidget(header_widget, 0)  # stretch=0，固定大小
        
        # 2. 视图配置中心（集成屏幕控制功能）- 主要区域
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(0, 0, 0, 0)
        self.create_enhanced_config_center(config_layout)
        main_layout.addWidget(config_widget, 3)  # stretch=3，占主要空间
        
        # 3. 运行日志面板 - 较小比例
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        self.create_log_panel(log_layout)
        main_layout.addWidget(log_widget, 1)  # stretch=1，占较小空间
        
    def create_enhanced_header_section(self, parent_layout):
        """创建增强标题栏（包含快速操作按钮）"""
        header_frame = QFrame()
        header_frame.setStyleSheet(HEADER_FRAME_STYLE)
        # 移除固定高度限制，让标题栏自适应内容
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(5, 3, 5, 3)
        header_layout.setSpacing(1)
        
        # 左侧：标题信息 - 改为水平布局
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        
        # 主标题
        title_label = QLabel("🖥️ 多屏幕内容管理器")
        title_label.setStyleSheet(MAIN_TITLE_STYLE)
        
        # 副标题
        subtitle_label = QLabel("简洁高效的多显示器内容投放解决方案")
        subtitle_label.setStyleSheet(SUBTITLE_STYLE)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        header_layout.addLayout(title_layout)
        
        # 弹性空间
        header_layout.addStretch()
        
        # 右侧：快速操作按钮
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(1)
        
        # 设置按钮
        settings_btn = QPushButton("⚙️ 设置")
        settings_btn.setStyleSheet(STANDARD_BUTTON_STYLE)
        settings_btn.clicked.connect(self.show_settings_dialog)
        
        # 刷新屏幕按钮
        refresh_btn = QPushButton("🔄 刷新屏幕")
        refresh_btn.setStyleSheet(STANDARD_BUTTON_STYLE)
        refresh_btn.clicked.connect(self.refresh_screens)
        
        # 显示所有内容按钮
        show_all_btn = QPushButton("👁️ 显示所有")
        show_all_btn.setStyleSheet(STANDARD_BUTTON_STYLE)
        show_all_btn.clicked.connect(self.show_all_windows)
        
        # 隐藏所有内容按钮
        hide_all_btn = QPushButton("🙈 隐藏所有")
        hide_all_btn.setStyleSheet(STANDARD_BUTTON_STYLE)
        hide_all_btn.clicked.connect(self.hide_all_windows)
        
        actions_layout.addWidget(settings_btn)
        actions_layout.addWidget(refresh_btn)
        actions_layout.addWidget(show_all_btn)
        actions_layout.addWidget(hide_all_btn)
        
        header_layout.addLayout(actions_layout)
        parent_layout.addWidget(header_frame)
        
    def create_enhanced_config_center(self, parent_layout):
        """创建增强的视图配置中心（集成屏幕控制功能）"""
        # 直接使用视图配置管理器，占据整个中间区域
        config_manager_panel = self.create_config_manager_panel()
        parent_layout.addWidget(config_manager_panel)
        
        
    def create_config_manager_panel(self):
        """创建配置管理面板"""
        config_widget = QWidget()
        config_widget.setStyleSheet(CONFIG_PANEL_STYLE)
        
        config_layout = QVBoxLayout(config_widget)
        config_layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        config_layout.setSpacing(1)  # 减小间距为1px
        
        # 创建一个相对布局容器来放置标题和内容
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 将标题放在左上角，使用绝对定位
        title_label = QLabel("🎮 视图配置中心", content_container)
        title_label.setStyleSheet(CONFIG_CENTER_TITLE_STYLE)
        title_label.setFixedSize(title_label.sizeHint())
        title_label.move(10, 5)  # 定位到左上角
        
        # 视图配置管理器，添加顶部边距为标题留空间
        manager_widget = QWidget()
        manager_layout = QVBoxLayout(manager_widget)
        manager_layout.setContentsMargins(0, 35, 0, 0)  # 顶部留出标题空间
        manager_layout.addWidget(self.view_config_manager)
        
        content_layout.addWidget(manager_widget)
        config_layout.addWidget(content_container)
        
        return config_widget
        
    def create_log_panel(self, parent_layout):
        """创建底部运行日志面板"""
        
        # 日志面板容器
        log_group = QGroupBox("📋 运行日志")
        log_group.setStyleSheet(LOG_GROUP_BOX_STYLE)
        # 移除固定高度，让日志面板占用合适的比例空间
        
        log_layout = QVBoxLayout(log_group)
        log_layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        log_layout.setSpacing(1)  # 减小间距为1px
        
        # 日志文本显示区域
        self.log_text = QTextEdit()
        self.log_text.setStyleSheet(LOG_TEXT_EDIT_STYLE)
        self.log_text.setReadOnly(True)
        self.log_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.log_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 底部控制按钮栏
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(1)  # 减小间距为1px
        
        # 使用小型按钮样式
        
        # 清空日志按钮
        clear_btn = QPushButton("🗑️")
        clear_btn.setToolTip("清空日志")
        clear_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        clear_btn.clicked.connect(self.clear_log)
        clear_btn.setMaximumWidth(60)
        
        # 保存日志按钮
        save_log_btn = QPushButton("💾")
        save_log_btn.setToolTip("保存日志")
        save_log_btn.setStyleSheet(SMALL_BUTTON_STYLE)
        save_log_btn.clicked.connect(self.save_log)
        save_log_btn.setMaximumWidth(60)
        
        controls_layout.addWidget(clear_btn)
        controls_layout.addWidget(save_log_btn)
        controls_layout.addStretch()
        
        # 实时显示开关
        self.auto_scroll_checkbox = QPushButton("📜")
        self.auto_scroll_checkbox.setToolTip("自动滚动")
        self.auto_scroll_checkbox.setCheckable(True)
        self.auto_scroll_checkbox.setChecked(True)
        self.auto_scroll_checkbox.setStyleSheet(SMALL_BUTTON_STYLE)
        self.auto_scroll_checkbox.setMaximumWidth(60)
        
        controls_layout.addWidget(self.auto_scroll_checkbox)
        
        log_layout.addWidget(self.log_text)
        log_layout.addLayout(controls_layout)
        
        parent_layout.addWidget(log_group)
        
        # 简化初始化日志
        self.log_message("🚀 多屏幕内容管理器启动", "INFO")
        
    def log_message(self, message, level="INFO"):
        """添加日志消息"""
        from datetime import datetime
        
        # 获取当前时间
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 根据日志级别选择颜色和图标
        if level == "INFO":
            color = "#00ffff"
            icon = "ℹ️"
        elif level == "SUCCESS":
            color = "#00ff7f"
            icon = "✅"
        elif level == "WARNING":
            color = "#ffa500"
            icon = "⚠️"
        elif level == "ERROR":
            color = "#ff1493"
            icon = "❌"
        else:
            color = "#e0e6ed"
            icon = "📝"
        
        # 格式化日志消息
        formatted_message = f'<span style="color: #7fb3d3;">[{timestamp}]</span> <span style="color: {color};">{icon} {level}:</span> <span style="color: #e0e6ed;">{message}</span>'
        
        # 添加到日志显示区域
        if hasattr(self, 'log_text'):
            self.log_text.append(formatted_message)
            
            # 自动滚动到底部
            if hasattr(self, 'auto_scroll_checkbox') and self.auto_scroll_checkbox.isChecked():
                scrollbar = self.log_text.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self.log_message("🗑️ 日志已清空", "INFO")
        
    def save_log(self):
        """保存日志到文件"""
        from datetime import datetime
        from PyQt5.QtWidgets import QFileDialog
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"运行日志_{timestamp}.txt"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存日志文件", default_filename, 
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if filename:
            try:
                # 获取纯文本内容（去除HTML格式）
                plain_text = self.log_text.toPlainText()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(plain_text)
                self.log_message(f"💾 日志已保存到: {filename}", "SUCCESS")
            except Exception as e:
                self.log_message(f"❌ 保存日志失败: {str(e)}", "ERROR")
        
    def setup_screens(self):
        """初始化屏幕信息"""
        screens = self.screen_manager.get_screens()
        self.screens = screens
        
        self.log_message(f"🖥️ 检测到 {len(screens)} 个屏幕", "INFO")
        
        # 将屏幕信息传递给ViewConfigManager，但不预创建窗口（按需创建）
        for i, screen in enumerate(screens):
            self.view_config_manager.add_screen(i, screen)
            self.log_message(f"✅ 检测到屏幕 {i + 1}: {screen['width']}x{screen['height']}", "INFO")
            
        self.log_message("✅ 屏幕信息加载完成", "SUCCESS")
            
    def select_file(self, text_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            text_edit.setText(file_path)
    
    def create_content_window_for_screen(self, screen_index):
        """为指定屏幕创建内容窗口"""
        try:
            # 获取屏幕信息
            if hasattr(self, 'screens') and screen_index < len(self.screens):
                screen_info = self.screens[screen_index]
                
                # 创建内容窗口
                content_window = ThreadedContentWindow(screen_index, screen_info)
                content_window.window_closed.connect(self.on_content_window_closed)
                self.content_windows[screen_index] = content_window
                
                self.log_message(f"✅ 为屏幕 {screen_index + 1} 创建内容窗口", "SUCCESS")
                return True
            else:
                self.log_message(f"❌ 屏幕 {screen_index + 1} 信息不存在", "ERROR")
                return False
                
        except Exception as e:
            self.log_message(f"❌ 创建屏幕 {screen_index + 1} 内容窗口失败: {str(e)}", "ERROR")
            return False
            
    def apply_content(self, screen_index, content_type, content):
        # 如果内容窗口不存在，先创建它
        if screen_index not in self.content_windows:
            self.create_content_window_for_screen(screen_index)
        
        if screen_index in self.content_windows:
            window = self.content_windows[screen_index]
            window.set_content(content_type, content)
            window.show()
            self.log_message(f"✅ 屏幕 {screen_index + 1} 已应用{content_type}内容", "SUCCESS")
            
            # 更新视图配置
            self.view_config_manager.update_screen_content(screen_index, content_type, content)
        else:
            self.log_message(f"❌ 无法为屏幕 {screen_index + 1} 创建内容窗口", "ERROR")
            
    def apply_saved_config(self, screens_config):
        """应用保存的配置 - 只为有内容的屏幕创建窗口"""
        self.log_message("📂 开始应用保存的配置...", "INFO")
        
        applied_count = 0
        for screen_index_str, config in screens_config.items():
            try:
                screen_index = int(screen_index_str)
                content_type = config.get('content_type', '无内容')
                content = config.get('content', '')
                
                # 只处理有内容的屏幕
                if content_type != '无内容' and content.strip():
                    self.apply_content(screen_index, content_type, content)
                    applied_count += 1
                    self.log_message(f"📄 屏幕 {screen_index + 1} 应用配置: {content_type}", "INFO")
                else:
                    # 如果屏幕有窗口但配置为无内容，关闭该窗口
                    if screen_index in self.content_windows:
                        self.content_windows[screen_index].close()
                        del self.content_windows[screen_index]
                        self.log_message(f"🚫 屏幕 {screen_index + 1} 无内容，关闭窗口", "INFO")
                    
            except (ValueError, KeyError) as e:
                self.log_message(f"应用配置失败 - 屏幕 {screen_index_str}: {e}", "ERROR")
                
        if applied_count > 0:
            self.log_message(f"✅ 配置应用完成，共处理 {applied_count} 个有内容的屏幕", "SUCCESS")
        else:
            self.log_message("ℹ️ 配置中没有需要显示的内容", "INFO")
            
    def refresh_screens(self):
        self.log_message("🔄 正在刷新屏幕配置...", "INFO")
        
        # 清空视图配置
        self.view_config_manager.clear_screens()
        
        # 重新获取屏幕信息
        self.screen_manager.refresh()
        self.setup_screens()
        
        self.log_message("✅ 屏幕刷新完成", "SUCCESS")
        
    def show_all_windows(self):
        self.log_message("👁️ 显示所有屏幕窗口", "INFO")
        for window in self.content_windows.values():
            window.show()
        self.log_message(f"✅ 已显示 {len(self.content_windows)} 个窗口", "SUCCESS")
            
    def hide_all_windows(self):
        self.log_message("🚫 隐藏所有屏幕窗口", "INFO")
        for window in self.content_windows.values():
            window.hide()
        self.log_message(f"✅ 已隐藏 {len(self.content_windows)} 个窗口", "SUCCESS")
            
    def connect_signals(self):
        """连接信号"""
        # 连接视图配置管理器的屏幕选择信号
        self.view_config_manager.screen_layout_view.screen_selected.connect(self.on_screen_selected_from_view)
        
        # 连接配置应用请求信号
        self.view_config_manager.apply_config_requested.connect(self.apply_saved_config)
        
    def on_content_window_closed(self, screen_index):
        """处理内容窗口关闭事件"""
        if screen_index in self.content_windows:
            del self.content_windows[screen_index]
        self.log_message(f"📄 屏幕 {screen_index + 1} 窗口已关闭", "INFO")
        
    def on_screen_selected_from_view(self, screen_index):
        """从视图配置中选择屏幕的处理"""
        self.selected_screen_index = screen_index
        self.log_message(f"从视图中选择了屏幕 {screen_index + 1}", "INFO")
        
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
        
    def closeEvent(self, event):
        # 保存窗口状态
        self.save_window_state()
        
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
            self.log_message(f"保存默认配置失败: {e}", "ERROR")
        
        # 关闭所有内容窗口
        for window in self.content_windows.values():
            window.close()
            
        # 关闭设置对话框
        if self.settings_dialog:
            self.settings_dialog.close()
            
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
            self.log_message(f"加载上次会话配置失败: {e}", "ERROR")
    
    def log_window_status(self):
        """定期记录窗口状态"""
        window_count = len(self.content_windows)
        if window_count > 0:
            self.log_message(f"📊 当前运行 {window_count} 个内容窗口", "INFO")
    
    def show_settings_dialog(self):
        """显示设置对话框"""
        if self.settings_dialog is None:
            self.settings_dialog = SettingsDialog(self)
            self.settings_dialog.settings_changed.connect(self.apply_settings)
        
        self.settings_dialog.show()
        self.settings_dialog.raise_()
        self.settings_dialog.activateWindow()
    
    def load_settings(self):
        """加载设置"""
        try:
            self.settings_dialog = SettingsDialog(self)
            self.current_settings = self.settings_dialog.get_settings()
            self.apply_settings(self.current_settings)
        except Exception as e:
            self.log_message(f"加载设置失败: {e}", "ERROR")
            self.current_settings = {}
    
    def apply_settings(self, settings):
        """应用设置"""
        self.current_settings = settings
        # 这里可以添加设置应用逻辑
    
    def save_window_state(self):
        """保存窗口状态"""
        if self.current_settings.get("remember_position", True):
            try:
                state = {
                    "geometry": [self.x(), self.y(), self.width(), self.height()],
                    "maximized": self.isMaximized()
                }
                
                with open("window_state.json", 'w', encoding='utf-8') as f:
                    json.dump(state, f, indent=2)
                    
            except Exception as e:
                self.log_message(f"保存窗口状态失败: {e}", "ERROR")
    
    def restore_window_state(self):
        """恢复窗口状态 - 临时禁用以确保窗口居中"""
        # 暂时禁用窗口状态恢复，强制居中显示
        self.log_message("🚫 窗口状态恢复已禁用，强制居中显示", "INFO")
        return

def start_with_splash():
    """带启动画面的启动函数"""
    # 设置QApplication属性（必须在创建QApplication之前）
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    
    # 创建应用程序
    app = QApplication(sys.argv)
    app.setApplicationName("多屏幕内容管理器")
    app.setApplicationVersion("2.0")
    
    # 立即创建并显示启动画面
    from splash_screen import SplashScreen
    splash = SplashScreen()
    splash.show()
    splash.update_progress(5, "正在启动...")
    
    # 强制处理事件，确保启动画面立即显示
    app.processEvents()
    
    # 主窗口实例
    main_window = None
    
    def create_main_window_step_by_step():
        """分步创建主窗口"""
        nonlocal main_window
        
        try:
            # 步骤1: 初始化基础组件
            splash.update_progress(15, "初始化系统组件...")
            app.processEvents()
            QTimer.singleShot(50, step_2)
            
        except Exception as e:
            print(f"步骤1失败: {e}")
            
    def step_2():
        """步骤2: 创建资源目录"""
        try:
            if not os.path.exists("assets"):
                os.makedirs("assets")
            splash.update_progress(25, "创建资源目录...")
            app.processEvents()
            QTimer.singleShot(50, step_3)
        except Exception as e:
            print(f"步骤2失败: {e}")
            
    def step_3():
        """步骤3: 开始创建主窗口"""
        try:
            splash.update_progress(35, "初始化主窗口...")
            app.processEvents()
            QTimer.singleShot(100, step_4)
        except Exception as e:
            print(f"步骤3失败: {e}")
            
    def step_4():
        """步骤4: 实际创建主窗口对象"""
        nonlocal main_window
        try:
            main_window = MainController()
            splash.update_progress(70, "加载界面组件...")
            app.processEvents()
            QTimer.singleShot(100, step_5)
        except Exception as e:
            print(f"步骤4失败: {e}")
            
    def step_5():
        """步骤5: 完成初始化"""
        try:
            splash.update_progress(85, "准备用户界面...")
            app.processEvents()
            QTimer.singleShot(100, step_6)
        except Exception as e:
            print(f"步骤5失败: {e}")
            
    def step_6():
        """步骤6: 最终完成"""
        try:
            splash.update_progress(95, "最后准备...")
            app.processEvents()
            QTimer.singleShot(100, final_step)
        except Exception as e:
            print(f"步骤6失败: {e}")
            
    def final_step():
        """最终步骤"""
        try:
            splash.update_progress(100, "启动完成！")
            app.processEvents()
        except Exception as e:
            print(f"最终步骤失败: {e}")
    
    def on_splash_complete():
        """启动画面完成后的处理"""
        try:
            # 隐藏启动画面
            splash.hide()
            
            # 显示主窗口
            if main_window:
                main_window.show()
                main_window.raise_()
                main_window.activateWindow()
            else:
                print("错误：主窗口未创建成功")
        except Exception as e:
            print(f"启动完成处理失败: {e}")
    
    # 连接启动完成信号
    splash.startup_complete.connect(on_splash_complete)
    
    # 延迟50ms后开始创建主窗口，确保启动画面先显示
    QTimer.singleShot(50, create_main_window_step_by_step)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    start_with_splash()