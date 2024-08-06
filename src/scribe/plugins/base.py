from abc import ABC, abstractmethod
from typing import List


class BasePlugin(ABC):

    @abstractmethod
    def generate_commit_message(self, diff_summary: str) -> str:
        pass

    @abstractmethod
    def refine_commit_message(self, message: str, diff_summary: str) -> str:
        pass

    @abstractmethod
    def generate_pull_request_message(self, diff_summary: str, commit_messages: List[str]) -> str:
        pass
