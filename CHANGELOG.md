# Changelog

All notable changes to the edutools-moodle package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.2] - 2025-01-02

### Added
- **MoodleGroups Module**: Enhanced groupings management with 5 new methods
  - `get_grouping_groups(grouping_id, course_id)` - Get all groups belonging to a specific grouping
  - `get_grouping_groups_with_members(grouping_id, course_id)` - Get grouping groups with member counts
  - `get_groups_by_member_count(course_id, min_members, max_members)` - Filter groups by size
  - `assign_group_to_grouping(grouping_id, group_id)` - Assign a group to a grouping
  - `unassign_group_from_grouping(grouping_id, group_id)` - Remove a group from a grouping

### Improved
- Complete grouping-to-group relationship management
- Efficient group filtering for large courses (e.g., 230 groups)
- Support for class grouping identification and filtering

### Documentation
- Updated PERMISSIONS.md with new grouping APIs and required user permissions
- Added examples for grouping-based filtering workflows

## [0.3.1] - 2025-01-02

### Added
- **MoodleGroups Module**: Added groupings management methods
  - `get_course_groupings(course_id)` - Get all groupings in a course
  - `get_grouping_by_name(course_id, grouping_name)` - Find a grouping by name
  - Support for filtering groups by grouping membership

### Improved
- Better grouping support for class/group organization
- Enhanced group filtering capabilities

## [0.3.0] - 2025-01-02

### Added
- **New MoodleCourses Module**: Comprehensive course management with 11 methods
  - `get_user_courses()` - Get courses enrolled by a user (or authenticated user)
  - `get_enrolled_users()` - Get all users enrolled in a course with optional filtering
  - `get_course_by_field()` - Search courses by field (id, shortname, idnumber, category)
  - `get_categories()` - Get all course categories with optional criteria
  - `get_course_contents()` - Get complete course structure (sections, modules, resources)
  - `get_recent_courses()` - Get recently accessed courses for a user
  - `search_courses()` - Full-text search for courses by name/summary
  - `get_enrolled_users_by_capability()` - Filter enrolled users by specific capability
  - `get_course_modules()` - Extract all activity modules from course contents
  - `get_course_by_id()` - Get a single course by its ID
  - All methods include comprehensive error handling and type hints

### Documentation
- Added **PERMISSIONS.md**: Complete documentation of all required Moodle web service functions
  - Per-module permission requirements (Courses, Groups, Assignments, Grades, Users)
  - Setup instructions for Moodle administrators
  - Minimum permissions for MoodleGrader application (8 functions)
  - SQL verification queries for database-level checks
  - Moodle version compatibility information (3.9+)

### Changed
- Updated `MoodleAPI` facade to include `courses` module initialization
- Updated `__init__.py` exports to include `MoodleCourses` class
- Updated README.md with new module documentation and examples
- Updated version badges to 0.3.0

### Testing
- Added 18 automated unit tests for MoodleCourses module (test_courses.py)
- Added 10 exploratory tests for manual validation (manual_test_courses.py)
- All tests passing with 100% success rate

## [0.2.1] - 2024-12-29

### Added
- PEP 561 compliance with `py.typed` marker file for full IDE IntelliSense support
- Type hints recognition in VSCode, PyCharm, and other IDEs
- Enhanced autocomplete and function signature hints

## [0.2.0] - 2024-12-29

### Fixed

#### MoodleBase Module
- **CRITICAL**: Completely rewrote `_validate_response()` method to properly handle Moodle API responses
- Fixed response validation to correctly identify warnings vs errors
- Improved error messages with detailed exception context

#### MoodleUsers Module (7 functions validated)
- Fixed `create_user()` - Corrected parameters and response handling
- Fixed `get_user_by_username()` - Now properly handles user search
- Fixed `get_user_by_email()` - Improved email-based user lookup
- Fixed `get_users_by_field()` - Enhanced field-based user queries
- Fixed `check_username_exists()` - Simplified boolean return logic
- Fixed `enroll_user_in_course()` - Corrected enrollment parameter structure
- Fixed `send_notification()` - Fixed notification delivery mechanism

#### MoodleGroups Module (20 functions validated)
- Fixed `get_course_groups()` - Optimized to return only essential group fields
- Fixed `get_user_groups()` - Removed non-existent groupingid filter parameter
- Fixed `add_user_to_group()` - Corrected API endpoint and parameters
- Fixed `remove_member_from_group()` - Fixed member removal logic
- Fixed `get_group_members()` - Enhanced member data retrieval
- Fixed `create_group()` - Added missing description parameter
- Fixed `delete_group()` - Implemented proper group deletion
- Fixed `update_group()` - Added complete update functionality
- Fixed `get_cohort_members()` - Corrected cohort member retrieval
- Fixed `check_user_in_cohort()` - Fixed cohort membership validation
- Fixed `get_cohorts()` - Added cohort listing functionality
- Fixed `create_cohort()` - Implemented cohort creation
- Fixed `delete_cohort()` - Added cohort deletion
- Fixed `update_cohort()` - Implemented cohort updates
- Fixed `add_cohort_members()` - Fixed batch member addition
- Fixed `remove_cohort_members()` - Fixed batch member removal
- Fixed `get_course_groupings()` - Added grouping retrieval
- Fixed `create_grouping()` - Implemented grouping creation
- Fixed `assign_group_to_grouping()` - Fixed group-grouping assignment
- Fixed `unassign_group_from_grouping()` - Added unassignment functionality

#### MoodleAssignments Module (4 functions validated)
- Fixed `get_assignments()` - Optimized to return only 11 essential assignment fields (reduced from 50+ fields)
- Fixed `get_assignment_id_by_cmid()` - Corrected course module ID to assignment ID mapping
- Fixed `get_user_submission()` - Optimized to return only 8 essential submission fields
- Removed `get_assignment_submissions()` - Function deleted (API endpoint deprecated/unavailable)

#### MoodleGrades Module (6 functions validated, 1 removed)
- Fixed `get_grades()` - Migrated from deprecated `core_grades_get_grades` to `gradereport_user_get_grade_items`
- Fixed `get_grades()` - Optimized to return only 10 essential fields per grade item (reduced from 30+ fields)
- Fixed `add_grade()` - Corrected parameter structure with proper feedback format
- Fixed `update_grade()` - Added all missing required parameters (attemptnumber, addattempt, workflowstate, applytoall)
- Fixed `update_grade()` - Changed from non-existent `mod_assign_save_grade` to `mod_assign_save_grades`
- Fixed `update_grade()` - Always include feedback structure to prevent NULL database errors
- Fixed `get_course_grades()` - Added required user_id parameter to prevent timeout on large courses
- Fixed `get_grades_for_assignment()` - Validated assignment-specific grade retrieval
- Removed `get_grade_items()` - API endpoint doesn't exist in Moodle, functionality available via `get_grades()`

### Added
- Complete API documentation extracted from Moodle instance (119 modules, 765 functions)
- Structured API reference in `docs/api/` directory with per-module Markdown files
- Added `docs/moodle_api_reference.html` - Complete offline API reference
- Added `docs/extract_api_docs.py` - Script to extract API documentation from HTML

### Improved
- **Performance**: Reduced response payload sizes across all modules by filtering unnecessary fields
- **MoodleGroups.get_course_groups()**: Reduced from 15+ fields to 6 essential fields per group
- **MoodleAssignments.get_assignments()**: Reduced from 50+ fields to 11 essential fields per assignment  
- **MoodleAssignments.get_user_submission()**: Reduced from 30+ fields to 8 essential fields per submission
- **MoodleGrades.get_grades()**: Reduced from 30+ fields to 10 essential fields per grade item
- Better error handling and validation across all modules
- Improved parameter documentation and type hints

### Changed
- **BREAKING**: `MoodleGrades.get_course_grades()` now requires `user_id` parameter (prevents timeout)
- **BREAKING**: Removed `MoodleAssignments.get_assignment_submissions()` (deprecated API)
- **BREAKING**: Removed `MoodleGrades.get_grade_items()` (API doesn't exist)
- Updated API endpoints to use current Moodle standards
- Standardized parameter naming across all modules

### Notes
- All 38 core functions systematically tested and validated
- 35 functions fully working, 2 removed (deprecated APIs), 1 has known limitations
- Tested against Moodle 3.9+ instance
- Known limitation: `add_grades()` may create incomplete feedback records in Moodle database (Moodle API limitation, not package bug)

## [0.1.0] - 2024-12-15

### Added
- Initial release
- Basic Moodle API wrapper with groups, users, assignments, and grades modules
- Composition-based architecture with MoodleAPI facade

### Known Issues (Fixed in 0.2.0)
- Response validation incorrectly treating warnings as errors
- Missing parameters in multiple functions
- Using deprecated/non-existent API endpoints
- Performance issues due to excessive data retrieval
- Incomplete error handling

---

## Migration Guide: 0.1.0 → 0.2.0

### Breaking Changes

1. **`get_course_grades()` requires user_id:**
   ```python
   # Before (0.1.0) - would timeout on large courses
   grades = api.grades.get_course_grades(course_id=34)
   
   # After (0.2.0) - requires user_id
   grades = api.grades.get_course_grades(course_id=34, user_id=123)
   ```

2. **Removed functions:**
   ```python
   # These functions no longer exist:
   api.assignments.get_assignment_submissions()  # Use get_user_submission() instead
   api.grades.get_grade_items()  # Use get_grades() instead
   ```

3. **Response structure changes:**
   - All functions now return fewer fields (optimized for performance)
   - Essential data preserved, verbose metadata removed
   - Check response structure if you rely on specific fields

### Recommended Updates

Update your code to handle the new optimized response structures:

```python
# Groups now return 6 fields instead of 15+
groups = api.groups.get_course_groups(course_id=34)
# Available fields: id, name, description, courseid, idnumber, timecreated

# Assignments now return 11 fields instead of 50+
assignments = api.assignments.get_assignments(course_ids=[34])
# Check documentation for available fields

# Grades optimized to 10 essential fields
grades = api.grades.get_grades(course_id=34, user_id=123)
# Available fields: userid, userfullname, gradeitems with 10 fields each
```
