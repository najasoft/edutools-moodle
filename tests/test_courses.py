"""
Unit tests for MoodleCourses module.
"""
import pytest
from unittest.mock import Mock, patch
from edutools_moodle import MoodleCourses, MoodleAPIError


@pytest.fixture
def mock_courses():
    """Create a MoodleCourses instance with mocked API calls."""
    courses = MoodleCourses("https://test.moodle.com", "test_token")
    courses.call_api = Mock()
    return courses


class TestGetUserCourses:
    """Tests for get_user_courses method."""
    
    def test_get_user_courses_with_user_id(self, mock_courses):
        """Test getting courses for a specific user."""
        mock_courses.call_api.return_value = [
            {'id': 1, 'shortname': 'CS101', 'fullname': 'Computer Science 101'},
            {'id': 2, 'shortname': 'MATH201', 'fullname': 'Mathematics 201'}
        ]
        
        result = mock_courses.get_user_courses(user_id=42)
        
        assert len(result) == 2
        assert result[0]['shortname'] == 'CS101'
        mock_courses.call_api.assert_called_once_with(
            'core_enrol_get_users_courses',
            {'userid': 42}
        )
    
    def test_get_user_courses_without_user_id(self, mock_courses):
        """Test getting courses for authenticated user."""
        mock_courses.call_api.side_effect = [
            {'userid': 99},  # get_site_info response
            [{'id': 1, 'shortname': 'CS101'}]  # get_users_courses response
        ]
        
        result = mock_courses.get_user_courses()
        
        assert len(result) == 1
        assert mock_courses.call_api.call_count == 2


class TestGetEnrolledUsers:
    """Tests for get_enrolled_users method."""
    
    def test_get_enrolled_users_basic(self, mock_courses):
        """Test getting enrolled users without options."""
        mock_courses.call_api.return_value = [
            {'id': 1, 'firstname': 'John', 'lastname': 'Doe'},
            {'id': 2, 'firstname': 'Jane', 'lastname': 'Smith'}
        ]
        
        result = mock_courses.get_enrolled_users(course_id=123)
        
        assert len(result) == 2
        assert result[0]['firstname'] == 'John'
        mock_courses.call_api.assert_called_once_with(
            'core_enrol_get_enrolled_users',
            {'courseid': 123}
        )
    
    def test_get_enrolled_users_with_options(self, mock_courses):
        """Test getting enrolled users with filter options."""
        mock_courses.call_api.return_value = [
            {'id': 1, 'firstname': 'John'}
        ]
        
        options = [
            {'name': 'onlyactive', 'value': 1},
            {'name': 'userfields', 'value': 'email'}
        ]
        
        result = mock_courses.get_enrolled_users(course_id=123, options=options)
        
        assert len(result) == 1
        call_args = mock_courses.call_api.call_args[0][1]
        assert call_args['courseid'] == 123
        assert call_args['options[0][name]'] == 'onlyactive'
        assert call_args['options[1][name]'] == 'userfields'


class TestGetCourseByField:
    """Tests for get_course_by_field method."""
    
    def test_get_course_by_id(self, mock_courses):
        """Test getting course by ID."""
        mock_courses.call_api.return_value = {
            'courses': [{'id': 123, 'fullname': 'Test Course'}]
        }
        
        result = mock_courses.get_course_by_field('id', 123)
        
        assert len(result) == 1
        assert result[0]['id'] == 123
        mock_courses.call_api.assert_called_once_with(
            'core_course_get_courses_by_field',
            {'field': 'id', 'value': 123}
        )
    
    def test_get_course_by_shortname(self, mock_courses):
        """Test getting course by shortname."""
        mock_courses.call_api.return_value = {
            'courses': [{'shortname': 'CS101'}]
        }
        
        result = mock_courses.get_course_by_field('shortname', 'CS101')
        
        assert len(result) == 1
        assert result[0]['shortname'] == 'CS101'


class TestGetCategories:
    """Tests for get_categories method."""
    
    def test_get_all_categories(self, mock_courses):
        """Test getting all categories without criteria."""
        mock_courses.call_api.return_value = [
            {'id': 1, 'name': 'Science', 'coursecount': 5},
            {'id': 2, 'name': 'Arts', 'coursecount': 3}
        ]
        
        result = mock_courses.get_categories()
        
        assert len(result) == 2
        assert result[0]['name'] == 'Science'
        mock_courses.call_api.assert_called_once_with(
            'core_course_get_categories',
            {}
        )
    
    def test_get_categories_with_criteria(self, mock_courses):
        """Test getting categories with search criteria."""
        mock_courses.call_api.return_value = [
            {'id': 1, 'name': 'Science'}
        ]
        
        criteria = [{'key': 'id', 'value': '1'}]
        result = mock_courses.get_categories(criteria=criteria)
        
        assert len(result) == 1
        call_args = mock_courses.call_api.call_args[0][1]
        assert call_args['criteria[0][key]'] == 'id'


class TestGetCourseContents:
    """Tests for get_course_contents method."""
    
    def test_get_course_contents(self, mock_courses):
        """Test getting course contents."""
        mock_courses.call_api.return_value = [
            {
                'id': 1,
                'name': 'Topic 1',
                'modules': [
                    {'id': 10, 'modname': 'assign', 'name': 'Assignment 1'},
                    {'id': 11, 'modname': 'quiz', 'name': 'Quiz 1'}
                ]
            }
        ]
        
        result = mock_courses.get_course_contents(course_id=123)
        
        assert len(result) == 1
        assert result[0]['name'] == 'Topic 1'
        assert len(result[0]['modules']) == 2
        mock_courses.call_api.assert_called_once_with(
            'core_course_get_contents',
            {'courseid': 123}
        )


class TestGetRecentCourses:
    """Tests for get_recent_courses method."""
    
    def test_get_recent_courses_with_user_id(self, mock_courses):
        """Test getting recent courses for specific user."""
        mock_courses.call_api.return_value = [
            {'id': 1, 'fullname': 'Recent Course 1'},
            {'id': 2, 'fullname': 'Recent Course 2'}
        ]
        
        result = mock_courses.get_recent_courses(user_id=42, limit=5)
        
        assert len(result) == 2
        mock_courses.call_api.assert_called_once_with(
            'core_course_get_recent_courses',
            {'userid': 42, 'limit': 5}
        )
    
    def test_get_recent_courses_default_limit(self, mock_courses):
        """Test getting recent courses with default limit."""
        mock_courses.call_api.side_effect = [
            {'userid': 99},
            [{'id': 1}]
        ]
        
        result = mock_courses.get_recent_courses()
        
        assert len(result) == 1
        call_args = mock_courses.call_api.call_args_list[1][0][1]
        assert call_args['limit'] == 10


class TestSearchCourses:
    """Tests for search_courses method."""
    
    def test_search_courses(self, mock_courses):
        """Test searching courses by keyword."""
        mock_courses.call_api.return_value = {
            'courses': [
                {'id': 1, 'fullname': 'Python Programming'},
                {'id': 2, 'fullname': 'Advanced Python'}
            ],
            'warnings': []
        }
        
        result = mock_courses.search_courses('Python', page=0, perpage=20)
        
        assert len(result['courses']) == 2
        assert result['courses'][0]['fullname'] == 'Python Programming'
        mock_courses.call_api.assert_called_once_with(
            'core_course_search_courses',
            {
                'criterianame': 'search',
                'criteriavalue': 'Python',
                'page': 0,
                'perpage': 20
            }
        )


class TestGetEnrolledUsersByCapability:
    """Tests for get_enrolled_users_by_capability method."""
    
    def test_get_enrolled_users_by_capability(self, mock_courses):
        """Test getting users with specific capability."""
        mock_courses.call_api.return_value = [
            {'id': 1, 'firstname': 'Student1'},
            {'id': 2, 'firstname': 'Student2'}
        ]
        
        result = mock_courses.get_enrolled_users_by_capability(
            course_id=123,
            capability='mod/assignment:submit'
        )
        
        assert len(result) == 2
        call_args = mock_courses.call_api.call_args[0][1]
        assert call_args['courseid'] == 123
        assert call_args['options[0][name]'] == 'withcapability'
        assert call_args['options[0][value]'] == 'mod/assignment:submit'


class TestGetCourseModules:
    """Tests for get_course_modules method."""
    
    def test_get_course_modules(self, mock_courses):
        """Test getting all modules from a course."""
        mock_courses.call_api.return_value = [
            {
                'modules': [
                    {'id': 1, 'modname': 'assign'},
                    {'id': 2, 'modname': 'quiz'}
                ]
            },
            {
                'modules': [
                    {'id': 3, 'modname': 'forum'}
                ]
            }
        ]
        
        result = mock_courses.get_course_modules(course_id=123)
        
        assert len(result) == 3
        assert result[0]['modname'] == 'assign'
        assert result[1]['modname'] == 'quiz'
        assert result[2]['modname'] == 'forum'


class TestGetCourseById:
    """Tests for get_course_by_id method."""
    
    def test_get_course_by_id_found(self, mock_courses):
        """Test getting course by ID when found."""
        mock_courses.call_api.return_value = {
            'courses': [{'id': 123, 'fullname': 'Test Course'}]
        }
        
        result = mock_courses.get_course_by_id(course_id=123)
        
        assert result is not None
        assert result['id'] == 123
        assert result['fullname'] == 'Test Course'
    
    def test_get_course_by_id_not_found(self, mock_courses):
        """Test getting course by ID when not found."""
        mock_courses.call_api.return_value = {'courses': []}
        
        result = mock_courses.get_course_by_id(course_id=999)
        
        assert result is None


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_api_error_propagation(self, mock_courses):
        """Test that API errors are properly propagated."""
        mock_courses.call_api.side_effect = MoodleAPIError("API Error")
        
        with pytest.raises(MoodleAPIError):
            mock_courses.get_user_courses(user_id=42)
    
    def test_invalid_course_id(self, mock_courses):
        """Test handling of invalid course ID."""
        mock_courses.call_api.return_value = []
        
        result = mock_courses.get_enrolled_users(course_id=-1)
        
        assert result == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
