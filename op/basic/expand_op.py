# from uniflow.op.op import Op
# from uniflow.node import Node
# from typing import Any, Mapping, Sequence

# class ExpandOp(Op):
#     def __init__(self, split_function=None, name="ExpandOp"):
#         super().__init__(name=name)  
#         self.split_function = split_function
#         # self.node=node
#     def _transform(self, value_dict):
#         if isinstance(value_dict, dict):
        
#             n = len(value_dict)

#             split_function = self.split_function or (lambda x: (dict(list(x.items())[:n//2]), dict(list(x.items())[n//2:])))
#             expand_1_dict, expand_2_dict = split_function(value_dict)


#             # expand_1_node = Node(name="expand_1", value_dict=expand_1_dict,prev_nodes=[node])
#             # expand_2_node = Node(name="expand_2", value_dict=expand_2_dict,prev_nodes=[node])

#         else:
#             print(value_dict)
#             # print(value_dict.value_dict)
#             print("Error: value_dict should be a dictionary.")
#         return expand_1_dict,expand_2_dict
#     # def __init__(self, split_function=None, name="ExpandOp"):
#     #     super(ExpandOp, self).__init__(name=name)
#     #     self.split_function = split_function

#     def __call__(self, node):
#         self.node=node

#         if isinstance(self.node, Node):
#             if self.node.value_dict is None:
#                 print("There is no value_dict!")
#         # value_dict = node.value_dict
#         # output_nodes = []
#         # for node in nodes:
#             else:
#                 print(self.node)
#                 print("Calling _transform with value_dict:", self.node.value_dict)
#                 expand_1_dict,expand_2_dict = self._transform(self.node.value_dict)
#                 output_dict_list = [expand_1_dict,expand_2_dict]
#                 # output_nodes=[Node(name="expand_1", value_dict=expand_1_dict,prev_nodes=[node]),
#                 #                     Node(name="expand_2", value_dict=expand_2_dict,prev_nodes=[node])]
#         else:
#             print("Input is not Node.")
#         # if isinstance(value_dict, dict):
        
#         #     n = len(value_dict)

#         #     split_function = self.split_function or (lambda x: (dict(list(x.items())[:n//2]), dict(list(x.items())[n//2:])))
#         #     expand_1_dict, expand_2_dict = split_function(value_dict)


#         #     expand_1_node = Node(name="expand_1", value_dict=expand_1_dict,prev_nodes=[node])
#         #     expand_2_node = Node(name="expand_2", value_dict=expand_2_dict,prev_nodes=[node])
#         #     output_nodes=[expand_1_node, expand_2_node]

#         return output_dict_list




from typing import Any, Mapping, List

from uniflow.node import Node
from uniflow.op.op import Op

class ExpandOp(Op):
    def __init__(self, split_function=None, name="ExpandOp"):
        super().__init__(name=name)
        # Use the provided split_function or a default lambda function
        self.split_function = split_function or (lambda x: (dict(list(x.items())[:len(x)//2]), dict(list(x.items())[len(x)//2:])))

    def _transform(self, value_dict: Mapping[str, Any]) -> Mapping[str, Any]:
        # Apply the split_function to the value_dict
        expand_1_dict, expand_2_dict = self.split_function(value_dict)
        return expand_1_dict, expand_2_dict

    def __call__(self, node: Node) -> List[Node]:
        # Check if the input is a Node
        if not isinstance(node, Node):
            raise ValueError("Input must be a Node.")

        # Check if the value_dict of the node is a dictionary
        if not isinstance(node.value_dict[0], dict):


            pass
            # raise ValueError("Value_dict of the Node must be a dictionary.")
        
        # Apply the transformation to the value_dict of the node
        expand_1_dict, expand_2_dict = self._transform(node.value_dict[0])

        # Create new nodes with the transformed value_dicts
        expand_1_node = Node(name="expand_1", value_dict=expand_1_dict, prev_nodes=[node])
        expand_2_node = Node(name="expand_2", value_dict=expand_2_dict, prev_nodes=[node])

        # Return a list with the new nodes
        return [expand_1_node, expand_2_node]


