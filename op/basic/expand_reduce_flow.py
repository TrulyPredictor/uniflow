from uniflow.flow.flow import Flow
from uniflow.op.basic.expand_op import ExpandOp
from uniflow.op.basic.reduce_op import ReduceOp
from uniflow.node import Node
import sqlite3
from typing import Any, Sequence

class ExpandReduceFlow(Flow):
    def __init__(self, database_path=":memory:"):
        super().__init__()
        self.database_path = database_path
        self.initialize_database()

    def initialize_database(self):
        self.connection = sqlite3.connect(self.database_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS output_data (key TEXT, value TEXT)")
        self.connection.commit()

    def _store_in_database(self, key, value):
        self.cursor.execute("INSERT INTO output_data VALUES (?, ?)", (key, value))
        self.connection.commit()

    def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:
        if not nodes:
            raise ValueError("Please set the input nodes.")

        expand_op = ExpandOp()
        reduce_op = ReduceOp()
        output_nodes = []

        for node in nodes:
            expand_output = expand_op(node)
            reduce_1_node = reduce_op(expand_output)
            output_nodes.append(reduce_1_node)

            # Store output key-value pairs in the database
            for key, value in reduce_1_node.value_dict.items():
                self._store_in_database(key, value)

        return output_nodes



# from uniflow.flow.flow import Flow
# from uniflow.op.basic import copy_op,expand_op,reduce_op
# from uniflow.op.basic.expand_op import ExpandOp
# from uniflow.op.basic.reduce_op import ReduceOp
# from uniflow.node import Node
# from typing import Any, Mapping, Sequence
# import sqlite3

# class ExpandReduceFlow(Flow):
#     def __init__(self):
#         super().__init__
#     def __call__(self, nodes: Sequence[Node]) -> Sequence[Node]:

#         if not nodes:
#             raise ValueError("Please set the input node.")
        

#         # Define operations
#         expand_op = ExpandOp()
#         reduce_op = ReduceOp()
#         output_nodes = []
#         for node in nodes:

#             expand_output = expand_op(node)

#             reduce_1_node = reduce_op(expand_output)

#             # # Set output nodes
#             output_nodes.append(reduce_1_node)
            

#         return output_nodes