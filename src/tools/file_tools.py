"""File operations tools for patent document processing."""

from crewai_tools import FileReadTool, DirectoryReadTool

# Tool for reading individual files
file_read_tool = FileReadTool()

# Tool for reading all files in a directory
directory_read_tool = DirectoryReadTool()

__all__ = ["file_read_tool", "directory_read_tool"]
