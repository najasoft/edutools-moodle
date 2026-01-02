"""
Course management module for edutools-moodle.

This module provides functions for managing Moodle courses,
including retrieving enrolled users and user's courses.
"""

from typing import List, Dict, Any, Optional
from .base import MoodleBase


class MoodleCourses(MoodleBase):
    """Course operations for Moodle."""

    def get_user_courses(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all courses a user is enrolled in.
        
        Args:
            user_id: User ID. If None, uses the authenticated user.
            
        Returns:
            List of course dictionaries with keys:
                - id: Course ID
                - shortname: Course short name
                - fullname: Course full name
                - enrolledusercount: Number of enrolled users
                - idnumber: Course ID number
                - visible: Whether course is visible
                - summary: Course summary
                - summaryformat: Summary format (1=HTML, 0=plain text)
                - format: Course format (weeks, topics, etc.)
                - startdate: Course start timestamp
                - enddate: Course end timestamp
                
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> courses = moodle.get_user_courses()
            >>> for course in courses:
            ...     print(f"{course['shortname']}: {course['fullname']}")
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        if user_id is None:
            # Get current user ID from site info
            site_info = self.call_api('core_webservice_get_site_info')
            user_id = site_info.get('userid')
        
        params = {'userid': user_id}
        return self.call_api('core_enrol_get_users_courses', params)
    
    def get_enrolled_users(self, course_id: int, 
                          options: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Get list of users enrolled in a course.
        
        Args:
            course_id: Course ID
            options: Optional list of option dictionaries:
                - {'name': 'withcapability', 'value': 'mod/assignment:submit'}
                - {'name': 'groupid', 'value': '1'}
                - {'name': 'onlyactive', 'value': 1}
                - {'name': 'userfields', 'value': 'email,groups'}
                
        Returns:
            List of user dictionaries with keys:
                - id: User ID
                - username: Username
                - firstname: First name
                - lastname: Last name
                - fullname: Full name
                - email: Email address
                - department: Department
                - firstaccess: First access timestamp
                - lastaccess: Last access timestamp
                - lastcourseaccess: Last course access timestamp
                - description: User description
                - profileimageurlsmall: Small profile image URL
                - profileimageurl: Profile image URL
                - groups: List of groups (if requested)
                - roles: List of roles (if requested)
                
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> students = moodle.get_enrolled_users(123)
            >>> print(f"{len(students)} students enrolled")
            
            >>> # Get only active users with email field
            >>> options = [
            ...     {'name': 'onlyactive', 'value': 1},
            ...     {'name': 'userfields', 'value': 'email'}
            ... ]
            >>> students = moodle.get_enrolled_users(123, options)
            
        Raises:
            MoodleAPIError: If the API call fails
            MoodleResourceNotFoundError: If course not found
        """
        params = {'courseid': course_id}
        
        if options:
            for idx, option in enumerate(options):
                params[f'options[{idx}][name]'] = option['name']
                params[f'options[{idx}][value]'] = option['value']
        
        return self.call_api('core_enrol_get_enrolled_users', params)
    
    def get_course_by_field(self, field: str = 'id', value: Any = None) -> List[Dict[str, Any]]:
        """
        Get courses by field value.
        
        Args:
            field: Field name to search ('id', 'ids', 'shortname', 'idnumber', 'category')
            value: Value to search for
            
        Returns:
            List of course dictionaries
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> courses = moodle.get_course_by_field('shortname', 'CS101')
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        params = {
            'field': field,
            'value': value
        }
        result = self.call_api('core_course_get_courses_by_field', params)
        return result.get('courses', [])
    
    def get_categories(self, criteria: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Get course categories.
        
        Args:
            criteria: Optional search criteria:
                - {'key': 'id', 'value': '1'}
                - {'key': 'name', 'value': 'Category Name'}
                - {'key': 'parent', 'value': '0'}
                
        Returns:
            List of category dictionaries
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> categories = moodle.get_categories()
            >>> for cat in categories:
            ...     print(f"{cat['name']} ({cat['coursecount']} courses)")
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        params = {}
        
        if criteria:
            for idx, criterion in enumerate(criteria):
                params[f'criteria[{idx}][key]'] = criterion['key']
                params[f'criteria[{idx}][value]'] = criterion['value']
        
        return self.call_api('core_course_get_categories', params)
    
    def get_course_contents(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Get course contents (sections and modules).
        
        Args:
            course_id: Course ID
            
        Returns:
            List of section dictionaries with modules
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> sections = moodle.get_course_contents(123)
            >>> for section in sections:
            ...     print(f"Section: {section['name']}")
            ...     for module in section['modules']:
            ...         print(f"  - {module['modname']}: {module['name']}")
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        params = {'courseid': course_id}
        return self.call_api('core_course_get_contents', params)
    
    def get_recent_courses(self, user_id: Optional[int] = None, 
                          limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get user's recently accessed courses.
        
        Args:
            user_id: User ID. If None, uses the authenticated user.
            limit: Maximum number of courses to return (default: 10)
            
        Returns:
            List of recently accessed course dictionaries
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> recent = moodle.get_recent_courses(limit=5)
            >>> for course in recent:
            ...     print(f"{course['fullname']} - Last access: {course['timeaccess']}")
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        if user_id is None:
            site_info = self.call_api('core_webservice_get_site_info')
            user_id = site_info.get('userid')
        
        params = {
            'userid': user_id,
            'limit': limit
        }
        return self.call_api('core_course_get_recent_courses', params)
    
    def search_courses(self, search: str, page: int = 0, 
                      perpage: int = 10) -> Dict[str, Any]:
        """
        Search for courses by name, shortname, or summary.
        
        Args:
            search: Search string
            page: Page number (0-indexed)
            perpage: Courses per page
            
        Returns:
            Dictionary with 'courses' and 'warnings' keys
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> result = moodle.search_courses("Python", page=0, perpage=20)
            >>> print(f"Found {len(result['courses'])} courses")
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        params = {
            'criterianame': 'search',
            'criteriavalue': search,
            'page': page,
            'perpage': perpage
        }
        return self.call_api('core_course_search_courses', params)
    
    def get_enrolled_users_by_capability(self, course_id: int, 
                                        capability: str) -> List[Dict[str, Any]]:
        """
        Get users enrolled in a course with a specific capability.
        
        Args:
            course_id: Course ID
            capability: Capability string (e.g., 'mod/assignment:submit')
            
        Returns:
            List of user dictionaries with the specified capability
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> # Get all students who can submit assignments
            >>> students = moodle.get_enrolled_users_by_capability(
            ...     123, 'mod/assignment:submit'
            ... )
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        options = [
            {'name': 'withcapability', 'value': capability}
        ]
        return self.get_enrolled_users(course_id, options)
    
    def get_course_modules(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Get all activity modules in a course.
        
        Args:
            course_id: Course ID
            
        Returns:
            List of activity modules with their details
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> modules = moodle.get_course_modules(123)
            >>> assignments = [m for m in modules if m['modname'] == 'assign']
            >>> quizzes = [m for m in modules if m['modname'] == 'quiz']
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        sections = self.get_course_contents(course_id)
        modules = []
        for section in sections:
            for module in section.get('modules', []):
                modules.append(module)
        return modules
    
    def get_course_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a single course by ID.
        
        Args:
            course_id: Course ID
            
        Returns:
            Course dictionary or None if not found
            
        Example:
            >>> moodle = MoodleCourses("https://moodle.com", "token")
            >>> course = moodle.get_course_by_id(123)
            >>> if course:
            ...     print(f"Course: {course['fullname']}")
            
        Raises:
            MoodleAPIError: If the API call fails
        """
        courses = self.get_course_by_field('id', course_id)
        return courses[0] if courses else None
