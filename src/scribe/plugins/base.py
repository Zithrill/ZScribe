from abc import ABC, abstractmethod


class BasePlugin(ABC):
    @abstractmethod
    def list_models(self) -> list[str]:
        pass

    @abstractmethod
    def generate_commit_message(self, diff_summary: str) -> str:
        pass

    @abstractmethod
    def refine_commit_message(self, message: str, diff_summary: str) -> str:
        pass

    @abstractmethod
    def generate_pull_request_message(self, diff_summary: str, commit_messages: list[str]) -> str:
        pass