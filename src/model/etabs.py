from typing import List
from src.model.structural_model import StructuralModel
from src.core.cross_section import RectangularSection
from src.core.materials import MaterialFactory
from src.utils.units import Convert
from src.core.internal_forces import InternalForces

class EtabsModel(StructuralModel):
    """Implementation StructuralModel base class specific for ETABS"""

    def setup_model(self) -> None:
        self.load()
        self.validate()
        self.get_units() # NOTE: We can't call get_units() if we don't validate() first

    # NOTE: method enforces '@Model' as model_attribute for EtabsModel
    def load(self, model_attribute = '@Model') -> None:
        super().load(model_attribute = model_attribute)

    # NOTE: method enforces 'specs' and 'elements' to be given in commit. This is with a "Everything" send from ETABS
    def validate(self, attributes = None) -> None:
        if not attributes: # NOTE: due to PylintW0102
            attributes = ['specs', 'elements']
        super().validate(attributes = attributes)

    def get_units(self, length_unit: str = None, force_unit: str = None) -> None:
        length_unit = self.model.specs.settings.modelUnits.length # NOTE: due to PylintW0221
        force_unit = self.model.specs.settings.modelUnits.force # NOTE: due to PylintW0221
        super().get_units(length_unit = length_unit, force_unit = force_unit)

    def filter_columns(self) -> List['Element1D']:
        columns = []
        for element in self.model.elements: #TODO: multithreading
            if str(getattr(element, 'type', '')) == 'ElementType1D.Column':
                columns.append(element)
            else: # NOTE: these objects are logged for automation results
                self.automate_results.elements_not_selected.append(element.id)
        return columns

    # NOTE: error handling within the design_columns() base class function
    def parse_length(self, element_1d) -> float:
        return Convert.length(element_1d.baseLine.length, input_unit = self.units.length_unit)

    # NOTE: error handling within the design_columns() base class function
    def parse_cross_section(self, element_1d) -> 'CrossSection':
        if element_1d.property.profile.shapeName == 'Rectangular':
            width = Convert.length(element_1d.property.profile.width, input_unit = self.units.length_unit)
            depth = Convert.length(element_1d.property.profile.depth, input_unit = self.units.length_unit)
            area = Convert.area(element_1d.property.profile.area, input_unit = self.units.length_unit)
            moment_of_intertia_about_y = Convert.moment_of_inertia(element_1d.property.profile.Iyy, input_unit = self.units.length_unit)
            moment_of_intertia_about_z = Convert.moment_of_inertia(element_1d.property.profile.Izz, input_unit = self.units.length_unit)
            return RectangularSection(width,
                                      depth,
                                      area,
                                      moment_of_intertia_about_y,
                                      moment_of_intertia_about_z)
        else:
            raise ValueError(f'Shape {element_1d.property.profile.shapeName} not recognised')

    # NOTE: error handling within the design_columns() base class function
    def parse_material(self, element_1d) -> 'Material':
        return MaterialFactory.get_material(region = 'Britain',
                                            material_name=element_1d.property.material.name)

    # NOTE: error handling within the design_columns() base class function
    def parse_internal_forces(self, element_1d) -> InternalForces:
        data = []
        if not hasattr(element_1d, 'AnalysisResults'):
            raise ValueError('Send "Column Forces" with model')
        for load_combination in element_1d.AnalysisResults.resultsByLoadCombination:
            result_case = load_combination.resultCase.name
            for result in load_combination.results1D:
                data.append({
                    'result_case': result_case,
                    'station': result.position,
                    'axial_force': Convert.force(result.forceX, input_unit = self.units.force_unit),
                    'shear_y': Convert.force(result.forceY, input_unit = self.units.force_unit),
                    'shear_z': Convert.force(result.forceZ, input_unit = self.units.force_unit),
                    'bending_y': Convert.force(Convert.length(result.momentYY, input_unit = self.units.length_unit), input_unit = self.units.force_unit),
                    'bending_z': Convert.force(Convert.length(result.momentZZ, input_unit = self.units.length_unit), input_unit = self.units.force_unit),
                    'torsion': Convert.force(Convert.length(result.momentXX, input_unit = self.units.length_unit), input_unit = self.units.force_unit)
                })
        return InternalForces(data = data)
