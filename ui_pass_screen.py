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
        self.verticalLayout = QVBoxLayout(PassWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.winLabel = QLabel(PassWindow)
        self.winLabel.setObjectName(u"winLabel")

        self.horizontalLayout.addWidget(self.winLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(PassWindow)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.moveCounter = QLabel(PassWindow)
        self.moveCounter.setObjectName(u"moveCounter")

        self.horizontalLayout.addWidget(self.moveCounter)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.nextLevelButton = QPushButton(PassWindow)
        self.nextLevelButton.setObjectName(u"nextLevelButton")

        self.verticalLayout.addWidget(self.nextLevelButton)


        self.retranslateUi(PassWindow)

        QMetaObject.connectSlotsByName(PassWindow)
    # setupUi

    def retranslateUi(self, PassWindow):
        PassWindow.setWindowTitle(QCoreApplication.translate("PassWindow", u"PassWindow", None))
        self.winLabel.setText(QCoreApplication.translate("PassWindow", u"Congratulations!", None))
        self.label_2.setText(QCoreApplication.translate("PassWindow", u"You finished in ", None))
        self.moveCounter.setText(QCoreApplication.translate("PassWindow", u"999", None))
        self.nextLevelButton.setText(QCoreApplication.translate("PassWindow", u"Next Level ->", None))
    # retranslateUi

