"""
Main Moodle API client.

Provides a unified interface to all Moodle modules through composition.
This is a facade pattern that aggregates specialized modules.
"""

import logging
from typing import Optional
from .groups import MoodleGroups
from .assignments import MoodleAssignments
from .grades import MoodleGrades
from .users import MoodleUsers
from .courses import MoodleCourses


class MoodleAPI:
    """
    Main facade class for interacting with Moodle API.
    
    This class aggregates specialized modules for different Moodle functionalities:
    - courses: Course and enrollment management
    - groups: Group, grouping, and cohort management
    - assignments: Assignment and submission handling
    - grades: Grade management
    - users: User account management
    
    Example:
        >>> moodle = MoodleAPI("https://moodle.example.com", "token")
        >>> moodle.courses.get_user_courses()
        >>> moodle.groups.add_user_to_group(group_id=1, user_id=42)
        >>> moodle.users.create_user("johndoe", "pass123", "John", "Doe", "john@example.com")
        >>> moodle.assignments.get_assignments(course_id=123)
    """

    def __init__(self, moodle_url: str, token: str, timeout: int = 30,
                 logger: Optional[logging.Logger] = None):
        """
        Initialize the Moodle API client with all modules.

        Args:
            moodle_url: Base URL of the Moodle instance (e.g., 'https://moodle.example.com')
            token: Web service token for authentication
            timeout: Request timeout in seconds (default: 30)
            logger: Optional logger instance (will be shared across all modules)

        Raises:
            ValueError: If moodle_url or token is empty
        """
        if not moodle_url or not token:
            raise ValueError("Both moodle_url and token are required")

        # Initialize all specialized modules with shared logger
        self.courses = MoodleCourses(moodle_url, token, timeout=timeout, logger=logger)
        self.groups = MoodleGroups(moodle_url, token, timeout=timeout, logger=logger)
        self.assignments = MoodleAssignments(moodle_url, token, timeout=timeout, logger=logger)
        self.grades = MoodleGrades(moodle_url, token, timeout=timeout, logger=logger)
        self.users = MoodleUsers(moodle_url, token, timeout=timeout, logger=logger)

        # Store base module for direct API access
        self._base = self.groups  # Reuse base from one of the modules

    def get_site_info(self) -> dict:
        """
        Get information about the Moodle site including version.
        
        This method retrieves general information about the Moodle site,
        including the Moodle version, site name, and available functions.
        
        Returns:
            Dictionary containing site information with keys:
                - sitename: Name of the Moodle site
                - username: Current user's username
                - firstname: Current user's first name
                - lastname: Current user's last name
                - release: Moodle version (e.g., "4.1.1 (Build: 20230123)")
                - version: Moodle version code
                - functions: List of available web service functions
                
        Example:
            >>> moodle = MoodleAPI("https://moodle.com", "token")
            >>> info = moodle.get_site_info()
            >>> print(f"Moodle version: {info['release']}")
            Moodle version: 4.1.1 (Build: 20230123)
            
        Raises:
            MoodleAuthenticationError: If authentication fails
            MoodleAPIError: If the API call fails
        """
        return self._base.call_api('core_webservice_get_site_info')

    def check_moodle_version(self, min_version: str = "3.9") -> bool:
        """
        Check if the Moodle version meets the minimum requirement.
        
        Args:
            min_version: Minimum required version (e.g., "3.9", "4.0")
            
        Returns:
            True if Moodle version >= min_version, False otherwise
            
        Example:
            >>> moodle = MoodleAPI("https://moodle.com", "token")
            >>> if moodle.check_moodle_version("3.9"):
            ...     print("Moodle version is compatible")
        """
        try:
            info = self.get_site_info()
            release = info.get('release', '')
            # Extract version number (e.g., "4.1.1" from "4.1.1 (Build: 20230123)")
            import re
            match = re.match(r'(\d+\.\d+)', release)
            if match:
                current_version = match.group(1)
                # Simple version comparison
                current_parts = [int(x) for x in current_version.split('.')]
                min_parts = [int(x) for x in min_version.split('.')]
                
                # Pad shorter version with zeros
                while len(current_parts) < len(min_parts):
                    current_parts.append(0)
                while len(min_parts) < len(current_parts):
                    min_parts.append(0)
              
                return current_parts >= min_parts
        except Exception:
            pass
        return False

    def check_permissions(self, verbose: bool = True) -> dict:
        """
        Verify that all required Moodle web service permissions are granted.
        
        This method tests each web service function required by edutools-moodle
        to ensure proper configuration. It's recommended to run this after
        setting up your Moodle web service.
        
        Args:
            verbose: If True, print detailed results for each permission check
            
        Returns:
            Dictionary with permission check results:
                - 'total': Total number of permissions checked
                - 'granted': Number of permissions granted
                - 'denied': Number of permissions denied
                - 'details': List of dicts with 'function', 'module', 'status', 'error'
                - 'missing': List of missing function names
                
        Example:
            >>> moodle = MoodleAPI("https://moodle.com", "token")
            >>> result = moodle.check_permissions()
            >>> if result['denied'] > 0:
            ...     print(f"Missing permissions: {result['missing']}")
        """
        from .base import MoodleAPIError
        
        # Temporarily disable error logging during permission checks
        import logging
        original_level = self._base.logger.level
        self._base.logger.setLevel(logging.CRITICAL)  # Only show critical errors
        
        try:
            return self._check_permissions_impl(verbose)
        finally:
            # Restore original logging level
            self._base.logger.setLevel(original_level)
    
    def _check_permissions_impl(self, verbose: bool) -> dict:
        """Internal implementation of permission checking."""
        from .base import MoodleAPIError
        
        # Define all required permissions grouped by module
        required_permissions = {
            'core': [
                ('core_webservice_get_site_info', 'Get site information'),
            ],
            'courses': [
                ('core_enrol_get_users_courses', 'Get user courses'),
                ('core_enrol_get_enrolled_users', 'Get enrolled users'),
                ('core_course_get_courses_by_field', 'Get courses by field'),
                ('core_course_get_categories', 'Get course categories'),
                ('core_course_get_contents', 'Get course contents'),
                ('core_course_get_recent_courses', 'Get recent courses'),
                ('core_course_search_courses', 'Search courses'),
            ],
            'groups': [
                ('core_group_get_course_groups', 'Get course groups'),
                ('core_group_get_group_members', 'Get group members'),
                ('core_group_add_group_members', 'Add users to group'),
                ('core_group_delete_group_members', 'Remove users from group'),
                ('core_group_create_groups', 'Create groups'),
                ('core_group_delete_groups', 'Delete groups'),
            ],
            'assignments': [
                ('mod_assign_get_assignments', 'Get assignments'),
                ('mod_assign_get_submissions', 'Get submissions'),
            ],
            'grades': [
                ('mod_assign_get_grades', 'Get grades'),
                ('mod_assign_save_grade', 'Save grade'),
            ],
            'users': [
                ('core_user_create_users', 'Create users'),
                ('core_user_get_users', 'Get users'),
                ('core_user_update_users', 'Update users'),
            ],
        }
        
        results = {
            'total': 0,
            'granted': 0,
            'denied': 0,
            'details': [],
            'missing': []
        }
        
        if verbose:
            print("\n" + "="*80)
            print("MOODLE WEB SERVICE PERMISSIONS CHECK")
            print("="*80)
        
        # Check each permission
        for module, functions in required_permissions.items():
            if verbose:
                print(f"\n📦 Module: {module.upper()}")
                print("-" * 80)
            
            for function_name, description in functions:
                results['total'] += 1
                status = 'granted'
                error_msg = None
                
                try:
                    # Try to call the function with minimal parameters
                    if function_name == 'core_webservice_get_site_info':
                        self._base.call_api(function_name)
                    elif function_name == 'core_enrol_get_users_courses':
                        # Will fail if no userid, but permission error is different
                        try:
                            self._base.call_api(function_name, {'userid': 1})
                        except MoodleAPIError as e:
                            if 'not valid' in str(e).lower() or 'not found' in str(e).lower():
                                pass  # Expected error, permission is OK
                            else:
                                raise
                    elif function_name in ['core_enrol_get_enrolled_users', 'core_group_get_course_groups',
                                          'core_course_get_contents', 'mod_assign_get_assignments']:
                        try:
                            param_name = 'courseid' if 'course' in function_name or 'enrol' in function_name or 'group' in function_name else 'courseids'
                            if function_name == 'mod_assign_get_assignments':
                                self._base.call_api(function_name, {'courseids': [1]})
                            else:
                                self._base.call_api(function_name, {param_name: 1})
                        except MoodleAPIError as e:
                            if 'not valid' in str(e).lower() or 'not found' in str(e).lower() or 'cannot find' in str(e).lower():
                                pass
                            else:
                                raise
                    elif function_name == 'core_course_get_courses_by_field':
                        self._base.call_api(function_name, {'field': 'id', 'value': 1})
                    elif function_name == 'core_course_get_categories':
                        self._base.call_api(function_name, {})
                    elif function_name == 'core_course_get_recent_courses':
                        try:
                            self._base.call_api(function_name, {'userid': 1})
                        except MoodleAPIError as e:
                            if 'not valid' in str(e).lower() or 'not found' in str(e).lower():
                                pass
                            else:
                                raise
                    elif function_name == 'core_course_search_courses':
                        self._base.call_api(function_name, {'criterianame': 'search', 'criteriavalue': 'test'})
                    else:
                        # For other functions, just try with empty params or minimal params
                        try:
                            if 'get' in function_name:
                                self._base.call_api(function_name, {'id': 1})
                            else:
                                self._base.call_api(function_name, {})
                        except MoodleAPIError as e:
                            if 'required' in str(e).lower() or 'missing' in str(e).lower() or 'not valid' in str(e).lower():
                                pass
                            else:
                                raise
                    
                    results['granted'] += 1
                    if verbose:
                        print(f"  ✅ {function_name:<45} {description}")
                    
                except MoodleAPIError as e:
                    error_str = str(e).lower()
                    if 'not authorised' in error_str or 'access denied' in error_str or 'permission' in error_str or 'capability' in error_str:
                        status = 'denied'
                        error_msg = str(e)
                        results['denied'] += 1
                        results['missing'].append(function_name)
                        if verbose:
                            print(f"  ❌ {function_name:<45} PERMISSION DENIED")
                    else:
                        # Other errors (invalid params, not found, etc.) mean permission is OK
                        results['granted'] += 1
                        if verbose:
                            print(f"  ✅ {function_name:<45} {description}")
                except Exception as e:
                    status = 'error'
                    error_msg = str(e)
                    results['denied'] += 1
                    if verbose:
                        print(f"  ⚠️  {function_name:<45} ERROR: {e}")
                
                results['details'].append({
                    'function': function_name,
                    'module': module,
                    'description': description,
                    'status': status,
                    'error': error_msg
                })
        
        if verbose:
            print("\n" + "="*80)
            print("SUMMARY")
            print("="*80)
            print(f"Total permissions checked: {results['total']}")
            print(f"✅ Granted: {results['granted']}")
            print(f"❌ Denied: {results['denied']}")
            
            if results['denied'] > 0:
                print("\n⚠️  MISSING PERMISSIONS:")
                print("Add these functions to your Moodle web service:")
                for func in results['missing']:
                    print(f"  - {func}")
                print("\nSee PERMISSIONS.md for detailed setup instructions.")
            else:
                print("\n✅ All required permissions are granted!")
        
        return results

    def __repr__(self) -> str:
        """String representation of the MoodleAPI instance."""
        return f"<MoodleAPI: courses, groups, assignments, grades, users>"
