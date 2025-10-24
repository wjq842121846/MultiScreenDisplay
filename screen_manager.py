from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtCore import QRect
import sys

class ScreenManager:
    def __init__(self):
        self.screens = []
        self.refresh()
        
    def refresh(self):
        """刷新屏幕信息"""
        self.screens = []
        
        if QApplication.instance() is None:
            app = QApplication([])
        else:
            app = QApplication.instance()
            
        desktop = QDesktopWidget()
        screen_count = desktop.screenCount()
        
        for i in range(screen_count):
            screen_geometry = desktop.screenGeometry(i)
            available_geometry = desktop.availableGeometry(i)
            
            screen_info = {
                'index': i,
                'name': f"Display {i + 1}",
                'geometry': screen_geometry,
                'available_geometry': available_geometry,
                'width': screen_geometry.width(),
                'height': screen_geometry.height(),
                'x': screen_geometry.x(),
                'y': screen_geometry.y(),
                'is_primary': i == desktop.primaryScreen()
            }
            
            self.screens.append(screen_info)
            
    def get_screens(self):
        """获取所有屏幕信息"""
        return self.screens
        
    def get_screen(self, index):
        """获取指定索引的屏幕信息"""
        if 0 <= index < len(self.screens):
            return self.screens[index]
        return None
        
    def get_primary_screen(self):
        """获取主屏幕信息"""
        for screen in self.screens:
            if screen['is_primary']:
                return screen
        return self.screens[0] if self.screens else None
        
    def get_screen_count(self):
        """获取屏幕数量"""
        return len(self.screens)
        
    def get_screen_by_position(self, x, y):
        """根据坐标获取屏幕信息"""
        for screen in self.screens:
            geometry = screen['geometry']
            if (geometry.x() <= x <= geometry.x() + geometry.width() and
                geometry.y() <= y <= geometry.y() + geometry.height()):
                return screen
        return None
        
    def print_screen_info(self):
        """打印所有屏幕信息（调试用）"""
        print(f"检测到 {len(self.screens)} 个屏幕:")
        for i, screen in enumerate(self.screens):
            print(f"屏幕 {i + 1}:")
            print(f"  名称: {screen['name']}")
            print(f"  分辨率: {screen['width']} x {screen['height']}")
            print(f"  位置: ({screen['x']}, {screen['y']})")
            print(f"  主屏幕: {'是' if screen['is_primary'] else '否'}")
            print()

if __name__ == "__main__":
    # 测试代码
    app = QApplication(sys.argv)
    screen_manager = ScreenManager()
    screen_manager.print_screen_info()