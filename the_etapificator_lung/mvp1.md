from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date

# --- MODELOS DE DATOS (La Estructura) ---

class ReglaOncologica(BaseModel):
    """Tu propiedad intelectual. Reglas curadas por ti."""
    gen: str
    variante_regex: str  # Expresión regular para capturar variaciones (ej: V600E, V600K)
    droga_aprobada: str
    nivel_evidencia: str
    snippet_educativo: str # El "Micro-learning" para el médico
    texto_justificacion: str # Para la carta al seguro

class PacienteInput(BaseModel):
    """Datos que entran del hospital (Radioactivos/PHI)."""
    id_anonimizado: str
    fecha_diagnostico: date
    diagnostico_path: str
    genes_detectados: List[dict] # Lista de mutaciones del reporte NGS

    @validator('diagnostico_path')
    def validar_diagnostico(cls, v):
        # Aquí podrías normalizar texto: "Ca Pulmon" -> "NSCLC"
        return v.title()

# --- TU BASE DE CONOCIMIENTO (Simulación de DB) ---

BASE_CONOCIMIENTO = [
    ReglaOncologica(
        gen="BRAF",
        variante_regex="V600[EK]",
        droga_aprobada="Dabrafenib + Trametinib",
        nivel_evidencia="Categoria 1 (NCCN)",
        snippet_educativo="💡 Dato clave: En melanoma, V600K es más común en pacientes añosos con daño solar crónico.",
        texto_justificacion="El estudio COMBI-d demostró beneficio en OS..."
    )
]

# --- EL MOTOR DE PROCESAMIENTO (El Servicio) ---

class MotorDeDecision:
    def procesar_caso(self, paciente: PacienteInput) -> dict:
        recomendaciones = []
        
        # Lógica de cruce (Matching)
        for mutacion in paciente.genes_detectados:
            for regla in BASE_CONOCIMIENTO:
                # Si el gen coincide y la variante matchea la regla...
                if mutacion['gen'] == regla.gen and mutacion['variante'] in regla.variante_regex:
                    recomendaciones.append({
                        "accion": f"Iniciar {regla.droga_aprobada}",
                        "educacion": regla.snippet_educativo,
                        "para_reporte": regla.texto_justificacion
                    })
        
        if not recomendaciones:
            return {"status": "Sin target accionable", "accion": "Considerar Ensayo Clínico"}
            
        return {"status": "Match Encontrado", "resultados": recomendaciones}

# --- EJEMPLO DE USO (Simulando tu App) ---

# 1. Llega un dato "sucio" del mundo real
input_raw = {
    "id_anonimizado": "PT-2024-001",
    "fecha_diagnostico": "2024-01-15",
    "diagnostico_path": "melanoma metastasico",
    "genes_detectados": [{"gen": "BRAF", "variante": "V600E"}]
}

# 2. Tu sistema valida y estructura
try:
    paciente = PacienteInput(**input_raw)
    
    # 3. El motor procesa
    motor = MotorDeDecision()
    resultado = motor.procesar_caso(paciente)
    
    # 4. Salida (Output)
    print(f"--- REPORTE AUTOMÁTICO PARA {paciente.diagnostico_path} ---")
    for rec in resultado.get('resultados', []):
        print(f"💊 RECOMENDACIÓN: {rec['accion']}")
        print(f"🎓 LEARNING POINT: {rec['educacion']}")

except Exception as e:
    print(f"Error de validación: {e}")

    # Arquitectura Técnica: Proyecto "Sludge-Buster"

**Principio Rector:** Separación total entre Lógica (IP) y Datos del Paciente (PHI).
**Stack Tecnológico:** Python (Backend) + Streamlit (Frontend MVP) + PostgreSQL (Persistencia).

## 1. Componentes del Sistema
* **Ingestion Engine:** Módulo de normalización de datos. Convierte texto libre y fechas caóticas en objetos estandarizados `Pydantic`.
* **Knowledge Core (IP):** Base de datos de reglas oncológicas. Es el activo principal de la empresa. Contiene la lógica de decisión y el contenido educativo.
* **Template Generator:** Motor (`Jinja2`) que toma las decisiones del Knowledge Core e inyecta los datos en formatos pre-aprobados (Cartas, Actas).

## 2. Flujo de Datos (Data Pipeline)
1.  **Entrada:** Médico carga CSV o ingresa datos en formulario web.
2.  **Anonimización (Cliente):** Los datos sensibles se enmascaran en memoria.
3.  **Consulta (Servidor):** Se envía el perfil molecular (ej: "Lung + EGFR L858R") al Knowledge Core.
4.  **Respuesta:** El servidor devuelve el objeto de recomendación + snippet educativo.
5.  **Renderizado:** El navegador del médico reconstruye el documento final con los datos del paciente (que nunca salieron de su control total).

## 3. Ventaja Competitiva Técnica
A diferencia de los EMR tradicionales que son "bases de datos pasivas", esta arquitectura es un **"Motor de Inferencia Activo"**. Cada interacción educa al usuario, transformando un proceso administrativo (llenar un formulario) en una actividad docente (aprender sobre la mutación).