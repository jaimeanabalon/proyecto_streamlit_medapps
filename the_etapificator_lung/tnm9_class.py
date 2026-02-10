import json

class LungTumorStagingPro:
    def __init__(self, patient_id: str, diameter_mm: float, 
                 invasion_pleura_visceral: bool = False,
                 invasion_estructuras_mediastino: bool = False,
                 nodulos_satelites_mismo_lobulo: bool = False,
                 nodulos_satelites_distinto_lobulo: bool = False):
        
        self.patient_id = patient_id
        self.diameter_mm = diameter_mm
        
        # Hallazgos morfológicos/clínicos
        self.invasion_pleura = invasion_pleura_visceral
        self.invasion_mediastino = invasion_estructuras_mediastino
        self.satelites_ipsi_lob = nodulos_satelites_mismo_lobulo
        self.satelites_ipsi_dist_lob = nodulos_satelites_distinto_lobulo
        
        self.t_category = self._calculate_t_category()

    def _calculate_t_category(self) -> str:
        # 1. Base por tamaño (mismo código previo)
        d = self.diameter_mm
        t_size = "T1a" if d <= 10 else "T1b" if d <= 20 else "T1c" if d <= 30 else \
                 "T2a" if d <= 40 else "T2b" if d <= 50 else "T3" if d <= 70 else "T4"
        
        # 2. Escalada por criterios de invasión y multiplicidad
        # Priorizamos el hallazgo más grave (T4 > T3 > T2)
        
        # Criterios T4: Invasión estructuras mediastínicas o nódulo en distinto lóbulo ipsilateral
        if self.invasion_mediastino or self.satelites_ipsi_dist_lob:
            return "T4"
        
        # Criterios T3: Invasión de pared torácica (asumida aquí) o nódulo en mismo lóbulo
        if self.satelites_ipsi_lob:
            return "T3"
            
        # Criterios T2: Invasión de pleura visceral (mínimo T2a si el tamaño es menor)
        if self.invasion_pleura:
            # Si el tamaño indicaba T1, la invasión pleural lo sube a T2a automáticamente
            if t_size.startswith("T1"):
                return "T2a"
        
        return t_size

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "t_category": self.t_category,
            "is_ct1c": self.t_category == "T1c",
            "clinical_flags": {
                "visceral_pleural_invasion": self.invasion_pleura,
                "satellite_nodules_ipsilateral": self.satelites_ipsi_lob or self.satelites_ipsi_dist_lob
            }
        }

# Ejemplo: Tumor de 15mm (T1b) pero con nódulo satélite en el mismo lóbulo (T3)
paciente_onco = LungTumorStagingPro(
    patient_id="MT-8821", 
    diameter_mm=15, 
    nodulos_satelites_mismo_lobulo=True
)

print(json.dumps(paciente_onco.to_dict(), indent=4))