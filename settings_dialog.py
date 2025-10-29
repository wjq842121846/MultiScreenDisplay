#!/usr/bin/env python3
"""
设置对话框组件
包含字体设置、开机自启等配置选项
"""

import os
import sys
import json
import winreg
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QCheckBox, QGroupBox,
                             QSlider, QMessageBox, QComboBox, QFrame,
                             QTabWidget, QWidget, QGridLayout, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SettingsDialog(QDialog):
    """设置对话框"""
    
    # 设置变更信号
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = self.load_settings()
        self.init_ui()
        self.load_current_settings()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("🔧 软件设置")
        self.setFixedSize(600, 500)
        self.setModal(True)
        
        # 设置对话框样式
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #2c3e50, stop:1 #34495e);
                color: #ecf0f1;
                font-size: 16px;
            }
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 15px;
                padding-top: 15px;
                background: rgba(52, 152, 219, 0.1);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 5px 12px;
                background: #3498db;
                border-radius: 6px;
                color: white;
                font-size: 16px;
            }
            QLabel {
                font-size: 16px;
                color: #ecf0f1;
                padding: 5px;
            }
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
                min-height: 35px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
            QPushButton:pressed {
                background: #21618c;
            }
            QCheckBox {
                font-size: 16px;
                color: #ecf0f1;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 3px;
                border: 2px solid #3498db;
                background: #2c3e50;
            }
            QCheckBox::indicator:checked {
                background: #3498db;
                border-color: #2980b9;
            }
            QSpinBox, QComboBox {
                background: #34495e;
                border: 2px solid #3498db;
                border-radius: 6px;
                padding: 8px 12px;
                color: #ecf0f1;
                font-size: 16px;
                min-height: 25px;
            }
            QSpinBox:focus, QComboBox:focus {
                border-color: #2980b9;
            }
            QSlider::groove:horizontal {
                border: 1px solid #34495e;
                height: 8px;
                background: #2c3e50;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 2px solid #2980b9;
                width: 20px;
                border-radius: 10px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #2980b9;
            }
            QTabWidget::pane {
                border: 2px solid #3498db;
                border-radius: 8px;
                background: rgba(52, 152, 219, 0.05);
            }
            QTabBar::tab {
                background: #34495e;
                color: #ecf0f1;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background: #2980b9;
            }
        """)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("🔧 软件设置")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #3498db;
                padding: 10px;
                border-bottom: 2px solid #3498db;
                margin-bottom: 15px;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        
        # 字体设置选项卡
        font_tab = self.create_font_settings_tab()
        tab_widget.addTab(font_tab, "🔤 字体设置")
        
        # 系统设置选项卡
        system_tab = self.create_system_settings_tab()
        tab_widget.addTab(system_tab, "⚙️ 系统设置")
        
        # 界面设置选项卡
        ui_tab = self.create_ui_settings_tab()
        tab_widget.addTab(ui_tab, "🎨 界面设置")
        
        main_layout.addWidget(tab_widget)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 重置按钮
        reset_btn = QPushButton("🔄 重置默认")
        reset_btn.setStyleSheet("""
            QPushButton {
                background: #e67e22;
                min-width: 120px;
            }
            QPushButton:hover {
                background: #d35400;
            }
        """)
        reset_btn.clicked.connect(self.reset_to_defaults)
        
        # 取消按钮
        cancel_btn = QPushButton("❌ 取消")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        # 确定按钮
        ok_btn = QPushButton("✅ 确定")
        ok_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #229954;
            }
        """)
        ok_btn.clicked.connect(self.accept_settings)
        
        button_layout.addWidget(reset_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        
        main_layout.addLayout(button_layout)
        
    def create_font_settings_tab(self):
        """创建字体设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # 字体大小设置组
        font_size_group = QGroupBox("📏 字体大小设置")
        font_size_layout = QGridLayout(font_size_group)
        font_size_layout.setSpacing(15)
        
        # 全局字体大小
        font_size_layout.addWidget(QLabel("全局字体大小:"), 0, 0)
        self.global_font_size = QSpinBox()
        self.global_font_size.setRange(12, 24)
        self.global_font_size.setSuffix(" px")
        self.global_font_size.valueChanged.connect(self.preview_font_changes)
        font_size_layout.addWidget(self.global_font_size, 0, 1)
        
        # 标题字体大小
        font_size_layout.addWidget(QLabel("标题字体大小:"), 1, 0)
        self.title_font_size = QSpinBox()
        self.title_font_size.setRange(20, 40)
        self.title_font_size.setSuffix(" px")
        self.title_font_size.valueChanged.connect(self.preview_font_changes)
        font_size_layout.addWidget(self.title_font_size, 1, 1)
        
        # 按钮字体大小
        font_size_layout.addWidget(QLabel("按钮字体大小:"), 2, 0)
        self.button_font_size = QSpinBox()
        self.button_font_size.setRange(12, 20)
        self.button_font_size.setSuffix(" px")
        self.button_font_size.valueChanged.connect(self.preview_font_changes)
        font_size_layout.addWidget(self.button_font_size, 2, 1)
        
        layout.addWidget(font_size_group)
        
        # 字体缩放设置组
        scale_group = QGroupBox("🔍 界面缩放")
        scale_layout = QVBoxLayout(scale_group)
        
        scale_info_layout = QHBoxLayout()
        scale_info_layout.addWidget(QLabel("界面缩放比例:"))
        scale_info_layout.addStretch()
        self.scale_value_label = QLabel("100%")
        self.scale_value_label.setStyleSheet("color: #3498db; font-weight: bold;")
        scale_info_layout.addWidget(self.scale_value_label)
        scale_layout.addLayout(scale_info_layout)
        
        self.ui_scale_slider = QSlider(Qt.Horizontal)
        self.ui_scale_slider.setRange(80, 150)
        self.ui_scale_slider.setValue(100)
        self.ui_scale_slider.setTickPosition(QSlider.TicksBelow)
        self.ui_scale_slider.setTickInterval(10)
        self.ui_scale_slider.valueChanged.connect(self.update_scale_label)
        scale_layout.addWidget(self.ui_scale_slider)
        
        # 缩放提示
        scale_tip = QLabel("💡 提示: 调整界面缩放比例以适应不同分辨率的显示器")
        scale_tip.setStyleSheet("color: #7fb3d3; font-size: 14px; font-style: italic;")
        scale_tip.setWordWrap(True)
        scale_layout.addWidget(scale_tip)
        
        layout.addWidget(scale_group)
        
        # 字体预览区域
        preview_group = QGroupBox("👁️ 字体预览")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_title = QLabel("🖥️ 多屏幕内容管理器")
        self.preview_title.setStyleSheet("color: #3498db; font-weight: bold;")
        preview_layout.addWidget(self.preview_title)
        
        self.preview_label = QLabel("这是普通文本的预览效果")
        preview_layout.addWidget(self.preview_label)
        
        self.preview_button = QPushButton("这是按钮的预览效果")
        self.preview_button.setEnabled(False)
        preview_layout.addWidget(self.preview_button)
        
        layout.addWidget(preview_group)
        
        layout.addStretch()
        return widget
        
    def create_system_settings_tab(self):
        """创建系统设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # 启动设置组
        startup_group = QGroupBox("🚀 启动设置")
        startup_layout = QVBoxLayout(startup_group)
        startup_layout.setSpacing(15)
        
        # 开机自启动
        self.auto_startup_cb = QCheckBox("开机自动启动")
        self.auto_startup_cb.setToolTip("勾选后程序将在系统启动时自动运行")
        self.auto_startup_cb.stateChanged.connect(self.on_auto_startup_changed)
        startup_layout.addWidget(self.auto_startup_cb)
        
        # 启动时最小化
        self.start_minimized_cb = QCheckBox("启动时最小化到系统托盘")
        self.start_minimized_cb.setToolTip("程序启动后自动最小化，不显示主窗口")
        startup_layout.addWidget(self.start_minimized_cb)
        
        # 自动加载上次配置
        self.auto_load_config_cb = QCheckBox("自动加载上次使用的配置")
        self.auto_load_config_cb.setToolTip("启动时自动应用上次退出时的屏幕配置")
        startup_layout.addWidget(self.auto_load_config_cb)
        
        layout.addWidget(startup_group)
        
        # 性能设置组
        performance_group = QGroupBox("⚡ 性能设置")
        performance_layout = QVBoxLayout(performance_group)
        performance_layout.setSpacing(15)
        
        # 启用硬件加速
        self.hardware_acceleration_cb = QCheckBox("启用硬件加速")
        self.hardware_acceleration_cb.setToolTip("提高视频播放和界面渲染性能")
        performance_layout.addWidget(self.hardware_acceleration_cb)
        
        # 内存优化
        self.memory_optimization_cb = QCheckBox("启用内存优化")
        self.memory_optimization_cb.setToolTip("定期清理未使用的内存资源")
        performance_layout.addWidget(self.memory_optimization_cb)
        
        layout.addWidget(performance_group)
        
        # 存储设置组
        storage_group = QGroupBox("💾 存储设置")
        storage_layout = QGridLayout(storage_group)
        storage_layout.setSpacing(15)
        
        # 配置文件数量限制
        storage_layout.addWidget(QLabel("最大配置文件数量:"), 0, 0)
        self.max_configs = QSpinBox()
        self.max_configs.setRange(10, 100)
        self.max_configs.setSuffix(" 个")
        storage_layout.addWidget(self.max_configs, 0, 1)
        
        # 自动备份
        self.auto_backup_cb = QCheckBox("自动备份配置文件")
        self.auto_backup_cb.setToolTip("定期备份重要的配置文件")
        storage_layout.addWidget(self.auto_backup_cb, 1, 0, 1, 2)
        
        layout.addWidget(storage_group)
        
        layout.addStretch()
        return widget
        
    def create_ui_settings_tab(self):
        """创建界面设置选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # 主题设置组
        theme_group = QGroupBox("🎨 主题设置")
        theme_layout = QGridLayout(theme_group)
        theme_layout.setSpacing(15)
        
        # 主题选择
        theme_layout.addWidget(QLabel("界面主题:"), 0, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["深色主题", "浅色主题", "跟随系统"])
        theme_layout.addWidget(self.theme_combo, 0, 1)
        
        # 透明度设置
        theme_layout.addWidget(QLabel("窗口透明度:"), 1, 0)
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(70, 100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.update_opacity_label)
        theme_layout.addWidget(self.opacity_slider, 1, 1)
        
        self.opacity_label = QLabel("100%")
        self.opacity_label.setStyleSheet("color: #3498db; font-weight: bold;")
        theme_layout.addWidget(self.opacity_label, 1, 2)
        
        layout.addWidget(theme_group)
        
        # 动画设置组
        animation_group = QGroupBox("🎭 动画设置")
        animation_layout = QVBoxLayout(animation_group)
        animation_layout.setSpacing(15)
        
        # 启用动画效果
        self.enable_animations_cb = QCheckBox("启用界面动画效果")
        self.enable_animations_cb.setToolTip("包括窗口切换、按钮悬停等动画")
        animation_layout.addWidget(self.enable_animations_cb)
        
        # 动画速度
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(QLabel("动画速度:"))
        self.animation_speed = QComboBox()
        self.animation_speed.addItems(["慢速", "正常", "快速"])
        self.animation_speed.setCurrentText("正常")
        speed_layout.addWidget(self.animation_speed)
        speed_layout.addStretch()
        animation_layout.addLayout(speed_layout)
        
        layout.addWidget(animation_group)
        
        # 窗口设置组
        window_group = QGroupBox("🖼️ 窗口设置")
        window_layout = QVBoxLayout(window_group)
        window_layout.setSpacing(15)
        
        # 记住窗口位置
        self.remember_position_cb = QCheckBox("记住窗口位置和大小")
        self.remember_position_cb.setToolTip("下次启动时恢复上次的窗口位置")
        window_layout.addWidget(self.remember_position_cb)
        
        # 总是置顶
        self.always_on_top_cb = QCheckBox("主窗口总是置顶")
        self.always_on_top_cb.setToolTip("让主窗口始终显示在其他窗口之上")
        window_layout.addWidget(self.always_on_top_cb)
        
        layout.addWidget(window_group)
        
        layout.addStretch()
        return widget
        
    def preview_font_changes(self):
        """预览字体变化"""
        global_size = self.global_font_size.value()
        title_size = self.title_font_size.value()
        button_size = self.button_font_size.value()
        
        self.preview_label.setStyleSheet(f"font-size: {global_size}px;")
        self.preview_title.setStyleSheet(f"color: #3498db; font-weight: bold; font-size: {title_size}px;")
        self.preview_button.setStyleSheet(f"font-size: {button_size}px;")
        
    def update_scale_label(self, value):
        """更新缩放标签"""
        self.scale_value_label.setText(f"{value}%")
        
    def update_opacity_label(self, value):
        """更新透明度标签"""
        self.opacity_label.setText(f"{value}%")
        
    def on_auto_startup_changed(self, state):
        """开机自启状态改变"""
        if state == Qt.Checked:
            self.set_auto_startup(True)
        else:
            self.set_auto_startup(False)
            
    def set_auto_startup(self, enable):
        """设置开机自启"""
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "多屏幕内容管理器"
            exe_path = os.path.abspath(sys.argv[0])
            
            if enable:
                # 添加到注册表
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, f'"{exe_path}"')
                winreg.CloseKey(key)
            else:
                # 从注册表删除
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                    winreg.DeleteValue(key, app_name)
                    winreg.CloseKey(key)
                except FileNotFoundError:
                    pass  # 项不存在，忽略
                    
        except Exception as e:
            QMessageBox.warning(self, "警告", f"设置开机自启失败: {str(e)}")
            
    def check_auto_startup(self):
        """检查是否已设置开机自启"""
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            app_name = "多屏幕内容管理器"
            
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, app_name)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
            
    def load_settings(self):
        """加载设置"""
        default_settings = {
            "global_font_size": 16,
            "title_font_size": 24,
            "button_font_size": 16,
            "ui_scale": 100,
            "auto_startup": False,
            "start_minimized": False,
            "auto_load_config": True,
            "hardware_acceleration": True,
            "memory_optimization": True,
            "max_configs": 50,
            "auto_backup": True,
            "theme": "深色主题",
            "opacity": 100,
            "enable_animations": True,
            "animation_speed": "正常",
            "remember_position": True,
            "always_on_top": False
        }
        
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                # 合并默认设置和加载的设置
                default_settings.update(settings)
        except Exception as e:
            print(f"加载设置失败: {e}")
            
        return default_settings
        
    def save_settings(self):
        """保存设置"""
        try:
            with open("settings.json", 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败: {str(e)}")
            
    def load_current_settings(self):
        """加载当前设置到界面"""
        # 字体设置
        self.global_font_size.setValue(self.settings["global_font_size"])
        self.title_font_size.setValue(self.settings["title_font_size"])
        self.button_font_size.setValue(self.settings["button_font_size"])
        self.ui_scale_slider.setValue(self.settings["ui_scale"])
        self.update_scale_label(self.settings["ui_scale"])
        
        # 系统设置
        self.auto_startup_cb.setChecked(self.check_auto_startup())
        self.start_minimized_cb.setChecked(self.settings["start_minimized"])
        self.auto_load_config_cb.setChecked(self.settings["auto_load_config"])
        self.hardware_acceleration_cb.setChecked(self.settings["hardware_acceleration"])
        self.memory_optimization_cb.setChecked(self.settings["memory_optimization"])
        self.max_configs.setValue(self.settings["max_configs"])
        self.auto_backup_cb.setChecked(self.settings["auto_backup"])
        
        # 界面设置
        self.theme_combo.setCurrentText(self.settings["theme"])
        self.opacity_slider.setValue(self.settings["opacity"])
        self.update_opacity_label(self.settings["opacity"])
        self.enable_animations_cb.setChecked(self.settings["enable_animations"])
        self.animation_speed.setCurrentText(self.settings["animation_speed"])
        self.remember_position_cb.setChecked(self.settings["remember_position"])
        self.always_on_top_cb.setChecked(self.settings["always_on_top"])
        
        # 预览字体变化
        self.preview_font_changes()
        
    def collect_current_settings(self):
        """收集当前界面设置"""
        self.settings.update({
            "global_font_size": self.global_font_size.value(),
            "title_font_size": self.title_font_size.value(),
            "button_font_size": self.button_font_size.value(),
            "ui_scale": self.ui_scale_slider.value(),
            "auto_startup": self.auto_startup_cb.isChecked(),
            "start_minimized": self.start_minimized_cb.isChecked(),
            "auto_load_config": self.auto_load_config_cb.isChecked(),
            "hardware_acceleration": self.hardware_acceleration_cb.isChecked(),
            "memory_optimization": self.memory_optimization_cb.isChecked(),
            "max_configs": self.max_configs.value(),
            "auto_backup": self.auto_backup_cb.isChecked(),
            "theme": self.theme_combo.currentText(),
            "opacity": self.opacity_slider.value(),
            "enable_animations": self.enable_animations_cb.isChecked(),
            "animation_speed": self.animation_speed.currentText(),
            "remember_position": self.remember_position_cb.isChecked(),
            "always_on_top": self.always_on_top_cb.isChecked()
        })
        
    def reset_to_defaults(self):
        """重置为默认设置"""
        reply = QMessageBox.question(
            self, "确认重置",
            "确定要重置所有设置为默认值吗？\n此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 重置为默认值
            self.global_font_size.setValue(16)
            self.title_font_size.setValue(24)
            self.button_font_size.setValue(16)
            self.ui_scale_slider.setValue(100)
            
            self.auto_startup_cb.setChecked(False)
            self.start_minimized_cb.setChecked(False)
            self.auto_load_config_cb.setChecked(True)
            self.hardware_acceleration_cb.setChecked(True)
            self.memory_optimization_cb.setChecked(True)
            self.max_configs.setValue(50)
            self.auto_backup_cb.setChecked(True)
            
            self.theme_combo.setCurrentText("深色主题")
            self.opacity_slider.setValue(100)
            self.enable_animations_cb.setChecked(True)
            self.animation_speed.setCurrentText("正常")
            self.remember_position_cb.setChecked(True)
            self.always_on_top_cb.setChecked(False)
            
            # 更新预览
            self.preview_font_changes()
            self.update_scale_label(100)
            self.update_opacity_label(100)
            
            QMessageBox.information(self, "重置完成", "所有设置已重置为默认值")
            
    def accept_settings(self):
        """确认设置"""
        self.collect_current_settings()
        self.save_settings()
        
        # 发送设置变更信号
        self.settings_changed.emit(self.settings)
        
        QMessageBox.information(self, "设置已保存", "设置已成功保存，部分设置需要重启程序后生效")
        self.accept()
        
    def get_settings(self):
        """获取当前设置"""
        return self.settings.copy()