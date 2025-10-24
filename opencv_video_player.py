#!/usr/bin/env python3
"""
基于OpenCV的内嵌视频播放器
真正在容器内播放视频
"""

import cv2
import os
import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class OpenCVVideoThread(QThread):
    """OpenCV视频播放线程"""
    
    frameReady = pyqtSignal(np.ndarray)
    positionChanged = pyqtSignal(int)
    durationChanged = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.video_path = None
        self.cap = None
        self.playing = False
        self.paused = False
        self.current_frame = 0
        self.total_frames = 0
        self.fps = 30
        self.seek_frame = -1
        
    def load_video(self, video_path):
        """加载视频"""
        self.video_path = video_path
        
    def run(self):
        """播放线程主循环"""
        try:
            if not self.video_path or not os.path.exists(self.video_path):
                self.error.emit("视频文件不存在")
                return
                
            # 打开视频文件
            self.cap = cv2.VideoCapture(self.video_path)
            
            if not self.cap.isOpened():
                self.error.emit("无法打开视频文件")
                return
                
            # 获取视频信息
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            duration = int(self.total_frames / self.fps)
            
            self.durationChanged.emit(duration)
            
            print(f"视频信息: {self.total_frames}帧, {self.fps}fps, {duration}秒")
            
            self.playing = True
            frame_delay = int(1000 / self.fps)  # 毫秒
            
            while self.playing and self.cap.isOpened():
                if self.seek_frame >= 0:
                    # 跳转到指定帧
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.seek_frame)
                    self.current_frame = self.seek_frame
                    self.seek_frame = -1
                
                if not self.paused:
                    ret, frame = self.cap.read()
                    
                    if not ret:
                        # 视频结束，循环播放
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        self.current_frame = 0
                        continue
                    
                    # 发送帧数据
                    self.frameReady.emit(frame)
                    self.positionChanged.emit(self.current_frame)
                    
                    self.current_frame += 1
                
                # 控制播放速度
                self.msleep(frame_delay)
                
        except Exception as e:
            self.error.emit(f"播放错误: {str(e)}")
        finally:
            if self.cap:
                self.cap.release()
            self.finished.emit()
            
    def play(self):
        """播放"""
        self.paused = False
        
    def pause(self):
        """暂停"""
        self.paused = True
        
    def stop(self):
        """停止"""
        self.playing = False
        self.wait()
        
    def seek(self, frame_number):
        """跳转到指定帧"""
        if 0 <= frame_number < self.total_frames:
            self.seek_frame = frame_number

class OpenCVVideoPlayer(QWidget):
    """OpenCV视频播放器组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.video_thread = None
        self.current_video = None
        
        self.init_ui()
        
    def init_ui(self):
        """初始化界面 - 简化版本，只保留视频显示"""
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)  # 减小边距
        
        # 视频显示区域 - 占据整个空间
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("""
            QLabel {
                background-color: black;
                border: 1px solid #3498db;
                border-radius: 3px;
            }
        """)
        self.video_label.setText("准备播放视频...")
        self.video_label.setMinimumSize(400, 300)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.video_label)
        
        # 添加缓存的尺寸和缩放图像
        self.cached_size = None
        self.cached_scaled_image = None
        
        # 移除所有控制面板、进度条和状态标签
        # 只保留视频显示功能
        
    def play_video(self, video_path):
        """播放视频"""
        print(f"OpenCV播放器加载视频: {video_path}")
        
        # 停止之前的播放
        self.stop_video()
        
        self.current_video = video_path
        
        # 确保界面已完全初始化
        QApplication.processEvents()
        
        # 预设视频标签尺寸，避免初始缩放
        if self.video_label.size().width() < 100:
            self.video_label.resize(400, 300)
            
        # 重置缓存
        self.cached_size = None
        self.cached_scaled_image = None
        
        # 创建播放线程
        self.video_thread = OpenCVVideoThread()
        self.video_thread.load_video(video_path)
        
        # 连接信号
        self.video_thread.frameReady.connect(self.update_frame)
        self.video_thread.positionChanged.connect(self.update_position)
        self.video_thread.durationChanged.connect(self.update_duration)
        self.video_thread.finished.connect(self.on_playback_finished)
        self.video_thread.error.connect(self.on_playback_error)
        
        # 延迟启动播放，确保界面稳定
        QTimer.singleShot(300, self._delayed_start)
        
        return True
        
    def _delayed_start(self):
        """延迟启动播放"""
        if self.video_thread:
            self.video_thread.start()
        
    def update_frame(self, frame):
        """更新视频帧"""
        try:
            # 转换OpenCV图像为QImage
            height, width, channels = frame.shape
            bytes_per_line = channels * width
            
            # 从BGR转换为RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            qt_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # 获取当前标签尺寸
            label_size = self.video_label.size()
            
            # 只有当尺寸变化时才重新缩放
            if self.cached_size != label_size or self.cached_scaled_image is None:
                # 确保最小尺寸
                if label_size.width() < 100 or label_size.height() < 100:
                    label_size = QSize(400, 300)
                
                self.cached_size = label_size
                
                # 缩放图像以适应标签大小
                scaled_image = qt_image.scaled(
                    label_size, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                
                # 缓存基础缩放图像
                self.cached_scaled_image = scaled_image
            else:
                # 使用缓存的尺寸进行快速缩放
                scaled_image = qt_image.scaled(
                    self.cached_size, 
                    Qt.KeepAspectRatio, 
                    Qt.FastTransformation  # 使用快速变换
                )
            
            # 更新显示
            pixmap = QPixmap.fromImage(scaled_image)
            self.video_label.setPixmap(pixmap)
            
        except Exception as e:
            print(f"更新帧失败: {e}")
            
    def update_position(self, frame_number):
        """更新播放位置 - 简化版本"""
        # 不再需要更新进度条和时间显示
        pass
            
    def update_duration(self, duration):
        """更新视频总时长 - 简化版本"""
        # 不再需要设置进度条最大值
        pass
            
                
    def stop_video(self):
        """停止播放"""
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread = None
            
        self.video_label.setText("视频已停止")
        self.video_label.setPixmap(QPixmap())
            
    def on_playback_finished(self):
        """播放完成"""
        print("视频播放完成")
        
    def on_playback_error(self, error_msg):
        """播放错误"""
        print(f"播放错误: {error_msg}")
        self.video_label.setText(f"播放错误: {error_msg}")
        self.video_label.setPixmap(QPixmap())
        
    def cleanup(self):
        """清理资源"""
        self.stop_video()
        
    def enable_fullscreen_mode(self):
        """启用全屏模式 - 移除所有边距和边框"""
        self.setStyleSheet("""
            QWidget {
                background: black;
                border: none;
                margin: 0px;
                padding: 0px;
            }
            QLabel {
                background: black;
                border: none;
                margin: 0px;
                padding: 0px;
            }
        """)
        
        # 调整视频标签填满整个空间
        if self.video_label:
            self.video_label.setStyleSheet("""
                QLabel {
                    background: black;
                    border: none;
                    margin: 0px;
                    padding: 0px;
                }
            """)
            
    def disable_fullscreen_mode(self):
        """禁用全屏模式 - 恢复原始样式"""
        self.setStyleSheet("")
        
        if self.video_label:
            self.video_label.setStyleSheet("""
                QLabel {
                    background-color: black;
                    border: 1px solid #3498db;
                    border-radius: 3px;
                }
            """)
        
    def resizeEvent(self, event):
        """窗口尺寸变化事件"""
        super().resizeEvent(event)
        # 重置缓存，强制重新缩放
        self.cached_size = None
        self.cached_scaled_image = None
        
    def closeEvent(self, event):
        """关闭事件"""
        self.cleanup()
        event.accept()

# 导出主要类
__all__ = ['OpenCVVideoPlayer']