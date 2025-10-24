"""
UI样式配置文件
包含整个应用程序的CSS样式定义
"""

# 主窗口样式
MAIN_WINDOW_STYLE = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #2c3e50, stop:1 #3498db);
    color: #ecf0f1;
    font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
}

QWidget {
    background-color: transparent;
    color: #ecf0f1;
    font-size: 14px;
}
"""

# 标题样式
TITLE_STYLE = """
QLabel {
    color: #ecf0f1;
    font-size: 24px;
    font-weight: bold;
    padding: 15px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #34495e, stop:1 #2c3e50);
    border-radius: 8px;
    margin: 10px;
    border: 2px solid #3498db;
}
"""

# 分组框样式
GROUP_BOX_STYLE = """
QGroupBox {
    font-size: 16px;
    font-weight: bold;
    color: #ecf0f1;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #34495e, stop:1 #2c3e50);
    border: 2px solid #3498db;
    border-radius: 10px;
    margin: 10px 5px;
    padding-top: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 5px 10px;
    background-color: #3498db;
    color: white;
    border-radius: 5px;
    font-weight: bold;
}
"""

# 预览分组框样式
PREVIEW_GROUP_STYLE = """
QGroupBox {
    font-size: 16px;
    font-weight: bold;
    color: #ecf0f1;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #1abc9c, stop:1 #16a085);
    border: 2px solid #1abc9c;
    border-radius: 10px;
    margin: 10px 5px;
    padding-top: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 5px 10px;
    background-color: #1abc9c;
    color: white;
    border-radius: 5px;
    font-weight: bold;
}
"""

# 按钮样式
BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #3498db, stop:1 #2980b9);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: bold;
    min-width: 90px;
    min-height: 35px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #5dade2, stop:1 #3498db);
    transform: translateY(-1px);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #2980b9, stop:1 #1f618d);
}

QPushButton:disabled {
    background: #7f8c8d;
    color: #bdc3c7;
}
"""

# 主要操作按钮样式
PRIMARY_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #e74c3c, stop:1 #c0392b);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 22px;
    font-size: 15px;
    font-weight: bold;
    min-width: 110px;
    min-height: 40px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ec7063, stop:1 #e74c3c);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #c0392b, stop:1 #a93226);
}
"""

# 成功按钮样式
SUCCESS_BUTTON_STYLE = """
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #27ae60, stop:1 #229954);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: bold;
    min-width: 90px;
    min-height: 35px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #58d68d, stop:1 #27ae60);
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #229954, stop:1 #1e8449);
}
"""

# 下拉框样式
COMBO_BOX_STYLE = """
QComboBox {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ecf0f1, stop:1 #bdc3c7);
    color: #2c3e50;
    border: 2px solid #3498db;
    border-radius: 5px;
    padding: 6px 12px;
    font-size: 14px;
    min-width: 130px;
    min-height: 30px;
}

QComboBox:hover {
    border-color: #5dade2;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #f8f9fa, stop:1 #ecf0f1);
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: 1px solid #3498db;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    background: #3498db;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid white;
    margin: 0px;
}

QComboBox QAbstractItemView {
    background-color: #ecf0f1;
    color: #2c3e50;
    border: 1px solid #3498db;
    selection-background-color: #3498db;
    selection-color: white;
}
"""

# 文本输入框样式
TEXT_EDIT_STYLE = """
QTextEdit {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #ffffff, stop:1 #f8f9fa);
    color: #2c3e50;
    border: 2px solid #3498db;
    border-radius: 5px;
    padding: 10px;
    font-size: 14px;
    font-family: 'Consolas', 'Courier New', monospace;
}

QTextEdit:focus {
    border-color: #e74c3c;
    background: white;
}

QTextEdit:hover {
    border-color: #5dade2;
}
"""

# 标签样式
LABEL_STYLE = """
QLabel {
    color: #ecf0f1;
    font-size: 14px;
    font-weight: bold;
    padding: 3px;
}
"""

# 信息标签样式
INFO_LABEL_STYLE = """
QLabel {
    color: #7fb3d3;
    font-size: 13px;
    font-style: italic;
    padding: 3px;
}
"""

# 滚动区域样式
SCROLL_AREA_STYLE = """
QScrollArea {
    border: 2px solid #34495e;
    border-radius: 8px;
    background: transparent;
}

QScrollBar:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #34495e, stop:1 #2c3e50);
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3498db, stop:1 #2980b9);
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #5dade2, stop:1 #3498db);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

# 预览窗口样式
PREVIEW_WIDGET_STYLE = """
QWidget {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 #2c3e50, stop:1 #34495e);
    border: 2px solid #1abc9c;
    border-radius: 8px;
    padding: 5px;
}
"""

# 预览标签样式
PREVIEW_LABEL_STYLE = """
QLabel {
    background-color: #34495e;
    border: 1px solid #7f8c8d;
    border-radius: 4px;
    padding: 12px;
    color: #ecf0f1;
    font-size: 12px;
    text-align: center;
}
"""