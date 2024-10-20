import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox # type: ignore
from service.converter import Converter
from model.geographicCord import GeographicCord
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt  # Import Qt here
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from model.cartesien import Cartesien

class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()

        self.converter = Converter()

        # Set up the layout
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle("Coordinate Converter")
        self.setFixedSize(400, 400)

        # Main layout
        layout = QVBoxLayout()

        # Stylesheet for the entire window
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                border: 2px solid #a0a0a0;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Conversion type combo box
        self.conversion_type = QComboBox(self)
        self.conversion_type.addItem("Geographic to Cartesian")
        self.conversion_type.addItem("Cartesian to Geographic")
        self.conversion_type.currentIndexChanged.connect(self.update_fields)
        layout.addWidget(self.conversion_type)

        # Latitude/X input
        self.latitude_input = QLineEdit(self)
        self.latitude_input.setPlaceholderText("Enter Latitude or X")
        layout.addWidget(QLabel("Latitude/X:"))
        layout.addWidget(self.latitude_input)

        # Longitude/Y input
        self.longitude_input = QLineEdit(self)
        self.longitude_input.setPlaceholderText("Enter Longitude or Y")
        layout.addWidget(QLabel("Longitude/Y:"))
        layout.addWidget(self.longitude_input)

        # Altitude/Z input
        self.altitude_input = QLineEdit(self)
        self.altitude_input.setPlaceholderText("Enter Altitude or Z")
        layout.addWidget(QLabel("Altitude/Z:"))
        layout.addWidget(self.altitude_input)

        # Convert button
        convert_button = QPushButton("Convert", self)
        convert_button.clicked.connect(self.convert)
        layout.addWidget(convert_button)

        # Result label
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def update_fields(self):
        # Update placeholders based on conversion type
        if self.conversion_type.currentText() == "Geographic to Cartesian":
            self.latitude_input.setPlaceholderText("Enter Latitude")
            self.longitude_input.setPlaceholderText("Enter Longitude")
            self.altitude_input.setPlaceholderText("Enter Altitude")
        else:
            self.latitude_input.setPlaceholderText("Enter X")
            self.longitude_input.setPlaceholderText("Enter Y")
            self.altitude_input.setPlaceholderText("Enter Z")

    def convert(self):
        # Determine the conversion type
        if self.conversion_type.currentText() == "Geographic to Cartesian":
            self.convert_to_cartesian()
        else:
            self.convert_to_geographic()

    def convert_to_cartesian(self):
        try:
            latitude = float(self.latitude_input.text())
            longitude = float(self.longitude_input.text())
            altitude = float(self.altitude_input.text())

            # Create GeographicCord object
            geographic_coord = GeographicCord(latitude, longitude, altitude)

            # Convert to Cartesian coordinates
            X, Y, Z = self.converter.converterToCartesien(geographic_coord)

            # Display the results in the result_label
            self.result_label.setText(f"X: {X:.2f}\nY: {Y:.2f}\nZ: {Z:.2f}")
            self.result_label.setStyleSheet("font-weight: bold; color: #2e8b57;")
        except ValueError:
            self.result_label.setText("Please enter valid numerical values.")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")

    def convert_to_geographic(self):
        try:
            X = float(self.latitude_input.text())
            Y = float(self.longitude_input.text())
            Z = float(self.altitude_input.text())

            # Create Cartesien object
            cartesian_coord = Cartesien(X, Y, Z)

            # Convert to Geographic coordinates
            latitude, longitude, altitude = self.converter.converterToGeographic(cartesian_coord)

            # Display the results in the result_label
            self.result_label.setText(f"Latitude: {latitude:.6f}\nLongitude: {longitude:.6f}\nAltitude: {altitude:.2f}")
            self.result_label.setStyleSheet("font-weight: bold; color: #2e8b57;")
        except ValueError:
            self.result_label.setText("Please enter valid numerical values.")
            self.result_label.setStyleSheet("color: red; font-weight: bold;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConverterApp()
    window.show()
    sys.exit(app.exec_())
