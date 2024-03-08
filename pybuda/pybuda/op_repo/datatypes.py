# SPDX-FileCopyrightText: © 2024 Tenstorrent AI ULC

# SPDX-License-Identifier: Apache-2.0
# Operator repository models


from typing import List, Optional, Callable, Type, Union
from dataclasses import dataclass, field


@dataclass
class OperatorParamNumber:
    name: str
    type: Type[Union[int, float]]
    min_value: Optional[int]
    max_value: Optional[int]


OperatorParam = Union[OperatorParamNumber]


@dataclass
class OperatorDefinition:
    name: str
    full_name: str
    input_num: int
    instantiate: bool = False  # nn in Torch require instantiation in constructor
    constructor_params: List[OperatorParam] = field(default_factory=list)
    forward_code: Optional[Callable[[], str]] = None
    forward_params: List[OperatorParam] = field(default_factory=list)
    operands: List[str] = field(default_factory=list)  # TODO describe operand and shapes

    def is_operator(self) -> bool:
        return not self.instantiate

    def is_layer(self) -> bool:
        return self.instantiate


class OperatorRepository:

    def __init__(self, operators: List[OperatorDefinition]):
        self.operators = operators

    def get_by_name(self, name: str):
        return [op for op in self.operators if op.name == name][0]
