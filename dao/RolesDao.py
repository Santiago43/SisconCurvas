import mysql.connector
from mysql.connector import errorcode
from dao.dao import dao
from dao.models import Rol
from dao.models import Permiso
class RolesDao(dao):
    """
    Clase de objeto de acceso a datos que maneja los roles y sus permisos
    """
    def crearRol(self,rol):
        """
        Método que permite hacer el registro de un rol
        Parámetros:
        - rol : que es el rol que se registrará 
        """
        try:
            sql= "insert into Rol (Nombre) values (%s);"
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql,(rol.nombre,))
            cnx.commit()
            super().cerrarConexion(cursor,cnx)
            return True
        except Exception as e:
            raise e

    def consultarRol(self,id):
        """
        Método que permite consultar un rol mediante su ID
        Parámetros:
        - id : que es el ID de rol 
        """
        try:
            sql= "select * from Rol where Rol_ID="+str(id)+";"
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            rol = Rol(result[0],result[1],list())
            sql2='select p.* from Rol_tiene_Permiso as rp inner join Rol as r on r.Rol_ID=rp.Rol_ID inner join Permiso as p on p.Permiso_ID=rp.Permiso_ID where r.Rol_ID='+str(id)+';'
            cursor.execute(sql2)
            for row in cursor:
                rol.permisos.append(Permiso(row[0],row[1]))
            super().cerrarConexion(cursor,cnx)
            return rol
        except Exception as e:
            raise e

    def actualizarRol(self,rol):
        """
        Método que permite actualizar un rol (su nombre)
        Parámetros:
        - rol : que es el rol que se actualizará
        """
        try:
            sql = 'update Rol set Nombre=%s where Rol_ID = %s;'
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql,(rol.nombre,rol.idRol))
            cnx.commit()
            super().cerrarConexion(cursor,cnx)
            return True
        except Exception as e:
            raise e

    def eliminarRol(self,rol):
        """
        Método que permite eliminar un rol mediante su id
        - rol : que es el rol que se elinará
        """
        try:
            sql="delete from Rol where Rol_ID="+str(rol.idRol)+";"
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql)
            cursor.commit()
            super().cerrarConexion(cursor,cnx)
            return True
        except Exception as e:
            raise e

    def agregarPermiso(self, rol, permiso):
        """
        Método que permite agregar permiso a un rol
        - rol : que es el rol al que se le agregará el permiso
        - permiso : que es el permiso que se le agregará al rol
        """
        try:
            sql='insert into Rol_tiene_Permiso (Rol_ID,Permiso_ID) values (%s,%s);'
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql,(rol.idRol,permiso.permiso_ID))
            cnx.commit()
            super().cerrarConexion(cursor,cnx)
            return True
        except Exception as e:
            raise e
        
    def removerPermiso(self, rol, permiso):
        if len(rol.permisos)==0:
            return False
        contador=0
        for perm in rol.permisos:
            if perm.permiso_ID!=permiso.permiso_ID:
                contador+=1
        if contador==len(rol.permisos):
            return False
        try:
            sql='delete from Rol_tiene_Permiso where (Rol_ID,Permiso_ID) =(%s,%s);'
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql,(rol.idRol,permiso.permiso_ID))
            cnx.commit()
            super().cerrarConexion(cursor,cnx)
            return True
        except Exception as e:
            raise e

    def consultarRoles(self):
        """
        Método que permite consultar todos los roles
        """
        try:
            roles = list()
            sql= "select * from Rol;"
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                sql2='select p.* from Rol_tiene_Permiso as rp inner join Rol as r on r.Rol_ID=rp.Rol_ID inner join Permiso as p on p.Permiso_ID=rp.Permiso_ID where r.Rol_ID= '+str(i[0])+';'
                cursor=cnx.cursor()
                cursor.execute(sql2)
                permisos=[]
                for row in cursor:
                    permiso = Permiso(row[0],row[1])
                    permisos.append(permiso)
                rol = Rol(i[0],i[1],permisos)
                roles.append(rol)
            super().cerrarConexion(cursor,cnx)
            return roles
        except Exception as e:
            raise e
    def consultarRolPorNombre(self,nombre):
        """
        Método que permite consultar un rol mediante su ID
        Parámetros:
        - nombre : que es el nombre del rol
        """
        try:
            sql= "select * from Rol where Nombre='"+nombre+"';"
            cnx=super().connectDB()
            cursor=cnx.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            rol=None
            if result is not None:
                rol = Rol(result[0],result[1],list())
                sql2='select p.* from Rol_tiene_Permiso as rp inner join Rol as r on r.Rol_ID=rp.Rol_ID inner join Permiso as p on p.Permiso_ID=rp.Permiso_ID where r.Rol_ID='+str(rol.idRol)+';'
                cursor.execute(sql2)
                for row in cursor:
                    rol.permisos.append(Permiso(row[0],row[1]))
            super().cerrarConexion(cursor,cnx)
            return rol
        except Exception as e:
            raise e