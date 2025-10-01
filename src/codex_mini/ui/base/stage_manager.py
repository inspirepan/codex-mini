from __future__ import annotations

from enum import Enum
from typing import Awaitable, Callable


class Stage(Enum):
    WAITING = "waiting"
    THINKING = "thinking"
    ASSISTANT = "assistant"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"


class StageManager:
    """Manage display stage transitions and invoke lifecycle callbacks."""

    def __init__(
        self,
        *,
        finish_assistant: Callable[[], Awaitable[None]],
        finish_thinking: Callable[[], Awaitable[None]],
        on_enter_thinking: Callable[[], None],
    ):
        self._stage = Stage.WAITING
        self._finish_assistant = finish_assistant
        self._finish_thinking = finish_thinking
        self._on_enter_thinking = on_enter_thinking

    @property
    def current_stage(self) -> Stage:
        return self._stage

    async def transition_to(self, new_stage: Stage) -> None:
        if self._stage == new_stage:
            return
        await self._leave_current_stage()
        self._stage = new_stage

    async def enter_thinking_stage(self) -> None:
        if self._stage == Stage.THINKING:
            return
        await self.transition_to(Stage.THINKING)
        self._on_enter_thinking()

    async def finish_assistant(self) -> None:
        if self._stage != Stage.ASSISTANT:
            await self._finish_assistant()
            return
        await self._finish_assistant()
        self._stage = Stage.WAITING

    async def finish_thinking(self) -> None:
        await self._finish_thinking()
        if self._stage == Stage.THINKING:
            self._stage = Stage.WAITING

    async def _leave_current_stage(self) -> None:
        if self._stage == Stage.ASSISTANT:
            await self.finish_assistant()
        elif self._stage == Stage.THINKING:
            await self.finish_thinking()
        elif self._stage != Stage.WAITING:
            self._stage = Stage.WAITING
