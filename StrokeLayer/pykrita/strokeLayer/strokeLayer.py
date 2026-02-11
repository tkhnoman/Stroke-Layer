
from krita import *
from PyQt5.QtWidgets import QFileDialog, QListWidget, QInputDialog, QMessageBox, QLabel



class StrokeMenuShow(QDialog):
    def __init__(self):
        krita_window = Krita.instance().activeWindow().qwindow()
        super().__init__(krita_window)
        self.setWindowTitle("Add Stroke Layer")

        self.setMinimumSize(320, 305)
        self.setFixedSize(self.size())
        
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFocus(True)
        
        MainLayout = QVBoxLayout()
        self.setLayout(MainLayout)
        
        # ####################
        
        TabWidget = QTabWidget()
        Tab1 = QWidget()
        TabWidget.addTab(Tab1, "&Stroke")
        
        TabLayout = QVBoxLayout()
        Tab1.setLayout(TabLayout)
        
        OKcancelLayout = QHBoxLayout()
        
        MainLayout.addWidget(TabWidget)
        MainLayout.addLayout(OKcancelLayout)
        
        
        # ####################
        
        LineGroup = QGroupBox("")
        LRlayout = QHBoxLayout()
        
        TabLayout.addWidget(LineGroup)
        TabLayout.addLayout(LRlayout)

        Llayout = QVBoxLayout()
        Rlayout = QVBoxLayout()
        LRlayout.addLayout(Llayout)
        LRlayout.addLayout(Rlayout)
        
        # ####################
        
        LineLayout = QVBoxLayout()
        LineGroup.setLayout(LineLayout)
        
        WidthLayout = QHBoxLayout()
        LineLayout.addLayout(WidthLayout)
        
        # ColorGroup = QGroupBox("Color")
        ColorGroup = QGroupBox("")
        Llayout.addWidget(ColorGroup)
        
        # LocationGroup = QGroupBox("Location")
        LocationGroup = QGroupBox("")
        LocationGroup.setMaximumSize(120, 500)
        Rlayout.addWidget(LocationGroup)
        
        EtcGroup = QGroupBox()
        EtcGroup.setMaximumSize(120, 40)
        Rlayout.addWidget(EtcGroup)
        
        ColorLayout = QVBoxLayout()
        ColorGroup.setLayout(ColorLayout)
        
        LocationLayout = QVBoxLayout()
        LocationGroup.setLayout(LocationLayout)
        
        EtcLayout = QVBoxLayout()
        EtcGroup.setLayout(EtcLayout)
        
        # ####################
        
        WidthLabel = QLabel("Width: ")
        WidthLabel.setMaximumSize(50, 50)
        WidthLayout.addWidget(WidthLabel)
        
        WidthInput = QSpinBox()
        WidthInput.setMinimum(1)
        WidthInput.setMaximum(1000000)
        WidthLayout.addWidget(WidthInput)
        
        UnitInput = QComboBox()
        UnitInput.setMaximumSize(50, 50)
        UnitInput.addItem("px")
        UnitInput.addItem("mm")
        UnitInput.addItem("inch")
        WidthLayout.addWidget(UnitInput)
        
        
        # ####################
        
        
        ForeRadio = QRadioButton("Foreground Color")
        BackRadio = QRadioButton("Background Color")
        CustomRadio = QRadioButton("Custom Color")
        ColorButton = QPushButton("")
        ColorLayout.addWidget(ForeRadio)
        ColorLayout.addWidget(BackRadio)
        ColorLayout.addWidget(CustomRadio)
        ColorLayout.addWidget(ColorButton)
        # ColorLayout.addStretch(1)
        
        ColorButton.setDefault(False)
        
        
        ColorButton.clicked.connect(self.ColorPick)
        
        # ####################
        
        
        InsideRadio = QRadioButton("Inside")
        CenterRadio = QRadioButton("Center")
        OutsideRadio = QRadioButton("Outside")
        LocationLayout.addWidget(InsideRadio)
        LocationLayout.addWidget(CenterRadio)
        LocationLayout.addWidget(OutsideRadio)
        # LocationLayout.addStretch(1)
        
        
        SmoothCheck = QCheckBox("Smooth")
        EtcLayout.addWidget(SmoothCheck)
        
        # ####################
        
        SpacerOKcancel = QHBoxLayout()
        OKcancelLayout.addLayout(SpacerOKcancel)
        
        OKbutton = QPushButton("&OK")
        Cancelbutton = QPushButton("&Cancel")
        OKbutton.setMinimumSize(100, 30)
        Cancelbutton.setMinimumSize(100, 30)
        OKbutton.setDefault(True)
        Cancelbutton.setDefault(False)
        SpacerOKcancel.addStretch(1)
        SpacerOKcancel.addWidget(OKbutton)
        SpacerOKcancel.addWidget(Cancelbutton)
        
        OKbutton.clicked.connect(self.OKpress)
        Cancelbutton.clicked.connect(self.CancelPress)
        
        # ####################
        
        self.WidthInput = WidthInput
        self.UnitInput = UnitInput
        self.ColorButton = ColorButton
        
        self.ForeRadio = ForeRadio
        self.BackRadio = BackRadio
        self.InsideRadio = InsideRadio
        self.OutsideRadio = OutsideRadio
        self.SmoothCheck = SmoothCheck
        
        app = Krita.instance()

        width = int(app.readSetting("strokeLayer", "width", "1"))
        self.WidthInput.setValue(width)
        
        unitw = int(app.readSetting("strokeLayer", "unitw", "0"))
        UnitInput.setCurrentIndex(unitw)
        
        self.color = app.readSetting("strokeLayer", "color", "#ff0000")
        self.UpdateColor()
        
        colorselected = int(app.readSetting("strokeLayer", "colorselected", "1"))
        if colorselected == 1:
            ForeRadio.setChecked(True)
        elif  colorselected == 2:
            BackRadio.setChecked(True)
        else:
            CustomRadio.setChecked(True)
            
        
        
        
        location = int(app.readSetting("strokeLayer", "location", "1"))
        if location == 1:
            InsideRadio.setChecked(True)
        elif  location == 3:
            OutsideRadio.setChecked(True)
        else:
            CenterRadio.setChecked(True)
            
        
        smooth = int(app.readSetting("strokeLayer", "smooth", "0"))
        if smooth == 1:
            SmoothCheck.setChecked(True)
        else:
            SmoothCheck.setChecked(False)
            
        
        self.show()
        self.setup()
        
        WidthInput.setFocus(True)

    def setup(self):
        self.notifier = Application.notifier()
        self.notifier.setActive(True)
        self.notifier.applicationClosing.connect(self.CancelPress)

    def ColorPick(self):
        color = QColorDialog.getColor(QColor(self.color), self)
        if color.isValid():
            self.color = color.name()
            self.UpdateColor()

    
    def OKpress(self):
        if self.strokeLayer():
            self.close()
        
    def CancelPress(self):
        self.close()
        
    def UpdateColor(self):
        self.ColorButton.setStyleSheet("background-color: "+self.color+";  border-radius: 1px;")
        
    def clamp(self, value, min_val, max_val):
        """Clamps a number (value) between a minimum and maximum value."""
        if value < min_val:
            return min_val
        if value > max_val:
            return max_val
        return value
    
    def strokeLayer(self):
        app = Krita.instance()
        document = app.activeDocument()
        window = app.activeWindow()
        layer = document.activeNode()
        bounds = document.bounds()
        view = window.activeView()
        canvas = view.canvas()
        
        app.writeSetting("strokeLayer", "width", str(self.WidthInput.value()) )
        app.writeSetting("strokeLayer", "unitw", str(self.UnitInput.currentIndex()) )
        app.writeSetting("strokeLayer", "color", self.color)
        
        
        if self.ForeRadio.isChecked():
            app.writeSetting("strokeLayer", "colorselected", "1")
        elif self.BackRadio.isChecked():
            app.writeSetting("strokeLayer", "colorselected", "2")
        else:
            app.writeSetting("strokeLayer", "colorselected", "3")
            
        if self.InsideRadio.isChecked():
            app.writeSetting("strokeLayer", "location", "1")
        elif self.OutsideRadio.isChecked():
            app.writeSetting("strokeLayer", "location", "3")
        else:
            app.writeSetting("strokeLayer", "location", "2")
        
        if self.SmoothCheck.isChecked():
            app.writeSetting("strokeLayer", "smooth", "1")
        else:
            app.writeSetting("strokeLayer", "smooth", "0")
            
    
        
        pixelData = layer.pixelData(bounds.x(), bounds.y(), bounds.width(), bounds.height())
        pixelArray = bytearray(pixelData)
        selectionArray = bytearray(int(len(pixelArray)/4))
    
    
        selection = Selection()
        
        selectionFound = False
        
        if document.selection(): # if Selection exist
            selectionData = document.selection().pixelData(bounds.x(), bounds.y(), bounds.width(), bounds.height())
            selectionArray = bytearray(selectionData)
            
            for i in range(0, len(selectionArray)):
                pixelArray[(i*4)+3] = selectionArray[i]
                if selectionArray[i] > 0:
                    # selectionArray[i] = 255
                    selectionArray[i] = self.clamp(int(selectionArray[i]  * 6), 0, 255)
                    selectionFound = True
                else:
                    selectionArray[i] = 0
        else:
            for i in range(0, len(selectionArray)):
                selectionArray[i] = pixelArray[(i*4)+3]
                if selectionArray[i] > 0:
                    selectionArray[i] = self.clamp(int(selectionArray[i]  * 6), 0, 255)
                    # selectionArray[i] = 255
                    selectionFound = True
                else:
                    selectionArray[i] = 0
        
        if selectionFound:
            selection.setPixelData(selectionArray, bounds.x(), bounds.y(), bounds.width(), bounds.height())

            strokeSize = self.WidthInput.value()
            
            dpi = document.xRes()
            
            strokeVal = float(strokeSize)
            
            if self.InsideRadio.isChecked() or self.OutsideRadio.isChecked():    
                strokeVal = strokeVal * 2
                
            if self.UnitInput.currentIndex() == 1: # mm
                strokeVal = dpi * strokeVal/ 25.4 / 2
            elif self.UnitInput.currentIndex() == 2: # inch
                strokeVal = (dpi * strokeVal ) / 2
            # ##################################################    
            else:
                strokeVal = strokeVal / 2
                
            onOutside = self.OutsideRadio.isChecked()
            
            strokeSize = int(round(strokeVal + 0.011)) # 0.011 is to ignore Banker's Rounding in python
            
            
            if strokeSize <= 1:
                strokeSize = 1
                
                # special calculation for stroke 1
                if self.InsideRadio.isChecked():
                    selection.shrink(1,1, False)
                elif not self.OutsideRadio.isChecked():
                    onOutside = True
                    selection.shrink(1,1, False)
                    
            
            selectionC = Selection.duplicate(selection)
            
            # selection.border(strokeSize, strokeSize)
            selection.grow(strokeSize, strokeSize)
            
            if self.InsideRadio.isChecked():
                selectionC.shrink(strokeSize,strokeSize, False)
            else:
                shrinkReduceSize = int(strokeSize / 1.2)
                selectionC.shrink(shrinkReduceSize,shrinkReduceSize, False)
                
            selection.subtract(selectionC)
            
            # selection.border(strokeSize, strokeSize)
            
            # ##################################################
            
            if self.SmoothCheck.isChecked():
                selection.smooth()
        
        
            selectionArray = bytearray(selection.pixelData(bounds.x(), bounds.y(), bounds.width(), bounds.height()))
            
            colorArray = QColor(self.color)
            if self.ForeRadio.isChecked():
                colorArray = window.activeView().foregroundColor().colorForCanvas(canvas)
            elif self.BackRadio.isChecked():
                colorArray = window.activeView().backgroundColor().colorForCanvas(canvas)
            
            
            
            for i in range(0, len(selectionArray)):
                if selectionArray[i] > 0:
                    pixelArray[(i*4)] = colorArray.blue()
                    pixelArray[(i*4)+1] = colorArray.green()
                    pixelArray[(i*4)+2] = colorArray.red()
                    
                    if onOutside:
                        if pixelArray[(i*4) + 3] > 0:
                            pixelArray[(i*4) + 3] = 255 - pixelArray[(i*4) + 3]
                        else:
                            pixelArray[(i*4) + 3] = selectionArray[i]
                    elif self.InsideRadio.isChecked():
                        if pixelArray[(i*4) + 3] > 0 and pixelArray[(i*4) + 3] > selectionArray[i]:
                            pixelArray[(i*4) + 3] = selectionArray[i]
                        # else use pixelArray[(i*4) + 3]
                    else:
                        pixelArray[(i*4) + 3] = selectionArray[i]
                else:
                     pixelArray[(i*4) + 3] = 0
                    
        
        
            new_layer = document.createNode(layer.name() + "-stroke", "paintlayer")
            new_layer.setPixelData(bytes(pixelArray), bounds.x(), bounds.y(), bounds.width(), bounds.height())
            layer.parentNode().addChildNode(new_layer, layer)
        
        
            document.refreshProjection()
            return True
        else:
            QMessageBox.information(app.activeWindow().qwindow(), "Stroke Failed", "No Opaque Pixel found in layer.")
            return False

class STROKE_LAYER(Extension):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.strokeWindow = None

    def setup(self):
        pass
    
    def moveMenu(self):
        app = Krita.instance()
        qwindow = app.activeWindow().qwindow()
        menu_bar = qwindow.menuBar()
        actions = next(
            (a for a in menu_bar.actions() if a.objectName() == "edit"), None
        )
        
        if actions:
            menu = actions.menu()
            for actionEach in menu.actions():
                if actionEach.objectName() == "stroke_shapes":
                    menu.removeAction(self.strokeShow)
                    menu.insertAction(actionEach, self.strokeShow)
                    break
                    
    def createActions(self, window):
        self.strokeShow = window.createAction(
            "strokeLayer", "Add Stroke Layer...", "Edit"
        )
        
        self.strokeShow.triggered.connect(self.strokeLayer)
        
        QTimer.singleShot(0, self.moveMenu)
        
        
    def strokeLayer(self):
        app = Krita.instance()
        window = app.activeWindow()
        
        doc = app.activeDocument()
        view = window.activeView()

        if doc is None or view is None:
            QMessageBox.information(app.activeWindow().qwindow(), "Error", "No active document found.")
        else:
            if doc.activeNode():
                layer = doc.activeNode()
                
                if layer.type() == "paintlayer":
                    if self.strokeWindow and self.strokeWindow.isVisible():
                        self.strokeWindow.raise_()
                        self.strokeWindow.activateWindow()
                        return

                    self.strokeWindow = StrokeMenuShow()
                    self.strokeWindow.exec_()

                    # When menu is closed, reset the reference
                    self.strokeWindow = None
                else:
                     view.showFloatingMessage( "Stroke can only be used on Paint Layer", Krita.instance().icon( "paintLayer" ), 1000, 0 )
                
                
            else:
                view.showFloatingMessage( "No layer selected", Krita.instance().icon( "paintLayer" ), 1000, 0 )
                



Krita.instance().addExtension(STROKE_LAYER(Krita.instance()))
