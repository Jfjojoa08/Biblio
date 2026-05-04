from conexion import *
import pytest

class Test_usuarios:

    def setup_class(self):
        # Preparación del entorno de las pruebas
        self.url = "http://localhost:5080/usuarios"
        id = "final881"
        nombre = "Fidel Nalisco"
        contra = hashlib.sha512("4321".encode("UTF-8")).hexdigest()
        sql = f"INSERT INTO usuarios (idUsuario,nombre,contrasena) VALUES ('{id}','{nombre}','{contra}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def teardown_class(self):
        # Limpia la base de datos
        sql = f"DELETE FROM usuarios WHERE idUsuario='final881'"
        mi_cursor.execute(sql)
        mi_db.commit()

    def test_lista_usuarios(self):
        esperado = "usuarios"
        # Ejecutar la prueba
        calculado = requests.get(self.url)
        # Verificación
        assert calculado.status_code == 200
        assert calculado.json()["mensaje"]==esperado
    
    @pytest.mark.parametrize(
        ["nuevo_entrada","esperado_entrada"],
        [({"id":"test2026", "nombre":"Usuario Pruebas","contrasena":"6666"},"Usuario agregado con éxito"),
         ({"id":"final881", "nombre":"Fidel Nalisco", "contrasena":"1111"},"Id de usuario ya existe")]
    )
    def test_agregar(self,nuevo_entrada,esperado_entrada):
        contra = hashlib.sha512(nuevo_entrada["contrasena"].encode("UTF-8")).hexdigest()
        nuevo_entrada["contrasena"] = contra
        # Ejecutar la prueba
        calculado = requests.post(self.url,json=nuevo_entrada)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado_entrada == calculado.json()["mensaje"]
#        if calculado.json()["mensaje"]=="Usuario agregado con éxito":
#            sql =f"SELECT * FROM usuarios WHERE idUsuario='{nuevo_entrada["id"]}'"
#            mi_cursor.execute(sql)
#            datos = mi_cursor.fetchall()[0]
#            assert datos[1]=="Usuario Pruebas"

    @pytest.mark.parametrize(
        ["id_entrada","contra_entrada","esperado_entrada"],
        [("final881","4321",{"mensaje":"Bienvenido Fidel Nalisco"}),
         ("final881","1234",{"mensaje":"Credenciales inválidas"}),
         ("118final","hgtr",{"mensaje":"Credenciales inválidas"})]
    )
    def test_login(self,id_entrada,contra_entrada,esperado_entrada):
        id = id_entrada
        contra = hashlib.sha512(contra_entrada.encode("UTF-8")).hexdigest()
        esperado = esperado_entrada
        # Ejecutar la prueba
        usuario = {"id":id, "contra":contra}
        calculado = requests.post(f"{self.url}/{id}",json=usuario)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert calculado.json() == esperado

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("final881","Usuario encontrado"),
         ("118final","Usuario no encontrado")]
    )
    def test_busqueda(self,id_entrada,esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.get(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    # Para cuando el usuario existe y se modifica con éxito
    def test_modifica1(self):
        id = "final881"
        nombre = "Fidelino Nalisco"
        contra = hashlib.sha512("4321".encode("UTF-8")).hexdigest()
        nuevo = {"id":id, "nombre":nombre, "contrasena":contra}
        esperado = "Usuario modificado con éxito"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        sql =f"SELECT * FROM usuarios WHERE idUsuario='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()[0]
        assert nombre==datos[1] and contra==datos[2]

# Para cuando el usuario no existe
    def test_modifica2(self):
        id = "testfail"
        nombre = "Fidelino Nalisco"
        contra = hashlib.sha512("9876".encode("UTF-8")).hexdigest()
        nuevo = {"id":id, "nombre":nombre, "contrasena":contra}
        esperado = "Usuario no existe"
        # Ejecutar la prueba
        calculado = requests.put(f"{self.url}/{id}",json=nuevo)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]

    @pytest.mark.parametrize(
        ["id_entrada","esperado_entrada"],
        [("test2026","Usuario eliminado con éxito!"),
         ("testfail","Usuario no existe")]
    )
    def test_elimina(self,id_entrada, esperado_entrada):
        id = id_entrada
        esperado = esperado_entrada
        # Ejecutar la prueba
        calculado = requests.delete(f"{self.url}/{id}")
        # Verificar la prueba
        assert calculado.status_code == 200
        assert esperado in calculado.json()["mensaje"]
        mi_db.commit()
        sql =f"SELECT * FROM usuarios WHERE idUsuario='{id}'"
        mi_cursor.execute(sql)
        datos = mi_cursor.fetchall()
        assert len(datos)==0
    
    



"""
    def test_login1(self):
        id = "final881"
        contra = hashlib.sha512("4321".encode("UTF-8")).hexdigest()
        esperado = {"mensaje":"Bienvenido Fidel Nalisco"}
        # Ejecutar la prueba
        usuario = {"id":id, "contra":contra}
        calculado = requests.post(f"{self.url}/{id}",json=usuario)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert calculado.json() == esperado

    def test_login2(self):
        id = "final881"
        contra = hashlib.sha512("1234".encode("UTF-8")).hexdigest()
        esperado = {"mensaje":"Credenciales inválidas"}
        # Ejecutar la prueba
        usuario = {"id":id, "contra":contra}
        calculado = requests.post(f"{self.url}/{id}",json=usuario)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert calculado.json() == esperado
    def test_login3(self):
        id = "final188"
        contra = hashlib.sha512("1234".encode("UTF-8")).hexdigest()
        esperado = {"mensaje":"Credenciales inválidas"}
        # Ejecutar la prueba
        usuario = {"id":id, "contra":contra}
        calculado = requests.post(f"{self.url}/{id}",json=usuario)
        # Verificar la prueba
        assert calculado.status_code == 200
        assert calculado.json() == esperado
"""