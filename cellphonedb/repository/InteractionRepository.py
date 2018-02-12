import pandas as pd
from sqlalchemy import or_

from cellphonedb.database.Repository import Repository
from cellphonedb.models.interaction.db_model_interaction import Interaction
from cellphonedb.models.interaction.functions_interaction import expand_interactions_multidatas
from cellphonedb.models.multidata.db_model_multidata import Multidata


class InteractionRepository(Repository):
    name = 'interaction'

    def get_all(self):
        query = self.database_manager.database.session.query(Interaction)
        interactions = pd.read_sql(query.statement, self.database_manager.database.engine)

        return interactions

    def get_interactions_by_multidata_id(self, id):
        """

        :type id: int
        :rtype: pd.DataFrame
        """
        query = self.database_manager.database.session.query(Interaction).filter(
            or_(Interaction.multidata_1_id == int(id), Interaction.multidata_2_id == int(id)))
        result = pd.read_sql(query.statement, self.database_manager.database.engine)

        return result

    def get_interactions_multidata_by_multidata_id(self, id):
        """

        :type id: int
        :rtype: pd.DataFrame
        """

        interactions = self.get_interactions_by_multidata_id(id)
        multidatas_expanded = self.database_manager.get_repository('multidata').get_all_expanded()
        interactions_expanded = expand_interactions_multidatas(interactions, multidatas_expanded)
        return interactions_expanded

    # TODO: Not tested
    def get_all_expanded(self):
        interactions_query = self.database_manager.database.session.query(Interaction)
        interactions = pd.read_sql(interactions_query.statement, self.database_manager.database.engine)

        multidata_expanded = self.database_manager.get_repository('multidata').get_all_expanded()

        interactions = pd.merge(interactions, multidata_expanded, left_on=['multidata_1_id'], right_on=['id_multidata'])
        interactions = pd.merge(interactions, multidata_expanded, left_on=['multidata_2_id'], right_on=['id_multidata'],
                                suffixes=['_1', '_2'])

        interactions.drop(['id_multidata_1', 'id_multidata_2'], axis=1, inplace=True)

        return interactions
