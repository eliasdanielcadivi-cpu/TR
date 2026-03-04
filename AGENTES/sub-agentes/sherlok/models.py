from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class SegmentosMercado(BaseModel):
    estudiantes: bool
    educacion: bool
    profesionales: bool
    pymes: bool
    corporativo: bool
    industria: bool
    salud: bool
    petrolero: bool
    logistica: bool
    comercio: bool
    marketing: bool
    eventos: bool
    ecommerce: bool
    investigacion: bool
    gubernamental: bool

class EntornosAplicacion(BaseModel):
    oficina: bool
    educativo: bool
    industrial: bool
    creativo: bool
    desarrollo: bool
    datos: bool
    infraestructura: bool
    seguridad: bool

class RelacionTecnica(BaseModel):
    tipo: Literal["standalone", "plugin", "modulo", "libreria", "framework", "servicio", "driver", "utilidad_sistema"]
    para_que_sirve: str = Field(..., max_length=150)
    requiere: List[str]
    integra_con: List[str]
    reemplaza_a: List[str]
    parte_de: Optional[str]

class AnalisisAres(BaseModel):
    score: int = Field(..., ge=1, le=10)
    razon: str
    categoria_ares: Literal["core", "plugin", "opcional", "basura", "incompatible"]
    casos_uso: List[str]

class ProgramaAudit(BaseModel):
    id: str
    nombre: str
    version_detectada: Optional[str]
    descripcion: str = Field(..., min_length=20, max_length=300)
    categoria_general: Literal["sistema", "desarrollo", "multimedia", "oficina", "red", "seguridad", "ciencia", "otro"]
    licencia: Literal["foss", "propietaria", "desconocida"]
    interfaz: List[Literal["cli", "gui", "api", "daemon", "web"]]
    lenguaje: str
    segmentos_mercado: SegmentosMercado
    entornos_aplicacion: EntornosAplicacion
    contexto_tecnico: RelacionTecnica
    dependencias_criticas: List[str]
    documentacion_existente: List[str]
    analisis_ares: AnalisisAres
    recomendacion: Literal["integrar", "evaluar", "descartar", "monitorizar"]
    notas_forense: Optional[str]
