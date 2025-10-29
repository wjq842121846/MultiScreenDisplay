import sys
import math
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QScrollArea, QApplication,
                             QToolTip, QSizePolicy, QComboBox, QLineEdit,
                             QMessageBox, QInputDialog, QListWidget, QListWidgetItem,
                             QGroupBox, QTextEdit, QSplitter, QTableWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt, QRect, QTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPixmap, QCursor
from ui_styles_complete import PREVIEW_GROUP_STYLE, PREVIEW_WIDGET_STYLE

class ScreenViewWidget(QWidget):
    """单个屏幕的视图组件，模拟真实屏幕"""
    
    clicked = pyqtSignal(int)  # 屏幕被点击信号
    
    def __init__(self, screen_index, screen_info, scale_factor=0.1):
        super().__init__()
        self.screen_index = screen_index
        self.screen_info = screen_info
        self.scale_factor = scale_factor
        self.content_type = "无内容"
        self.content_preview = ""
        self.is_selected = False
        self.is_primary = screen_info.get('is_primary', False)
        
        self.init_ui()
        self.setup_geometry()
        
    def init_ui(self):
        """初始化屏幕视图界面"""
        self.setMouseTracking(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        # 设置工具提示
        tooltip_text = (f"屏幕 {self.screen_index + 1}\\n"
                       f"分辨率: {self.screen_info['width']} x {self.screen_info['height']}\\n"
                       f"位置: ({self.screen_info['x']}, {self.screen_info['y']})\\n"
                       f"主屏幕: {'是' if self.is_primary else '否'}\\n"
                       f"内容: {self.content_type}")
        self.setToolTip(tooltip_text)
        
    def setup_geometry(self):
        """设置屏幕几何尺寸"""
        # 按比例缩放屏幕尺寸
        scaled_width = int(self.screen_info['width'] * self.scale_factor)
        scaled_height = int(self.screen_info['height'] * self.scale_factor)
        
        # 确保最小尺寸
        scaled_width = max(scaled_width, 80)
        scaled_height = max(scaled_height, 60)
        
        self.setFixedSize(scaled_width, scaled_height)
        
    def update_content(self, content_type, content_preview=""):
        """更新屏幕内容信息"""
        self.content_type = content_type
        self.content_preview = content_preview
        
        # 更新工具提示
        tooltip_text = (f"屏幕 {self.screen_index + 1}\\n"
                       f"分辨率: {self.screen_info['width']} x {self.screen_info['height']}\\n"
                       f"位置: ({self.screen_info['x']}, {self.screen_info['y']})\\n"
                       f"主屏幕: {'是' if self.is_primary else '否'}\\n"
                       f"内容: {self.content_type}")
        self.setToolTip(tooltip_text)
        
        self.update()  # 触发重绘
        
    def set_selected(self, selected):
        """设置选中状态"""
        self.is_selected = selected
        self.update()
        
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.screen_index)
        super().mousePressEvent(event)
        
    def paintEvent(self, event):
        """绘制屏幕视图"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 获取绘制区域
        rect = self.rect()
        
        # 根据内容类型选择颜色
        if self.content_type == "文本":
            bg_color = QColor(46, 204, 113, 180)  # 绿色
            border_color = QColor(39, 174, 96)
        elif self.content_type == "图片":
            bg_color = QColor(52, 152, 219, 180)  # 蓝色
            border_color = QColor(41, 128, 185)
        elif self.content_type == "视频":
            bg_color = QColor(231, 76, 60, 180)   # 红色
            border_color = QColor(192, 57, 43)
        elif self.content_type == "网页":
            bg_color = QColor(155, 89, 182, 180)  # 紫色
            border_color = QColor(142, 68, 173)
        else:
            bg_color = QColor(52, 73, 94, 180)    # 灰色
            border_color = QColor(44, 62, 80)
            
        # 如果被选中，使用高亮颜色
        if self.is_selected:
            border_color = QColor(241, 196, 15)  # 金色边框
            painter.setPen(QPen(border_color, 3))
        else:
            painter.setPen(QPen(border_color, 2))
            
        # 绘制屏幕背景
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 6, 6)
        
        # 绘制屏幕编号
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        
        # 屏幕编号文本
        screen_text = str(self.screen_index + 1)
        if self.is_primary:
            screen_text += "★"  # 主屏幕标记
            
        painter.drawText(rect, Qt.AlignCenter, screen_text)
        
        # 绘制内容类型图标
        if self.content_type != "无内容":
            painter.setFont(QFont("Arial", 8))
            content_icon = self.get_content_icon()
            icon_rect = QRect(rect.x() + 2, rect.y() + 2, 16, 16)
            painter.drawText(icon_rect, Qt.AlignCenter, content_icon)
            
        # 绘制分辨率信息（小字体）
        if rect.width() > 100:  # 只在足够大的屏幕上显示
            painter.setFont(QFont("Arial", 7))
            resolution_text = f"{self.screen_info['width']}x{self.screen_info['height']}"
            res_rect = QRect(rect.x(), rect.bottom() - 15, rect.width(), 12)
            painter.drawText(res_rect, Qt.AlignCenter, resolution_text)
            
    def get_content_icon(self):
        """根据内容类型返回图标"""
        icons = {
            "文本": "📝",
            "图片": "🖼️",
            "视频": "🎬",
            "网页": "🌐"
        }
        return icons.get(self.content_type, "")


class ScreenLayoutView(QWidget):
    """屏幕布局视图，模拟Windows显示设置"""
    
    screen_selected = pyqtSignal(int)  # 屏幕选择信号
    
    def __init__(self):
        super().__init__()
        self.screen_widgets = {}
        self.selected_screen = -1
        self.init_ui()
        
    def init_ui(self):
        """初始化布局视图"""
        self.setMinimumSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #2c3e50, stop:1 #34495e);
                border: 2px solid #1abc9c;
                border-radius: 10px;
            }
        """)
        
    def add_screen(self, screen_index, screen_info):
        """添加屏幕到布局视图"""
        # 计算合适的缩放比例
        scale_factor = self.calculate_scale_factor(screen_info)
        
        screen_widget = ScreenViewWidget(screen_index, screen_info, scale_factor)
        screen_widget.clicked.connect(self.on_screen_clicked)
        
        self.screen_widgets[screen_index] = screen_widget
        screen_widget.setParent(self)
        
        self.update_layout()
        
    def calculate_scale_factor(self, screen_info=None):
        """计算屏幕缩放比例"""
        if not self.screen_widgets and not screen_info:
            return 0.1
            
        # 获取所有屏幕的边界
        all_screens = list(self.screen_widgets.values())
        if screen_info and screen_info not in [w.screen_info for w in all_screens]:
            # 临时创建一个屏幕对象来计算边界
            temp_screens = all_screens + [type('obj', (object,), {'screen_info': screen_info})()]
        else:
            temp_screens = all_screens
            
        if not temp_screens:
            return 0.1
            
        # 计算所有屏幕的总边界
        min_x = min([w.screen_info['x'] for w in temp_screens if hasattr(w, 'screen_info')])
        max_x = max([w.screen_info['x'] + w.screen_info['width'] for w in temp_screens if hasattr(w, 'screen_info')])
        min_y = min([w.screen_info['y'] for w in temp_screens if hasattr(w, 'screen_info')])
        max_y = max([w.screen_info['y'] + w.screen_info['height'] for w in temp_screens if hasattr(w, 'screen_info')])
        
        total_width = max_x - min_x
        total_height = max_y - min_y
        
        # 根据视图大小计算缩放比例
        view_width = self.width() - 40  # 留出边距
        view_height = self.height() - 40
        
        scale_x = view_width / total_width if total_width > 0 else 0.1
        scale_y = view_height / total_height if total_height > 0 else 0.1
        
        # 使用较小的缩放比例，确保所有屏幕都能显示
        scale = min(scale_x, scale_y, 0.15)  # 最大缩放比例0.15
        
        return max(scale, 0.05)  # 最小缩放比例0.05
        
    def update_layout(self):
        """更新屏幕布局位置"""
        if not self.screen_widgets:
            return
            
        # 重新计算缩放比例
        scale_factor = self.calculate_scale_factor()
        
        # 获取所有屏幕的边界
        screens_info = [widget.screen_info for widget in self.screen_widgets.values()]
        min_x = min([info['x'] for info in screens_info])
        min_y = min([info['y'] for info in screens_info])
        
        # 计算视图中心点
        view_center_x = self.width() // 2
        view_center_y = self.height() // 2
        
        # 计算缩放后的总布局尺寸
        scaled_screens = []
        for info in screens_info:
            scaled_width = int(info['width'] * scale_factor)
            scaled_height = int(info['height'] * scale_factor)
            scaled_x = int((info['x'] - min_x) * scale_factor)
            scaled_y = int((info['y'] - min_y) * scale_factor)
            scaled_screens.append((scaled_x, scaled_y, scaled_width, scaled_height))
            
        # 计算总布局尺寸
        if scaled_screens:
            layout_width = max([x + w for x, y, w, h in scaled_screens])
            layout_height = max([y + h for x, y, w, h in scaled_screens])
            
            # 计算偏移量，使布局居中
            offset_x = view_center_x - layout_width // 2
            offset_y = view_center_y - layout_height // 2
        else:
            offset_x = offset_y = 0
        
        # 更新每个屏幕小部件的位置和大小
        for screen_index, widget in self.screen_widgets.items():
            info = widget.screen_info
            
            # 重新设置缩放比例
            widget.scale_factor = scale_factor
            widget.setup_geometry()
            
            # 计算位置
            scaled_x = int((info['x'] - min_x) * scale_factor) + offset_x
            scaled_y = int((info['y'] - min_y) * scale_factor) + offset_y
            
            widget.move(scaled_x, scaled_y)
            widget.show()
            
    def update_screen_content(self, screen_index, content_type, content_preview=""):
        """更新屏幕内容"""
        if screen_index in self.screen_widgets:
            self.screen_widgets[screen_index].update_content(content_type, content_preview)
            
            # 如果正在预览，更新预览标签
            if hasattr(self.parent(), 'is_previewing') and self.parent().is_previewing:
                if hasattr(self.parent(), 'update_preview_label'):
                    self.parent().update_preview_label(screen_index, content_type, content_preview)
            
    def on_screen_clicked(self, screen_index):
        """屏幕点击处理"""
        # 更新选中状态
        for idx, widget in self.screen_widgets.items():
            widget.set_selected(idx == screen_index)
            
        self.selected_screen = screen_index
        self.screen_selected.emit(screen_index)
        
    def clear_screens(self):
        """清空所有屏幕"""
        for widget in self.screen_widgets.values():
            widget.setParent(None)
        self.screen_widgets.clear()
        self.selected_screen = -1
        
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        # 延迟更新布局，避免频繁计算
        QTimer.singleShot(100, self.update_layout)


class ViewConfigManager(QWidget):
    """视图配置管理器 - 支持保存和加载多屏幕配置"""
    
    # 添加信号
    apply_config_requested = pyqtSignal(dict)  # 请求应用配置
    
    def __init__(self):
        super().__init__()
        self.screen_layout_view = ScreenLayoutView()
        self.current_configs = {}  # 当前屏幕配置
        self.config_dir = "view_configs"  # 配置文件目录
        self.ensure_config_dir()
        self.init_ui()
        
    def ensure_config_dir(self):
        """确保配置目录存在"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
    def init_ui(self):
        """初始化界面 - 修改为上下两部分：上部为水平布局（屏幕预览+控制配置），下部为配置中心"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距
        layout.setSpacing(1)  # 减小间距
        
        # 上部分：屏幕布局预览和屏幕控制配置 - 水平布局
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(1)  # 减小间距
        
        # 左侧：屏幕布局预览
        display_widget = QWidget()
        display_layout = QVBoxLayout(display_widget)
        display_layout.setContentsMargins(0, 0, 0, 0)
        self.create_screen_display_section(display_layout)
        top_layout.addWidget(display_widget, 1)  # stretch=1
        
        # 右侧：屏幕控制与配置
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 0, 0, 0)
        self.create_config_details_section(details_layout)
        top_layout.addWidget(details_widget, 2)  # stretch=2，占更大空间
        
        layout.addWidget(top_widget, 2)  # stretch=2，上部分占主要空间
        
        # 下部分：配置中心列表
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        self.create_config_center_section(center_layout)
        layout.addWidget(center_widget, 1)  # stretch=1，下部分占较小空间
        
        # 连接信号
        self.screen_layout_view.screen_selected.connect(self.on_screen_selected)
        
    def create_screen_display_section(self, parent_layout):
        """创建屏幕位置显示区域（上部分）"""
        display_group = QGroupBox("🖥️ 屏幕布局预览")
        display_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(52, 152, 219, 0.15),
                                          stop:1 rgba(52, 152, 219, 0.05));
                color: #ecf0f1;
                /* 移除固定高度，使用弹性布局 */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 5px 12px 5px 12px;
                background: #3498db;
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }
        """)
        
        display_layout = QVBoxLayout(display_group)
        display_layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        
        # 操作提示
        tip_label = QLabel("💡 点击屏幕可选择要编辑的显示器，预览模式下可查看配置效果")
        tip_label.setStyleSheet("""
            QLabel {
                color: #7fb3d3;
                font-size: 12px;
                font-weight: normal;
                background: rgba(127, 179, 211, 0.1);
                border-radius: 6px;
                padding: 8px;
                margin: 5px;
            }
        """)
        display_layout.addWidget(tip_label)
        
        # 屏幕布局视图
        display_layout.addWidget(self.screen_layout_view)
        
        parent_layout.addWidget(display_group)
        
    def create_config_details_section(self, parent_layout):
        """创建屏幕控制和配置详情区域（集成屏幕控制功能）"""
        details_group = QGroupBox("🖥️ 屏幕控制与配置")
        details_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #000000;
                background: #ffffff;
                border: 1px solid #87ceeb;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                /* 移除固定高度，自适应内容 */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 5px 12px 5px 12px;
                background: #87ceeb;
                border-radius: 6px;
                color: #000000;
                font-size: 14px;
            }
        """)
        
        details_layout = QVBoxLayout(details_group)
        details_layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        
        # 创建滚动区域来容纳多个屏幕配置
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #87ceeb;
                border-radius: 6px;
                background: #ffffff;
            }
        """)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(True)
        
        # 屏幕配置容器 - 改为水平布局以支持4个屏幕横向排列
        self.config_container = QWidget()
        self.config_container.setStyleSheet("background: transparent;")
        self.config_layout = QHBoxLayout(self.config_container)
        self.config_layout.setSpacing(1)  # 减小间距为1px
        self.config_layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        
        scroll_area.setWidget(self.config_container)
        details_layout.addWidget(scroll_area)
        
        parent_layout.addWidget(details_group)
        
    def create_config_center_section(self, parent_layout):
        """创建配置中心列表（下部分）"""
        center_group = QGroupBox("🎮 配置中心")
        center_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #e67e22;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 rgba(230, 126, 34, 0.15),
                                          stop:1 rgba(230, 126, 34, 0.05));
                color: #ecf0f1;
                /* 移除固定高度，自适应内容 */
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
        
        center_layout = QVBoxLayout(center_group)
        center_layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        center_layout.setSpacing(1)  # 减小间距为1px
        
        # 配置操作区域
        self.create_config_operations(center_layout)
        
        # 配置列表表格
        self.create_config_table(center_layout)
        
        parent_layout.addWidget(center_group)
        
    def create_config_operations(self, parent_layout):
        """创建配置操作区域"""
        operations_layout = QHBoxLayout()
        operations_layout.setSpacing(1)  # 减小间距为1px
        
        # 保存配置按钮
        save_config_btn = QPushButton("💾 保存配置")
        save_config_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #229954;
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:pressed {
                background: #1e8449;
            }
        """)
        save_config_btn.clicked.connect(self.save_current_config)
        
        # 预览配置按钮
        self.preview_config_btn = QPushButton("👁️ 预览配置")
        self.preview_config_btn.setStyleSheet("""
            QPushButton {
                background: #f39c12;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #d68910;
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:pressed {
                background: #ca6f1e;
            }
        """)
        self.preview_config_btn.clicked.connect(self.toggle_preview)
        
        # 取消预览按钮
        self.cancel_preview_btn = QPushButton("❌ 取消预览")
        self.cancel_preview_btn.setStyleSheet("""
            QPushButton {
                background: #e67e22;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #d35400;
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:pressed {
                background: #a04000;
            }
        """)
        self.cancel_preview_btn.clicked.connect(self.cancel_preview)
        self.cancel_preview_btn.hide()  # 初始隐藏
        
        # 预览状态标志
        self.is_previewing = False
        self.original_screen_content = {}
        
        # 应用配置按钮
        apply_config_btn = QPushButton("✅ 应用配置")
        apply_config_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #2980b9;
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:pressed {
                background: #21618c;
            }
        """)
        apply_config_btn.clicked.connect(self.apply_selected_config)
        
        # 删除配置按钮
        delete_config_btn = QPushButton("🗑️ 删除配置")
        delete_config_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #c0392b;
                border: 1px solid rgba(255,255,255,0.3);
            }
            QPushButton:pressed {
                background: #a93226;
            }
        """)
        delete_config_btn.clicked.connect(self.delete_selected_config)
        
        operations_layout.addWidget(save_config_btn)
        operations_layout.addWidget(self.preview_config_btn)
        operations_layout.addWidget(self.cancel_preview_btn)
        operations_layout.addWidget(apply_config_btn)
        operations_layout.addWidget(delete_config_btn)
        operations_layout.addStretch()
        
        parent_layout.addLayout(operations_layout)
        
    def create_config_table(self, parent_layout):
        """创建配置列表表格"""
        from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
        
        # 创建表格 - 改为6列：配置名、描述、屏幕1-4
        self.config_table = QTableWidget()
        self.config_table.setColumnCount(6)  # 配置名、描述、屏幕1、屏幕2、屏幕3、屏幕4
        self.config_table.setHorizontalHeaderLabels([
            "配置名称", "描述", "屏幕1", "屏幕2", "屏幕3", "屏幕4"
        ])
        
        self.config_table.setStyleSheet("""
            QTableWidget {
                background: rgba(44, 62, 80, 0.3);
                border: 1px solid #34495e;
                border-radius: 6px;
                gridline-color: #34495e;
                color: #ecf0f1;
                selection-background-color: #3498db;
                alternate-background-color: rgba(52, 73, 94, 0.3);
                font-size: 11px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #34495e;
            }
            QTableWidget::item:selected {
                background: #3498db;
                color: white;
            }
            QTableWidget::horizontalHeader {
                background: rgba(52, 152, 219, 0.8);
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QTableWidget::horizontalHeader::section {
                background: rgba(52, 152, 219, 0.8);
                border-right: 1px solid #2980b9;
                padding: 8px;
                font-weight: bold;
            }
            QTableWidget::verticalHeader {
                background: rgba(52, 73, 94, 0.5);
                color: #ecf0f1;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(52, 73, 94, 0.3);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #e67e22;
                border-radius: 4px;
                /* 移除固定高度，自适应内容 */
            }
        """)
        
        # 设置表格属性
        self.config_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.config_table.setAlternatingRowColors(True)
        self.config_table.horizontalHeader().setStretchLastSection(True)
        self.config_table.verticalHeader().setVisible(False)
        
        # 设置等分列宽
        header = self.config_table.horizontalHeader()
        # 配置名称和描述列稍宽，屏幕列等分
        header.resizeSection(0, 150)  # 配置名称
        header.resizeSection(1, 200)  # 描述
        # 屏幕列等分剩余空间
        for i in range(2, 6):  # 屏幕1-4列
            header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        # 双击应用配置
        self.config_table.itemDoubleClicked.connect(self.apply_config_from_table)
        
        parent_layout.addWidget(self.config_table)
        
        # 刷新配置列表
        self.refresh_config_table()
        
    def create_screen_config_widget(self, screen_index, screen_info):
        """为每个屏幕创建完整的控制配置小部件"""
        screen_widget = QWidget()
        screen_widget.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border: 1px solid #87ceeb;
                border-radius: 8px;
                padding: 8px;
                margin: 3px;
                /* 移除固定尺寸，使用弹性布局自适应 */
                flex: 1;
            }
        """)
        
        layout = QVBoxLayout(screen_widget)
        layout.setSpacing(1)  # 减小间距为1px
        layout.setContentsMargins(1, 1, 1, 1)  # 减小外边距为1px
        
        # 屏幕标题和信息
        header_layout = QHBoxLayout()
        
        # 屏幕标题
        primary_text = " (主屏幕)" if screen_info.get('is_primary', False) else ""
        title_label = QLabel(f"🖥️ 屏幕 {screen_index + 1}{primary_text}")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #000000;
                background: transparent;
                padding: 2px;
            }
        """)
        
        # 分辨率和位置信息
        info_label = QLabel(f"{screen_info['width']}×{screen_info['height']} 位置({screen_info['x']},{screen_info['y']})")
        info_label.setStyleSheet("""
            QLabel {
                font-size: 9px;
                color: #4169e1;
                background: transparent;
                padding: 0px;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(info_label)
        layout.addLayout(header_layout)
        
        # 内容类型选择
        type_layout = QHBoxLayout()
        content_type_label = QLabel("类型:")
        content_type_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #000000;
                background: transparent;
                font-weight: 500;
                /* 移除固定宽度，自适应内容 */
            }
        """)
        
        content_type_combo = QComboBox()
        content_type_combo.setStyleSheet("""
            QComboBox {
                background: #ffffff;
                color: #000000;
                border: 1px solid #87ceeb;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 10px;
                font-weight: 400;
                /* 移除固定高度，自适应内容 */
            }
            QComboBox:hover {
                border-color: #4169e1;
                background: #f0f8ff;
            }
            QComboBox:focus {
                border-color: #4169e1;
                outline: none;
            }
        """)
        content_type_combo.addItems(["无内容", "文本", "图片", "视频", "网页"])
        
        type_layout.addWidget(content_type_label)
        type_layout.addWidget(content_type_combo, 1)
        layout.addLayout(type_layout)
        
        # 内容输入区域
        content_label = QLabel("内容:")
        content_label.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #000000;
                background: transparent;
                font-weight: 500;
            }
        """)
        layout.addWidget(content_label)
        
        # 内容输入和文件选择
        input_layout = QHBoxLayout()
        
        content_input = QLineEdit()
        content_input.setPlaceholderText("请输入内容或选择文件...")
        content_input.setStyleSheet("""
            QLineEdit {
                background: #ffffff;
                color: #000000;
                border: 1px solid #87ceeb;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 10px;
                font-weight: 400;
                /* 移除固定高度，自适应内容 */
            }
            QLineEdit:focus {
                border-color: #4169e1;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #4169e1;
            }
        """)
        
        # 文件选择按钮
        file_select_btn = QPushButton("📁")
        file_select_btn.setToolTip("选择文件")
        file_select_btn.setStyleSheet("""
            QPushButton {
                background: #ffffff;
                color: #000000;
                border: 1px solid #87ceeb;
                border-radius: 3px;
                padding: 2px 4px;
                font-size: 10px;
                font-weight: 500;
                /* 移除固定宽度，但保持紧凑样式 */
                width: 1.5em;
                /* 移除固定高度，自适应内容 */
            }
            QPushButton:hover {
                background: #f0f8ff;
                border-color: #4169e1;
            }
            QPushButton:pressed {
                background: #e6f3ff;
            }
        """)
        file_select_btn.clicked.connect(lambda: self.select_file_for_screen(content_input))
        
        input_layout.addWidget(content_input, 2)
        input_layout.addWidget(file_select_btn)
        layout.addLayout(input_layout)
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        
        # 应用到屏幕按钮
        apply_btn = QPushButton("✅ 应用")
        apply_btn.setStyleSheet("""
            QPushButton {
                background: #f0f8ff;
                color: #000000;
                border: 1px solid #4169e1;
                border-radius: 3px;
                padding: 3px 8px;
                font-size: 10px;
                font-weight: 600;
                /* 移除固定宽度，自适应内容 */
                /* 移除固定高度，自适应内容 */
            }
            QPushButton:hover {
                background: #e6f3ff;
                border-color: #4169e1;
            }
            QPushButton:pressed {
                background: #ddeeff;
            }
        """)
        apply_btn.clicked.connect(lambda: self.apply_screen_content(screen_index, content_type_combo.currentText(), content_input.text()))
        
        button_layout.addWidget(apply_btn)
        layout.addLayout(button_layout)
        
        # 保存组件引用
        screen_widget.content_type_combo = content_type_combo
        screen_widget.content_input = content_input
        screen_widget.screen_index = screen_index
        screen_widget.screen_info = screen_info
        
        return screen_widget
        
    def apply_screen_content(self, screen_index, content_type, content):
        """应用内容到指定屏幕"""
        # 使用主控制器来应用内容
        if hasattr(self, 'main_controller') and self.main_controller:
            self.main_controller.apply_content(screen_index, content_type, content)
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "成功", f"✅ 屏幕 {screen_index + 1} 内容已应用：{content_type}")
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "错误", "无法连接到主控制器")
        
        # 更新屏幕布局视图
        self.screen_layout_view.update_screen_content(screen_index, content_type, content)
        
    def select_file_for_screen(self, line_edit):
        """为屏幕配置选择文件"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文件", "", 
            "所有文件 (*.*);;图片文件 (*.png *.jpg *.jpeg *.gif *.bmp);;视频文件 (*.mp4 *.avi *.mov *.wmv *.mkv)"
        )
        if file_path:
            line_edit.setText(file_path)
        
    def refresh_config_table(self):
        """刷新配置表格"""
        if not hasattr(self, 'config_table'):
            return
            
        # 获取所有配置文件
        configs = []
        if os.path.exists(self.config_dir):
            config_files = [f for f in os.listdir(self.config_dir) if f.endswith('.json') and not f.startswith('_')]
            for config_file in sorted(config_files):
                try:
                    config_path = os.path.join(self.config_dir, config_file)
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = json.load(f)
                    
                    configs.append({
                        'name': config_data.get('name', os.path.splitext(config_file)[0]),
                        'description': config_data.get('description', ''),
                        'screens': config_data.get('screens', {}),
                        'path': config_path
                    })
                except Exception as e:
                    print(f"读取配置文件 {config_file} 失败: {e}")
        
        # 设置表格行数
        self.config_table.setRowCount(len(configs))
        
        # 填充表格数据
        for row, config in enumerate(configs):
            # 配置名称
            name_item = QTableWidgetItem(config['name'])
            name_item.setData(Qt.UserRole, config['path'])  # 存储路径
            self.config_table.setItem(row, 0, name_item)
            
            # 描述
            desc_text = config['description'][:40] + '...' if len(config['description']) > 40 else config['description']
            desc_item = QTableWidgetItem(desc_text)
            self.config_table.setItem(row, 1, desc_item)
            
            # 屏幕配置（只显示前4个屏幕）
            for screen_col in range(2, 6):  # 屏幕1-4列
                screen_index = screen_col - 2  # 屏幕索引 0-3
                screen_key = str(screen_index)
                
                if screen_key in config['screens']:
                    screen_config = config['screens'][screen_key]
                    content_type = screen_config.get('content_type', '无')
                    screen_item = QTableWidgetItem(content_type)
                    
                    # 根据内容类型设置颜色
                    if content_type == "文本":
                        screen_item.setBackground(QColor(46, 204, 113, 100))
                    elif content_type == "图片":
                        screen_item.setBackground(QColor(52, 152, 219, 100))
                    elif content_type == "视频":
                        screen_item.setBackground(QColor(231, 76, 60, 100))
                    elif content_type == "网页":
                        screen_item.setBackground(QColor(155, 89, 182, 100))
                else:
                    screen_item = QTableWidgetItem("无")
                    screen_item.setBackground(QColor(52, 73, 94, 50))
                
                screen_item.setTextAlignment(Qt.AlignCenter)
                self.config_table.setItem(row, screen_col, screen_item)
        
    # =============================================================================
    # 新功能方法
    # =============================================================================
    
    def create_new_config(self):
        """创建新配置"""
        # 清空中间部分的配置详情
        self.clear_config_details()
        # 重新生成屏幕配置组件
        self.refresh_config_details()
        QMessageBox.information(self, "提示", "已创建新配置，请在中间区域设置各屏幕内容，然后保存")
        
    def clear_config_details(self):
        """清空配置详情区域"""
        if hasattr(self, 'config_layout'):
            for i in reversed(range(self.config_layout.count())):
                child = self.config_layout.itemAt(i).widget()
                if child:
                    child.setParent(None)
    
    def refresh_config_details(self):
        """刷新配置详情区域"""
        self.clear_config_details()
        
        # 为前4个屏幕创建配置组件
        screen_widgets = {}
        available_screens = self.get_available_screens()
        max_screens = min(4, len(available_screens))  # 最多显示4个屏幕
        
        for screen_index in range(max_screens):
            if screen_index < len(available_screens):
                screen_info = available_screens[screen_index]
                screen_widget = self.create_screen_config_widget(screen_index, screen_info)
                screen_widgets[screen_index] = screen_widget
                self.config_layout.addWidget(screen_widget)
        
        # 保存屏幕组件引用
        self.screen_config_widgets = screen_widgets
        
        # 添加弹性空间
        self.config_layout.addStretch()
    
    def get_available_screens(self):
        """获取可用屏幕信息"""
        # 从屏幕布局视图获取屏幕信息
        screens = []
        for screen_index, widget in self.screen_layout_view.screen_widgets.items():
            screens.append(widget.screen_info)
        return screens
    
    def toggle_preview(self):
        """切换预览状态"""
        if self.is_previewing:
            self.cancel_preview()
        else:
            self.start_preview()
    
    def start_preview(self):
        """开始预览配置"""
        current_row = self.config_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个配置！")
            return
            
        # 获取配置路径
        name_item = self.config_table.item(current_row, 0)
        config_path = name_item.data(Qt.UserRole)
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            screens_config = config_data.get('screens', {})
            config_name = config_data.get('name', '未命名')
            
            if not screens_config:
                QMessageBox.warning(self, "警告", "该配置没有屏幕设置！")
                return
            
            # 保存当前屏幕内容状态，以便取消预览时恢复
            self.save_current_screen_state()
            
            # 在屏幕布局视图中预览配置（限制前4个屏幕）
            for screen_index_str, config in screens_config.items():
                screen_index = int(screen_index_str)
                if screen_index >= 4:  # 只处理前4个屏幕
                    continue
                    
                content_type = config.get('content_type', '无内容')
                content = config.get('content', '')
                
                # 更新屏幕布局视图
                self.screen_layout_view.update_screen_content(screen_index, content_type)
                
                # 创建实际的预览内容窗口
                self.create_preview_window(screen_index, content_type, content)
            
            # 在配置详情区域显示配置
            self.load_config_to_details(screens_config)
            
            # 更新预览状态
            self.is_previewing = True
            self.preview_config_btn.setText("🔄 预览中...")
            self.preview_config_btn.setEnabled(False)
            self.cancel_preview_btn.show()
            
            QMessageBox.information(self, "预览", f"正在预览配置：{config_name}\n点击'取消预览'可恢复原状态")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"预览配置失败：{str(e)}")
    
    def cancel_preview(self):
        """取消预览，恢复原始状态"""
        if not self.is_previewing:
            return
            
        # 清理预览窗口
        self.cleanup_preview_windows()
        
        # 恢复原始屏幕状态
        self.restore_original_screen_state()
        
        # 重置预览状态
        self.is_previewing = False
        self.preview_config_btn.setText("👁️ 预览配置")
        self.preview_config_btn.setEnabled(True)
        self.cancel_preview_btn.hide()
        self.original_screen_content = {}
        
        QMessageBox.information(self, "取消预览", "已恢复到预览前的状态")
    
    def save_current_screen_state(self):
        """保存当前屏幕状态"""
        self.original_screen_content = {}
        
        # 保存屏幕布局视图的当前状态
        for screen_index, widget in self.screen_layout_view.screen_widgets.items():
            self.original_screen_content[screen_index] = {
                'content_type': widget.content_type,
                'content_preview': widget.content_preview
            }
    
    def restore_original_screen_state(self):
        """恢复原始屏幕状态"""
        for screen_index, original_state in self.original_screen_content.items():
            if screen_index in self.screen_layout_view.screen_widgets:
                content_type = original_state.get('content_type', '无内容')
                content_preview = original_state.get('content_preview', '')
                self.screen_layout_view.update_screen_content(screen_index, content_type, content_preview)
    
    def create_preview_window(self, screen_index, content_type, content):
        """创建预览内容窗口"""
        # 检查屏幕布局视图中对应的屏幕位置
        if screen_index in self.screen_layout_view.screen_widgets:
            screen_widget = self.screen_layout_view.screen_widgets[screen_index]
            
            # 创建一个简单的预览标签覆盖在屏幕小部件上
            preview_label = QLabel(screen_widget)
            preview_label.setAlignment(Qt.AlignCenter)
            preview_label.setStyleSheet("""
                QLabel {
                    background: rgba(0, 0, 0, 150);
                    color: white;
                    font-size: 10px;
                    font-weight: bold;
                    border-radius: 3px;
                    padding: 2px;
                }
            """)
            
            # 根据内容类型设置预览文本
            if content_type == "文本":
                preview_text = f"📝 {content[:10]}..." if len(content) > 10 else f"📝 {content}"
            elif content_type == "图片":
                preview_text = f"🖼️ 图片\n{os.path.basename(content) if content else '无文件'}"
            elif content_type == "视频":
                preview_text = f"🎬 视频\n{os.path.basename(content) if content else '无文件'}"
            elif content_type == "网页":
                preview_text = f"🌐 网页\n{content[:15]}..." if len(content) > 15 else f"🌐 {content}"
            else:
                preview_text = "⭕ 无内容"
            
            preview_label.setText(preview_text)
            preview_label.resize(screen_widget.size())
            preview_label.show()
            
            # 保存预览标签的引用，以便清理
            if not hasattr(self, 'preview_labels'):
                self.preview_labels = {}
            self.preview_labels[screen_index] = preview_label
    
    def cleanup_preview_windows(self):
        """清理预览窗口"""
        if hasattr(self, 'preview_labels'):
            for screen_index, label in self.preview_labels.items():
                if label:
                    label.setParent(None)
            self.preview_labels = {}
    
    def preview_selected_config(self):
        """预览选中的配置 - 保持向后兼容"""
        self.start_preview()
    
    def load_config_to_details(self, screens_config):
        """将配置加载到详情区域"""
        if not hasattr(self, 'screen_config_widgets'):
            return
            
        # 更新各屏幕的配置
        for screen_index, widget in self.screen_config_widgets.items():
            screen_key = str(screen_index)
            if screen_key in screens_config:
                config = screens_config[screen_key]
                content_type = config.get('content_type', '无内容')
                content = config.get('content', '')
                
                # 设置内容类型
                combo = widget.content_type_combo
                index = combo.findText(content_type)
                if index >= 0:
                    combo.setCurrentIndex(index)
                
                # 设置内容
                widget.content_input.setText(content)
            else:
                # 重置为默认值
                widget.content_type_combo.setCurrentIndex(0)  # 无内容
                widget.content_input.clear()
    
    def apply_config_from_table(self, item):
        """从表格双击应用配置"""
        if item.column() == 0:  # 只有点击配置名称列才应用
            self.apply_selected_config()
    
    def collect_config_from_details(self):
        """从详情区域收集配置（最多4个屏幕）"""
        if not hasattr(self, 'screen_config_widgets'):
            return {}
            
        config = {}
        available_screens = self.get_available_screens()
        
        # 只处理前4个屏幕
        for screen_index, widget in self.screen_config_widgets.items():
            if screen_index >= 4:  # 限制只处理前4个屏幕
                continue
                
            content_type = widget.content_type_combo.currentText()
            content = widget.content_input.text().strip()
            
            if content_type != "无内容" and content:
                # 获取屏幕信息并转换为可序列化的格式
                screen_info = {}
                if screen_index < len(available_screens):
                    original_info = available_screens[screen_index]
                    screen_info = {
                        'width': original_info.get('width', 0),
                        'height': original_info.get('height', 0),
                        'x': original_info.get('x', 0),
                        'y': original_info.get('y', 0),
                        'is_primary': original_info.get('is_primary', False)
                    }
                
                config[str(screen_index)] = {
                    'content_type': content_type,
                    'content': content,
                    'screen_info': screen_info
                }
        
        return config
        
    def create_save_config_section(self, parent_layout):
        """创建保存配置区域"""
        group = QGroupBox("💾 保存当前配置")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 配置名称输入
        name_layout = QHBoxLayout()
        name_label = QLabel("配置名称:")
        name_label.setStyleSheet("color: #bdc3c7; font-weight: normal;")
        self.config_name_input = QLineEdit()
        self.config_name_input.setPlaceholderText("输入配置名称，如：工作模式、娱乐模式...")
        self.config_name_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #34495e;
                border-radius: 3px;
                background: #2c3e50;
                color: #ecf0f1;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.config_name_input)
        layout.addLayout(name_layout)
        
        # 配置描述
        desc_label = QLabel("配置描述:")
        desc_label.setStyleSheet("color: #bdc3c7; font-weight: normal;")
        self.config_desc_input = QTextEdit()
        self.config_desc_input.setPlaceholderText("可选：输入配置的详细描述...")
        self.config_desc_input.setMaximumHeight(60)
        self.config_desc_input.setStyleSheet("""
            QTextEdit {
                padding: 5px;
                border: 1px solid #34495e;
                border-radius: 3px;
                background: #2c3e50;
                color: #ecf0f1;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(desc_label)
        layout.addWidget(self.config_desc_input)
        
        # 保存按钮
        save_btn = QPushButton("💾 保存当前配置")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #27ae60;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2ecc71;
            }
            QPushButton:pressed {
                background: #229954;
            }
        """)
        save_btn.clicked.connect(self.save_current_config)
        layout.addWidget(save_btn)
        
        parent_layout.addWidget(group)
        
    def create_saved_configs_section(self, parent_layout):
        """创建已保存配置列表区域"""
        group = QGroupBox("📋 已保存的配置")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #9b59b6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 配置列表
        self.config_list = QListWidget()
        self.config_list.setStyleSheet("""
            QListWidget {
                background: #2c3e50;
                border: 1px solid #34495e;
                border-radius: 3px;
                color: #ecf0f1;
                selection-background-color: #3498db;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:hover {
                background: #34495e;
            }
            QListWidget::item:selected {
                background: #3498db;
            }
        """)
        self.config_list.itemDoubleClicked.connect(self.on_config_double_clicked)
        layout.addWidget(self.config_list)
        
        # 刷新配置列表
        self.refresh_config_table()
        
        parent_layout.addWidget(group)
        
    def create_action_buttons_section(self, parent_layout):
        """创建操作按钮区域"""
        group = QGroupBox("🎮 操作")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e74c3c;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # 第一行按钮
        row1_layout = QHBoxLayout()
        
        apply_btn = QPushButton("✅ 应用选中配置")
        apply_btn.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #2980b9;
            }
        """)
        apply_btn.clicked.connect(self.apply_selected_config)
        
        delete_btn = QPushButton("🗑️ 删除配置")
        delete_btn.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_config)
        
        row1_layout.addWidget(apply_btn)
        row1_layout.addWidget(delete_btn)
        layout.addLayout(row1_layout)
        
        # 第二行按钮
        row2_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新列表")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #95a5a6;
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #7f8c8d;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_config_table)
        
        export_btn = QPushButton("📤 导出配置")
        export_btn.setStyleSheet("""
            QPushButton {
                background: #f39c12;
                color: white;
                border: none;
                padding: 6px 10px;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #d68910;
            }
        """)
        export_btn.clicked.connect(self.export_config)
        
        row2_layout.addWidget(refresh_btn)
        row2_layout.addWidget(export_btn)
        layout.addLayout(row2_layout)
        
        parent_layout.addWidget(group)
        
    # =============================================================================
    # 配置管理核心功能
    # =============================================================================
    
    def save_current_config(self):
        """保存当前配置 - 从详情区域收集"""
        config_name, ok = QInputDialog.getText(
            self, "保存配置", "请输入配置名称:",
            text=f"配置_{datetime.now().strftime('%m%d_%H%M')}"
        )
        
        if not ok or not config_name.strip():
            return
            
        config_name = config_name.strip()
        
        # 从详情区域收集配置
        screens_config = self.collect_config_from_details()
        
        if not screens_config:
            QMessageBox.information(self, "提示", "当前没有配置的屏幕内容！")
            return
        
        # 检查配置是否已存在
        config_file = os.path.join(self.config_dir, f"{config_name}.json")
        if os.path.exists(config_file):
            reply = QMessageBox.question(
                self, "确认覆盖", 
                f"配置 '{config_name}' 已存在，是否覆盖？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # 收集配置数据
        config_data = {
            "name": config_name,
            "description": f"保存于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "created_time": datetime.now().isoformat(),
            "screens": screens_config
        }
        
        # 保存到文件
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            screen_count = len(screens_config)
            QMessageBox.information(self, "成功", f"配置 '{config_name}' 已保存！\n包含 {screen_count} 个屏幕设置")
            
            # 刷新配置表格
            self.refresh_config_table()
            
            # 更新当前配置
            self.current_configs = screens_config.copy()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存配置失败：{str(e)}")
    
    def refresh_config_list(self):
        """刷新配置列表"""
        if hasattr(self, 'config_list'):
            self.config_list.clear()
        
        if not os.path.exists(self.config_dir):
            return
            
        # 获取所有配置文件
        config_files = [f for f in os.listdir(self.config_dir) if f.endswith('.json')]
        config_files.sort()
        
        for config_file in config_files:
            try:
                config_path = os.path.join(self.config_dir, config_file)
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                # 创建列表项
                config_name = config_data.get('name', os.path.splitext(config_file)[0])
                created_time = config_data.get('created_time', '')
                description = config_data.get('description', '')
                screen_count = len(config_data.get('screens', {}))
                
                # 格式化显示文本
                if created_time:
                    try:
                        dt = datetime.fromisoformat(created_time)
                        time_str = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        time_str = created_time[:16]
                else:
                    time_str = "未知时间"
                
                display_text = f"📝 {config_name}\n"
                display_text += f"🕒 {time_str} | 🖥️ {screen_count}个屏幕"
                if description:
                    display_text += f"\n💭 {description[:50]}{'...' if len(description) > 50 else ''}"
                
                if hasattr(self, 'config_list'):
                    item = QListWidgetItem(display_text)
                    item.setData(Qt.UserRole, config_path)  # 存储文件路径
                    self.config_list.addItem(item)
                
            except Exception as e:
                print(f"加载配置文件 {config_file} 失败: {e}")
    
    def apply_selected_config(self):
        """应用选中的配置"""
        current_row = self.config_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个配置！")
            return
            
        # 获取配置路径
        name_item = self.config_table.item(current_row, 0)
        config_path = name_item.data(Qt.UserRole)
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            screens_config = config_data.get('screens', {})
            config_name = config_data.get('name', '未命名')
            
            if not screens_config:
                QMessageBox.warning(self, "警告", "该配置没有屏幕设置！")
                return
            
            # 发送应用配置信号到主控制器
            self.apply_config_requested.emit(screens_config)
            
            # 更新当前配置显示
            for screen_index_str, config in screens_config.items():
                screen_index = int(screen_index_str)
                content_type = config.get('content_type', '无内容')
                self.screen_layout_view.update_screen_content(screen_index, content_type)
            
            # 加载到详情区域
            self.load_config_to_details(screens_config)
            
            QMessageBox.information(self, "成功", f"配置 '{config_name}' 已应用！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"应用配置失败：{str(e)}")
    
    def delete_selected_config(self):
        """删除选中的配置"""
        current_row = self.config_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个配置！")
            return
            
        # 获取配置路径和名称
        name_item = self.config_table.item(current_row, 0)
        if not name_item:
            QMessageBox.warning(self, "警告", "无法获取配置信息！")
            return
            
        config_path = name_item.data(Qt.UserRole)
        config_name = name_item.text()
        
        if not config_path:
            QMessageBox.warning(self, "警告", "无法获取配置文件路径！")
            return
            
        if not os.path.exists(config_path):
            QMessageBox.warning(self, "警告", f"配置文件不存在：{config_path}")
            self.refresh_config_table()  # 刷新列表移除无效项
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除配置 '{config_name}' 吗？\n此操作无法撤销！",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(config_path)
                QMessageBox.information(self, "成功", f"配置 '{config_name}' 已删除！")
                self.refresh_config_table()
            except FileNotFoundError:
                QMessageBox.warning(self, "警告", f"文件不存在：{config_path}")
                self.refresh_config_table()
            except PermissionError:
                QMessageBox.critical(self, "错误", f"权限不足，无法删除文件：{config_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除配置失败：{str(e)}\n路径：{config_path}")
    
    def export_config(self):
        """导出配置（复制到剪贴板）"""
        current_row = self.config_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "警告", "请先选择一个配置！")
            return
            
        # 获取配置路径
        name_item = self.config_table.item(current_row, 0)
        config_path = name_item.data(Qt.UserRole)
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()
            
            clipboard = QApplication.clipboard()
            clipboard.setText(config_content)
            
            QMessageBox.information(self, "成功", "配置已复制到剪贴板！\n可以分享给其他用户。")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出配置失败：{str(e)}")
    
    def on_config_double_clicked(self, item):
        """双击配置项时应用配置"""
        self.apply_selected_config()
    
    # =============================================================================
    # 原有功能保持兼容
    # =============================================================================
        
    def create_legend(self, parent_layout):
        """创建颜色图例"""
        legend_frame = QFrame()
        legend_frame.setStyleSheet("""
            QFrame {
                background: rgba(52, 73, 94, 100);
                border: 1px solid #34495e;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        legend_frame.setMaximumHeight(60)
        
        legend_layout = QHBoxLayout(legend_frame)
        legend_layout.setSpacing(15)
        
        # 图例项目
        legends = [
            ("📝 文本", "#2ecc71"),
            ("🖼️ 图片", "#3498db"), 
            ("🎬 视频", "#e74c3c"),
            ("🌐 网页", "#9b59b6"),
            ("⭕ 无内容", "#34495e")
        ]
        
        for text, color in legends:
            legend_item = QLabel(text)
            legend_item.setStyleSheet(f"""
                QLabel {{
                    color: white;
                    background-color: {color};
                    border-radius: 3px;
                    padding: 3px 8px;
                    font-size: 11px;
                    font-weight: bold;
                }}
            """)
            legend_layout.addWidget(legend_item)
            
        legend_layout.addStretch()
        parent_layout.addWidget(legend_frame)
        
    def add_screen(self, screen_index, screen_info):
        """添加屏幕"""
        self.screen_layout_view.add_screen(screen_index, screen_info)
        # 初始化屏幕配置
        if str(screen_index) not in self.current_configs:
            # 确保 screen_info 是可序列化的
            serializable_info = {
                'width': screen_info.get('width', 0),
                'height': screen_info.get('height', 0),
                'x': screen_info.get('x', 0),
                'y': screen_info.get('y', 0),
                'is_primary': screen_info.get('is_primary', False)
            }
            self.current_configs[str(screen_index)] = {
                'content_type': '无内容',
                'content': '',
                'screen_info': serializable_info
            }
        
        # 刷新配置详情区域
        QTimer.singleShot(100, self.refresh_config_details)
        
    def update_screen_content(self, screen_index, content_type, content=""):
        """更新屏幕内容"""
        self.screen_layout_view.update_screen_content(screen_index, content_type, content)
        # 更新当前配置
        self.current_configs[str(screen_index)] = {
            'content_type': content_type,
            'content': content,
            'screen_info': self.current_configs.get(str(screen_index), {}).get('screen_info', {})
        }
        
    def clear_screens(self):
        """清空屏幕"""
        self.screen_layout_view.clear_screens()
        self.current_configs.clear()
        
    def on_screen_selected(self, screen_index):
        """屏幕选择事件处理"""
        print(f"选中屏幕: {screen_index + 1}")
        
    def get_selected_screen(self):
        """获取当前选中的屏幕"""
        return self.screen_layout_view.selected_screen
        
    def get_current_config(self):
        """获取当前配置"""
        return self.current_configs.copy()