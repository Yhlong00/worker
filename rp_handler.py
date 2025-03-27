"""Example handler file."""

import runpod
import time
import random
import json
from dataclasses import dataclass, field, asdict
import typing
import os
import asyncio
from datetime import timedelta

logger = runpod.RunPodLogger()


@dataclass
class Range:
    min: float = 0
    max: float = 0
    current: float = -1.0

    def __post_init__(self):
        if self.current < 0:
            self.update()

    def update(self) -> float:
        current = random.uniform(self.min, self.max)
        self.current = current
        return current


class StateDict(typing.TypedDict, total=False):
    cold_start_range: typing.Optional[Range]
    execution_range: typing.Optional[Range]
    concurrency: typing.Optional[int]


@dataclass
class State:
    __cache__: typing.ClassVar[typing.Union[None, "State"]] = None
    updated_at: int = time.time_ns()
    filename: str = "state.json"
    cold_start_range: Range = field(default_factory=Range)
    execution_range: Range = field(default_factory=Range)
    concurrency: int = 1

    @staticmethod
    def load_from_env():
        minimum = float(os.environ.get("COLD_START_MIN", 0))
        maximum = max(float(os.environ.get("COLD_START_MAX", 0)), minimum)
        delay = float(os.environ.get("COLD_START_DELAY", 0))
        return State(
            updated_at=time.time_ns(),
            cold_start_range=Range(
                min=minimum,
                max=maximum,
                current=delay,
            ),
        )

    @staticmethod
    def load_from_file(filename: str = "state.json"):
        if not os.path.exists(filename):
            input = State.load_from_env()
            input.save_to_file(filename)
            return input
        with open(filename, "r") as f:
            input = json.load(f)
        return State(**input)

    def save_to_file(self, filename: str = "state.json"):
        filename = self.filename
        dct = asdict(self)
        dct["cold_start_range"] = asdict(self.cold_start_range)
        dct["execution_range"] = asdict(self.execution_range)
        json.dump(dct, open(filename, "w"))

    def update(self, dct: StateDict):
        for key in self.__dict__.keys():
            if key in dct:
                self.__dict__[key] = dct[key]
                self.updated_at = time.time_ns()
        self.execution_range.update()
        self.cold_start_range.update()
        self.save_to_file()

    # def __json__(self) -> dict[str, typing.Any]:
    #     return {
    #         "updated_at": self.updated_at,
    #         "cold_start_range": asdict(self.cold_start_range),
    #         "execution_range": asdict(self.execution_range),
    #         "concurrency": self.concurrency,
    #     }


@dataclass
class TaskOutput:
    started_at: int
    ended_at: int
    execution_duration: int


@dataclass
class TaskInput:
    execution_duration: timedelta


@dataclass
class JobOutput:
    state: State
    started_at: int
    results: list[TaskOutput]
    ended_at: int
    execution_duration: int
    queue_duration: int


@dataclass
class JobInput:
    created_at: int
    state: typing.Optional[StateDict] = None


state = State.load_from_file(os.environ.get("STATE_FILE", "state.json"))

time.sleep(state.cold_start_range.current)


def get_concurrency(*args: typing.Any, **kwargs: typing.Any) -> int:
    return state.concurrency


async def run_task(input: TaskInput) -> TaskOutput:
    started_at = time.time_ns()
    await asyncio.sleep(input.execution_duration.total_seconds())
    ended_at = time.time_ns()
    return TaskOutput(
        started_at=started_at,
        ended_at=ended_at,
        execution_duration=ended_at - started_at,
    )


async def handler(job: dict[str, typing.Any]) -> JobOutput:
    started_at = time.time_ns()
    input = JobInput(**job.get("input", {}))
    logger.info(f"Job input: {input}")
    if input.state is not None:
        state.update(input.state)
    logger.info(f"State: {state}")
    output = JobOutput(
        state=state,
        started_at=started_at,
        results=[],
        ended_at=0,
        execution_duration=0,
        queue_duration=started_at - input.created_at,
    )
    results = await asyncio.gather(
        *(
            run_task(
                TaskInput(
                    execution_duration=timedelta(seconds=state.execution_range.current)
                )
            )
            for _ in range(state.concurrency)
        )
    )
    logger.info(f"Results: {results}")
    output.results = results
    output.ended_at = time.time_ns()
    output.execution_duration = output.ended_at - output.started_at
    logger.info(f"Output: {output}")
    return output


if __name__ == "__main__":
    runpod.serverless.start({"handler": handler, "concurrency": get_concurrency})
