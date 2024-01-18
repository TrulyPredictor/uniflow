from uniflow.op.op import Op
from uniflow.node import Node
from typing import Any, Mapping, Sequence

class ReduceOp(Op):
    def __init__(self,merge_function=None, name="ReduceOp"):
        super().__init__(name=name)
        self.merge_function = merge_function
        # self.nodes=nodes
    def _transform(self, value_dict_1: Mapping[str, Any],value_dict_2: Mapping[str, Any]) -> Mapping[str, Any]:
        merge_function = self.merge_function or self.default_merge_function

        return merge_function(value_dict_1, value_dict_2)
    def __call__(self, nodes) -> Node:
        # if len(nodes)!=2:
        #         print("Input Nodes aren't paired.")
        # else:
    # output_nodes = []
    # for node in nodes:
        value_dict_1 = nodes[0].value_dict

        value_dict_2 = nodes[1].value_dict

        reduce_dict = self._transform(value_dict_1,value_dict_2)

        output_node=Node(name="reduce_1", value_dict=reduce_dict,prev_nodes=[nodes[0],nodes[1]])




        # reduce_1_node = Node(name="reduce_1", value_dict=reduce_1_dict,prev_nodes=[expand_1,expand_2])

        return output_node

    @staticmethod
    def default_merge_function(value_dict_1, value_dict_2):
        result_dict = {}
        keys_1 = list(value_dict_1.keys())
        keys_2 = list(value_dict_2.keys())
        for i in range(min(len(keys_1), len(keys_2))):
            key_1 = keys_1[i]
            key_2 = keys_2[i]
            result_dict[key_1 + " " + key_2] = value_dict_1[key_1] + " " + value_dict_2[key_2]
        return result_dict