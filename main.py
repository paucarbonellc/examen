import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem,
    QAbstractItemView, QHeaderView
)
from PySide6.QtUiTools import QUiLoader
from database import Database


class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.modal = False
        self.confirm = False
        self.action = False
        self.loader = QUiLoader()
        self.init_modals()
        interface_path = os.path.join(os.path.dirname(__file__), "interface.ui")
        self.ui = self.loader.load(interface_path, None)
        self.db = Database()

        # Configuració del QTableWidget:

        # Amagar la columna ID (columna 0)
        self.ui.tableWidget.setColumnHidden(0, True)

        # Seleccionar tota la fila quan es fa clic
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Deshabilitar l'edició directa a la taula
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Configurar el redimensionament de les columnes:
        # Indiquem que la columna del nom (columna 1) s'estiri per omplir l'espai
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        # I que les columnes de preu (columna 2) i quantitat (columna 3) es redimensionin en funció del seu contingut
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.load_products()

        # Assignació dels botons i esdeveniments
        # self.ui.btnAfegir.clicked.connect(self.add_product)
        # self.ui.btnModificar.clicked.connect(self.update_product)
        self.ui.btnEliminar.clicked.connect(self.show_delete_confirm)
        self.ui.btnAfegir.clicked.connect(self.show_window)
        self.ui.tableWidget.itemSelectionChanged.connect(self.load_selected_product)

        self.ui.show()

    def show_delete_confirm(self):
        self.show_confirm(action=self.delete_product)

    def show_window(self):
        self.modal.show()
        self.clear_inputs()
    
    def init_modals(self):
        loader = QUiLoader()
        if self.modal == False:
            self.modal = loader.load(os.path.join(os.path.dirname(__file__), "modal.ui"), None)
            self.modal.btnAfegir.clicked.connect(self.add_product)
            self.modal.btnModificar.clicked.connect(self.show_mofify_confirm)

    def show_mofify_confirm(self):
        self.show_confirm(action=self.update_product)

    def show_confirm(self, action):
        loader = QUiLoader()
        if self.confirm == False:
            self.confirm = loader.load(os.path.join(os.path.dirname(__file__), "confirm.ui"), None)
            self.confirm.cancel.clicked.connect(self.confirm.close)
            self.confirm.accept.clicked.connect(self.confirm_action)

        self.action = action
        self.confirm.show()

    def confirm_action(self):
        if self.action == False:
            return

        self.action()
        self.confirm.close()
        self.action = False


    def load_products(self):
        """Carrega els productes a la taula."""
        self.ui.tableWidget.setRowCount(0)
        products = self.db.get_all_products()

        for row_index, product in enumerate(products):
            self.ui.tableWidget.insertRow(row_index)
            for col_index, data in enumerate(product):
                self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def add_product(self):
        """Afegeix un nou producte."""
        nom = self.modal.txtNom.text()
        preu = self.modal.txtPreu.text()
        quantitat = self.modal.txtQuantitat.text()

        if nom and preu and quantitat:
            self.db.add_product(nom, float(preu), int(quantitat))
            self.load_products()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Tots els camps són obligatoris")

    def update_product(self):
        """Modifica el producte seleccionat."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un producte per modificar")
            return

        product_id = int(self.ui.tableWidget.item(selected_row, 0).text())
        nom = self.modal.txtNom.text()
        preu = self.modal.txtPreu.text()
        quantitat = self.modal.txtQuantitat.text()

        if nom and preu and quantitat:
            self.db.update_product(product_id, nom, float(preu), int(quantitat))
            self.load_products()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Error", "Tots els camps són obligatoris")

    def delete_product(self):
        """Elimina el producte seleccionat."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un producte per eliminar")
            return

        product_id = int(self.ui.tableWidget.item(selected_row, 0).text())
        self.db.delete_product(product_id)
        self.load_products()
        self.clear_inputs()

    def load_selected_product(self):
        """Carrega les dades del producte seleccionat als camps d’entrada."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row != -1:
            self.modal.txtNom.setText(self.ui.tableWidget.item(selected_row, 1).text())
            self.modal.txtPreu.setText(self.ui.tableWidget.item(selected_row, 2).text())
            self.modal.txtQuantitat.setValue(int(self.ui.tableWidget.item(selected_row, 3).text()))

    def clear_inputs(self):
        """Buida els camps d’entrada."""
        self.modal.txtNom.clear()
        self.modal.txtPreu.clear()
        self.modal.txtQuantitat.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    sys.exit(app.exec())
