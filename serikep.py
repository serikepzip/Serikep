import os
import sys
import zipfile
import py7zr
import rarfile
import tarfile
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from pyqtribbon import RibbonBar, RibbonStyle

class SerikepApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Serikep - Zipper and Archiver")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(200, 200, 800, 600)

        # Setup Ribbon UI
        ribbon = RibbonBar(maxRows=6)
        ribbon.setRibbonStyle(RibbonStyle.Default)
        self.setMenuBar(ribbon)

        # Main widget and layout
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        central_widget.setLayout(layout)

        # Welcome Web View
        self.web_view = QWebEngineView()
        welcome_path = os.path.abspath("welcome.html")
        self.web_view.load(QtCore.QUrl.fromLocalFile(welcome_path))
        layout.addWidget(self.web_view)

        # Ribbon: File Operations
        file_category = ribbon.addCategory("File Operations")
        file_panel = file_category.addPanel("Zipping and Archiving", showPanelOptionButton=False)

        zip_button = file_panel.addLargeButton("Zip Folder", icon=QIcon("icons/zip_icon.png"))
        zip_button.clicked.connect(self.zip_folder)

        rar_button = file_panel.addLargeButton("Rar Folder", icon=QIcon("icons/rar_icon.png"))
        rar_button.clicked.connect(self.rar_folder)

        seven_zip_button = file_panel.addLargeButton("7z Folder", icon=QIcon("icons/sevenzip_icon.png"))
        seven_zip_button.clicked.connect(self.seven_zip_folder)

        tar_button = file_panel.addLargeButton("Tar Folder", icon=QIcon("icons/tar_icon.png"))
        tar_button.clicked.connect(self.tar_folder)

        # Ribbon: Help
        help_category = ribbon.addCategory("Help")
        help_panel = help_category.addPanel("Archiving Help", showPanelOptionButton=False)

        help_button = help_panel.addLargeButton("How to Use", icon=QIcon("icons/help_icon.png"))
        help_button.clicked.connect(self.show_help)

        website_panel = help_category.addPanel("Website", showPanelOptionButton=False)
        website_button = website_panel.addLargeButton("Open Website", icon=QIcon("icons/web_icon.png"))
        website_button.clicked.connect(self.open_website)

        self.show()

    def zip_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder to Zip")
        if folder_path:
            zip_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Zip File", "", "Zip Files (*.zip)")
            if zip_filename:
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(file_path, folder_path))
                QtWidgets.QMessageBox.information(self, "Success", "Folder successfully zipped!")

    def rar_folder(self):
        QtWidgets.QMessageBox.warning(self, "Unavailable", "We are sorry but RAR Writing doesnt work we will fix this issue on the next update")
        # RAR writing is not supported until the next update

    def seven_zip_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder to 7z")
        if folder_path:
            seven_zip_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save 7z File", "", "7z Files (*.7z)")
            if seven_zip_filename:
                with py7zr.SevenZipFile(seven_zip_filename, 'w') as archive:
                    archive.writeall(folder_path, os.path.basename(folder_path))
                QtWidgets.QMessageBox.information(self, "Success", "Folder successfully archived as 7z!")

    def tar_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder to Tar")
        if folder_path:
            tar_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Tar File", "", "Tar Files (*.tar)")
            if tar_filename:
                with tarfile.open(tar_filename, 'w') as tarf:
                    tarf.add(folder_path, arcname=os.path.basename(folder_path))
                QtWidgets.QMessageBox.information(self, "Success", "Folder successfully archived as Tar!")

    def show_help(self):
        QtWidgets.QMessageBox.information(
            self,
            "How to Use",
            "To archive a folder:\n\n"
            "- Click the appropriate format button (Zip, 7z, Tar).\n"
            "- Select a folder to archive.\n"
            "- Choose where to save the archive.\n\n"
            "RAR support is not working we will fix this issue in the next update"
        )

    def open_website(self):
        webbrowser.open("https://serikepzip.github.io") 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    app.setStyle("Fusion")

    window = SerikepApp()
    sys.exit(app.exec_())

