import pytest
from PySide6.QtWidgets import QApplication
from PySide6 import QtCore
from main import ProductApp
from database import Database

@pytest.fixture
def app(qtbot):
    test_app = ProductApp()
    qtbot.addWidget(test_app.ui)
    return test_app

@pytest.fixture
def db():
    return Database()

def test_add_product(app, qtbot, db):
    app.modal.txtNom.setText("1")
    app.modal.txtPreu.setText("1")
    app.modal.txtQuantitat.setValue(2)
    
    qtbot.mouseClick(app.modal.btnAfegir, QtCore.Qt.LeftButton)
    qtbot.wait(500)
    
    products = db.get_all_products()
    assert any(p[1] == "1" and p[2] == 1 and p[3] == 2 for p in products)
    
    table_items = [app.ui.tableWidget.item(row, 1).text() for row in range(app.ui.tableWidget.rowCount())]
    assert "1" in table_items

def test_update_product(app, qtbot, db):
    if app.ui.tableWidget.rowCount() == 0:
        pytest.skip("No hay productos que actualizar")
    
    app.ui.tableWidget.selectRow(0)
    qtbot.wait(500)
    
    app.show_window()
    app.modal.txtNom.setText("3")
    app.modal.txtPreu.setText("2")
    app.modal.txtQuantitat.setValue(1)
    
    qtbot.mouseClick(app.modal.btnModificar, QtCore.Qt.LeftButton)
    qtbot.wait(500)
    
    products = db.get_all_products()
    assert any(p[1] == "3" and p[2] == 2 and p[3] == 1 for p in products)

    table_items = [app.ui.tableWidget.item(row, 1).text() for row in range(app.ui.tableWidget.rowCount())]
    assert "3" in table_items

def test_delete_product(app, qtbot, db):
    if app.ui.tableWidget.rowCount() == 0:
        pytest.skip("No hya productos que eliminar")
    
    app.ui.tableWidget.selectRow(0)
    qtbot.wait(500)
    
    qtbot.mouseClick(app.ui.btnEliminar, QtCore.Qt.LeftButton)
    qtbot.wait(500)
    
    products = db.get_all_products()
    assert len(products) == app.ui.tableWidget.rowCount()
    
    assert app.ui.tableWidget.rowCount() == len(products)
