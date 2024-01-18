"""Flow class."""
from typing import Any, Dict, Sequence

from uniflow.constants import TRANSFORM
from uniflow.flow.flow import Flow
from uniflow.node import Node
from uniflow.op.basic.expand_reduce_flow import ExpandReduceFlow
from uniflow.op.prompt import PromptTemplate


class TransformExpandReduceFlow(Flow):
    """Expand and Reduce flow class.

    """

    TAG = TRANSFORM

    def __init__(
        self,
        prompt_template: PromptTemplate,
        model_config: Dict[str, Any],
    ) -> None:  # pylint: disable=useless-parent-delegation
        """Initialize ExpandReduceFlow class."""
        self._expand_reduce_flow = ExpandReduceFlow()
        super().__init__()

    def run(self, nodes: Sequence[Node]) -> Sequence[Node]:
        """Run ExpandReduceFlow.

        Args:
            nodes (Sequence[Node]): Nodes to run.

        Returns:
            Sequence[Node]: Nodes after running.
        """
        return self._expand_reduce_flow(nodes)
