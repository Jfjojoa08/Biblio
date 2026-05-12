from conexion import *
import pytest

class Test_editoriales:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5083/editoriales"
        # Insertar país de apoyo para la FK (si no existe)
        sql_pais = "INSERT IGNORE INTO paises (idPais, nombre, continente) VALUES ('CO', 'Colombia', 'America')"
        mi_cursor.execute(sql_pais)
        mi_db.commit()
        # Insertar editorial de prueba base
        id = "ED001"
        nombre = "Norma"
        idPais = "CO"
        sql = f"INSERT INTO editoriales (idEditorial, nombre, idPais) VALUES ('{id}', '{nombre}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = "DELETE FROM editoriales WHERE idEditorial='ED001'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_editoriales(self):
        esperado = "editoriales"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "ED002", "nombre": "Planeta", "idPais": "CO"}, "Editorial agregada con éxito"),
            ({"id": "ED001", "nombre": "Norma",   "idPais": "CO"}, "Id de editorial ya existe")
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url, json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]
        if calculado.json()["mensaje"] == "Editorial agregada con éxito":
            id = nuevo_entrada["id"]
            sql = f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
            mi_cursor.execute(sql)
            datos = mi_cursor.fetchall()[0]
            assert datos[1] == "Planeta"

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("ED001", "Editorial encontrada"),
            ("ED999", "Editorial no encontrada")
        ]
    )
    def test_busqueda(self, id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    # Para cuando la editorial existe y se modifica con éxito
    def test_modifica1(self):
        id = "ED001"
        nombre = "Editorial Norma S.A."
        idPais = "CO"
        nuevo = {"id": id, "nombre": nombre, "idPais": idPais}
        esperado = "Editorial modificada con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre == datos[1] and idPais == datos[2]

    # Para cuando la editorial no existe
    def test_modifica2(self):
        id = "ED999"
        nombre = "Editorial Fantasma"
        idPais = "CO"
        nuevo = {"id": id, "nombre": nombre, "idPais": idPais}
        esperado = "Editorial no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("ED002", "Editorial eliminada con éxito!"),
            ("ED999", "Editorial no existe")
        ]
    )
    def test_elimina(self, id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0