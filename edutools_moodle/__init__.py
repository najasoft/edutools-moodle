"""
Edutools Moodle - Python package for Moodle API interactions in educational contexts.

Version: 0.3.3

Main exports:
    - MoodleAPI: Main facade API client (recommended)
    - MoodleBase: Base class for custom extensions
    - MoodleCourses: Course and enrollment management
    - MoodleGroups: Groups, groupings and cohorts management
    - MoodleAssignments: Assignments handling
    - MoodleGrades: Grades management
    - MoodleUsers: User account management
    
Exceptions:
    - MoodleAPIError: Base exception for API errors
    - MoodleAuthenticationError: Authentication failures
    - MoodleResourceNotFoundError: Resource not found
"""

from .base import (
    MoodleBase,
    MoodleAPIError,
    MoodleAuthenticationError,
    MoodleResourceNotFoundError
)
from .api import MoodleAPI
from .courses import MoodleCourses
from .groups import MoodleGroups
from .assignments import MoodleAssignments
from .grades import MoodleGrades
from .users import MoodleUsers

__version__ = "0.3.3"
__author__ = "Nadiri Abdeljalil"
__email__ = "nadiri@najasoft.com"

__all__ = [
    "MoodleAPI",
    "MoodleBase",
    "MoodleCourses",
    "MoodleGroups",
    "MoodleAssignments",
    "MoodleGrades",
    "MoodleUsers",
    "MoodleAPIError",
    "MoodleAuthenticationError",
    "MoodleResourceNotFoundError",
]
