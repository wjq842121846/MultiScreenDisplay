#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动动画窗口
显示logo和进度条，提供更好的启动体验
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient, QBrush, QPen

class SplashScreen(QWidget):
    """启动画面窗口"""
    
    # 信号：启动完成
    startup_complete = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.progress_value = 0
        self.init_ui()
        self.setup_animation()
        
    def init_ui(self):
        """初始化界面"""
        # 设置窗口属性
        self.setWindowTitle("多屏幕内容管理器")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口大小和位置
        self.setFixedSize(500, 350)
        self.center_window()
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 创建背景容器
        self.create_background_style()
        
        # Logo区域
        self.create_logo_section(main_layout)
        
        # 应用信息区域
        self.create_info_section(main_layout)
        
        # 进度条区域
        self.create_progress_section(main_layout)
        
        # 状态信息区域
        self.create_status_section(main_layout)
        
    def center_window(self):
        """居中显示窗口"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        
        x = (screen_width - self.width()) // 2
        y = (screen_height - self.height()) // 2
        self.move(x, y)
        
    def create_background_style(self):
        """创建背景样式"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #1a1a2e,
                    stop: 0.5 #16213e,
                    stop: 1 #0f3460
                );
                border-radius: 20px;
                border: 2px solid #00ffff;
            }
        """)
        
    def create_logo_section(self, parent_layout):
        """创建Logo区域"""
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        
        # Logo图标（使用文字代替，可以后续替换为图片）
        self.logo_label = QLabel("🖥️")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFont(QFont("Microsoft YaHei", 48))
        self.logo_label.setStyleSheet("""
            QLabel {
                color: #00ffff;
                background: transparent;
                border: none;
            }
        """)
        
        logo_layout.addWidget(self.logo_label)
        parent_layout.addLayout(logo_layout)
        
    def create_info_section(self, parent_layout):
        """创建应用信息区域"""
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.setSpacing(5)
        
        # 应用标题
        title_label = QLabel("多屏幕内容管理器")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background: transparent;
                border: none;
            }
        """)
        
        # 应用副标题
        subtitle_label = QLabel("Multi-Screen Content Manager")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setFont(QFont("Microsoft YaHei", 12))
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                background: transparent;
                border: none;
            }
        """)
        
        # 版本信息
        version_label = QLabel("版本 2.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont("Microsoft YaHei", 10))
        version_label.setStyleSheet("""
            QLabel {
                color: #888888;
                background: transparent;
                border: none;
            }
        """)
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(subtitle_label)
        info_layout.addWidget(version_label)
        parent_layout.addLayout(info_layout)
        
    def create_progress_section(self, parent_layout):
        """创建进度条区域"""
        progress_layout = QVBoxLayout()
        progress_layout.setAlignment(Qt.AlignCenter)
        progress_layout.setSpacing(10)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #2d2d44;
                border: 1px solid #555;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00ffff,
                    stop: 0.5 #00ccff,
                    stop: 1 #0099ff
                );
                border-radius: 3px;
            }
        """)
        
        # 进度百分比
        self.progress_label = QLabel("0%")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setFont(QFont("Microsoft YaHei", 10))
        self.progress_label.setStyleSheet("""
            QLabel {
                color: #00ffff;
                background: transparent;
                border: none;
            }
        """)
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        parent_layout.addLayout(progress_layout)
        
    def create_status_section(self, parent_layout):
        """创建状态信息区域"""
        status_layout = QVBoxLayout()
        status_layout.setAlignment(Qt.AlignCenter)
        
        # 状态标签
        self.status_label = QLabel("正在启动...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Microsoft YaHei", 11))
        self.status_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                background: transparent;
                border: none;
            }
        """)
        
        status_layout.addWidget(self.status_label)
        parent_layout.addLayout(status_layout)
        
    def setup_animation(self):
        """设置动画效果"""
        # Logo呼吸动画
        self.logo_animation = QPropertyAnimation(self.logo_label, b"styleSheet")
        self.logo_animation.setDuration(2000)
        self.logo_animation.setLoopCount(-1)  # 无限循环
        
        # 创建呼吸效果的样式
        bright_style = """
            QLabel {
                color: #00ffff;
                background: transparent;
                border: none;
                text-shadow: 0 0 20px #00ffff;
            }
        """
        
        dim_style = """
            QLabel {
                color: #008888;
                background: transparent;
                border: none;
            }
        """
        
        self.logo_animation.setKeyValueAt(0, bright_style)
        self.logo_animation.setKeyValueAt(0.5, dim_style)
        self.logo_animation.setKeyValueAt(1, bright_style)
        self.logo_animation.setEasingCurve(QEasingCurve.InOutSine)
        
        # 启动Logo动画
        self.logo_animation.start()
        
    def update_progress(self, value, status=""):
        """更新进度"""
        self.progress_value = value
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")
        
        if status:
            self.status_label.setText(status)
            
        # 进度完成时的特效
        if value >= 100:
            self.status_label.setText("启动完成！")
            # 停止Logo动画
            self.logo_animation.stop()
            self.logo_label.setStyleSheet("""
                QLabel {
                    color: #00ff00;
                    background: transparent;
                    border: none;
                    text-shadow: 0 0 30px #00ff00;
                }
            """)
            
            # 延迟一点时间后发送完成信号
            QTimer.singleShot(500, self.startup_complete.emit)
            
    def start_progress_simulation(self):
        """启动进度模拟（用于测试）"""
        self.timer = QTimer()
        self.timer.timeout.connect(self._simulate_progress)
        self.timer.start(50)  # 每50ms更新一次
        
    def _simulate_progress(self):
        """模拟进度更新"""
        self.progress_value += 1
        
        # 模拟不同阶段的状态
        if self.progress_value <= 20:
            status = "初始化系统组件..."
        elif self.progress_value <= 40:
            status = "加载界面框架..."
        elif self.progress_value <= 60:
            status = "检测屏幕配置..."
        elif self.progress_value <= 80:
            status = "载入配置文件..."
        elif self.progress_value <= 95:
            status = "准备用户界面..."
        else:
            status = "启动完成！"
            
        self.update_progress(self.progress_value, status)
        
        if self.progress_value >= 100:
            self.timer.stop()
            
    def closeEvent(self, event):
        """关闭事件"""
        if hasattr(self, 'logo_animation'):
            self.logo_animation.stop()
        event.accept()

# 测试代码
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.show()
    
    # 启动进度模拟
    splash.start_progress_simulation()
    
    # 连接完成信号
    splash.startup_complete.connect(lambda: print("启动完成！"))
    
    sys.exit(app.exec_())