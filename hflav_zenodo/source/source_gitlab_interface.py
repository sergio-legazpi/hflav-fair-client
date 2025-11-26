from abc import ABC, abstractmethod


class SourceGitlabInterface(ABC):
    """Interface to interact with GitLab repositories."""

    @abstractmethod
    def get_schema_inside_repository(self, tag_version="main") -> dict:
        """
        Retrieve the JSON schema file from the GitLab repository for a given tag version.
        :param tag_version: The tag or branch name to retrieve the schema from.
        :return: A dictionary representing the JSON schema.
        """
        pass
