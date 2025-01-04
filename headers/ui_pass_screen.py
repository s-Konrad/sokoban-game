# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'level_pass.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_PassWindow(object):
    def setupUi(self, PassWindow):
        if not PassWindow.objectName():
            PassWindow.setObjectName(u"PassWindow")
        PassWindow.resize(400, 300)
        PassWindow.setLayoutDirection(Qt.LeftToRight)
        PassWindow.setStyleSheet(u"QWidget#nextLevelButton{background-color: qradialgradient(spread:repeat, cx:0.5, cy:0.5, radius:0.077, fx:0.5, fy:0.5, stop:0 rgba(0, 169, 255, 147), stop:0.497326 rgba(0, 0, 0, 0), stop:1 rgba(0, 169, 255, 147))}")
        self.verticalLayout = QVBoxLayout(PassWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.winLabel = QLabel(PassWindow)
        self.winLabel.setObjectName(u"winLabel")
        self.winLabel.setStyleSheet(u"QWidget#winLabel {font: 22pt}")
        self.winLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.winLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.moveCounter = QLabel(PassWindow)
        self.moveCounter.setObjectName(u"moveCounter")

        self.horizontalLayout.addWidget(self.moveCounter, 0, Qt.AlignHCenter)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.nextLevelButton = QPushButton(PassWindow)
        self.nextLevelButton.setObjectName(u"nextLevelButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nextLevelButton.sizePolicy().hasHeightForWidth())
        self.nextLevelButton.setSizePolicy(sizePolicy)
        self.nextLevelButton.setMinimumSize(QSize(100, 0))
        self.nextLevelButton.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_2.addWidget(self.nextLevelButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(PassWindow)

        QMetaObject.connectSlotsByName(PassWindow)
    # setupUi

    def retranslateUi(self, PassWindow):
        PassWindow.setWindowTitle(QCoreApplication.translate("PassWindow", u"PassWindow", None))
        self.winLabel.setText(QCoreApplication.translate("PassWindow", u"Congratulations!", None))
        self.moveCounter.setText(QCoreApplication.translate("PassWindow", u"999", None))
        self.nextLevelButton.setText(QCoreApplication.translate("PassWindow", u"Next Level ->", None))
    # retranslateUi

