import pandas as pd

from cellphonedb.tools import filters
from utilities import dataframe_format


def call(interactions_expanded: pd.DataFrame) -> pd.DataFrame:
    interactions_expanded.rename(index=str, columns={'name_1': 'multidata_name_1', 'name_2': 'multidata_name_2'},
                                 inplace=True)
    filters.remove_not_defined_columns(interactions_expanded,
                                       ['comments', 'entry_name_1', 'entry_name_2', 'multidata_name_1',
                                        'multidata_name_2', 'score_1', 'score_2', 'source'])

    interactions_extended = dataframe_format.bring_columns_to_start(
        ['multidata_name_1', 'entry_name_1', 'multidata_name_2',
         'entry_name_2'], interactions_expanded)

    return interactions_extended
