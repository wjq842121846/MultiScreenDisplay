#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化启动器 - 解决import *问题
"""

import sys
import os

def main():
    """主启动函数"""
    # 最小化导入
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal
    from PyQt5.QtGui import QFont
    
    class SimpleSplash(QWidget):
        startup_complete = pyqtSignal()
        
        def __init__(self):
            super().__init__()
            self.progress_value = 0
            self.init_ui()
            
        def init_ui(self):
            self.setWindowTitle("多屏幕内容管理器")
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setFixedSize(400, 200)
            
            # 居中显示
            screen = QApplication.primaryScreen()
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2
            y = (screen_geometry.height() - self.height()) // 2
            self.move(x, y)
            
            # 样式
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(
                        x1: 0, y1: 0, x2: 1, y2: 1,
                        stop: 0 #1a1a2e,
                        stop: 1 #0f3460
                    );
                    border-radius: 15px;
                    border: 2px solid #00ffff;
                }
            """)
            
            layout = QVBoxLayout(self)
            layout.setContentsMargins(20, 20, 20, 20)
            layout.setSpacing(15)
            layout.setAlignment(Qt.AlignCenter)
            
            # Logo
            logo_label = QLabel("🖥️")
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setFont(QFont("Microsoft YaHei", 32))
            logo_label.setStyleSheet("color: #00ffff; background: transparent;")
            
            # 标题
            title_label = QLabel("多屏幕内容管理器")
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
            title_label.setStyleSheet("color: #ffffff; background: transparent;")
            
            # 进度条
            self.progress_bar = QProgressBar()
            self.progress_bar.setMinimum(0)
            self.progress_bar.setMaximum(100)
            self.progress_bar.setValue(0)
            self.progress_bar.setFixedHeight(6)
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setStyleSheet("""
                QProgressBar {
                    background-color: #2d2d44;
                    border: 1px solid #555;
                    border-radius: 3px;
                }
                QProgressBar::chunk {
                    background: #00ffff;
                    border-radius: 2px;
                }
            """)
            
            # 状态
            self.status_label = QLabel("正在启动...")
            self.status_label.setAlignment(Qt.AlignCenter)
            self.status_label.setFont(QFont("Microsoft YaHei", 9))
            self.status_label.setStyleSheet("color: #cccccc; background: transparent;")
            
            layout.addWidget(logo_label)
            layout.addWidget(title_label)
            layout.addWidget(self.progress_bar)
            layout.addWidget(self.status_label)
            
        def update_progress(self, value, status=""):
            self.progress_value = value
            self.progress_bar.setValue(value)
            if status:
                self.status_label.setText(status)
            
            if value >= 100:
                self.status_label.setText("启动完成！")
                QTimer.singleShot(300, self.startup_complete.emit)
    
    # 创建应用程序 - 先设置属性再创建QApplication
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    
    app = QApplication(sys.argv)
    
    # 显示启动画面
    splash = SimpleSplash()
    splash.show()
    splash.update_progress(10, "正在启动...")
    app.processEvents()
    
    # 主窗口
    main_window = None
    
    def load_main_app():
        """加载主应用程序"""
        nonlocal main_window
        try:
            splash.update_progress(30, "加载主程序...")
            app.processEvents()
            
            # 直接导入并创建主窗口，避免subprocess
            splash.update_progress(50, "初始化主窗口...")
            app.processEvents()
            
            # 导入主程序模块
            from main import MainController
            
            splash.update_progress(70, "创建主窗口...")
            app.processEvents()
            
            # 创建主窗口
            main_window = MainController()
            
            splash.update_progress(90, "准备显示...")
            app.processEvents()
            
            splash.update_progress(100, "启动完成！")
            
            def show_main():
                splash.hide()
                if main_window:
                    main_window.show()
                    main_window.raise_()
                    main_window.activateWindow()
                    
            splash.startup_complete.connect(show_main)
            
        except Exception as e:
            splash.status_label.setText(f"启动失败: {str(e)}")
            print(f"启动失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 延迟启动主程序
    QTimer.singleShot(500, load_main_app)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()