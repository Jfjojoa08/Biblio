"""
Se tendrá aquí el modelo para la gestión de autores,
es decir todo aquello que tenga que ver con la persistencia
(SQL)
"""
from conexion import *

class Autores:
    def listar(self):
        sql = "SELECT * FROM autores"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        sql = f"SELECT * FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, nombre, email, idPais):
        sql = f"INSERT INTO autores (idAutor, nombre, email, idPais) VALUES ('{id}', '{nombre}', '{email}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, nombre, email, idPais):
        sql = f"UPDATE autores SET nombre='{nombre}', email='{email}', idPais='{idPais}' WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        sql = f"DELETE FROM autores WHERE idAutor='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mis_autores = Autores()