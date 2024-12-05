from abc import ABC, abstractmethod
from typing import List, Dict
from collections import defaultdict
from src.design.logger import CalculationLog

class DesignCode(ABC):
    """Design code base class"""

    def __init__(self, code: str, design_parameters: dict):
        self.code = code
        self.design_parameters = design_parameters
        self.calculation_log: defaultdict[str, List[CalculationLog]] = defaultdict(list)

    @abstractmethod
    def design_column(self, column: 'Column') -> 'DesignResults':
        """Region specific design checks contained within implementation. Log needs to be cleared beforehand."""
        self.calculation_log.clear()  # NOTE: Every column design should receive a blank instance of the logger

        self.calculation_log['Geometric Parameters'].append(CalculationLog('b', column.cross_section.width, 'm'))
        self.calculation_log['Geometric Parameters'].append(CalculationLog('h', column.cross_section.depth, 'm'))
        self.calculation_log['Geometric Parameters'].append(CalculationLog('l', column.length, 'm'))