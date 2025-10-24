#!/usr/bin/env python3
"""
嵌入式视频播放器
直接调用外部播放器并嵌入到应用窗口中
"""

import os
import sys
import subprocess
import time
import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import ctypes
from ctypes import wintypes

class EmbeddedVideoPlayer(QWidget):
    """嵌入式视频播放器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_process = None
        self.video_hwnd = None
        self.video_path = None
        self.player_type = None
        
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setMinimumSize(400, 300)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        
        # 视频容器
        self.video_container = QWidget()
        self.video_container.setStyleSheet("""
            QWidget {
                background-color: black;
                border: 1px solid #3498db;
                border-radius: 5px;
            }
        """)
        self.layout.addWidget(self.video_container)
        
        # 控制面板
        self.create_control_panel()
        
    def create_control_panel(self):
        """创建控制面板"""
        control_frame = QFrame()
        control_frame.setMaximumHeight(80)
        control_frame.setStyleSheet("""
            QFrame {
                background: #34495e;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        
        control_layout = QVBoxLayout(control_frame)
        
        # 状态标签
        self.status_label = QLabel("准备播放视频...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #ecf0f1; font-size: 12px; padding: 5px;")
        control_layout.addWidget(self.status_label)
        
        # 按钮组
        button_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶️ 播放")
        self.play_btn.clicked.connect(self.toggle_play)
        self.play_btn.setStyleSheet(self.get_button_style("#27ae60"))
        button_layout.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("⏹️ 停止")
        self.stop_btn.clicked.connect(self.stop_video)
        self.stop_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        button_layout.addWidget(self.stop_btn)
        
        self.external_btn = QPushButton("🎬 外部播放")
        self.external_btn.clicked.connect(self.play_external)
        self.external_btn.setStyleSheet(self.get_button_style("#3498db"))
        button_layout.addWidget(self.external_btn)
        
        control_layout.addLayout(button_layout)
        
        self.layout.addWidget(control_frame)
        
    def get_button_style(self, color):
        """获取按钮样式"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
        
    def play_video(self, video_path):
        """播放视频"""
        self.video_path = video_path
        print(f"嵌入式播放器尝试播放: {video_path}")
        
        # 先尝试多种播放器
        players = [
            ("VLC", self.try_vlc_player),
            ("PotPlayer", self.try_potplayer),
            ("Windows Media Player", self.try_windows_media_player),
            ("默认播放器", self.try_default_player)
        ]
        
        for name, player_func in players:
            try:
                print(f"尝试 {name}...")
                if player_func(video_path):
                    self.player_type = name
                    self.status_label.setText(f"🎬 使用 {name} 播放")
                    print(f"✅ {name} 启动成功")
                    return True
            except Exception as e:
                print(f"❌ {name} 失败: {e}")
                continue
                
        # 如果都失败了，显示文件信息
        self.show_video_info(video_path)
        return False
        
    def try_vlc_player(self, video_path):
        """尝试VLC播放器"""
        vlc_paths = [
            r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
            "vlc.exe"  # PATH中的VLC
        ]
        
        for vlc_path in vlc_paths:
            if os.path.exists(vlc_path) or vlc_path == "vlc.exe":
                try:
                    # VLC命令行参数
                    cmd = [
                        vlc_path,
                        video_path,
                        "--intf", "dummy",  # 不显示界面
                        "--extraintf", "rc",  # 远程控制接口
                        "--loop",  # 循环播放
                        "--fullscreen",  # 全屏
                        "--no-video-title-show",  # 不显示标题
                    ]
                    
                    self.video_process = subprocess.Popen(cmd)
                    time.sleep(1)  # 等待进程启动
                    
                    if self.video_process.poll() is None:  # 进程还在运行
                        return True
                        
                except Exception as e:
                    print(f"VLC启动失败: {e}")
                    
        return False
        
    def try_potplayer(self, video_path):
        """尝试PotPlayer"""
        pot_paths = [
            r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe",
            r"C:\Program Files (x86)\DAUM\PotPlayer\PotPlayerMini.exe",
            "PotPlayerMini64.exe"
        ]
        
        for pot_path in pot_paths:
            if os.path.exists(pot_path) or "PotPlayer" in pot_path:
                try:
                    cmd = [pot_path, video_path, "/loop", "/fullscreen"]
                    self.video_process = subprocess.Popen(cmd)
                    time.sleep(1)
                    
                    if self.video_process.poll() is None:
                        return True
                        
                except Exception as e:
                    print(f"PotPlayer启动失败: {e}")
                    
        return False
        
    def try_windows_media_player(self, video_path):
        """尝试Windows Media Player"""
        try:
            cmd = ["wmplayer.exe", video_path, "/fullscreen"]
            self.video_process = subprocess.Popen(cmd)
            time.sleep(1)
            
            if self.video_process.poll() is None:
                return True
                
        except Exception as e:
            print(f"Windows Media Player启动失败: {e}")
            
        return False
        
    def try_default_player(self, video_path):
        """尝试系统默认播放器"""
        try:
            # 使用os.startfile在后台启动
            self.video_process = subprocess.Popen(["cmd", "/c", "start", "", video_path], shell=True)
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"默认播放器启动失败: {e}")
            return False
            
    def show_video_info(self, video_path):
        """显示视频信息（当无法播放时）"""
        # 清理容器
        for child in self.video_container.findChildren(QWidget):
            child.setParent(None)
            
        # 创建信息显示
        info_layout = QVBoxLayout(self.video_container)
        
        # 视频文件信息
        file_info = QLabel(f"""
🎥 视频文件

文件名: {os.path.basename(video_path)}
路径: {video_path}
大小: {self.get_file_size(video_path)}

⚠️ 无法使用内置播放器播放
💡 请点击"外部播放"使用系统播放器
        """)
        file_info.setAlignment(Qt.AlignCenter)
        file_info.setWordWrap(True)
        file_info.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                background: rgba(52, 73, 94, 150);
                padding: 20px;
                border-radius: 10px;
                font-size: 12px;
                border: 2px dashed #3498db;
            }
        """)
        info_layout.addWidget(file_info)
        
        # 操作按钮
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        open_folder_btn = QPushButton("📂 打开文件夹")
        open_folder_btn.clicked.connect(lambda: self.open_folder(video_path))
        open_folder_btn.setStyleSheet(self.get_button_style("#9b59b6"))
        button_layout.addWidget(open_folder_btn)
        
        repair_btn = QPushButton("🔧 修复工具")
        repair_btn.clicked.connect(self.open_repair_tool)
        repair_btn.setStyleSheet(self.get_button_style("#e67e22"))
        button_layout.addWidget(repair_btn)
        
        info_layout.addWidget(button_frame)
        
        self.status_label.setText("📄 显示视频信息")
        
    def get_file_size(self, file_path):
        """获取文件大小"""
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
            
    def toggle_play(self):
        """切换播放/暂停"""
        if self.video_process:
            if self.video_process.poll() is None:
                self.stop_video()
            else:
                if self.video_path:
                    self.play_video(self.video_path)
        else:
            if self.video_path:
                self.play_video(self.video_path)
                
    def stop_video(self):
        """停止视频"""
        if self.video_process:
            try:
                # 温和地终止进程
                self.video_process.terminate()
                time.sleep(0.5)
                
                # 如果还没结束，强制终止
                if self.video_process.poll() is None:
                    self.video_process.kill()
                    
            except Exception as e:
                print(f"停止播放失败: {e}")
            finally:
                self.video_process = None
                
        self.status_label.setText("⏹️ 已停止")
        self.play_btn.setText("▶️ 播放")
        
    def play_external(self):
        """外部播放器播放"""
        if self.video_path:
            try:
                os.startfile(self.video_path)
                self.status_label.setText("🎬 已用外部播放器打开")
            except Exception as e:
                print(f"外部播放失败: {e}")
                self.status_label.setText("❌ 外部播放失败")
                
    def open_folder(self, file_path):
        """打开文件所在文件夹"""
        try:
            subprocess.run(['explorer', '/select,', file_path])
        except Exception as e:
            print(f"打开文件夹失败: {e}")
            
    def open_repair_tool(self):
        """打开修复工具"""
        try:
            subprocess.Popen([sys.executable, 'video_repair_tool.py'])
        except Exception as e:
            print(f"打开修复工具失败: {e}")
            
    def cleanup(self):
        """清理资源"""
        self.stop_video()
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.cleanup()
        event.accept()

# 导出主要类
__all__ = ['EmbeddedVideoPlayer']