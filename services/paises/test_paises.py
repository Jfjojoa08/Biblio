from conexion import *
import pytest

class Test_paises:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5081/paises"
        id = "CO"
        nombre = "Colombia"
        continente = "America"
        sql = f"INSERT INTO paises (idPais, nombre, continente) VALUES ('{id}', '{nombre}', '{continente}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = "DELETE FROM paises WHERE idPais='CO'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_paises(self):
        esperado = "paises"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "AR", "nombre": "Argentina", "continente": "America"}, "País agregado con éxito"),
            ({"id": "CO", "nombre": "Colombia",  "continente": "America"}, "Id de país ya existe")
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url, json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]
        if calculado.json()["mensaje"] == "País agregado con éxito":
            id = nuevo_entrada["id"]
            sql = f"SELECT * FROM paises WHERE idPais='{id}'"
            mi_cursor.execute(sql)
            datos = mi_cursor.fetchall()[0]
            assert datos[1] == "Argentina"

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("CO", "País encontrado"),
            ("ZZ", "País no encontrado")
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

    # Para cuando el país existe y se modifica con éxito
    def test_modifica1(self):
        id = "CO"
        nombre = "República de Colombia"
        continente = "America"
        nuevo = {"id": id, "nombre": nombre, "continente": continente}
        esperado = "País modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre == datos[1] and continente == datos[2]

    # Para cuando el país no existe
    def test_modifica2(self):
        id = "ZZ"
        nombre = "País Inexistente"
        continente = "Ninguno"
        nuevo = {"id": id, "nombre": nombre, "continente": continente}
        esperado = "País no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("AR", "País eliminado con éxito!"),
            ("ZZ", "País no existe")
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
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0