# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLayout,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Menu(object):
    def setupUi(self, Menu):
        if not Menu.objectName():
            Menu.setObjectName(u"Menu")
        Menu.resize(400, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Menu.sizePolicy().hasHeightForWidth())
        Menu.setSizePolicy(sizePolicy)
        Menu.setBaseSize(QSize(400, 0))
        Menu.setAutoFillBackground(False)
        Menu.setStyleSheet(u"QWidget#PlayButton {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(32, 96, 210, 255), stop:1 rgba(255, 255, 255, 255))}\n"
"QWidget#QuitButton {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(32, 96, 210, 255), stop:1 rgba(255, 255, 255, 255))}\n"
"QWidget#label {font:  22pt}\n"
"")
        self.horizontalLayout = QHBoxLayout(Menu)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer = QSpacerItem(141, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.label = QLabel(Menu)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 80))
        self.label.setText(u"Sokoban")
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout.addWidget(self.label)

        self.PlayButton = QPushButton(Menu)
        self.PlayButton.setObjectName(u"PlayButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PlayButton.sizePolicy().hasHeightForWidth())
        self.PlayButton.setSizePolicy(sizePolicy1)
        self.PlayButton.setMinimumSize(QSize(80, 25))
        self.PlayButton.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout.addWidget(self.PlayButton)

        self.QuitButton = QPushButton(Menu)
        self.QuitButton.setObjectName(u"QuitButton")
        sizePolicy1.setHeightForWidth(self.QuitButton.sizePolicy().hasHeightForWidth())
        self.QuitButton.setSizePolicy(sizePolicy1)
        self.QuitButton.setLayoutDirection(Qt.LeftToRight)
        self.QuitButton.setAutoFillBackground(False)

        self.verticalLayout.addWidget(self.QuitButton)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.retranslateUi(Menu)

        QMetaObject.connectSlotsByName(Menu)
    # setupUi

    def retranslateUi(self, Menu):
        Menu.setWindowTitle(QCoreApplication.translate("Menu", u"Menu", None))
        self.PlayButton.setText(QCoreApplication.translate("Menu", u"Play", None))
        self.QuitButton.setText(QCoreApplication.translate("Menu", u"Quit", None))
    # retranslateUi

