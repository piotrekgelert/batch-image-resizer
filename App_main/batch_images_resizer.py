import os
import sys

import PyQt6.QtWidgets as qtw
from PIL import Image, ImageEnhance
from UI.resize_images_in_batches_ui import Ui_mw_window


class BatchImageResizer(qtw.QMainWindow, Ui_mw_window):
    files_path, save_path, img_name, img_ext = '', '', '', ''
    new_width, new_heigth = 0, 0
    
    pix_work, perc_work, gb_pix_sharp, gb_perc_sharp = False, False, False, False
    sharp: float = 0.0

    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pb_open_images_path.clicked.connect(self.get_images_path)
        self.pb_save_images_path.clicked.connect(self.get_save_images_path)
        self.pb_reset_paths.clicked.connect(self.reset_paths)
        self.pb_calculate_pixels.clicked.connect(self.pixels_setup)
        self.pb_calculate_percent.clicked.connect(self.percent_setup)
        self.pb_reset_pixels.clicked.connect(self.pixels_reset)
        self.pb_reset_percent.clicked.connect(self.percent_reset)
        
        self.gb_sharpness_pixels.toggled.connect(self.gb_sharp_pix)
        self.gb_sharpness_percent.toggled.connect(self.gb_sharp_perc)

        self.pb_main_resize.clicked.connect(self.resize_images)
        self.pb_main_cancel.clicked.connect(self.close)

    
    def get_images_path(self):
        self.files_path = qtw.QFileDialog.getExistingDirectory()
        self.lb_get_images_path.setText(self.files_path)
    
    def get_save_images_path(self):
        s_path = qtw.QFileDialog.getExistingDirectory()
        if s_path == self.files_path:
            self.lb_message.setText("folder 'resized' is added to save path")
            new_s_path = os.path.join(s_path, 'resized')
            os.mkdir(new_s_path)
            self.save_path = new_s_path
            self.lb_save_images_path.setText(new_s_path)
        else:
            self.save_path = s_path
            self.lb_save_images_path.setText(self.save_path)
            self.lb_message.clear()
    
    def reset_paths(self):
        self.lb_get_images_path.clear()
        self.files_path = ''
        self.lb_save_images_path.clear()
        self.save_path = ''
    
    def gb_sharp_pix(self):
        self.gb_pix_sharp = self.gb_sharpness_pixels.isChecked()
    
    def gb_sharp_perc(self):
        self.gb_perc_sharp = self.gb_sharpness_percent.isChecked()
    

    def pixels_setup(self):
        if len(self.le_pixels_width.text())\
            and len(self.le_pixels_height.text()):
                self.new_width = int(self.le_pixels_width.text())
                self.new_heigth = int(self.le_pixels_height.text())
                self.pix_work = True
                self.perc_work = False
                self.lb_message.setText(
                    'new dimentions of the images will be [{}px, {}px] '.format(
                        self.le_pixels_width.text(),
                        self.le_pixels_height.text()
                        ))
        else:
            self.lb_message.setText('width and height has to be filled in')
        
    def sharp_pixels(self):
        if self.gb_pix_sharp:
            if self.rb_04_pix.isChecked():
                self.sharp = 0.4
            elif self.rb_06_pix.isChecked():
                self.sharp = 0.6
            elif self.rb_08_pix.isChecked():
                self.sharp = 0.8
            elif self.rb_1_pix.isChecked():
                self.sharp = 1.0
    
    def pixels_reset(self):
        self.le_pixels_width.clear()
        self.le_pixels_height.clear()
        self.sharp = 0
        self.rb_04_pix.setChecked(True)
        self.gb_sharpness_pixels.setChecked(False)
    
    def percent_setup(self):
        if len(self.le_percent_width.text()) and\
            len(self.le_percent_height.text()):
                self.pix_work = False
                self.perc_work = True
                self.lb_message.setText(
                    'new dimentions will be [{}%, {}%] of the original image'.format(
                        self.le_percent_width.text(),
                        self.le_percent_height.text()
                        ))
        else:
            self.lb_message.setText('width and height has to be filled in')
    
    def sharp_percent(self):
        if self.gb_perc_sharp:
            if self.rb_04_perc.isChecked():
                self.sharp = 0.4
            elif self.rb_06_perc.isChecked():
                self.sharp = 0.6
            elif self.rb_08_perc.isChecked():
                self.sharp = 0.8
            elif self.rb_1_perc.isChecked():
                self.sharp = 1.0

    def percent_reset(self):
        self.le_percent_width.clear()
        self.le_percent_height.clear()
        self.sharp = 0
        self.rb_04_perc.setChecked(True)
        self.gb_sharpness_percent.setChecked(False)

    def resize_images(self):
        for image in os.listdir(self.files_path):
            try:
                img_name, img_ext = image.split('.')
                if self.pix_work:
                    with Image.open(os.path.join(self.files_path, image)) as im:
                        img = im.resize(
                            (self.new_width, self.new_heigth),
                            resample=Image.Resampling.LANCZOS,
                        )
                        if self.sharp > 0:
                            img = ImageEnhance.Sharpness(img)
                            img = img.enhance(1 + self.sharp)
                        
                        img.save(
                            os.path.join(
                                self.save_path,
                                '{}.{}'.format(img_name, img_ext)
                                )
                            )
                elif self.perc_work:
                    with Image.open(os.path.join(self.files_path, image)) as im:
                        self.new_width = int(
                            (
                                float(self.le_percent_width.text()) / 100
                                ) * im.width)
                        self.new_heigth = int(
                            (
                                float(self.le_percent_height.text()) / 100
                                ) * im.height)
                                
                        img = im.resize(
                            (self.new_width, self.new_heigth),
                            resample=Image.Resampling.LANCZOS,
                        )
                        if self.sharp > 0:
                            img = ImageEnhance.Sharpness(img)
                            img = img.enhance(1 + self.sharp)
                        
                        img.save(
                            os.path.join(
                                self.save_path,
                                '{}.{}'.format(img_name, img_ext)
                                )
                            )
            except:
                pass
        self.lb_message.setText('Images resized, check folder')
    
    

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = BatchImageResizer()
    window.show()
    sys.exit(app.exec())