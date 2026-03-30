from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Carga .env si existe (entorno local)

# ────────────────────────────────────────────────────────────────────────────
# Configuración de la base de datos
# ────────────────────────────────────────────────────────────────────────────

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # PostgreSQL en producción (Render)
    # Render provee URLs con prefijo "postgres://" pero SQLAlchemy necesita "postgresql://"
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL, echo=False)
else:
    # SQLite en desarrollo local
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLITE_URL = f"sqlite:///{os.path.join(BASE_DIR, '..', 'anotaciones.db')}"
    engine = create_engine(
        SQLITE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )

# Crear session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos ORM
Base = declarative_base()

# ────────────────────────────────────────────────────────────────────────────
# Modelos ORM
# ────────────────────────────────────────────────────────────────────────────

class EscuelaDB(Base):
    """Modelo ORM para escuelas"""
    __tablename__ = "escuelas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), unique=True, index=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    clases = relationship("ClaseDB", back_populates="escuela_obj")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_creacion": self.fecha_creacion
        }


class ClaseDB(Base):
    """Modelo ORM para clases"""
    __tablename__ = "clases"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(String(50), nullable=False)
    depto = Column(String(100), nullable=False)
    escuela = Column(String(255), ForeignKey("escuelas.nombre"), nullable=False)
    grado = Column(String(50), nullable=False)
    letra = Column(String(10), nullable=False)
    nombreMaestra = Column(String(255), nullable=False)
    anotacion = Column(Integer, ForeignKey("anotacion.id"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    escuela_obj = relationship("EscuelaDB", back_populates="clases")
    anotacion_rel = relationship(
        "AnotacionDB",
        back_populates="clase",
        uselist=False,
        foreign_keys=[anotacion],
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "depto": self.depto,
            "escuela": self.escuela,
            "grado": self.grado,
            "letra": self.letra,
            "nombreMaestra": self.nombreMaestra,
            "anotacion": self.anotacion_rel.to_dict() if self.anotacion_rel else None,
            "fecha_creacion": self.fecha_creacion
        }


class GrupoDB(Base):
    """Modelo ORM para grupos"""
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, index=True, nullable=False)
    descripcion = Column(String(500), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion
        }


class AnotacionDB(Base):
    """Modelo ORM para anotaciones adicionales"""
    __tablename__ = "anotacion"
    id = Column(Integer, primary_key=True, index=True)
    dictada = Column(Boolean, nullable=False)
    correspondePago = Column(Boolean, nullable=False)
    registroClase = Column(String(1000), nullable=False)
    observaciones = Column("Observaciones", String(1000), nullable=True)
    clase = relationship(
        "ClaseDB",
        back_populates="anotacion_rel",
        uselist=False,
        foreign_keys="ClaseDB.anotacion",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "dictada": self.dictada,
            "correspondePago": self.correspondePago,
            "registroClase": self.registroClase,
            "observaciones": self.observaciones
        }


# ────────────────────────────────────────────────────────────────────────────
# Funciones de utilidad
# ────────────────────────────────────────────────────────────────────────────

def crear_tablas():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas de la base de datos creadas/verificadas")


def obtener_sesion():
    """Obtiene una sesión de la base de datos"""
    return SessionLocal()


def cerrar_sesion(db):
    """Cierra la sesión de la base de datos"""
    if db:
        db.close()
