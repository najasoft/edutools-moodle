"""
Exploratory tests for MoodleCourses module.
These tests are meant to be run manually against a real Moodle instance.

Prerequisites:
- Create .env file with MOODLE_URL and MOODLE_TOKEN
- Ensure user has necessary permissions (see PERMISSIONS.md)
"""
import os
from dotenv import load_dotenv
from edutools_moodle import MoodleAPI


def test_get_user_courses():
    """Test getting current user's courses."""
    print("\n=== Test 1: Get User Courses ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    courses = moodle.courses.get_user_courses()
    print(f"Found {len(courses)} courses")
    
    if courses:
        print("\nFirst course details:")
        course = courses[0]
        print(f"  ID: {course.get('id')}")
        print(f"  Short name: {course.get('shortname')}")
        print(f"  Full name: {course.get('fullname')}")
        print(f"  Category: {course.get('category')}")
    
    return courses


def test_get_enrolled_users(course_id):
    """Test getting enrolled users for a course."""
    print(f"\n=== Test 2: Get Enrolled Users (Course {course_id}) ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    users = moodle.courses.get_enrolled_users(course_id)
    print(f"Found {len(users)} enrolled users")
    
    if users:
        print("\nFirst user details:")
        user = users[0]
        print(f"  ID: {user.get('id')}")
        print(f"  Full name: {user.get('fullname')}")
        print(f"  Email: {user.get('email')}")
    
    return users


def test_get_course_by_field(field, value):
    """Test getting course by field."""
    print(f"\n=== Test 3: Get Course by Field ({field}={value}) ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    courses = moodle.courses.get_course_by_field(field, value)
    print(f"Found {len(courses)} matching courses")
    
    if courses:
        print("\nCourse details:")
        course = courses[0]
        print(f"  ID: {course.get('id')}")
        print(f"  Short name: {course.get('shortname')}")
        print(f"  Full name: {course.get('fullname')}")
    
    return courses


def test_get_categories():
    """Test getting course categories."""
    print("\n=== Test 4: Get Categories ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    categories = moodle.courses.get_categories()
    print(f"Found {len(categories)} categories")
    
    if categories:
        print("\nFirst 3 categories:")
        for cat in categories[:3]:
            print(f"  - {cat.get('name')} (ID: {cat.get('id')}, Courses: {cat.get('coursecount')})")
    
    return categories


def test_get_course_contents(course_id):
    """Test getting course contents."""
    print(f"\n=== Test 5: Get Course Contents (Course {course_id}) ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    contents = moodle.courses.get_course_contents(course_id)
    print(f"Found {len(contents)} sections")
    
    if contents:
        print("\nFirst section:")
        section = contents[0]
        print(f"  Name: {section.get('name')}")
        print(f"  Modules: {len(section.get('modules', []))}")
        
        if section.get('modules'):
            print("\n  First 3 modules:")
            for mod in section.get('modules', [])[:3]:
                print(f"    - {mod.get('name')} ({mod.get('modname')})")
    
    return contents


def test_get_recent_courses():
    """Test getting recent courses."""
    print("\n=== Test 6: Get Recent Courses ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    recent = moodle.courses.get_recent_courses(limit=5)
    print(f"Found {len(recent)} recent courses")
    
    if recent:
        print("\nRecent courses:")
        for course in recent:
            print(f"  - {course.get('fullname')} (ID: {course.get('id')})")
    
    return recent


def test_search_courses(search_term):
    """Test searching courses."""
    print(f"\n=== Test 7: Search Courses ('{search_term}') ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    result = moodle.courses.search_courses(search_term, page=0, perpage=5)
    courses = result.get('courses', [])
    print(f"Found {len(courses)} matching courses")
    
    if courses:
        print("\nMatching courses:")
        for course in courses:
            print(f"  - {course.get('fullname')} (ID: {course.get('id')})")
    
    return result


def test_get_enrolled_users_by_capability(course_id, capability):
    """Test getting users by capability."""
    print(f"\n=== Test 8: Get Users by Capability (Course {course_id}) ===")
    print(f"Capability: {capability}")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    users = moodle.courses.get_enrolled_users_by_capability(course_id, capability)
    print(f"Found {len(users)} users with this capability")
    
    if users:
        print("\nFirst 5 users:")
        for user in users[:5]:
            print(f"  - {user.get('fullname')} (ID: {user.get('id')})")
    
    return users


def test_get_course_modules(course_id):
    """Test getting all course modules."""
    print(f"\n=== Test 9: Get Course Modules (Course {course_id}) ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    modules = moodle.courses.get_course_modules(course_id)
    print(f"Found {len(modules)} modules")
    
    # Count by type
    mod_types = {}
    for mod in modules:
        modname = mod.get('modname', 'unknown')
        mod_types[modname] = mod_types.get(modname, 0) + 1
    
    print("\nModules by type:")
    for modname, count in mod_types.items():
        print(f"  - {modname}: {count}")
    
    return modules


def test_get_course_by_id(course_id):
    """Test getting course by ID."""
    print(f"\n=== Test 10: Get Course by ID ({course_id}) ===")
    load_dotenv()
    moodle = MoodleAPI(os.getenv('MOODLE_URL'), os.getenv('MOODLE_TOKEN'))
    
    course = moodle.courses.get_course_by_id(course_id)
    
    if course:
        print("Course found:")
        print(f"  ID: {course.get('id')}")
        print(f"  Short name: {course.get('shortname')}")
        print(f"  Full name: {course.get('fullname')}")
        print(f"  Category: {course.get('category')}")
    else:
        print("Course not found!")
    
    return course


def run_all_tests():
    """Run all exploratory tests."""
    print("=" * 80)
    print("EXPLORATORY TESTS FOR MoodleCourses")
    print("=" * 80)
    
    try:
        # Test 1: Get user courses
        courses = test_get_user_courses()
        
        if not courses:
            print("\n⚠️  No courses found. Cannot continue with other tests.")
            return
        
        # Use first course for subsequent tests
        course_id = courses[0]['id']
        
        # Test 2: Get enrolled users
        users = test_get_enrolled_users(course_id)
        
        # Test 3: Get course by field
        test_get_course_by_field('id', course_id)
        
        # Test 4: Get categories
        test_get_categories()
        
        # Test 5: Get course contents
        test_get_course_contents(course_id)
        
        # Test 6: Get recent courses
        test_get_recent_courses()
        
        # Test 7: Search courses
        test_search_courses(courses[0].get('shortname', 'test')[:5])
        
        # Test 8: Get users by capability (students can submit assignments)
        test_get_enrolled_users_by_capability(course_id, 'mod/assign:submit')
        
        # Test 9: Get course modules
        test_get_course_modules(course_id)
        
        # Test 10: Get course by ID
        test_get_course_by_id(course_id)
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during tests: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # Check if .env exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("\nPlease create a .env file with:")
        print("MOODLE_URL=https://your-moodle-site.com")
        print("MOODLE_TOKEN=your_webservice_token")
    else:
        run_all_tests()
