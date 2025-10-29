# -*- coding: utf-8 -*-
"""
完整的UI样式配置文件
包含多屏幕内容管理器的所有界面样式定义
方便统一管理和调试界面外观
"""

# ========================================
# 全局样式配置
# ========================================

# 主窗口样式 - 应用于整个应用程序
MAIN_WINDOW_STYLE = """
    /* 主窗口全局样式 */
    QMainWindow {
        background: #ffffff;                    /* 主背景色：纯白色 */
        font-size: 10px;                       /* 全局字体大小 */
        font-family: 'Microsoft YaHei UI', 'Segoe UI', 'SF Pro Display', Arial, sans-serif;  /* 字体家族 */
    }
    
    /* 全局组件默认样式 */
    QWidget {
        background: transparent;                /* 默认透明背景 */
        color: #000000;                        /* 默认文字颜色：黑色 */
    }
"""

# ========================================
# 标题栏样式
# ========================================

# 标题栏容器样式
HEADER_FRAME_STYLE = """
    QFrame {
        background: #ffffff;                    /* 标题栏背景：白色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 12px;                   /* 圆角：12像素 */
        margin: 0px;                           /* 外边距 */
        padding: 0px;                         /* 内边距 */
    }
"""

# 主标题样式
MAIN_TITLE_STYLE = """
    QLabel {
        color: #000000;                        /* 标题颜色：黑色 */
        font-size: 20px;                       /* 字体大小：24像素 */
        font-weight: bold;                     /* 粗体 */
        background: transparent;               /* 透明背景 */
        padding: 0px;                          /* 无内边距 */
        margin: 0px;                           /* 无外边距 */
    }
"""

# 副标题样式
SUBTITLE_STYLE = """
    QLabel {
        color: #4169e1;                        /* 副标题颜色：皇家蓝 */
        font-size: 12px;                       /* 字体大小：14像素 */
        font-weight: normal;                   /* 正常字重 */
        background: transparent;               /* 透明背景 */
        padding: 0px;                          /* 无内边距 */
        margin: 0px;                           /* 无外边距 */
    }
"""

# ========================================
# 按钮样式
# ========================================

# 标准按钮样式 - 用于标题栏和操作按钮
STANDARD_BUTTON_STYLE = """
    QPushButton {
        background: #ffffff;                   /* 按钮背景：白色 */
        color: #000000;                        /* 文字颜色：黑色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 6px;                    /* 圆角：6像素 */
        padding: 2px 4px;                     /* 内边距：上下8px，左右16px */
        font-size: 14px;                       /* 字体大小：14像素 */
        font-weight: 500;                      /* 字重：中等 */
        min-width: 80px;                       /* 最小宽度：80像素 */
        min-height: 25px;                      /* 最小高度：32像素 */
    }
    
    /* 悬停效果 */
    QPushButton:hover {
        background: #f0f8ff;                   /* 悬停背景：爱丽丝蓝 */
        border-color: #4169e1;                 /* 悬停边框：皇家蓝 */
    }
    
    /* 按下效果 */
    QPushButton:pressed {
        background: #e6f3ff;                   /* 按下背景：浅蓝色 */
    }
"""

# 小型按钮样式 - 用于日志面板控制按钮
SMALL_BUTTON_STYLE = """
    QPushButton {
        background: #ffffff;                   /* 按钮背景：白色 */
        color: #000000;                        /* 文字颜色：黑色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 6px;                    /* 圆角：6像素 */
        padding: 1px 2px;                     /* 内边距：上下6px，左右12px */
        font-size: 12px;                       /* 字体大小：12像素 */
        font-weight: 500;                      /* 字重：中等 */
        min-width: 30px;                       /* 最小宽度：50像素 */
        min-height: 15px;                      /* 最小高度：28像素 */
    }
    
    /* 悬停效果 */
    QPushButton:hover {
        background: #f0f8ff;                   /* 悬停背景：爱丽丝蓝 */
        border-color: #4169e1;                 /* 悬停边框：皇家蓝 */
    }
    
    /* 按下效果 */
    QPushButton:pressed {
        background: #e6f3ff;                   /* 按下背景：浅蓝色 */
    }
"""

# ========================================
# 配置面板样式
# ========================================

# 配置面板容器样式
CONFIG_PANEL_STYLE = """
    QWidget {
        background: #ffffff;                   /* 配置面板背景：白色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 8px;                    /* 圆角：8像素 */
        margin: 0px;                           /* 外边距：5像素 */
        padding: 0px;                         /* 内边距：10像素 */
    }
"""

# 配置中心标题样式（左上角小标题）
CONFIG_CENTER_TITLE_STYLE = """
    QLabel {
        color: #000000;                        /* 标题颜色：黑色 */
        font-size: 14px;                       /* 字体大小：14像素 */
        font-weight: bold;                     /* 粗体 */
        padding: 5px 10px;                     /* 内边距：上下5px，左右10px */
        background: #f0f8ff;                   /* 背景：爱丽丝蓝 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 4px;                    /* 圆角：4像素 */
    }
"""

# ========================================
# 日志面板样式
# ========================================

# 日志面板组框样式
LOG_GROUP_BOX_STYLE = """
    QGroupBox {
        background: #ffffff;                   /* 组框背景：白色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 8px;                    /* 圆角：8像素 */
        margin: 5px;                           /* 外边距：5像素 */
        padding-top: 15px;                     /* 顶部内边距：为标题留空间 */
        font-size: 14px;                       /* 字体大小：14像素 */
        font-weight: bold;                     /* 粗体 */
        color: #000000;                        /* 文字颜色：黑色 */
    }
    
    /* 组框标题样式 */
    QGroupBox::title {
        subcontrol-origin: margin;             /* 标题位置：边距区域 */
        subcontrol-position: top left;         /* 标题位置：左上角 */
        padding: 5px 10px;                     /* 标题内边距 */
        background: #f0f8ff;                   /* 标题背景：爱丽丝蓝 */
        border: 1px solid #87ceeb;             /* 标题边框：天蓝色 */
        border-radius: 4px;                    /* 标题圆角：4像素 */
        left: 10px;                            /* 标题左偏移：10像素 */
        top: -8px;                             /* 标题上偏移：-8像素 */
    }
"""

# 日志文本编辑框样式
LOG_TEXT_EDIT_STYLE = """
    QTextEdit {
        background: #ffffff;                   /* 文本框背景：白色 */
        color: #000000;                        /* 文字颜色：黑色 */
        font-family: 'Consolas', 'Courier New', 'SF Mono', monospace;  /* 等宽字体 */
        font-size: 12px;                       /* 字体大小：12像素 */
        font-weight: 400;                      /* 正常字重 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 6px;                    /* 圆角：6像素 */
        padding: 10px;                         /* 内边距：10像素 */
        line-height: 1.4;                      /* 行高：1.4倍 */
        selection-background-color: #87ceeb;   /* 选中背景：天蓝色 */
        selection-color: #000000;              /* 选中文字：黑色 */
    }
    
    /* 滚动条样式 */
    QTextEdit QScrollBar:vertical {
        background: #f0f8ff;                   /* 滚动条背景：爱丽丝蓝 */
        width: 12px;                           /* 滚动条宽度：12像素 */
        border-radius: 6px;                    /* 滚动条圆角：6像素 */
    }
    
    QTextEdit QScrollBar::handle:vertical {
        background: #87ceeb;                   /* 滚动条滑块：天蓝色 */
        border-radius: 6px;                    /* 滑块圆角：6像素 */
        min-height: 20px;                      /* 滑块最小高度：20像素 */
    }
    
    QTextEdit QScrollBar::handle:vertical:hover {
        background: #4169e1;                   /* 滑块悬停：皇家蓝 */
    }
"""

# ========================================
# 屏幕配置组件样式
# ========================================

# 屏幕配置小部件样式 - 用于每个屏幕的配置容器
SCREEN_CONFIG_WIDGET_STYLE = """
    QWidget {
        background: #ffffff;                   /* 屏幕配置背景：白色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 8px;                    /* 圆角：8像素 */
        padding: 3px;                          /* 内边距：8像素 */
        margin: 1px;                           /* 外边距：3像素 */
        /* 使用弹性布局自适应，不设置固定尺寸 */
    }
    
    /* 选中状态的屏幕配置容器 */
    QWidget:focus {
        border-color: #4169e1;                 /* 焦点边框：皇家蓝 */
        background: #f0f8ff;                   /* 焦点背景：爱丽丝蓝 */
    }
"""

# 屏幕标题样式
SCREEN_TITLE_STYLE = """
    QLabel {
        color: #4169e1;                        /* 屏幕标题颜色：皇家蓝 */
        font-size: 14px;                       /* 字体大小：14像素 */
        font-weight: bold;                     /* 粗体 */
        padding: 0px;                          /* 内边距：5像素 */
        background: transparent;               /* 透明背景 */
        border: none;                          /* 无边框 */
    }
"""

# 屏幕信息标签样式
SCREEN_INFO_STYLE = """
    QLabel {
        color: #666666;                        /* 信息文字颜色：灰色 */
        font-size: 11px;                       /* 字体大小：11像素 */
        font-weight: normal;                   /* 正常字重 */
        padding: 2px 5px;                      /* 内边距：上下2px，左右5px */
        background: transparent;               /* 透明背景 */
        border: none;                          /* 无边框 */
    }
"""

# ========================================
# 输入组件样式
# ========================================

# 下拉框样式
COMBO_BOX_STYLE = """
    QComboBox {
        background: #ffffff;                   /* 下拉框背景：白色 */
        color: #000000;                        /* 文字颜色：黑色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 4px;                    /* 圆角：4像素 */
        padding: 4px 8px;                      /* 内边距：上下4px，左右8px */
        font-size: 12px;                       /* 字体大小：12像素 */
        min-height: 24px;                      /* 最小高度：24像素 */
    }
    
    /* 下拉箭头 */
    QComboBox::drop-down {
        border: none;                          /* 无边框 */
        width: 20px;                           /* 箭头区域宽度：20像素 */
    }
    
    QComboBox::down-arrow {
        image: none;                           /* 使用默认箭头 */
        border: 1px solid #87ceeb;             /* 箭头边框：天蓝色 */
        width: 8px;                            /* 箭头宽度：8像素 */
        height: 8px;                           /* 箭头高度：8像素 */
    }
    
    /* 悬停效果 */
    QComboBox:hover {
        border-color: #4169e1;                 /* 悬停边框：皇家蓝 */
        background: #f0f8ff;                   /* 悬停背景：爱丽丝蓝 */
    }
    
    /* 下拉列表样式 */
    QComboBox QAbstractItemView {
        background: #ffffff;                   /* 列表背景：白色 */
        border: 1px solid #87ceeb;             /* 列表边框：天蓝色 */
        border-radius: 4px;                    /* 列表圆角：4像素 */
        selection-background-color: #f0f8ff;   /* 选中项背景：爱丽丝蓝 */
        selection-color: #000000;              /* 选中项文字：黑色 */
    }
"""

# 文本输入框样式
LINE_EDIT_STYLE = """
    QLineEdit {
        background: #ffffff;                   /* 输入框背景：白色 */
        color: #000000;                        /* 文字颜色：黑色 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 4px;                    /* 圆角：4像素 */
        padding: 4px 8px;                      /* 内边距：上下4px，左右8px */
        font-size: 12px;                       /* 字体大小：12像素 */
        min-height: 24px;                      /* 最小高度：24像素 */
    }
    
    /* 焦点状态 */
    QLineEdit:focus {
        border-color: #4169e1;                 /* 焦点边框：皇家蓝 */
        background: #f0f8ff;                   /* 焦点背景：爱丽丝蓝 */
    }
    
    /* 悬停效果 */
    QLineEdit:hover {
        border-color: #4169e1;                 /* 悬停边框：皇家蓝 */
    }
"""

# ========================================
# 容器和布局样式
# ========================================

# 分割器样式
SPLITTER_STYLE = """
    QSplitter::handle {
        background: #87ceeb;                   /* 分割条背景：天蓝色 */
        border: 1px solid #4169e1;             /* 分割条边框：皇家蓝 */
    }
    
    QSplitter::handle:horizontal {
        width: 3px;                            /* 水平分割条宽度：3像素 */
    }
    
    QSplitter::handle:vertical {
        height: 3px;                           /* 垂直分割条高度：3像素 */
    }
    
    QSplitter::handle:hover {
        background: #4169e1;                   /* 悬停时分割条背景：皇家蓝 */
    }
"""

# 滚动区域样式
SCROLL_AREA_STYLE = """
    QScrollArea {
        background: transparent;               /* 滚动区域背景：透明 */
        border: none;                          /* 无边框 */
    }
    
    QScrollArea > QWidget > QWidget {
        background: transparent;               /* 内容区域背景：透明 */
    }
    
    /* 滚动条样式 */
    QScrollArea QScrollBar:vertical {
        background: #f0f8ff;                   /* 垂直滚动条背景：爱丽丝蓝 */
        width: 12px;                           /* 滚动条宽度：12像素 */
        border-radius: 6px;                    /* 滚动条圆角：6像素 */
        margin: 0px;                           /* 无外边距 */
    }
    
    QScrollArea QScrollBar::handle:vertical {
        background: #87ceeb;                   /* 滚动条滑块：天蓝色 */
        border-radius: 6px;                    /* 滑块圆角：6像素 */
        min-height: 20px;                      /* 滑块最小高度：20像素 */
        margin: 2px;                           /* 滑块边距：2像素 */
    }
    
    QScrollArea QScrollBar::handle:vertical:hover {
        background: #4169e1;                   /* 滑块悬停：皇家蓝 */
    }
    
    QScrollArea QScrollBar:horizontal {
        background: #f0f8ff;                   /* 水平滚动条背景：爱丽丝蓝 */
        height: 12px;                          /* 滚动条高度：12像素 */
        border-radius: 6px;                    /* 滚动条圆角：6像素 */
        margin: 0px;                           /* 无外边距 */
    }
    
    QScrollArea QScrollBar::handle:horizontal {
        background: #87ceeb;                   /* 滚动条滑块：天蓝色 */
        border-radius: 6px;                    /* 滑块圆角：6像素 */
        min-width: 20px;                       /* 滑块最小宽度：20像素 */
        margin: 2px;                           /* 滑块边距：2像素 */
    }
    
    QScrollArea QScrollBar::handle:horizontal:hover {
        background: #4169e1;                   /* 滑块悬停：皇家蓝 */
    }
"""

# ========================================
# 菜单和工具提示样式
# ========================================

# 菜单样式
MENU_STYLE = """
    QMenu {
        background: #ffffff;                   /* 菜单背景：白色 */
        border: 1px solid #87ceeb;             /* 菜单边框：天蓝色 */
        border-radius: 6px;                    /* 菜单圆角：6像素 */
        padding: 4px;                          /* 菜单内边距：4像素 */
    }
    
    QMenu::item {
        background: transparent;               /* 菜单项背景：透明 */
        color: #000000;                        /* 菜单项文字：黑色 */
        padding: 6px 12px;                     /* 菜单项内边距：上下6px，左右12px */
        border-radius: 4px;                    /* 菜单项圆角：4像素 */
    }
    
    QMenu::item:selected {
        background: #f0f8ff;                   /* 选中项背景：爱丽丝蓝 */
        color: #4169e1;                        /* 选中项文字：皇家蓝 */
    }
    
    QMenu::separator {
        height: 1px;                           /* 分隔线高度：1像素 */
        background: #87ceeb;                   /* 分隔线颜色：天蓝色 */
        margin: 4px 8px;                       /* 分隔线边距：上下4px，左右8px */
    }
"""

# 工具提示样式
TOOLTIP_STYLE = """
    QToolTip {
        background: #ffffff;                   /* 提示背景：白色 */
        color: #000000;                        /* 提示文字：黑色 */
        border: 1px solid #87ceeb;             /* 提示边框：天蓝色 */
        border-radius: 4px;                    /* 提示圆角：4像素 */
        padding: 4px 8px;                      /* 提示内边距：上下4px，左右8px */
        font-size: 12px;                       /* 提示字体：12像素 */
    }
"""

# ========================================
# 特殊效果样式
# ========================================

# 阴影效果样式（可用于需要突出显示的组件）
SHADOW_EFFECT_STYLE = """
    QWidget {
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 8px;                    /* 圆角：8像素 */
        background: #ffffff;                   /* 背景：白色 */
        /* CSS3阴影效果（在支持的环境中有效） */
        box-shadow: 0 2px 8px rgba(135, 206, 235, 0.3);
    }
"""

# 渐变背景样式（可选的装饰效果）
GRADIENT_BACKGROUND_STYLE = """
    QWidget {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #ffffff,    /* 起始颜色：白色 */
                                    stop: 1 #f0f8ff);   /* 结束颜色：爱丽丝蓝 */
        border: 1px solid #87ceeb;             /* 边框：天蓝色 */
        border-radius: 8px;                    /* 圆角：8像素 */
    }
"""

# ========================================
# 样式组合和工具函数
# ========================================

def apply_standard_widget_style(widget):
    """
    为标准组件应用通用样式
    
    Args:
        widget: 要应用样式的PyQt5组件
    """
    widget.setStyleSheet("""
        QWidget {
            background: #ffffff;
            border: 1px solid #87ceeb;
            border-radius: 8px;
            padding: 8px;
            margin: 3px;
        }
    """)

def apply_button_style(button, style_type="standard"):
    """
    为按钮应用指定样式
    
    Args:
        button: 要应用样式的按钮组件
        style_type: 样式类型，可选 "standard" 或 "small"
    """
    if style_type == "small":
        button.setStyleSheet(SMALL_BUTTON_STYLE)
    else:
        button.setStyleSheet(STANDARD_BUTTON_STYLE)

def get_log_level_color(level):
    """
    根据日志级别获取对应的颜色
    
    Args:
        level: 日志级别字符串
    
    Returns:
        str: 对应的颜色代码
    """
    colors = {
        "INFO": "#00ffff",      # 青色
        "SUCCESS": "#00ff7f",   # 春绿色
        "WARNING": "#ffa500",   # 橙色
        "ERROR": "#ff1493",     # 深粉红色
        "DEBUG": "#e0e6ed"      # 浅灰色
    }
    return colors.get(level, "#e0e6ed")

# ========================================
# 样式常量集合
# ========================================

# 所有样式的集合，便于批量应用
ALL_STYLES = {
    'main_window': MAIN_WINDOW_STYLE,
    'header_frame': HEADER_FRAME_STYLE,
    'main_title': MAIN_TITLE_STYLE,
    'subtitle': SUBTITLE_STYLE,
    'standard_button': STANDARD_BUTTON_STYLE,
    'small_button': SMALL_BUTTON_STYLE,
    'config_panel': CONFIG_PANEL_STYLE,
    'config_title': CONFIG_CENTER_TITLE_STYLE,
    'log_group': LOG_GROUP_BOX_STYLE,
    'log_text': LOG_TEXT_EDIT_STYLE,
    'screen_widget': SCREEN_CONFIG_WIDGET_STYLE,
    'screen_title': SCREEN_TITLE_STYLE,
    'screen_info': SCREEN_INFO_STYLE,
    'combo_box': COMBO_BOX_STYLE,
    'line_edit': LINE_EDIT_STYLE,
    'splitter': SPLITTER_STYLE,
    'scroll_area': SCROLL_AREA_STYLE,
    'menu': MENU_STYLE,
    'tooltip': TOOLTIP_STYLE,
    'shadow': SHADOW_EFFECT_STYLE,
    'gradient': GRADIENT_BACKGROUND_STYLE
}

# ========================================
# 调试和开发辅助
# ========================================

def print_all_styles():
    """
    打印所有可用的样式名称，用于调试
    """
    print("可用的样式:")
    for style_name in ALL_STYLES.keys():
        print(f"  - {style_name}")

def get_style_by_name(name):
    """
    根据名称获取样式字符串
    
    Args:
        name: 样式名称
    
    Returns:
        str: 对应的样式字符串，如果不存在则返回空字符串
    """
    return ALL_STYLES.get(name, "")

# 导出的旧样式常量，保持向后兼容
GROUP_BOX_STYLE = LOG_GROUP_BOX_STYLE
TEXT_EDIT_STYLE = LOG_TEXT_EDIT_STYLE
BUTTON_STYLE = STANDARD_BUTTON_STYLE
PRIMARY_BUTTON_STYLE = STANDARD_BUTTON_STYLE

# ========================================
# 预览相关样式
# ========================================

# 预览组样式
PREVIEW_GROUP_STYLE = """
    QGroupBox {
        font-weight: bold;                      /* 粗体字 */
        border: 1px solid #87ceeb;              /* 边框：天蓝色 */
        border-radius: 8px;                     /* 圆角：8像素 */
        margin-top: 10px;                       /* 顶部边距：10像素 */
        padding-top: 15px;                      /* 顶部内边距：15像素 */
        background-color: #ffffff;              /* 背景：白色 */
        color: #000000;                         /* 文字：黑色 */
    }
    QGroupBox::title {
        subcontrol-origin: margin;              /* 标题位置控制 */
        left: 10px;                             /* 左边距：10像素 */
        padding: 0 8px 0 8px;                   /* 标题内边距 */
        color: #4169e1;                         /* 标题颜色：皇家蓝 */
        font-size: 14px;                        /* 标题字体大小 */
        background: #ffffff;                    /* 标题背景：白色 */
    }
"""

# 预览组件样式
PREVIEW_WIDGET_STYLE = """
    QWidget {
        background-color: #f0f8ff;              /* 背景：爱丽丝蓝 */
        border: 1px solid #87ceeb;              /* 边框：天蓝色 */
        border-radius: 4px;                     /* 圆角：4像素 */
        color: #000000;                         /* 文字：黑色 */
        padding: 4px;                           /* 内边距：4像素 */
        margin: 2px;                            /* 外边距：2像素 */
    }
"""