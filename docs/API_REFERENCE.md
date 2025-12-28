# Edutools Moodle - Complete API Reference

**Version:** 0.1.0  
**Author:** Nadiri Abdeljalil  
**Date:** December 23, 2025

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Classes](#core-classes)
   - [MoodleAPI](#moodleapi)
   - [MoodleBase](#moodlebase)
   - [MoodleGroups](#moodlegroups)
   - [MoodleAssignments](#moodleassignments)
   - [MoodleGrades](#moodlegrades)
   - [MoodleUsers](#moodleusers)
5. [Exceptions](#exceptions)
6. [Examples](#examples)

---

## Overview

Edutools Moodle is a Python package that provides a clean, object-oriented interface for interacting with Moodle Web Services API. It simplifies common educational tasks such as:

- Managing groups, groupings, and cohorts
- Creating and managing assignments
- Handling grades and student submissions
- Managing user accounts and enrollments

**Requirements:**
- Python 3.8+
- Moodle 3.9+ (recommended)
- Valid Moodle Web Services token

---

## Installation

### From source (development mode)

```bash
git clone https://github.com/najasoft/edutools-moodle.git
cd edutools-moodle
pip install -e .
```

### From PyPI (when published)

```bash
pip install edutools-moodle
```

---

## Quick Start

```python
from edutools_moodle import MoodleAPI

# Initialize the API client
moodle = MoodleAPI(
    moodle_url="https://your-moodle-instance.com",
    token="your_webservice_token"
)

# Get site information
info = moodle.get_site_info()
print(f"Moodle version: {info['release']}")

# Work with groups
groups = moodle.groups.get_course_groups(course_id=123)
moodle.groups.add_user_to_group(group_id=1, user_id=42)

# Work with assignments
assignments = moodle.assignments.get_assignments(course_id=123)
submissions = moodle.assignments.get_submissions(assignment_id=456)

# Work with grades
moodle.grades.add_grade(assignment_id=456, user_id=42, grade=85.5)

# Work with users
user_id = moodle.users.create_user(
    username="johndoe",
    password="secure_pass",
    firstname="John",
    lastname="Doe",
    email="john@example.com"
)
```

---

## Core Classes

### MoodleAPI

**Main facade class** for interacting with Moodle API. Provides unified access to all modules.

#### Constructor

```python
MoodleAPI(moodle_url: str, token: str, timeout: int = 30, logger: Optional[logging.Logger] = None)
```

**Parameters:**
- `moodle_url` (str): Base URL of the Moodle instance (e.g., 'https://moodle.example.com')
- `token` (str): Web service token for authentication
- `timeout` (int, optional): Request timeout in seconds. Default: 30
- `logger` (logging.Logger, optional): Logger instance for debugging. If not provided, creates a default logger

**Raises:**
- `ValueError`: If moodle_url or token is empty

**Attributes:**
- `groups` (MoodleGroups): Group management module
- `assignments` (MoodleAssignments): Assignment management module
- `grades` (MoodleGrades): Grade management module
- `users` (MoodleUsers): User management module

#### Methods

##### `get_site_info() -> dict`

Get information about the Moodle site including version.

**Returns:** Dictionary containing:
- `sitename`: Name of the Moodle site
- `username`: Current user's username
- `firstname`: Current user's first name
- `lastname`: Current user's last name
- `release`: Moodle version (e.g., "4.1.1 (Build: 20230123)")
- `version`: Moodle version code
- `functions`: List of available web service functions

**Raises:**
- `MoodleAuthenticationError`: If authentication fails
- `MoodleAPIError`: If the API call fails

**Example:**
```python
info = moodle.get_site_info()
print(f"Site: {info['sitename']}")
print(f"Version: {info['release']}")
```

##### `check_moodle_version(min_version: str = "3.9") -> bool`

Check if the Moodle version meets the minimum requirement.

**Parameters:**
- `min_version` (str): Minimum required version (e.g., "3.9", "4.0")

**Returns:** `True` if Moodle version >= min_version, `False` otherwise

**Example:**
```python
if moodle.check_moodle_version("3.9"):
    print("Moodle version is compatible")
```

---

### MoodleBase

**Base class** for all Moodle API modules. Provides core functionality for making API calls.

#### Constructor

```python
MoodleBase(moodle_url: str, token: str, timeout: int = 30, logger: Optional[logging.Logger] = None)
```

**Parameters:**
- `moodle_url` (str): Base URL of the Moodle instance
- `token` (str): Web service token for authentication
- `timeout` (int, optional): Request timeout in seconds. Default: 30
- `logger` (logging.Logger, optional): Logger instance

**Raises:**
- `ValueError`: If moodle_url or token is empty

#### Properties

##### `session -> requests.Session`

Lazy-loaded session for connection pooling and better performance.

**Returns:** Configured requests Session instance

#### Methods

##### `call_api(function_name: str, params: Dict[str, Any] = None) -> Any`

Call a Moodle Web Service API function.

**Parameters:**
- `function_name` (str): Name of the Moodle API function to call
- `params` (dict, optional): Dictionary of parameters to pass to the API function

**Returns:** API response (parsed JSON)

**Raises:**
- `MoodleAuthenticationError`: If authentication fails
- `MoodleAPIError`: For Moodle-specific errors
- `TimeoutError`: If request times out

**Example:**
```python
response = moodle_base.call_api('core_webservice_get_site_info')
```

##### `close()`

Close the session and cleanup resources.

---

### MoodleGroups

**Class for managing groups, groupings, and cohorts** in Moodle.

Inherits from: `MoodleBase`

#### Groups Methods

##### `get_course_groups(course_id: int) -> List[Dict[str, Any]]`

Get all groups in a course.

**Parameters:**
- `course_id` (int): ID of the course

**Returns:** List of group dictionaries containing group information

**Example:**
```python
groups = moodle.groups.get_course_groups(course_id=123)
for group in groups:
    print(f"Group: {group['name']} (ID: {group['id']})")
```

##### `get_group_by_name(course_id: int, group_name: str) -> Optional[Dict[str, Any]]`

Find a group by name in a course.

**Parameters:**
- `course_id` (int): ID of the course
- `group_name` (str): Name of the group

**Returns:** Group dictionary if found, `None` otherwise

##### `get_group_id_by_name(course_id: int, group_name: str) -> Optional[int]`

Retrieve the ID of a group by its name.

**Parameters:**
- `course_id` (int): ID of the course
- `group_name` (str): Name of the group to find

**Returns:** Group ID if found, `None` otherwise

##### `create_group(course_id: int, group_name: str, description: str = "") -> Dict[str, Any]`

Create a new group in a course.

**Parameters:**
- `course_id` (int): ID of the course
- `group_name` (str): Name for the new group
- `description` (str, optional): Optional description for the group

**Returns:** API response with created group information

**Example:**
```python
response = moodle.groups.create_group(
    course_id=123,
    group_name="Group A",
    description="First group"
)
```

##### `delete_group(group_id: int) -> Dict[str, Any]`

Delete a group.

**Parameters:**
- `group_id` (int): ID of the group to delete

**Returns:** API response

**Raises:**
- `Exception`: If the deletion operation fails

##### `add_user_to_group(group_id: int, user_id: int) -> Dict[str, Any]`

Add a user to a group.

**Parameters:**
- `group_id` (int): ID of the group
- `user_id` (int): ID of the user

**Returns:** API response

**Example:**
```python
moodle.groups.add_user_to_group(group_id=1, user_id=42)
```

##### `remove_member_from_group(group_id: int, user_id: int) -> Dict[str, Any]`

Remove a member from a group.

**Parameters:**
- `group_id` (int): ID of the group
- `user_id` (int): ID of the user

**Returns:** API response with warnings if any

**Raises:**
- `Exception`: If the removal operation fails

##### `get_group_members(group_id: int) -> List[int]`

Get all members of a group.

**Parameters:**
- `group_id` (int): ID of the group

**Returns:** List of user IDs in the group

##### `get_group_members_info(group_id: int) -> List[Dict[str, Any]]`

Get detailed information about all members of a group.

**Parameters:**
- `group_id` (int): ID of the group

**Returns:** List of dictionaries with user information (id, fullname, email, etc.)

**Example:**
```python
members = moodle.groups.get_group_members_info(group_id=1)
for member in members:
    print(f"{member['fullname']} ({member['email']})")
```

##### `get_user_groups(course_id: int, user_id: int) -> List[Dict[str, Any]]`

Get all groups that a user belongs to in a specific course.

**Parameters:**
- `course_id` (int): ID of the course
- `user_id` (int): ID of the user

**Returns:** List of group dictionaries the user is a member of

##### `get_user_groups_with_names(course_id: int, user_id: int) -> List[str]`

Get list of group names that a user belongs to in a course.

**Parameters:**
- `course_id` (int): ID of the course
- `user_id` (int): ID of the user

**Returns:** List of group names

##### `create_or_get_group(course_id: int, group_name: str, description: str = "") -> int`

Create a group or return its ID if it already exists.

**Parameters:**
- `course_id` (int): ID of the course
- `group_name` (str): Name of the group
- `description` (str, optional): Optional description

**Returns:** Group ID (existing or newly created)

**Raises:**
- `Exception`: If group creation fails

##### `move_user_to_group(course_id: int, user_id: int, old_group_id: Optional[int], new_group_id: int) -> bool`

Move a user from one group to another.

**Parameters:**
- `course_id` (int): ID of the course
- `user_id` (int): ID of the user
- `old_group_id` (int, optional): ID of the current group (can be None if user not in a group)
- `new_group_id` (int): ID of the target group

**Returns:** `True` if move was successful

**Raises:**
- `Exception`: If the operation fails

##### `batch_enroll_users_to_groups(course_id: int, enrollments: List[Dict[str, Any]]) -> Dict[str, Any]`

Enroll multiple users to groups in batch.

**Parameters:**
- `course_id` (int): ID of the course
- `enrollments` (list): List of dicts with 'user_id', 'group_name' keys

**Returns:** Dictionary with 'success' count and 'errors' list

**Example:**
```python
enrollments = [
    {'user_id': 123, 'group_name': 'Group A'},
    {'user_id': 456, 'group_name': 'Group B'}
]
result = moodle.groups.batch_enroll_users_to_groups(course_id=123, enrollments=enrollments)
print(f"Successful enrollments: {result['success']}")
```

##### `send_message_to_group(group_id: int, subject: str, message: str) -> Dict[str, Any]`

Send a message to all members of a group.

**Parameters:**
- `group_id` (int): ID of the group
- `subject` (str): Subject of the message
- `message` (str): Content of the message (HTML supported)

**Returns:** API response with sent message IDs

**Raises:**
- `Exception`: If the group has no members or message sending fails

##### `get_all_course_groups_dict(course_id: int) -> Dict[str, int]`

Get all groups in a course as a dictionary mapping names to IDs.

**Parameters:**
- `course_id` (int): ID of the course

**Returns:** Dictionary with group names as keys and IDs as values

**Example:**
```python
groups_dict = moodle.groups.get_all_course_groups_dict(course_id=123)
# Returns: {'Group A': 1, 'Group B': 2}
```

##### `is_user_in_group(group_id: int, user_id: int) -> bool`

Check if a user is a member of a specific group.

**Parameters:**
- `group_id` (int): ID of the group
- `user_id` (int): ID of the user

**Returns:** `True` if user is in the group, `False` otherwise

#### Groupings Methods

##### `create_or_get_grouping(course_id: int, grouping_name: str, description: str = "") -> Optional[int]`

Create a grouping in a course or return its ID if it already exists.

**Parameters:**
- `course_id` (int): ID of the course
- `grouping_name` (str): Name of the grouping
- `description` (str, optional): Description of the grouping

**Returns:** ID of the grouping

**Raises:**
- `Exception`: If creation or retrieval fails

#### Cohorts Methods

##### `is_user_in_cohort(user_id: int, cohort_name: str = "IIR2425") -> bool`

Check if a user is enrolled in a specific cohort.

**Parameters:**
- `user_id` (int): ID of the user in Moodle
- `cohort_name` (str, optional): Name of the cohort to check. Default: "IIR2425"

**Returns:** `True` if the user is in the cohort, `False` otherwise

##### `enroll_user_in_cohort(user_id: int, cohort_name: str = "IIR2425") -> bool`

Enroll a user in a specific cohort.

**Parameters:**
- `user_id` (int): ID of the user in Moodle
- `cohort_name` (str, optional): Name of the cohort to enroll the user in. Default: "IIR2425"

**Returns:** `True` if enrollment succeeds, `False` otherwise

---

### MoodleAssignments

**Class for managing assignments** in Moodle.

Inherits from: `MoodleBase`

#### Methods

##### `get_assignments(course_id: int, include_not_enrolled: bool = True) -> List[Dict[str, Any]]`

Get all assignments in a course.

**Parameters:**
- `course_id` (int): ID of the course
- `include_not_enrolled` (bool, optional): Include assignments from courses user is not enrolled in. Default: True

**Returns:** List of assignment dictionaries

**Example:**
```python
assignments = moodle.assignments.get_assignments(course_id=123)
for assignment in assignments:
    print(f"{assignment['name']} (ID: {assignment['id']})")
```

##### `get_assignment_id_by_cmid(cmid: int, course_id: int) -> Optional[int]`

Find assignment ID from its course module ID (cmid).

**Parameters:**
- `cmid` (int): Course module ID (visible in URLs)
- `course_id` (int): ID of the course

**Returns:** Assignment ID if found, `None` otherwise

**Note:** The course module ID (cmid) is the ID that appears in Moodle URLs when viewing an assignment.

##### `get_submissions(assignment_id: int, status: str = "", since: int = 0, before: int = 0) -> List[Dict[str, Any]]`

Get student submissions for a specific assignment.

**Parameters:**
- `assignment_id` (int): ID of the Moodle assignment
- `status` (str, optional): Submission status (e.g., 'submitted', 'draft')
- `since` (int, optional): Get submissions made after this date (UNIX timestamp)
- `before` (int, optional): Get submissions made before this date (UNIX timestamp)

**Returns:** List of student submissions

**Example:**
```python
submissions = moodle.assignments.get_submissions(assignment_id=456)
for sub in submissions:
    print(f"User {sub['userid']}: {sub['status']}")
```

##### `get_assignment_submissions(assignment_id: int) -> List[Dict[str, Any]]`

Get all submissions for an assignment (alias for get_submissions).

**Parameters:**
- `assignment_id` (int): ID of the assignment

**Returns:** List of submission dictionaries

##### `get_user_submission(assignment_id: int, user_id: int) -> Dict[str, Any]`

Get a specific user's submission for an assignment.

**Parameters:**
- `assignment_id` (int): ID of the assignment
- `user_id` (int): ID of the user

**Returns:** Submission dictionary or empty dict if not found

**Example:**
```python
submission = moodle.assignments.get_user_submission(assignment_id=456, user_id=42)
if submission:
    print(f"Status: {submission['status']}")
```

---

### MoodleGrades

**Class for managing grades** in Moodle.

Inherits from: `MoodleBase`

#### Methods

##### `add_grade(assignment_id: int, user_id: int, grade: float, attempt_number: int = -1, add_attempt: int = 0, workflow_state: str = "released", feedback_comment: Optional[str] = None) -> Dict[str, Any]`

Add a grade for a student in an assignment.

**Parameters:**
- `assignment_id` (int): ID of the assignment
- `user_id` (int): ID of the student
- `grade` (float): Grade to assign (must be a float)
- `attempt_number` (int, optional): Attempt number (-1 for current attempt). Default: -1
- `add_attempt` (int, optional): Whether to create a new attempt (0 or 1). Default: 0
- `workflow_state` (str, optional): Workflow state (e.g., "released", "draft"). Default: "released"
- `feedback_comment` (str, optional): Optional feedback comment for the student

**Returns:** API response dictionary

**Raises:**
- `ValueError`: If grade is not a valid number

**Example:**
```python
moodle.grades.add_grade(
    assignment_id=456,
    user_id=42,
    grade=85.5,
    feedback_comment="Great work!"
)
```

##### `add_grades(assignment_id: int, grades: List[Dict[str, Any]], applytoall: int = 1, attemptnumber: int = -1, addattempt: int = 0, workflowstate: str = "released") -> Dict[str, Any]`

Add grades for multiple students in an assignment (batch operation).

**Parameters:**
- `assignment_id` (int): ID of the assignment
- `grades` (list): List of dictionaries containing grade information
  - Example: `[{'userid': 1, 'grade': 85.5}, {'userid': 2, 'grade': 90.0}]`
- `applytoall` (int, optional): Whether grades apply to all attempts. Default: 1
- `attemptnumber` (int, optional): Attempt number to apply the grade to (-1 for current). Default: -1
- `addattempt` (int, optional): Whether to create a new attempt. Default: 0
- `workflowstate` (str, optional): Workflow state of the grades. Default: "released"

**Returns:** API response dictionary

**Raises:**
- `TypeError`: If grades is not a list
- `ValueError`: If grade entries are invalid

**Example:**
```python
grades = [
    {'userid': 42, 'grade': 85.5},
    {'userid': 43, 'grade': 92.0},
    {'userid': 44, 'grade': 78.5}
]
moodle.grades.add_grades(assignment_id=456, grades=grades)
```

##### `get_grades(course_id: int, user_id: int = None) -> List[Dict[str, Any]]`

Get grades for a course, optionally filtered by user.

**Parameters:**
- `course_id` (int): ID of the course
- `user_id` (int, optional): Optional user ID to filter grades

**Returns:** List of grade dictionaries

##### `update_grade(assignment_id: int, user_id: int, grade: float, feedback: str = "") -> Dict[str, Any]`

Update a grade for a user's assignment submission.

**Parameters:**
- `assignment_id` (int): ID of the assignment
- `user_id` (int): ID of the user
- `grade` (float): Grade value
- `feedback` (str, optional): Optional feedback text

**Returns:** API response

##### `get_course_grades(course_id: int) -> Dict[str, Any]`

Get all grades for a course.

**Parameters:**
- `course_id` (int): ID of the course

**Returns:** Dictionary with grade information

##### `get_grade_items(course_id: int) -> List[Dict[str, Any]]`

Get all grade items (assignments, quizzes, etc.) for a course.

**Parameters:**
- `course_id` (int): ID of the course

**Returns:** List of grade item dictionaries with structure information

##### `get_grades_for_assignment(assignment_id: int, user_ids: Optional[List[int]] = None) -> List[Dict[str, Any]]`

Get grades for specific users in an assignment.

**Parameters:**
- `assignment_id` (int): ID of the assignment
- `user_ids` (list, optional): Optional list of user IDs to filter by

**Returns:** List of grade dictionaries for the assignment

**Example:**
```python
grades = moodle.grades.get_grades_for_assignment(
    assignment_id=456,
    user_ids=[42, 43, 44]
)
```

---

### MoodleUsers

**Class for managing users** in Moodle.

Inherits from: `MoodleBase`

#### Methods

##### `get_student_name(user_id: int) -> Optional[str]`

Retrieve the full name of a student from Moodle.

**Parameters:**
- `user_id` (int): ID of the user

**Returns:** Full name (firstname + lastname) or `None` if not found

**Example:**
```python
name = moodle.users.get_student_name(user_id=42)
print(f"Student name: {name}")
```

##### `get_users_by_field(field: str, value: str) -> List[Dict[str, Any]]`

Search for users by a specific field.

**Parameters:**
- `field` (str): Search field (e.g., 'email', 'username', 'id')
- `value` (str): Value to search for

**Returns:** List of user dictionaries matching the criteria

**Example:**
```python
users = moodle.users.get_users_by_field('email', 'john@example.com')
```

##### `create_user(username: str, password: str, firstname: str, lastname: str, email: str, city: str = "Marrakech", country: str = "MA", send_email: bool = True) -> Optional[int]`

Create a new user in Moodle.

**Parameters:**
- `username` (str): Unique username
- `password` (str): User password
- `firstname` (str): First name
- `lastname` (str): Last name
- `email` (str): Email address
- `city` (str, optional): City. Default: "Marrakech"
- `country` (str, optional): Country code. Default: "MA" (Morocco)
- `send_email` (bool, optional): If True, Moodle will send a welcome email. Default: True

**Returns:** ID of created user or `None` if error occurred

**Example:**
```python
user_id = moodle.users.create_user(
    username="johndoe",
    password="SecurePass123!",
    firstname="John",
    lastname="Doe",
    email="john@example.com"
)
```

##### `check_username_exists(username: str) -> bool`

Check if a username already exists.

**Parameters:**
- `username` (str): Username to check

**Returns:** `True` if username exists, `False` otherwise

##### `send_notification(user_id: int, subject: str, message: str) -> bool`

Send a notification/message to a user.

**Parameters:**
- `user_id` (int): ID of the recipient user
- `subject` (str): Message subject
- `message` (str): Message content

**Returns:** `True` if sent successfully, `False` otherwise

**Example:**
```python
success = moodle.users.send_notification(
    user_id=42,
    subject="Assignment Due",
    message="Your assignment is due tomorrow!"
)
```

##### `enroll_user_in_course(course_id: int, user_id: int, role_id: int = 5, timestart: int = 0, timeend: int = 0, suspend: int = 0) -> bool`

Enroll a user in a course.

**Parameters:**
- `course_id` (int): ID of the course
- `user_id` (int): ID of the user to enroll
- `role_id` (int, optional): ID of the role (5 = student by default). Default: 5
- `timestart` (int, optional): Enrollment start timestamp (0 for immediate). Default: 0
- `timeend` (int, optional): Enrollment end timestamp (0 for unlimited). Default: 0
- `suspend` (int, optional): 0 for active, 1 for suspended. Default: 0

**Returns:** `True` if enrollment succeeds, `False` otherwise

**Common Role IDs:**
- 1: Manager
- 2: Course creator
- 3: Teacher
- 4: Non-editing teacher
- 5: Student

**Example:**
```python
# Enroll as student
moodle.users.enroll_user_in_course(course_id=123, user_id=42)

# Enroll as teacher
moodle.users.enroll_user_in_course(course_id=123, user_id=43, role_id=3)
```

##### `is_user_enrolled(course_id: int, user_id: int) -> bool`

Check if a user is enrolled in a course.

**Parameters:**
- `course_id` (int): ID of the course
- `user_id` (int): ID of the user

**Returns:** `True` if user is enrolled, `False` otherwise

**Raises:**
- `Exception`: If the operation fails

---

## Exceptions

### MoodleAPIError

**Base exception** for all Moodle API errors.

**Inherits from:** `Exception`

**Usage:**
```python
from edutools_moodle import MoodleAPIError

try:
    moodle.groups.get_course_groups(course_id=999)
except MoodleAPIError as e:
    print(f"API Error: {e}")
```

### MoodleAuthenticationError

**Authentication and token errors.**

**Inherits from:** `MoodleAPIError`

**Raised when:**
- Invalid or expired token
- Insufficient permissions
- Unauthorized access

**Usage:**
```python
from edutools_moodle import MoodleAuthenticationError

try:
    moodle = MoodleAPI("https://moodle.com", "invalid_token")
    moodle.get_site_info()
except MoodleAuthenticationError as e:
    print(f"Authentication failed: {e}")
```

### MoodleResourceNotFoundError

**Resource not found errors.**

**Inherits from:** `MoodleAPIError`

**Raised when:**
- Course, group, user, or assignment not found
- Invalid resource ID

---

## Examples

### Example 1: Managing Groups

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://moodle.example.com", "your_token")

course_id = 123

# Get all groups in a course
groups = moodle.groups.get_course_groups(course_id)
print(f"Found {len(groups)} groups")

# Create a new group
response = moodle.groups.create_group(
    course_id=course_id,
    group_name="Advanced Python",
    description="Students in advanced Python course"
)
group_id = response[0]['id']

# Add users to the group
user_ids = [42, 43, 44, 45]
for user_id in user_ids:
    moodle.groups.add_user_to_group(group_id, user_id)

# Get group members
members = moodle.groups.get_group_members_info(group_id)
print(f"Group has {len(members)} members")
```

### Example 2: Processing Assignment Submissions

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://moodle.example.com", "your_token")

assignment_id = 456

# Get all submissions
submissions = moodle.assignments.get_submissions(assignment_id)

# Grade each submission
for submission in submissions:
    user_id = submission['userid']
    
    # Calculate grade based on your logic
    grade = 85.0  # Example grade
    
    # Add the grade
    moodle.grades.add_grade(
        assignment_id=assignment_id,
        user_id=user_id,
        grade=grade,
        feedback_comment="Well done!"
    )
    
    print(f"Graded user {user_id}: {grade}")
```

### Example 3: Bulk User Creation and Enrollment

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://moodle.example.com", "your_token")

course_id = 123
students = [
    {"username": "john.doe", "firstname": "John", "lastname": "Doe", "email": "john@example.com"},
    {"username": "jane.smith", "firstname": "Jane", "lastname": "Smith", "email": "jane@example.com"},
    {"username": "bob.jones", "firstname": "Bob", "lastname": "Jones", "email": "bob@example.com"}
]

for student in students:
    # Check if user already exists
    if not moodle.users.check_username_exists(student['username']):
        # Create user
        user_id = moodle.users.create_user(
            username=student['username'],
            password="TempPass123!",
            firstname=student['firstname'],
            lastname=student['lastname'],
            email=student['email']
        )
        print(f"Created user: {student['username']} (ID: {user_id})")
        
        # Enroll in course
        moodle.users.enroll_user_in_course(course_id, user_id)
        print(f"Enrolled {student['username']} in course {course_id}")
    else:
        print(f"User {student['username']} already exists")
```

### Example 4: Batch Grading

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://moodle.example.com", "your_token")

assignment_id = 456

# Prepare grades for multiple students
grades_data = [
    {'userid': 42, 'grade': 85.5},
    {'userid': 43, 'grade': 92.0},
    {'userid': 44, 'grade': 78.5},
    {'userid': 45, 'grade': 88.0}
]

# Submit all grades at once
result = moodle.grades.add_grades(assignment_id, grades_data)
print(f"Batch grading completed")
```

### Example 5: Group Messaging

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://moodle.example.com", "your_token")

course_id = 123
group_name = "Advanced Python"

# Get group ID
group_id = moodle.groups.get_group_id_by_name(course_id, group_name)

if group_id:
    # Send message to all group members
    moodle.groups.send_message_to_group(
        group_id=group_id,
        subject="Class Reminder",
        message="Don't forget about the exam next week!"
    )
    print(f"Message sent to group '{group_name}'")
```

### Example 6: Error Handling

```python
from edutools_moodle import MoodleAPI, MoodleAuthenticationError, MoodleAPIError

try:
    moodle = MoodleAPI("https://moodle.example.com", "your_token")
    
    # Get site info
    info = moodle.get_site_info()
    print(f"Connected to {info['sitename']}")
    
    # Try to get a non-existent group
    groups = moodle.groups.get_course_groups(course_id=999999)
    
except MoodleAuthenticationError as e:
    print(f"Authentication failed: {e}")
    print("Please check your token")
    
except MoodleAPIError as e:
    print(f"API error occurred: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Example 7: Working with Cohorts

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://moodle.example.com", "your_token")

user_id = 42
cohort_name = "IIR2425"

# Check if user is in cohort
if not moodle.groups.is_user_in_cohort(user_id, cohort_name):
    # Enroll user in cohort
    success = moodle.groups.enroll_user_in_cohort(user_id, cohort_name)
    if success:
        print(f"User {user_id} enrolled in cohort {cohort_name}")
else:
    print(f"User {user_id} is already in cohort {cohort_name}")
```

### Example 8: Advanced Group Management

```python
from edutools_moodle import MoodleAPI

moodle = MoodleAPI("https://moodle.example.com", "your_token")

course_id = 123

# Batch enroll users to different groups
enrollments = [
    {'user_id': 42, 'group_name': 'Group A'},
    {'user_id': 43, 'group_name': 'Group A'},
    {'user_id': 44, 'group_name': 'Group B'},
    {'user_id': 45, 'group_name': 'Group B'},
    {'user_id': 46, 'group_name': 'Group C'}
]

result = moodle.groups.batch_enroll_users_to_groups(course_id, enrollments)
print(f"Successfully enrolled: {result['success']}")
print(f"Errors: {len(result['errors'])}")

for error in result['errors']:
    print(f"Failed: User {error['user_id']} to {error['group_name']}: {error['error']}")
```

---

## Best Practices

### 1. Use the MoodleAPI Facade

Always prefer using the `MoodleAPI` facade class instead of individual module classes:

```python
# Recommended
from edutools_moodle import MoodleAPI
moodle = MoodleAPI(url, token)
moodle.groups.get_course_groups(123)

# Not recommended (unless extending)
from edutools_moodle import MoodleGroups
groups = MoodleGroups(url, token)
```

### 2. Handle Exceptions Properly

Always wrap API calls in try-except blocks:

```python
from edutools_moodle import MoodleAPI, MoodleAPIError

try:
    result = moodle.groups.add_user_to_group(group_id, user_id)
except MoodleAPIError as e:
    # Handle the error appropriately
    logger.error(f"Failed to add user: {e}")
```

### 3. Use Logging

Enable logging for debugging:

```python
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Pass logger to MoodleAPI
moodle = MoodleAPI(url, token, logger=logger)
```

### 4. Check Moodle Version

Always verify Moodle version compatibility:

```python
if not moodle.check_moodle_version("3.9"):
    print("Warning: Moodle 3.9+ is recommended")
```

### 5. Use Batch Operations

For bulk operations, use batch methods when available:

```python
# Good: Single API call
moodle.grades.add_grades(assignment_id, grades_list)

# Bad: Multiple API calls
for grade in grades_list:
    moodle.grades.add_grade(assignment_id, grade['userid'], grade['grade'])
```

### 6. Close Sessions

If creating instances in loops, remember to close sessions:

```python
moodle = MoodleAPI(url, token)
try:
    # Do work
    pass
finally:
    moodle.groups.close()  # Close the session
```

---

## Troubleshooting

### Authentication Errors

**Problem:** `MoodleAuthenticationError: Invalid token`

**Solutions:**
1. Verify token is correct and not expired
2. Check that Web Services are enabled in Moodle
3. Ensure user has appropriate permissions
4. Verify the token user has the required capabilities

### Timeout Errors

**Problem:** `TimeoutError: Request timed out`

**Solutions:**
```python
# Increase timeout
moodle = MoodleAPI(url, token, timeout=60)  # 60 seconds
```

### Resource Not Found

**Problem:** Empty results or None returned

**Solutions:**
1. Verify IDs are correct
2. Check user permissions
3. Ensure resource exists in Moodle

### Version Compatibility

**Problem:** Some functions not working

**Solutions:**
1. Check Moodle version: `moodle.get_site_info()`
2. Review [MOODLE_VERSIONS.md](MOODLE_VERSIONS.md) for compatibility
3. Upgrade Moodle if necessary

---

## Additional Resources

- [Moodle Web Services Documentation](https://docs.moodle.org/dev/Web_services)
- [Moodle API Functions](https://docs.moodle.org/dev/Web_service_API_functions)
- [Project Repository](https://github.com/najasoft/edutools-moodle)
- [Version Compatibility](MOODLE_VERSIONS.md)

---

## License

MIT License - See [LICENSE](../LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Last Updated:** December 23, 2025  
**Version:** 0.1.0
