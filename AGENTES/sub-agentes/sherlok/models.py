from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class RelacionTecnica(BaseModel):
    tipo: Literal["standalone", "plugin", "modulo", "libreria", "framework", "servicio", "driver", "utilidad_sistema"]
    para_que_sirve: str = Field(..., max_length=150)
    requiere: List[str]
    integra_con: List[str]
    reemplaza_a: List[str]
    parte_de: Optional[str]

class AnalisisAres(BaseModel):
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
    contexto_tecnico: RelacionTecnica
    dependencias_criticas: List[str]
    documentacion_existente: List[str]
    analisis_ares: AnalisisAres
    notas_forense: Optional[str]
