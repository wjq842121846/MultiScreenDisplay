#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于线程的内容窗口
每个窗口在独立线程中运行，避免相互阻塞
"""

import os
import sys
import json
from threading import Thread, Event
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

# 尝试导入OpenCV播放器
try:
    import cv2
    from opencv_video_player import OpenCVVideoPlayer
    OPENCV_AVAILABLE = True
    print("OpenCV播放器导入成功")
except ImportError as e:
    OPENCV_AVAILABLE = False
    print(f"OpenCV播放器导入失败: {e}")
except Exception as e:
    OPENCV_AVAILABLE = False
    print(f"OpenCV播放器初始化错误: {e}")

try:
    from embedded_video_player import EmbeddedVideoPlayer
    EMBEDDED_AVAILABLE = True
    print("嵌入式播放器导入成功")
except ImportError as e:
    EMBEDDED_AVAILABLE = False
    print(f"嵌入式播放器导入失败: {e}")
except Exception as e:
    EMBEDDED_AVAILABLE = False
    print(f"嵌入式播放器初始化错误: {e}")

print(f"视频播放器状态: OpenCV={OPENCV_AVAILABLE}, Embedded={EMBEDDED_AVAILABLE}")

# 检查运行环境
import sys
print(f"运行环境: {sys.executable}")
print(f"是否为EXE: {'是' if hasattr(sys, 'frozen') else '否'}")


class ThreadedContentWindow(QWidget):
    """基于线程的内容窗口 - 优化的无边框设计"""
    
    window_closed = pyqtSignal(int)
    
    def __init__(self, screen_index, screen_info):
        super().__init__()
        self.screen_index = screen_index
        self.screen_info = screen_info
        self.current_content_type = None
        self.current_content = None
        
        # 媒体播放器
        self.media_player = None
        self.video_widget = None
        self.web_view = None
        self.opencv_player = None
        self.embedded_player = None
        
        # 窗口状态
        self.is_fullscreen = True  # 默认全屏
        
        # 线程同步
        self.content_loading = False
        
        self.init_ui()
        
    def init_ui(self):
        """初始化极简无边框界面"""
        # 设置窗口属性
        self.setWindowTitle(f"Content Display - Screen {self.screen_index + 1}")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # 设置窗口背景
        self.setStyleSheet("""
            QWidget {
                background: #000000;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        # 极简布局
        self.content_layout = QVBoxLayout(self)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # 优化初始化：只设置位置，不立即显示内容
        self.position_window()
        
        # 延迟显示默认内容和全屏设置
        QTimer.singleShot(100, self.show_default_content)
        QTimer.singleShot(300, self.showFullScreen)
        
    def position_window(self):
        """设置窗口位置"""
        # 设置到对应屏幕
        self.setGeometry(
            self.screen_info['x'],
            self.screen_info['y'], 
            self.screen_info['width'],
            self.screen_info['height']
        )
        
    def show_default_content(self):
        """显示默认内容"""
        self.clear_content()
        
        default_widget = QWidget()
        default_layout = QVBoxLayout(default_widget)
        default_layout.setAlignment(Qt.AlignCenter)
        
        # 简洁等待提示
        wait_label = QLabel("等待内容...")
        wait_label.setAlignment(Qt.AlignCenter)
        wait_label.setFont(QFont("Microsoft YaHei", 20))
        wait_label.setStyleSheet("""
            QLabel {
                color: #666666;
                background: transparent;
                border: none;
            }
        """)
        default_layout.addWidget(wait_label)
        
        self.content_layout.addWidget(default_widget)
        
    def _show_loading_indicator(self):
        """显示加载指示器"""
        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_layout.setAlignment(Qt.AlignCenter)
        
        loading_label = QLabel("⏳ 正在加载...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setFont(QFont("Microsoft YaHei", 18))
        loading_label.setStyleSheet("""
            QLabel {
                color: #00ffff;
                background: transparent;
                border: none;
            }
        """)
        loading_layout.addWidget(loading_label)
        
        self.content_layout.addWidget(loading_widget)
        
    def set_content(self, content_type, content):
        """设置内容 - 使用线程优化"""
        if self.content_loading:
            return  # 避免重复加载
            
        self.current_content_type = content_type
        self.current_content = content
        
        print(f"为屏幕 {self.screen_index + 1} 设置内容: {content_type}")
        
        # 立即清除所有内容，包括默认的"等待内容..."
        self.clear_content()
        
        # 显示加载提示
        self._show_loading_indicator()
        
        # 延迟加载新内容，确保界面更新完成
        QTimer.singleShot(100, lambda: self._load_content_safe(content_type, content))
        
    def _load_content_safe(self, content_type, content):
        """安全的内容加载"""
        if self.content_loading:
            return
            
        self.content_loading = True
        
        try:
            # 再次清除内容，确保加载指示器被移除
            self.clear_content()
            
            # 根据内容类型加载相应内容
            if content_type == "文本":
                self.set_text_content(content)
            elif content_type == "图片":
                self.set_image_content(content)
            elif content_type == "视频":
                self.set_video_content(content)
            elif content_type == "网页":
                self.set_web_content(content)
            else:
                self.show_error(f"不支持的内容类型: {content_type}")
                
        except Exception as e:
            self.show_error(f"内容加载失败: {str(e)}")
        finally:
            self.content_loading = False
            
    def set_text_content(self, text):
        """设置文本内容"""
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setAlignment(Qt.AlignCenter)
        
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Microsoft YaHei", 24, QFont.Bold))
        text_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                background: transparent;
                border: none;
            }
        """)
        text_label.setWordWrap(True)
        text_layout.addWidget(text_label)
        
        self.content_layout.addWidget(text_widget)
        
    def set_image_content(self, image_path):
        """设置图片内容"""
        if os.path.exists(image_path):
            try:
                image_widget = QWidget()
                image_layout = QVBoxLayout(image_widget)
                image_layout.setAlignment(Qt.AlignCenter)
                
                image_label = QLabel()
                pixmap = QPixmap(image_path)
                
                if not pixmap.isNull():
                    # 缩放图片以适应屏幕
                    scaled_pixmap = pixmap.scaled(
                        self.width() - 40,
                        self.height() - 40,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
                    image_label.setPixmap(scaled_pixmap)
                    image_label.setAlignment(Qt.AlignCenter)
                    image_layout.addWidget(image_label)
                    
                    self.content_layout.addWidget(image_widget)
                else:
                    self.show_error("图片格式不支持")
            except Exception as e:
                self.show_error(f"图片加载失败: {str(e)}")
        else:
            self.show_error("图片文件未找到")
            
    def set_video_content(self, video_path):
        """设置视频内容 - 线程优化版本"""
        if not os.path.exists(video_path):
            self.show_error(f"视频文件未找到: {video_path}")
            return
            
        print(f"为屏幕 {self.screen_index + 1} 加载视频: {video_path}")
        
        try:
            # 在线程中加载视频播放器以避免阻塞
            def load_video():
                try:
                    # 优先使用OpenCV播放器（性能最佳）
                    if OPENCV_AVAILABLE:
                        print(f"屏幕 {self.screen_index + 1}: 使用OpenCV播放器")
                        QTimer.singleShot(100, lambda: self._setup_opencv_player(video_path))
                    elif EMBEDDED_AVAILABLE:
                        print(f"屏幕 {self.screen_index + 1}: 使用嵌入式播放器")
                        QTimer.singleShot(100, lambda: self._setup_embedded_player(video_path))
                    else:
                        print(f"屏幕 {self.screen_index + 1}: 使用Qt默认播放器")
                        QTimer.singleShot(100, lambda: self._setup_qt_video_player(video_path))
                except Exception as e:
                    print(f"视频设置错误: {e}")
                    QTimer.singleShot(100, lambda: self.show_error(f"视频设置失败: {str(e)}"))
                    
            # 在主线程中启动
            load_video()
            
        except Exception as e:
            self.show_error(f"视频播放器初始化失败: {str(e)}")
            
    def _setup_opencv_player(self, video_path):
        """设置OpenCV播放器"""
        try:
            print(f"尝试创建OpenCV播放器实例...")
            self.opencv_player = OpenCVVideoPlayer()
            print(f"OpenCV播放器实例创建成功")
            self.content_layout.addWidget(self.opencv_player)
            print(f"OpenCV播放器添加到布局")
            
            # 延迟启动播放
            QTimer.singleShot(300, lambda: self._start_opencv_playback(video_path))
        except Exception as e:
            print(f"OpenCV播放器设置失败: {e}")
            import traceback
            traceback.print_exc()
            print(f"回退到Qt播放器")
            self._setup_qt_video_player(video_path)
            
    def _start_opencv_playback(self, video_path):
        """启动OpenCV播放"""
        if hasattr(self, 'opencv_player') and self.opencv_player:
            success = self.opencv_player.play_video(video_path)
            if not success:
                print("OpenCV播放失败，尝试Qt播放器")
                self.clear_content()
                self._setup_qt_video_player(video_path)
                
    def _setup_embedded_player(self, video_path):
        """设置嵌入式播放器"""
        try:
            self.embedded_player = EmbeddedVideoPlayer()
            self.content_layout.addWidget(self.embedded_player)
            
            QTimer.singleShot(300, lambda: self._start_embedded_playback(video_path))
        except Exception as e:
            print(f"嵌入式播放器设置失败: {e}")
            self._setup_qt_video_player(video_path)
            
    def _start_embedded_playback(self, video_path):
        """启动嵌入式播放"""
        if hasattr(self, 'embedded_player') and self.embedded_player:
            success = self.embedded_player.play_video(video_path)
            if not success:
                print("嵌入式播放失败，尝试Qt播放器")
                self.clear_content()
                self._setup_qt_video_player(video_path)
                
    def _setup_qt_video_player(self, video_path):
        """设置Qt媒体播放器"""
        try:
            self.video_widget = QVideoWidget()
            self.media_player = QMediaPlayer()
            
            self.media_player.setVideoOutput(self.video_widget)
            self.media_player.mediaStatusChanged.connect(self.handle_media_status)
            self.media_player.error.connect(self.handle_media_error)
            
            # 设置媒体内容
            media_content = QMediaContent(QUrl.fromLocalFile(os.path.abspath(video_path)))
            self.media_player.setMedia(media_content)
            
            self.content_layout.addWidget(self.video_widget)
            
            # 延迟开始播放
            QTimer.singleShot(500, self._start_qt_playback)
            
        except Exception as e:
            self.show_error(f"Qt播放器设置失败: {str(e)}")
            
    def _start_qt_playback(self):
        """启动Qt播放"""
        if self.media_player:
            self.media_player.play()
            
    def handle_media_status(self, status):
        """处理媒体状态"""
        if status == QMediaPlayer.LoadedMedia and self.media_player:
            self.media_player.play()
        elif status == QMediaPlayer.EndOfMedia and self.media_player:
            # 循环播放
            self.media_player.setPosition(0)
            self.media_player.play()
            
    def handle_media_error(self, error):
        """处理媒体错误"""
        error_msg = f"视频播放错误: {error}"
        print(error_msg)
        self.show_error(error_msg)
        
    def set_web_content(self, url):
        """设置网页内容"""
        try:
            self.web_view = QWebEngineView()
            if url.startswith(('http://', 'https://')):
                self.web_view.load(QUrl(url))
            else:
                self.web_view.load(QUrl('https://' + url))
                
            self.content_layout.addWidget(self.web_view)
            
        except Exception as e:
            self.show_error(f"网页加载失败: {str(e)}")
            
    def show_error(self, message):
        """显示错误信息"""
        error_widget = QWidget()
        error_layout = QVBoxLayout(error_widget)
        error_layout.setAlignment(Qt.AlignCenter)
        
        error_label = QLabel(f"⚠️ {message}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        error_label.setStyleSheet("""
            QLabel {
                color: #ff6666;
                background: transparent;
                border: none;
            }
        """)
        error_layout.addWidget(error_label)
        
        self.content_layout.addWidget(error_widget)
        
    def clear_content(self):
        """清空内容"""
        # 清理媒体播放器
        if hasattr(self, 'media_player') and self.media_player:
            self.media_player.stop()
            self.media_player = None
            
        if hasattr(self, 'video_widget') and self.video_widget:
            self.video_widget = None
            
        # 清理OpenCV播放器
        if hasattr(self, 'opencv_player') and self.opencv_player:
            self.opencv_player.cleanup()
            self.opencv_player = None
            
        # 清理嵌入式播放器
        if hasattr(self, 'embedded_player') and self.embedded_player:
            self.embedded_player.cleanup()
            self.embedded_player = None
            
        # 清理Web视图
        if hasattr(self, 'web_view') and self.web_view:
            self.web_view = None
            
        # 清空布局
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key_Escape:
            if self.is_fullscreen:
                self.showNormal()
                self.is_fullscreen = False
            else:
                self.close_window()
        elif event.key() == Qt.Key_F11:
            if self.is_fullscreen:
                self.showNormal()
                self.is_fullscreen = False
            else:
                self.showFullScreen()
                self.is_fullscreen = True
        super().keyPressEvent(event)
        
    def close_window(self):
        """关闭窗口"""
        print(f"关闭屏幕 {self.screen_index + 1} 的线程窗口")
        
        # 清理资源
        self.clear_content()
        
        self.window_closed.emit(self.screen_index)
        self.close()
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.close_window()
        event.accept()