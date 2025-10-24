import os
import json
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, 
                             QPushButton, QApplication, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, QUrl, QTimer, QPoint, QRect, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QFont, QColor, QCursor, QPainter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from video_player_alternatives import AlternativeVideoPlayer
from embedded_video_player import EmbeddedVideoPlayer

# 尝试导入OpenCV播放器
try:
    from opencv_video_player import OpenCVVideoPlayer
    OPENCV_AVAILABLE = True
except ImportError:
    print("OpenCV不可用，将使用其他播放方案")
    OPENCV_AVAILABLE = False

class PerformanceOptimizedControls(QWidget):
    """性能优化的窗口控件"""
    
    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    close_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(15)  # 减小高度到一半
        self.init_ui()
        
    def init_ui(self):
        """简化的界面初始化"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 1, 2, 1)  # 减小边距
        layout.setSpacing(3)  # 减小间距
        
        # 简化的窗口标题
        self.title_label = QLabel("内容容器")
        self.title_label.setStyleSheet("color: #ecf0f1; font-size: 9px; padding: 1px;")
        layout.addWidget(self.title_label)
        layout.addStretch()
        
        # 简化的按钮样式 - 移除复杂的渐变和特效
        simple_button_style = """
            QPushButton {
                background: #34495e;
                border: none;
                border-radius: 3px;
                color: white;
                font-size: 12px;
                font-weight: bold;
                min-width: 10px;
                min-height: 10px;
                max-width: 10px;
                max-height: 10px;
            }
            QPushButton:hover {
                background: #3498db;
            }
            QPushButton:pressed {
                background: #2980b9;
            }
        """
        
        # 最小化按钮
        self.minimize_btn = QPushButton("−")
        self.minimize_btn.setStyleSheet(simple_button_style)
        self.minimize_btn.setToolTip("最小化")
        self.minimize_btn.clicked.connect(self.minimize_clicked.emit)
        layout.addWidget(self.minimize_btn)
        
        # 最大化按钮
        self.maximize_btn = QPushButton("□")
        self.maximize_btn.setStyleSheet(simple_button_style)
        self.maximize_btn.setToolTip("最大化/还原")
        self.maximize_btn.clicked.connect(self.maximize_clicked.emit)
        layout.addWidget(self.maximize_btn)
        
        # 关闭按钮
        close_style = simple_button_style.replace("#34495e", "#e74c3c")
        self.close_btn = QPushButton("×")
        self.close_btn.setStyleSheet(close_style)
        self.close_btn.setToolTip("关闭")
        self.close_btn.clicked.connect(self.close_clicked.emit)
        layout.addWidget(self.close_btn)
        
    def set_title(self, title):
        """设置窗口标题"""
        self.title_label.setText(title)
        
    def update_maximize_button(self, is_maximized):
        """更新最大化按钮状态"""
        self.maximize_btn.setText("◱" if is_maximized else "□")
        self.maximize_btn.setToolTip("还原" if is_maximized else "最大化")


class OptimizedContentContainer(QWidget):
    """性能优化的内容容器窗口"""
    
    window_closed = pyqtSignal(int)
    
    def __init__(self, screen_index, screen_info):
        super().__init__()
        self.screen_index = screen_index
        self.screen_info = screen_info
        self.current_content_type = None
        self.current_content = None
        self.media_player = None
        self.web_view = None
        
        # 窗口状态
        self.is_maximized = False
        self.is_fullscreen = False
        self.normal_geometry = QRect()
        self.drag_position = QPoint()
        
        # 性能优化标志
        self.shadow_enabled = False  # 默认关闭阴影
        self.animations_enabled = False  # 默认关闭动画
        
        # 配置文件路径
        self.config_file = f"window_config_screen_{screen_index}.json"
        
        self.init_ui_fast()
        self.load_window_state()
        self.position_window()
        
    def init_ui_fast(self):
        """快速界面初始化 - 移除复杂特效"""
        # 设置窗口属性
        self.setWindowTitle(f"屏幕 {self.screen_index + 1} - 内容容器")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        # 移除透明背景设置，提升性能
        # self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置最小尺寸
        self.setMinimumSize(320, 240)
        
        # 简化的主框架 - 移除复杂的渐变和特效
        self.main_frame = QFrame()
        self.main_frame.setStyleSheet("""
            QFrame {
                background: #2c3e50;
                border: 0.5px solid #3498db;
                border-radius: 5px;
            }
        """)
        
        # 可选的阴影效果（默认关闭）
        if self.shadow_enabled:
            self.enable_shadow()
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)  # 减小边距
        main_layout.addWidget(self.main_frame)
        
        # 框架内布局
        frame_layout = QVBoxLayout(self.main_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        
        # 创建简化的标题栏
        self.title_bar = self.create_simple_title_bar()
        frame_layout.addWidget(self.title_bar)
        
        # 内容区域
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        
        frame_layout.addWidget(self.content_widget)
        
        # 延迟显示默认内容
        QTimer.singleShot(50, self.show_default_content)
        
    def enable_shadow(self):
        """启用阴影效果（可选）"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)  # 减小模糊半径
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))  # 减小透明度
        self.main_frame.setGraphicsEffect(shadow)
        
    def create_simple_title_bar(self):
        """创建简化的标题栏"""
        title_bar = QFrame()
        title_bar.setFixedHeight(18)  # 减小高度到一半
        title_bar.setStyleSheet("""
            QFrame {
                background: #3498db;
                border: none;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
            }
        """)
        
        # 标题栏布局
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(3, 0, 3, 0)
        
        # 窗口图标和标题（简化）
        primary_text = " - 主屏幕" if self.screen_info.get('is_primary', False) else ""
        self.title_text = QLabel(f"🖥️ 屏幕 {self.screen_index + 1}{primary_text}")
        self.title_text.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        title_layout.addWidget(self.title_text)
        
        title_layout.addStretch()
        
        # 简化的状态指示器
        self.status_label = QLabel("等待内容")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #f39c12;
                font-size: 10px;
                padding: 2px 4px;
                background: rgba(0, 0, 0, 100);
                border-radius: 2px;
            }
        """)
        title_layout.addWidget(self.status_label)
        
        # 窗口控件
        self.window_controls = PerformanceOptimizedControls()
        self.window_controls.minimize_clicked.connect(self.minimize_window)
        self.window_controls.maximize_clicked.connect(self.toggle_maximize)
        self.window_controls.close_clicked.connect(self.close_window)
        title_layout.addWidget(self.window_controls)
        
        return title_bar
        
    def show_default_content(self):
        """显示优化的默认内容"""
        self.clear_content()
        
        # 简化的默认内容
        default_widget = QWidget()
        default_layout = QVBoxLayout(default_widget)
        default_layout.setAlignment(Qt.AlignCenter)
        
        # 简化的图标
        icon_label = QLabel("🖥️")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Arial", 32))  # 减小字体
        icon_label.setStyleSheet("color: #7f8c8d; margin: 10px;")
        default_layout.addWidget(icon_label)
        
        # 主文本
        primary_text = " - 主屏幕" if self.screen_info.get('is_primary', False) else ""
        main_text = QLabel(f"屏幕 {self.screen_index + 1}{primary_text}")
        main_text.setAlignment(Qt.AlignCenter)
        main_text.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))  # 减小字体
        main_text.setStyleSheet("color: #ecf0f1; margin: 5px;")
        default_layout.addWidget(main_text)
        
        # 简化的详细信息
        info_text = f"{self.screen_info['width']} × {self.screen_info['height']}"
        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Microsoft YaHei", 10))
        info_label.setStyleSheet("color: #bdc3c7; margin: 5px;")
        default_layout.addWidget(info_label)
        
        # 简化的等待提示
        wait_label = QLabel("等待内容投放...")
        wait_label.setAlignment(Qt.AlignCenter)
        wait_label.setFont(QFont("Microsoft YaHei", 12))
        wait_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                padding: 10px;
                border: 1px dashed #3498db;
                border-radius: 4px;
                margin: 10px;
            }
        """)
        default_layout.addWidget(wait_label)
        
        self.content_layout.addWidget(default_widget)
        
    def set_content(self, content_type, content):
        """优化的内容设置"""
        self.current_content_type = content_type
        self.current_content = content
        
        # 更新状态（异步）
        QTimer.singleShot(10, lambda: self._update_status(content_type))
        
        # 延迟清空和加载内容，避免UI阻塞
        QTimer.singleShot(20, lambda: self._load_content_async(content_type, content))
        
    def _update_status(self, content_type):
        """异步更新状态"""
        self.status_label.setText(f"📄 {content_type}")
        self.window_controls.set_title(f"屏幕 {self.screen_index + 1} - {content_type}")
        
    def _load_content_async(self, content_type, content):
        """异步加载内容"""
        self.clear_content()
        
        if content_type == "文本":
            self.set_text_content_fast(content)
        elif content_type == "图片":
            self.set_image_content_fast(content)
        elif content_type == "视频":
            self.set_video_content_fast(content)
        elif content_type == "网页":
            self.set_web_content_fast(content)
            
    def set_text_content_fast(self, text):
        """快速文本内容设置"""
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setAlignment(Qt.AlignCenter)
        
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        text_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                background: #27ae60;
                border: 1px solid #2ecc71;
                border-radius: 5px;
                padding: 20px;
                margin: 10px;
            }
        """)
        text_label.setWordWrap(True)
        text_layout.addWidget(text_label)
        
        self.content_layout.addWidget(text_widget)
        
    def set_image_content_fast(self, image_path):
        """快速图片内容设置"""
        if os.path.exists(image_path):
            # 异步加载图片
            QTimer.singleShot(50, lambda: self._load_image_async(image_path))
        else:
            self.show_error_fast("图片文件未找到")
            
    def _load_image_async(self, image_path):
        """异步加载图片"""
        try:
            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)
            image_layout.setAlignment(Qt.AlignCenter)
            
            image_label = QLabel()
            pixmap = QPixmap(image_path)
            
            if not pixmap.isNull():
                # 限制图片大小，提升性能
                max_size = min(self.width() - 40, 800)  # 最大800px
                scaled_pixmap = pixmap.scaled(
                    max_size,
                    max_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
                image_label.setAlignment(Qt.AlignCenter)
                image_layout.addWidget(image_label)
                
                self.content_layout.addWidget(image_widget)
            else:
                self.show_error_fast("图片格式不支持")
        except Exception as e:
            self.show_error_fast(f"图片加载失败: {str(e)}")
            
    def set_video_content_fast(self, video_path):
        """快速视频内容设置 - 使用多种播放方案"""
        # 确保路径是绝对路径
        if not os.path.isabs(video_path):
            video_path = os.path.abspath(video_path)
            
        print(f"尝试加载视频: {video_path}")
        
        # 检查文件扩展名
        supported_formats = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v', '.3gp']
        file_ext = os.path.splitext(video_path)[1].lower()
        
        if file_ext not in supported_formats:
            self.show_error_fast(f"不支持的视频格式: {file_ext}")
            return
        
        if os.path.exists(video_path):
            try:
                # 检查文件是否可读
                with open(video_path, 'rb') as f:
                    # 读取前4个字节检查文件头
                    header = f.read(4)
                    if len(header) < 4:
                        self.show_error_fast("视频文件似乎已损坏（文件太小）")
                        return
                
                # 清理之前的播放器
                self.clear_video_content()
                
                # 优先使用OpenCV播放器（真正的内嵌播放）
                if OPENCV_AVAILABLE:
                    self.opencv_player = OpenCVVideoPlayer()
                    self.content_layout.addWidget(self.opencv_player)
                    self.status_label.setText("🎬 OpenCV播放器初始化中...")
                    # 增加延迟，确保容器完全展开
                    QTimer.singleShot(500, lambda: self._start_opencv_playback(video_path))
                else:
                    # 回退到嵌入式播放器
                    self.embedded_player = EmbeddedVideoPlayer()
                    self.content_layout.addWidget(self.embedded_player)
                    self.status_label.setText("🎬 初始化视频播放器...")
                    QTimer.singleShot(200, lambda: self._start_embedded_playback(video_path))
                
            except PermissionError:
                self.show_error_fast("无权限访问视频文件")
            except Exception as e:
                print(f"视频加载异常: {str(e)}")
                self.show_error_fast(f"视频加载失败: {str(e)}")
        else:
            print(f"视频文件不存在: {video_path}")
            self.show_error_fast(f"视频文件未找到: {video_path}")
            
    def _start_opencv_playback(self, video_path):
        """启动OpenCV播放器播放"""
        if hasattr(self, 'opencv_player') and self.opencv_player:
            success = self.opencv_player.play_video(video_path)
            if success:
                self.status_label.setText("🎬 OpenCV播放中")
            else:
                self.status_label.setText("❌ OpenCV播放失败")
                
    def _start_embedded_playback(self, video_path):
        """启动嵌入式播放器播放"""
        if hasattr(self, 'embedded_player') and self.embedded_player:
            success = self.embedded_player.play_video(video_path)
            if success:
                self.status_label.setText("🎬 视频播放中")
            else:
                self.status_label.setText("📄 显示视频信息")
                
    def clear_video_content(self):
        """清理视频内容"""
        # 清理传统媒体播放器
        if hasattr(self, 'media_player') and self.media_player:
            self.media_player.stop()
            self.media_player = None
            
        # 清理OpenCV播放器
        if hasattr(self, 'opencv_player') and self.opencv_player:
            self.opencv_player.cleanup()
            self.opencv_player = None
            
        # 清理替代播放器
        if hasattr(self, 'alternative_player') and self.alternative_player:
            self.alternative_player.stop()
            self.alternative_player = None
            
        # 清理嵌入式播放器
        if hasattr(self, 'embedded_player') and self.embedded_player:
            self.embedded_player.cleanup()
            self.embedded_player = None
            
    def _start_video_playback(self):
        """启动视频播放"""
        if self.media_player:
            print("开始播放视频...")
            self.media_player.play()
            
    def handle_media_error(self, error):
        """处理媒体播放错误"""
        error_messages = {
            QMediaPlayer.NoError: "无错误",
            QMediaPlayer.ResourceError: "资源错误 - 文件可能已损坏或不存在",
            QMediaPlayer.FormatError: "格式错误 - 可能缺少对应的解码器", 
            QMediaPlayer.NetworkError: "网络错误",
            QMediaPlayer.AccessDeniedError: "访问被拒绝 - 检查文件权限",
            QMediaPlayer.ServiceMissingError: "媒体服务缺失"
        }
        
        error_msg = error_messages.get(error, f"未知错误 ({error})")
        print(f"媒体播放错误: {error_msg}")
        
        # 针对格式错误提供解决方案
        if error == QMediaPlayer.FormatError:
            detailed_msg = f"""视频格式不兼容

可能的解决方案：
1. 安装 K-Lite Codec Pack 或 VLC Media Player
2. 尝试使用标准MP4格式（H.264编码）
3. 使用其他视频转换软件重新编码

当前系统可能不支持此视频的编解码器"""
            self.show_error_fast(detailed_msg)
        else:
            self.show_error_fast(f"视频播放错误: {error_msg}")
        
    def handle_media_state(self, state):
        """处理媒体播放状态变化"""
        state_messages = {
            QMediaPlayer.StoppedState: "已停止",
            QMediaPlayer.PlayingState: "正在播放", 
            QMediaPlayer.PausedState: "已暂停"
        }
        
        state_msg = state_messages.get(state, f"未知状态 ({state})")
        print(f"媒体播放状态: {state_msg}")
        
        if state == QMediaPlayer.PlayingState:
            self.status_label.setText("🎬 视频播放中")
            
    def set_web_content_fast(self, url):
        """快速网页内容设置"""
        try:
            # 延迟创建WebView，避免阻塞
            QTimer.singleShot(100, lambda: self._create_webview(url))
        except Exception as e:
            self.show_error_fast(f"网页加载失败: {str(e)}")
            
    def _create_webview(self, url):
        """异步创建WebView"""
        try:
            self.web_view = QWebEngineView()
            if url.startswith(('http://', 'https://')):
                self.web_view.load(QUrl(url))
            else:
                self.web_view.load(QUrl('https://' + url))
            
            self.content_layout.addWidget(self.web_view)
        except Exception as e:
            self.show_error_fast(f"网页创建失败: {str(e)}")
            
    def show_error_fast(self, message):
        """快速错误显示"""
        error_widget = QWidget()
        error_layout = QVBoxLayout(error_widget)
        error_layout.setAlignment(Qt.AlignCenter)
        
        error_label = QLabel(f"⚠️ {message}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        error_label.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                background: #fadbd8;
                border: 1px solid #e74c3c;
                border-radius: 5px;
                padding: 15px;
                margin: 10px;
            }
        """)
        error_layout.addWidget(error_label)
        
        self.content_layout.addWidget(error_widget)
        
    def handle_media_status(self, status):
        """处理媒体播放状态"""
        status_messages = {
            QMediaPlayer.UnknownMediaStatus: "未知状态",
            QMediaPlayer.NoMedia: "无媒体",
            QMediaPlayer.LoadingMedia: "加载中",
            QMediaPlayer.LoadedMedia: "已加载",
            QMediaPlayer.StalledMedia: "停滞",
            QMediaPlayer.BufferingMedia: "缓冲中",
            QMediaPlayer.BufferedMedia: "已缓冲",
            QMediaPlayer.EndOfMedia: "播放结束",
            QMediaPlayer.InvalidMedia: "无效媒体"
        }
        
        status_msg = status_messages.get(status, f"未知状态 ({status})")
        print(f"媒体状态: {status_msg}")
        
        if status == QMediaPlayer.LoadedMedia:
            print("媒体已加载，开始播放...")
            if self.media_player:
                self.media_player.play()
        elif status == QMediaPlayer.EndOfMedia and self.media_player:
            print("视频播放结束，重新开始...")
            self.media_player.setPosition(0)
            self.media_player.play()
        elif status == QMediaPlayer.InvalidMedia:
            self.show_error_fast("无效的视频格式或文件已损坏")
            
    def clear_content(self):
        """快速清空内容"""
        # 异步清理媒体播放器
        if hasattr(self, 'media_player') and self.media_player:
            QTimer.singleShot(10, self._cleanup_media)
            
        # 清理替代播放器
        if hasattr(self, 'alternative_player') and self.alternative_player:
            self.alternative_player.stop()
            
        # 清理OpenCV播放器
        if hasattr(self, 'opencv_player') and self.opencv_player:
            self.opencv_player.cleanup()
            
        # 清理嵌入式播放器
        if hasattr(self, 'embedded_player') and self.embedded_player:
            self.embedded_player.cleanup()
            
        # 快速清空布局
        for i in reversed(range(self.content_layout.count())):
            child = self.content_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
    def _cleanup_media(self):
        """异步清理媒体资源"""
        if hasattr(self, 'media_player') and self.media_player:
            self.media_player.stop()
            self.media_player.setMedia(QMediaContent())
            self.media_player = None
        if hasattr(self, 'video_widget') and self.video_widget:
            self.video_widget = None
                
    def position_window(self):
        """快速窗口定位"""
        # 设置默认大小为屏幕的50%（减小默认大小）
        default_width = int(self.screen_info['width'] * 0.5)
        default_height = int(self.screen_info['height'] * 0.5)
        
        # 居中位置
        x = self.screen_info['x'] + (self.screen_info['width'] - default_width) // 2
        y = self.screen_info['y'] + (self.screen_info['height'] - default_height) // 2
        
        self.setGeometry(x, y, default_width, default_height)
        self.normal_geometry = self.geometry()
        
    def minimize_window(self):
        """最小化窗口"""
        self.showMinimized()
        
    def toggle_maximize(self):
        """切换最大化状态"""
        if self.is_maximized:
            self.restore_window()
        else:
            self.maximize_window()
            
    def maximize_window(self):
        """最大化窗口"""
        if not self.is_maximized:
            self.normal_geometry = self.geometry()
            
        # 最大化到当前屏幕
        screen_rect = QRect(
            self.screen_info['x'],
            self.screen_info['y'],
            self.screen_info['width'],
            self.screen_info['height']
        )
        self.setGeometry(screen_rect)
        self.is_maximized = True
        self.window_controls.update_maximize_button(True)
        
    def restore_window(self):
        """还原窗口"""
        if self.normal_geometry.isValid():
            self.setGeometry(self.normal_geometry)
        self.is_maximized = False
        self.window_controls.update_maximize_button(False)
        
    def toggle_fullscreen(self):
        """切换全屏模式"""
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.enter_fullscreen()
            
    def enter_fullscreen(self):
        """进入全屏 - 优化为无边框纯内容显示"""
        if not self.is_fullscreen:
            self.normal_geometry = self.geometry()
        
        # 隐藏窗口
        self.hide()
        
        # 设置为真正的无边框全屏窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        
        # 获取主屏幕几何
        screen = QApplication.desktop().screenNumber(self)
        screen_rect = QApplication.desktop().screenGeometry(screen)
        
        # 设置窗口几何为整个屏幕（包含任务栏区域）
        self.setGeometry(screen_rect)
        
        # 强制移除所有可能的边框和边距
        self.setContentsMargins(0, 0, 0, 0)
        
        # 显示窗口
        self.show()
        
        # 立即显示为全屏
        self.showFullScreen()
        
        # 隐藏��有装饰性元素，只显示内容
        self.main_frame.setStyleSheet("""
            QFrame {
                background: black;
                border: none;
                border-radius: 0px;
                margin: 0px;
                padding: 0px;
                outline: none;
            }
        """)
        
        # 确保窗口本身没有边框
        self.setStyleSheet("""
            QWidget {
                border: none;
                outline: none;
                background: black;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        self.title_bar.hide()
        
        # 移除所有边距和间距
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 移除主布局的边距
        if self.layout():
            self.layout().setContentsMargins(0, 0, 0, 0)
            
        # 移除主框架的布局边距
        if hasattr(self.main_frame, 'layout') and self.main_frame.layout():
            self.main_frame.layout().setContentsMargins(0, 0, 0, 0)
            
        # 移除内容区域边距
        if hasattr(self, 'content_widget'):
            self.content_widget.setContentsMargins(0, 0, 0, 0)
        
        # 如果有视频播放器，让其填满整个窗口
        self.resize_content_to_fullscreen()
        
        self.is_fullscreen = True
        
        # 强制刷新界面
        self.update()
        self.repaint()
        QApplication.processEvents()
        
        # 显示退出提示（短暂显示后自动隐藏）
        QTimer.singleShot(100, self.show_fullscreen_exit_hint)
        
        # 强制窗口获得焦点
        self.raise_()
        self.activateWindow()
        self.setFocus()
        
    def show_fullscreen_exit_hint(self):
        """显示全屏退出提示"""
        if not hasattr(self, 'exit_hint_label'):
            self.exit_hint_label = QLabel(self)
            self.exit_hint_label.setText("按 ESC 键退出全屏")
            self.exit_hint_label.setStyleSheet("""
                QLabel {
                    background: rgba(0, 0, 0, 150);
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 8px;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
            """)
            self.exit_hint_label.setAlignment(Qt.AlignCenter)
            
        # 调整提示位置到右上角
        hint_width = 150
        hint_height = 40
        self.exit_hint_label.resize(hint_width, hint_height)
        self.exit_hint_label.move(self.width() - hint_width - 20, 20)
        self.exit_hint_label.show()
        
        # 3秒后自动隐藏提示
        QTimer.singleShot(3000, self.hide_fullscreen_exit_hint)
        
    def hide_fullscreen_exit_hint(self):
        """隐藏全屏退出提示"""
        if hasattr(self, 'exit_hint_label'):
            self.exit_hint_label.hide()
        
    def resize_content_to_fullscreen(self):
        """调整内容以填满全屏"""
        # 获取内容区域的所有小部件
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                # 移除边距
                widget.setStyleSheet("""
                    QWidget {
                        border: none;
                        margin: 0px;
                        padding: 0px;
                        border-radius: 0px;
                    }
                """)
                
                # 特殊处理不同类型的内容
                if hasattr(self, 'opencv_player') and self.opencv_player and widget == self.opencv_player:
                    self.opencv_player.enable_fullscreen_mode()
                
                elif hasattr(self, 'embedded_player') and self.embedded_player and widget == self.embedded_player:
                    self.embedded_player.setStyleSheet("""
                        QWidget {
                            border: none;
                            margin: 0px;
                            padding: 0px;
                            border-radius: 0px;
                            background: black;
                        }
                    """)
                
                elif hasattr(self, 'web_view') and self.web_view and widget == self.web_view:
                    self.web_view.setStyleSheet("""
                        QWebEngineView {
                            border: none;
                            margin: 0px;
                            padding: 0px;
                            border-radius: 0px;
                        }
                    """)
        
        # 强制刷新界面
        self.update()
        QApplication.processEvents()
        
    def exit_fullscreen(self):
        """退出全屏 - 恢复原始状态"""
        # 隐藏退出提示
        self.hide_fullscreen_exit_hint()
        
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        # 恢复主框架样式
        self.main_frame.setStyleSheet("""
            QFrame {
                background: #2c3e50;
                border: 0.5px solid #3498db;
                border-radius: 5px;
            }
        """)
        
        # 恢复窗口样式
        self.setStyleSheet("")
        
        # 显示标题栏
        self.title_bar.show()
        
        # 恢复内容区域的边距
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        
        # 恢复主布局的边距
        if self.layout():
            self.layout().setContentsMargins(5, 5, 5, 5)
            
        # 恢复内容区域边距
        if hasattr(self, 'content_widget'):
            if hasattr(self.content_widget, 'setContentsMargins'):
                self.content_widget.setContentsMargins(0, 0, 0, 0)
        
        # 恢复内容的原始样式
        self.restore_content_styles()
        
        # 恢复窗口几何
        if self.normal_geometry.isValid():
            self.setGeometry(self.normal_geometry)
        self.show()
        self.is_fullscreen = False
        
    def restore_content_styles(self):
        """恢复内容的原始样式"""
        # 恢复不同类型内容的样式
        if hasattr(self, 'opencv_player') and self.opencv_player:
            self.opencv_player.disable_fullscreen_mode()
        
        elif hasattr(self, 'embedded_player') and self.embedded_player:
            self.embedded_player.setStyleSheet("")
        
        elif hasattr(self, 'web_view') and self.web_view:
            self.web_view.setStyleSheet("")
        
        # 恢复所有子部件的样式
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget and widget.__class__.__name__ not in ['OpenCVVideoPlayer', 'EmbeddedVideoPlayer', 'QWebEngineView']:
                widget.setStyleSheet("")  # 恢复默认样式
        
    def close_window(self):
        """关闭窗口"""
        # 异步保存状态和清理
        QTimer.singleShot(10, self._async_cleanup)
        self.window_closed.emit(self.screen_index)
        self.close()
        
    def _async_cleanup(self):
        """异步清理"""
        self.save_window_state()
        self.clear_content()
        
    def save_window_state(self):
        """保存窗口状态"""
        state = {
            'geometry': [self.x(), self.y(), self.width(), self.height()],
            'is_maximized': self.is_maximized,
            'screen_index': self.screen_index
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception:
            pass  # 忽略保存错误，避免阻塞
            
    def load_window_state(self):
        """加载窗口状态"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    
                geometry = state.get('geometry')
                if geometry and len(geometry) == 4:
                    self.setGeometry(*geometry)
                    self.normal_geometry = self.geometry()
                    
                if state.get('is_maximized', False):
                    QTimer.singleShot(100, self.maximize_window)  # 延迟最大化
        except Exception:
            pass  # 忽略加载错误
            
    # 优化的事件处理
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton and self.title_bar.geometry().contains(event.pos()):
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            if not self.is_maximized and not self.is_fullscreen:
                self.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseDoubleClickEvent(self, event):
        """双击事件"""
        if self.title_bar.geometry().contains(event.pos()):
            self.toggle_maximize()
            
    def keyPressEvent(self, event):
        """键盘事件处理"""
        if event.key() == Qt.Key_Escape:
            if self.is_fullscreen:
                self.exit_fullscreen()
            else:
                self.close_window()
        elif event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key_F10:
            self.toggle_maximize()
        super().keyPressEvent(event)
        
    def closeEvent(self, event):
        """关闭事件处理"""
        self._async_cleanup()
        event.accept()
        
    def enable_advanced_features(self):
        """启用高级特性（可选）"""
        self.shadow_enabled = True
        self.animations_enabled = True
        self.enable_shadow()


# 向后兼容
ContentWindow = OptimizedContentContainer
ContentContainer = OptimizedContentContainer