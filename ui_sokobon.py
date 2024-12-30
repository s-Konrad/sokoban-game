# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'game_window.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_gameWindow(object):
    def setupUi(self, gameWindow):
        if not gameWindow.objectName():
            gameWindow.setObjectName(u"gameWindow")
        gameWindow.resize(460, 558)
        gameWindow.setAutoFillBackground(False)
        gameWindow.setStyleSheet(u"QWidget#levelView {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(32, 96, 210, 255), stop:1 rgba(255, 255, 255, 255));}")
        self.verticalLayout = QVBoxLayout(gameWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.levelLabel = QLabel(gameWindow)
        self.levelLabel.setObjectName(u"levelLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.levelLabel.sizePolicy().hasHeightForWidth())
        self.levelLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.levelLabel)

        self.moveCounter = QLabel(gameWindow)
        self.moveCounter.setObjectName(u"moveCounter")

        self.horizontalLayout.addWidget(self.moveCounter)

        self.undoButton = QPushButton(gameWindow)
        self.undoButton.setObjectName(u"undoButton")

        self.horizontalLayout.addWidget(self.undoButton)

        self.resetButton = QPushButton(gameWindow)
        self.resetButton.setObjectName(u"resetButton")

        self.horizontalLayout.addWidget(self.resetButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.levelView = QGraphicsView(gameWindow)
        self.levelView.setObjectName(u"levelView")

        self.verticalLayout.addWidget(self.levelView)


        self.retranslateUi(gameWindow)

        QMetaObject.connectSlotsByName(gameWindow)
    # setupUi

    def retranslateUi(self, gameWindow):
        gameWindow.setWindowTitle(QCoreApplication.translate("gameWindow", u"Form", None))
        self.levelLabel.setText(QCoreApplication.translate("gameWindow", u"Level: ", None))
        self.moveCounter.setText(QCoreApplication.translate("gameWindow", u"TextLabel", None))
        self.undoButton.setText(QCoreApplication.translate("gameWindow", u"Undo - (U)", None))
        self.resetButton.setText(QCoreApplication.translate("gameWindow", u"Restart - (R)", None))
    # retranslateUi

