"""
Se tendrá aquí el modelo para la gestión de editoriales,
es decir todo aquello que tenga que ver con la persistencia
(SQL)
"""
from conexion import *

class Editoriales:
    def listar(self):
        sql = "SELECT * FROM editoriales"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def consultar(self, id):
        sql = f"SELECT * FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        resultado = mi_cursor.fetchall()
        return resultado

    def agregar(self, id, nombre, idPais):
        sql = f"INSERT INTO editoriales (idEditorial, nombre, idPais) VALUES ('{id}', '{nombre}', '{idPais}')"
        mi_cursor.execute(sql)
        mi_db.commit()

    def modificar(self, id, nombre, idPais):
        sql = f"UPDATE editoriales SET nombre='{nombre}', idPais='{idPais}' WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()
        return self.consultar(id)

    def eliminar(self, id):
        sql = f"DELETE FROM editoriales WHERE idEditorial='{id}'"
        mi_cursor.execute(sql)
        mi_db.commit()

mis_editoriales = Editoriales()
