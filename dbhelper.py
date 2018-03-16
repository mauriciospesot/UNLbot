import sqlite3

class DBHelper:
    def __init__(self, dbname="unl.sqlite"): # Si se encuentra en un VPS, agregar la ruta completa en dbname
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS fich (id_materias integer PRIMARY KEY, horarios text NULL, materias text NULL, comisiones text NULL, aulas text NULL)"
        horamidx = "CREATE INDEX IF NOT EXISTS horarioIndex ON fich (horarios ASC)"
        materiaidx = "CREATE INDEX IF NOT EXISTS materiaIndex ON fich (materias ASC)"
        comisionidx = "CREATE INDEX IF NOT EXISTS comisionIndex ON fich (comisiones ASC)"
        aulaidx = "CREATE INDEX IF NOT EXISTS aulaIndex ON fich (aulas ASC)"
        self.conn.execute(stmt)
        self.conn.execute(horamidx)
        self.conn.execute(materiaidx)
        self.conn.execute(comisionidx)
        self.conn.execute(aulaidx)
        self.conn.commit()
        stmt = "CREATE TABLE IF NOT EXISTS fbcb (id_materias integer PRIMARY KEY, horarios text NULL, materias text NULL, comisiones text NULL, aulas text NULL)"
        horamidx = "CREATE INDEX IF NOT EXISTS horarioIndex ON fbcb (horarios ASC)"
        materiaidx = "CREATE INDEX IF NOT EXISTS materiaIndex ON fbcb (materias ASC)"
        comisionidx = "CREATE INDEX IF NOT EXISTS comisionIndex ON fbcb (comisiones ASC)"
        aulaidx = "CREATE INDEX IF NOT EXISTS aulaIndex ON fbcb (aulas ASC)"
        self.conn.execute(stmt)
        self.conn.execute(horamidx)
        self.conn.execute(materiaidx)
        self.conn.execute(comisionidx)
        self.conn.execute(aulaidx)
        self.conn.commit()
        stmt = "CREATE TABLE IF NOT EXISTS fcjs (id_materias integer PRIMARY KEY, horarios text NULL, materias text NULL, comisiones text NULL, aulas text NULL)"
        horamidx = "CREATE INDEX IF NOT EXISTS horarioIndex ON fcjs (horarios ASC)"
        materiaidx = "CREATE INDEX IF NOT EXISTS materiaIndex ON fcjs (materias ASC)"
        comisionidx = "CREATE INDEX IF NOT EXISTS comisionIndex ON fcjs (comisiones ASC)"
        aulaidx = "CREATE INDEX IF NOT EXISTS aulaIndex ON fcjs (aulas ASC)"
        self.conn.execute(stmt)
        self.conn.execute(horamidx)
        self.conn.execute(materiaidx)
        self.conn.execute(comisionidx)
        self.conn.execute(aulaidx)
        self.conn.commit()
        stmt = "CREATE TABLE IF NOT EXISTS fcm (id_materias integer PRIMARY KEY, horarios text NULL, materias text NULL, comisiones text NULL, aulas text NULL)"
        horamidx = "CREATE INDEX IF NOT EXISTS horarioIndex ON fcm (horarios ASC)"
        materiaidx = "CREATE INDEX IF NOT EXISTS materiaIndex ON fcm (materias ASC)"
        comisionidx = "CREATE INDEX IF NOT EXISTS comisionIndex ON fcm (comisiones ASC)"
        aulaidx = "CREATE INDEX IF NOT EXISTS aulaIndex ON fcm (aulas ASC)"
        self.conn.execute(stmt)
        self.conn.execute(horamidx)
        self.conn.execute(materiaidx)
        self.conn.execute(comisionidx)
        self.conn.execute(aulaidx)
        self.conn.commit()


    def agregar_materia(self, nombre_facultad, hora, materia, comision, aula):
        args = (hora, materia, comision, aula)
        stmt = "INSERT INTO " + nombre_facultad + " (horarios, materias, comisiones, aulas) VALUES (?, ?, ?, ?)"
        self.conn.execute(stmt, args)
        self.conn.commit()

    def eliminar_materia(self, nombre_facultad, id_materias):
        stmt = "DELETE FROM " + nombre_facultad + " WHERE id_materias=?"
        self.conn.execute(stmt, (id_materias,))
        self.conn.commit()

    def get_contenido_tabla(self, nombre_facultad):
        stmt = "SELECT * FROM " + nombre_facultad
        resultado = self.conn.execute(stmt)
        self.conn.commit()
        return resultado

    def get_horarios(self, nombre_facultad):
        stmt = "SELECT horarios FROM " + nombre_facultad
        return [x[0] for x in self.conn.execute(stmt)]

    def get_materias(self, nombre_facultad):
        stmt = "SELECT materias FROM " + nombre_facultad
        return [x[0] for x in self.conn.execute(stmt)]

    def get_comisiones(self, nombre_facultad):
        stmt = "SELECT comisiones FROM " + nombre_facultad
        return [x[0] for x in self.conn.execute(stmt)]

    def get_aulas(self, nombre_facultad):
        stmt = "SELECT aulas FROM " + nombre_facultad
        return [x[0] for x in self.conn.execute(stmt)]

    def vaciar_tabla(self, nombre_facultad):
        stmt = "DELETE FROM " + nombre_facultad
        self.conn.execute(stmt)
        self.conn.commit()
