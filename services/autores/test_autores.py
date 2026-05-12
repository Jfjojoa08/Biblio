from conexion import *
import pytest

class Test_autores:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5082/autores"
        # Insertar país de apoyo para la FK (si no existe)
        sql_pais = "INSERT IGNORE INTO paises (idPais, nombre, continente) VALUES ('CO', 'Colombia', 'America')"
        mi_cursor.execute(sql_pais)
        mi_db.commit()
        # Insertar autor de prueba base
        id = "autor001"
        nombre = "Gabriel García"
        email = "ggarcia@email.com"
        idPais = "CO"
        sql = f"INSERT INTO autores (idAutor, nombre, email, idPais) VALUES ('{id}', '{nombre}', '{email}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = "DELETE FROM autores WHERE idAutor='autor001'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_autores(self):
        esperado = "autores"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"] == esperado

    @pytest.mark.parametrize(
        ["nuevo_entrada", "esperado_entrada"],
        [
            ({"id": "autor002", "nombre": "Andrés Caicedo", "email": "acaicedo@email.com", "idPais": "CO"}, "Autor agregado con éxito"),
            ({"id": "autor001", "nombre": "Gabriel García", "email": "ggarcia@email.com", "idPais": "CO"}, "Id de autor ya existe")
        ]
    )
    def test_agregar(self, nuevo_entrada, esperado_entrada):
        # Ejecutar la prueba
        calculado = requests.post(self.url, json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]
        if calculado.json()["mensaje"] == "Autor agregado con éxito":
            id = nuevo_entrada["id"]
            sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
            mi_cursor.execute(sql)
            datos = mi_cursor.fetchall()[0]
            assert datos[1] == "Andrés Caicedo"

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("autor001", "Autor encontrado"),
            ("autor999", "Autor no encontrado")
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

    # Para cuando el autor existe y se modifica con éxito
    def test_modifica1(self):
        id = "autor001"
        nombre = "Gabriel García Márquez"
        email = "ggmarquez@email.com"
        idPais = "CO"
        nuevo = {"id": id, "nombre": nombre, "email": email, "idPais": idPais}
        esperado = "Autor modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        mi_db.commit()
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre == datos[1] and email == datos[2]

    # Para cuando el autor no existe
    def test_modifica2(self):
        id = "autor999"
        nombre = "Nadie Nadie"
        email = "nadie@email.com"
        idPais = "CO"
        nuevo = {"id": id, "nombre": nombre, "email": email, "idPais": idPais}
        esperado = "Autor no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}", json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada", "esperado_entrada"],
        [
            ("autor002", "Autor eliminado con éxito!"),
            ("autor999", "Autor no existe")
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
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos) == 0