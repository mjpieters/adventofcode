from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import partial
from operator import getitem, setitem
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
    cast,
    overload,
)

T = TypeVar("T", bound="CPU")
Registers = Dict[str, int]


class Halt(Exception):
    """Signal to end the program"""

    @classmethod
    def halt(cls) -> None:
        raise cls


class Memory(List[int]):
    def _grow(self, target: int) -> None:
        assert target + 1 < 2**16, f"Asking for too much memory: {target}"
        self.extend([0] * (target + 1 - len(self)))

    @overload
    def __getitem__(self, i: int) -> int:
        ...

    @overload
    def __getitem__(self, i: slice) -> List[int]:
        ...

    def __getitem__(self, i):
        try:
            return super().__getitem__(i)
        except IndexError:
            if isinstance(i, int):
                self._grow(i)
            return super().__getitem__(i)

    @overload
    def __setitem__(self, i: int, o: int) -> None:
        ...

    @overload
    def __setitem__(self, i: slice, o: Iterable[int]) -> None:
        ...

    def __setitem__(self, i, o) -> None:
        try:
            super().__setitem__(i, o)
        except IndexError:
            if isinstance(i, int):
                self._grow(i)
            super().__setitem__(i, o)


class _ParameterGetter(Protocol):
    def __call__(self, memory: Memory, pos: int, registers: Registers) -> int:
        ...


class _ParameterSetter(Protocol):
    def __call__(
        self, memory: Memory, pos: int, value: int, registers: Registers
    ) -> None:
        ...


class ParameterMode(Enum):
    # modes are an integer (0-9) mapping to a getter and setter definition
    position = (
        0,
        lambda *a, **kw: getitem(*a),
        lambda *a, **kw: setitem(*a),
    )
    # immediate mode should only ever be used as a getter; if used as a setter
    # anyway, Halt is raised.
    immediate = (1, lambda _, pos, **kw: pos, lambda *a, **kw: Halt.halt)
    relative = (
        2,
        lambda mem, pos, *, registers, **kw: getitem(
            mem, pos + registers["relative base"]
        ),
        lambda mem, pos, value, *, registers, **kw: setitem(
            mem, pos + registers["relative base"], value
        ),
    )

    if TYPE_CHECKING:
        get: _ParameterGetter
        set: _ParameterSetter

    def __new__(
        cls,
        value: int,
        getter: Optional[_ParameterGetter] = None,
        setter: Optional[_ParameterSetter] = None,
    ) -> ParameterMode:
        mode = object.__new__(cls)
        mode._value_ = value
        mode.get = getter
        mode.set = setter
        return mode


@dataclass
class _InstructionBaseFields:
    # An opcode takes N parameters, consisting of M arguments and an optional output
    arg_count: int = 0
    output: bool = False


class InstructionBase(ABC, _InstructionBaseFields):
    @abstractmethod
    def __call__(
        self, pos: int, *args: Any, registers: Registers, **kwargs: Any
    ) -> Tuple[int, Any]:
        """Produce a new CPU position and a result"""
        raise NotImplementedError()

    def bind(self, opcode: int, cpu: CPU) -> BoundInstruction:
        # assumption: on binding, cpu.pos points to the position in memory
        # for our opcode.
        paramcount = self.arg_count + int(self.output)
        modes = opcode // 100
        return BoundInstruction(
            self,
            tuple(ParameterMode(modes // (10**i) % 10) for i in range(paramcount)),
            cpu.pos + 1,
            cpu,
        )


@dataclass
class CallableInstructionBase:
    """Instruction mixin that accepts a callable to delegate instruction handling to"""

    # takes InstructionBase.arg_count integers
    f: Callable[..., Any]


@dataclass
class AdjustRelativeBaseInstruction(InstructionBase):
    """Adjust the 'relative base' register, by adding the single argument"""

    arg_count: int = 1

    def __call__(
        self, pos: int, *args: int, registers: Registers, **kwargs: Any
    ) -> Tuple[int, Any]:
        registers["relative base"] += args[0]
        return pos + 1 + self.arg_count + int(self.output), None


@dataclass
class Instruction(InstructionBase, CallableInstructionBase):
    def __call__(self, pos: int, *args: Any, **kwargs: Any) -> Tuple[int, Any]:
        """Produce a new CPU position and a result"""
        pos += 1 + self.arg_count + int(self.output)
        return pos, self.f(*args)


class JumpInstruction(Instruction):
    def __call__(self, pos: int, *args: int, **kwargs: Any) -> Tuple[int, Any]:
        """Use last argument as jump target if result is true-ish"""
        *jmpargs, jump_to = args
        pos, result = super().__call__(pos, *jmpargs)
        return jump_to if result else pos, result


@dataclass
class BoundInstruction:
    instruction: InstructionBase
    modes: Tuple[ParameterMode, ...]
    # where to read the arg values from
    offset: int
    cpu: CPU

    def __call__(self) -> int:
        mem, pos, registers, instr = (
            self.cpu.memory,
            self.cpu.pos,
            self.cpu.registers,
            self.instruction,
        )
        # apply each parameter mode to the memory values
        args = (
            param.get(mem, mem[i], registers=registers)
            for i, param in enumerate(self.modes[: instr.arg_count], start=self.offset)
        )
        newpos, result = instr(pos, *args, registers=registers)
        if instr.output:
            target = mem[self.offset + instr.arg_count]
            self.modes[-1].set(mem, target, int(result), registers=registers)
        return newpos


InstructionSet = Mapping[int, InstructionBase]


class CPU:
    memory: Memory
    pos: int
    opcodes: InstructionSet
    registers: Registers

    def __init__(self, opcodes: InstructionSet) -> None:
        self.opcodes = opcodes

    def __getitem__(self, opcode: int) -> BoundInstruction:
        return self.opcodes[opcode % 100].bind(opcode, self)

    def reset(self: T, memory: Optional[Union[List, Memory]] = None) -> T:
        if memory is None:
            memory = Memory()
        self.memory = Memory(memory)
        self.pos: int = 0
        self.registers = {"relative base": 0}
        return self  # allow chaining

    def execute(self) -> None:
        mem = self.memory
        try:
            while True:
                self.pos = self[mem[self.pos]]()
        except Halt:
            return


base_opcodes = {
    1: Instruction(operator.add, 2, True),
    2: Instruction(operator.mul, 2, True),
    3: Instruction(partial(input, "i> "), output=True),
    4: Instruction(print, 1),
    5: JumpInstruction(bool, 2),
    6: JumpInstruction(operator.not_, 2),
    7: Instruction(operator.lt, 2, True),
    8: Instruction(operator.eq, 2, True),
    9: AdjustRelativeBaseInstruction(),
    99: Instruction(Halt.halt),
}


@overload
def ioset(
    *inputs: Iterable[int], opcodes: Optional[InstructionSet] = None
) -> Tuple[List[int], InstructionSet]:
    ...


@overload
def ioset(
    *inputs: int, opcodes: Optional[InstructionSet] = None
) -> Tuple[List[int], InstructionSet]:
    ...


def ioset(
    *inputs: Union[int, Iterable[int]],
    opcodes: Optional[InstructionSet] = None,
) -> Tuple[List[int], InstructionSet]:
    """Create an output list and instructionset with given input"""
    if opcodes is None:
        opcodes = {}
    outputs: List[int] = []
    if len(inputs) == 1 and not isinstance(inputs[0], int):
        # a single input can be an iterable, in which case it provides
        # all inputs.
        inputs = cast(Iterable[int], iter(inputs[0]))  # type: ignore
    else:
        assert all(isinstance(i, int) for i in inputs)
    get_input = partial(next, iter(inputs))
    return (
        outputs,
        {
            **base_opcodes,
            **opcodes,
            3: Instruction(get_input, output=True),
            4: Instruction(outputs.append, 1),
        },
    )


if __name__ == "__main__":
    test_mem = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    cpu = CPU(base_opcodes)
    cpu.reset(test_mem).execute()
    assert cpu.memory[0] == 3500

    def test_jumpcodes(instr: List[int], tests: Mapping[int, int]) -> None:
        for inp, expected in tests.items():
            outputs, test_opcodes = ioset(inp)
            CPU(test_opcodes).reset(instr).execute()
            assert outputs == [expected]

    test_tests = (
        # input == 8, position mode
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], {8: 1, 7: 0}),
        # input < 8, position mode
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], {7: 1, 8: 0}),
        # input == 8, immediate mode
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], {8: 1, 7: 0}),
        # input < 8, position mode
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], {7: 1, 8: 0}),
        # cmp(input, 8), producing 999, 1000, 1001
        (
            [
                3,
                21,
                1008,
                21,
                8,
                20,
                1005,
                20,
                22,
                107,
                8,
                21,
                20,
                1006,
                20,
                31,
                1106,
                0,
                36,
                98,
                0,
                0,
                1002,
                21,
                125,
                20,
                4,
                20,
                1105,
                1,
                46,
                104,
                999,
                1105,
                1,
                46,
                1101,
                1000,
                1,
                20,
                4,
                20,
                1105,
                1,
                46,
                98,
                99,
            ],
            {7: 999, 8: 1000, 42: 1001},
        ),
    )
    for test in test_tests:
        test_jumpcodes(*test)

    outputs, test_opcodes = ioset()
    cpu = CPU(test_opcodes)

    quine = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    cpu.reset(quine).execute()
    assert outputs == quine

    outputs[:] = []
    large_num = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    cpu.reset(large_num).execute()
    assert outputs == [large_num[1] * large_num[2]]

    large_num_1 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
    cpu.reset(large_num_1).execute()
    assert outputs[-1] == large_num[1] * large_num[2]

    large_num_2 = [104, 1125899906842624, 99]
    cpu.reset(large_num_2).execute()
    assert outputs[-1] == large_num_2[1]
