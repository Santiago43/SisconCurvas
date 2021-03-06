import mysql.connector
from mysql.connector import errorcode
from dao.dao import dao
from dao.models import Origen
class OrigenDao(dao):
    """
    Clase de objeto de acceso a datos que maneja los orígenes en general
    """
    def consultarOrigenes(self):
        """
        Método que permite hacer la consulta de todos los orígenes (de venta, no empaque, no despacho, no distribución)
        """
        cnx=super().connectDB()
        cursor=cnx.cursor()
        try:
            sql= 'select * from Origen;'
            cursor.execute(sql)
            results=cursor.fetchall()
            origenes=list()
            for result in results:
                origen=Origen(result[0],result[1])
                origenes.append(origen)
            super().cerrarConexion(cursor,cnx)
            return origenes
        except Exception as e:
            super().cerrarConexion(cursor,cnx)
            raise e
    def consultarOrigen(self,id):
        """
        Método que permite hacer la consulta de un origen mediante su ID
        """
        cnx=super().connectDB()
        cursor=cnx.cursor()
        try:
            sql= 'select * from Origen where Origen_ID=%s;'
            cursor.execute(sql,(id,))
            result=cursor.fetchone()
            origen=None
            if result is not None:
                origen=Origen(result[0],result[1])
            super().cerrarConexion(cursor,cnx)
            return origen
        except Exception as e:
            super().cerrarConexion(cursor,cnx)
            raise e