"""
Se tendrá aquí el modelo para la gestión de países,
es decir todo aquello que tenga que ver con la persistencia
(SQL)
"""
from conexion import *
 
class Paises:
    def listar(self):
        sql = "SELECT * FROM paises"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
 
    def consultar(self, id):
        sql = f"SELECT * FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado
 
    def agregar(self, id, nombre, continente):
        sql = f"INSERT INTO paises (idPais, nombre, continente) VALUES ('{id}', '{nombre}', '{continente}')"
        mi_cursor.execute(sql)
        mi_db.commit()
 
    def modificar(self, id, nombre, continente):
        sql = f"UPDATE paises SET nombre='{nombre}', continente='{continente}' WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)
 
    def eliminar(self, id):
        sql = f"DELETE FROM paises WHERE idPais='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
 
mis_paises = Paises()