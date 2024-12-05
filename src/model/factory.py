from src.model.structural_model import StructuralModel
from src.model.etabs import EtabsModel

def model_loader(source_application: str,
                 received_object,
                 design_code: 'DesignCode',
                 automate_context: 'AutomationContext') -> StructuralModel:
    """Subclass instantiation of StructrualModel depending on source_application"""
    if source_application == 'ETABS':
        return EtabsModel(received_object, design_code, automate_context)
    else: # NOTE: to / can be extended by other source applications e.g. SAP 2000, Oasys etc.
        raise NotImplementedError(f'The source application of {source_application} is either not recognised / supported.')
