#!/usr/bin/env python3
"""
视频播放替代方案
提供多种视频播放解决方案
"""

import os
import sys
import subprocess
import tempfile
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class VideoPlayerType:
    """视频播放器类型"""
    QT_NATIVE = "qt_native"
    WEB_PLAYER = "web_player" 
    EXTERNAL_PLAYER = "external_player"
    IMAGE_FRAMES = "image_frames"

class AlternativeVideoPlayer(QWidget):
    """替代视频播放器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_video_path = None
        self.player_type = None
        self.media_player = None
        self.web_view = None
        self.external_process = None
        self.image_label = None
        self.frame_timer = None
        
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # 状态标签
        self.status_label = QLabel("准备播放视频...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                background: #34495e;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        self.layout.addWidget(self.status_label)
        
    def play_video(self, video_path):
        """播放视频 - 自动选择最佳方案"""
        self.current_video_path = video_path
        print(f"尝试播放视频: {video_path}")
        
        # 清理之前的播放器
        self.cleanup_players()
        
        # 按优先级尝试不同的播放方案
        methods = [
            (self.try_qt_native_player, "Qt原生播放器"),
            (self.try_web_player, "Web播放器"),
            (self.try_external_player, "外部播放器"),
            (self.try_image_preview, "图片预览")
        ]
        
        for method, name in methods:
            try:
                print(f"尝试 {name}...")
                if method(video_path):
                    print(f"✅ {name} 成功")
                    return True
            except Exception as e:
                print(f"❌ {name} 失败: {e}")
                continue
                
        self.show_error("所有视频播放方案都失败了")
        return False
        
    def try_qt_native_player(self, video_path):
        """尝试Qt原生播放器"""
        try:
            self.media_player = QMediaPlayer()
            self.video_widget = QVideoWidget()
            
            self.media_player.setVideoOutput(self.video_widget)
            self.media_player.error.connect(self.on_qt_player_error)
            self.media_player.mediaStatusChanged.connect(self.on_qt_status_changed)
            
            # 添加到布局
            self.layout.addWidget(self.video_widget)
            
            # 加载媒体
            file_url = QUrl.fromLocalFile(os.path.abspath(video_path))
            media_content = QMediaContent(file_url)
            self.media_player.setMedia(media_content)
            
            self.player_type = VideoPlayerType.QT_NATIVE
            self.status_label.setText("🎬 Qt原生播放器")
            
            # 延迟播放
            QTimer.singleShot(500, self.media_player.play)
            return True
            
        except Exception as e:
            print(f"Qt播放器初始化失败: {e}")
            return False
            
    def try_web_player(self, video_path):
        """尝试Web播放器"""
        try:
            self.web_view = QWebEngineView()
            
            # 创建HTML5视频播放器
            html_content = self.create_html5_player(video_path)
            
            # 写入临时HTML文件
            temp_dir = tempfile.gettempdir()
            html_file = os.path.join(temp_dir, "video_player.html")
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # 加载HTML
            self.web_view.load(QUrl.fromLocalFile(html_file))
            self.layout.addWidget(self.web_view)
            
            self.player_type = VideoPlayerType.WEB_PLAYER
            self.status_label.setText("🌐 Web播放器")
            return True
            
        except Exception as e:
            print(f"Web播放器失败: {e}")
            return False
            
    def try_external_player(self, video_path):
        """尝试外部播放器（嵌入窗口）"""
        try:
            # 创建一个容器来显示外部播放器的信息
            external_widget = QWidget()
            external_layout = QVBoxLayout(external_widget)
            
            # 信息显示
            info_label = QLabel(f"""
🎥 使用外部播放器

文件: {os.path.basename(video_path)}
路径: {video_path}

外部播放器正在运行...
按 ESC 或关闭窗口停止播放
            """)
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setStyleSheet("""
                QLabel {
                    color: #ecf0f1;
                    background: #2c3e50;
                    padding: 20px;
                    border-radius: 10px;
                    font-size: 14px;
                    border: 2px solid #3498db;
                }
            """)
            external_layout.addWidget(info_label)
            
            # 控制按钮
            control_layout = QHBoxLayout()
            
            open_btn = QPushButton("📂 在文件管理器中打开")
            open_btn.clicked.connect(lambda: self.open_in_explorer(video_path))
            open_btn.setStyleSheet("""
                QPushButton {
                    background: #27ae60;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #229954;
                }
            """)
            control_layout.addWidget(open_btn)
            
            play_btn = QPushButton("▶️ 用默认播放器打开")
            play_btn.clicked.connect(lambda: self.open_with_default_player(video_path))
            play_btn.setStyleSheet("""
                QPushButton {
                    background: #3498db;
                    color: white;
                    border: none;
                    padding: 10px 15px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #2980b9;
                }
            """)
            control_layout.addWidget(play_btn)
            
            external_layout.addLayout(control_layout)
            
            self.layout.addWidget(external_widget)
            
            self.player_type = VideoPlayerType.EXTERNAL_PLAYER
            self.status_label.setText("🎮 外部播放器")
            return True
            
        except Exception as e:
            print(f"外部播放器失败: {e}")
            return False
            
    def try_image_preview(self, video_path):
        """尝试视频缩略图预览"""
        try:
            preview_widget = QWidget()
            preview_layout = QVBoxLayout(preview_widget)
            
            # 视频信息
            info = self.get_video_info(video_path)
            info_text = f"""
📹 视频文件预览

文件名: {os.path.basename(video_path)}
大小: {self.get_file_size_str(video_path)}
路径: {video_path}

{info}

⚠️ 当前系统无法直接播放此视频格式
💡 建议使用视频修复工具转换格式
            """
            
            info_label = QLabel(info_text)
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setWordWrap(True)
            info_label.setStyleSheet("""
                QLabel {
                    color: #ecf0f1;
                    background: #e67e22;
                    padding: 20px;
                    border-radius: 10px;
                    font-size: 12px;
                    border: 2px solid #d35400;
                }
            """)
            preview_layout.addWidget(info_label)
            
            # 操作按钮
            button_layout = QHBoxLayout()
            
            repair_btn = QPushButton("🔧 视频修复工具")
            repair_btn.clicked.connect(self.open_repair_tool)
            repair_btn.setStyleSheet(self.get_button_style("#e74c3c"))
            button_layout.addWidget(repair_btn)
            
            external_btn = QPushButton("🎬 外部播放器")
            external_btn.clicked.connect(lambda: self.open_with_default_player(video_path))
            external_btn.setStyleSheet(self.get_button_style("#9b59b6"))
            button_layout.addWidget(external_btn)
            
            preview_layout.addLayout(button_layout)
            
            self.layout.addWidget(preview_widget)
            
            self.player_type = VideoPlayerType.IMAGE_FRAMES
            self.status_label.setText("📄 视频预览")
            return True
            
        except Exception as e:
            print(f"图片预览失败: {e}")
            return False
            
    def create_html5_player(self, video_path):
        """创建HTML5视频播放器"""
        video_url = QUrl.fromLocalFile(os.path.abspath(video_path)).toString()
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Video Player</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: #000;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        video {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .error {{
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <video controls autoplay loop>
        <source src="{video_url}" type="video/mp4">
        <source src="{video_url}" type="video/webm">
        <source src="{video_url}" type="video/ogg">
        <div class="error">
            <h2>无法播放视频</h2>
            <p>您的浏览器不支持此视频格式</p>
        </div>
    </video>
    
    <script>
        const video = document.querySelector('video');
        video.addEventListener('error', function(e) {{
            console.error('Video error:', e);
            document.body.innerHTML = '<div class="error"><h2>视频加载失败</h2><p>文件格式可能不受支持</p></div>';
        }});
        
        video.addEventListener('loadstart', function() {{
            console.log('Video loading started');
        }});
        
        video.addEventListener('canplay', function() {{
            console.log('Video can start playing');
        }});
    </script>
</body>
</html>
        """
        return html
        
    def get_video_info(self, video_path):
        """获取视频信息"""
        try:
            # 尝试使用ffprobe获取视频信息
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                
                format_info = data.get('format', {})
                duration = format_info.get('duration', 'Unknown')
                format_name = format_info.get('format_name', 'Unknown')
                
                video_stream = None
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        video_stream = stream
                        break
                
                if video_stream:
                    codec = video_stream.get('codec_name', 'Unknown')
                    width = video_stream.get('width', 'Unknown')
                    height = video_stream.get('height', 'Unknown')
                    
                    return f"编码: {codec}\\n分辨率: {width}x{height}\\n时长: {duration}秒\\n格式: {format_name}"
                    
        except Exception as e:
            print(f"获取视频信息失败: {e}")
            
        return "无法获取视频详细信息"
        
    def get_file_size_str(self, file_path):
        """获取文件大小字符串"""
        try:
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.1f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024):.1f} MB"
            else:
                return f"{size / (1024 * 1024 * 1024):.1f} GB"
        except:
            return "Unknown"
            
    def get_button_style(self, color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
        
    def open_in_explorer(self, file_path):
        """在文件管理器中打开"""
        try:
            subprocess.run(['explorer', '/select,', file_path])
        except Exception as e:
            print(f"打开文件管理器失败: {e}")
            
    def open_with_default_player(self, file_path):
        """用默认播放器打开"""
        try:
            os.startfile(file_path)
        except Exception as e:
            print(f"打开默认播放器失败: {e}")
            
    def open_repair_tool(self):
        """打开视频修复工具"""
        try:
            subprocess.Popen([sys.executable, 'video_repair_tool.py'])
        except Exception as e:
            print(f"打开修复工具失败: {e}")
            
    def on_qt_player_error(self, error):
        """Qt播放器错误处理"""
        print(f"Qt播放器错误: {error}")
        # 如果Qt播放器失败，尝试其他方案
        if self.current_video_path:
            self.cleanup_players()
            self.try_web_player(self.current_video_path)
            
    def on_qt_status_changed(self, status):
        """Qt播放器状态变化"""
        if status == QMediaPlayer.InvalidMedia:
            print("Qt播放器: 无效媒体，尝试其他方案")
            if self.current_video_path:
                self.cleanup_players()
                self.try_web_player(self.current_video_path)
                
    def show_error(self, message):
        """显示错误信息"""
        error_widget = QWidget()
        error_layout = QVBoxLayout(error_widget)
        
        error_label = QLabel(f"❌ {message}")
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                background: #fadbd8;
                padding: 20px;
                border-radius: 10px;
                font-size: 14px;
                border: 2px solid #e74c3c;
            }
        """)
        error_layout.addWidget(error_label)
        
        self.layout.addWidget(error_widget)
        self.status_label.setText("❌ 播放失败")
        
    def cleanup_players(self):
        """清理所有播放器"""
        # 清理Qt播放器
        if self.media_player:
            self.media_player.stop()
            self.media_player = None
            
        # 清理Web播放器
        if self.web_view:
            self.web_view.setParent(None)
            self.web_view = None
            
        # 清理外部进程
        if self.external_process:
            try:
                self.external_process.terminate()
            except:
                pass
            self.external_process = None
            
        # 清理布局中的组件
        while self.layout.count() > 1:  # 保留状态标签
            item = self.layout.takeAt(1)
            if item.widget():
                item.widget().setParent(None)
                
    def stop(self):
        """停止播放"""
        self.cleanup_players()
        self.status_label.setText("⏹️ 已停止")

# 导出主要类供其他模块使用
__all__ = ['AlternativeVideoPlayer', 'VideoPlayerType']