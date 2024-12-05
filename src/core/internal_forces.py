import pandas as pd

class InternalForces:
    """Dataframe for internal forces from the analysis results. This comes from the parse_internal_forces()"""
    def __init__(self, data):
        self.dataframe = pd.DataFrame(data)
