# Test Suite for edutools-moodle v0.2.0

This directory contains comprehensive tests for all modules in edutools-moodle v0.2.0.

## Test Coverage

### ✅ Modules Tested

- **MoodleBase** - Response validation and error handling
- **MoodleUsers** - 7 functions (user management)
- **MoodleGroups** - 20 functions (groups, cohorts, groupings)
- **MoodleAssignments** - 4 functions (optimized data retrieval)
- **MoodleGrades** - 6 functions (new APIs, breaking changes)

### 📊 Test Statistics

- **Total functions validated:** 37 functions
- **Functions removed:** 2 (deprecated APIs)
- **Breaking changes tested:** 3
- **Optimizations validated:** 4 modules

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install pytest python-dotenv
```

### 2. Configure Test Environment

Copy the example environment file and configure with your Moodle credentials:

```bash
cd tests
cp .env.example .env
```

Edit `.env` with your values:

```dotenv
MOODLE_URL=https://your-moodle-instance.com
MOODLE_TOKEN=your_webservice_token_here
COURSE_ID=34
GROUP_ID=1811
USER_ID=1037
GROUPING_ID=64
ASSIGNMENT_CMID=957
```

**⚠️ IMPORTANT:** The `.env` file contains sensitive credentials and is excluded from Git.

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Module

```bash
pytest tests/test_users.py -v
pytest tests/test_groups.py -v
pytest tests/test_assignments.py -v
pytest tests/test_grades.py -v
```

### Run Specific Test

```bash
pytest tests/test_grades.py::TestMoodleGrades::test_get_grades -v
```

### Run Tests Matching Pattern

```bash
pytest tests/ -k "test_get" -v
```

### Run with Coverage

```bash
pytest tests/ --cov=edutools_moodle --cov-report=html
```

## Test Files

### Core Test Files

- **`conftest.py`** - Shared fixtures (moodle instance, test config)
- **`test_users.py`** - User management tests (7 functions)
- **`test_groups.py`** - Groups/cohorts/groupings tests (20 functions)
- **`test_assignments.py`** - Assignment tests (4 functions)
- **`test_grades.py`** - Grade management tests (6 functions)

### Configuration Files

- **`.env`** - Your credentials (NOT in Git)
- **`.env.example`** - Template for configuration
- **`.env.template`** - Alternative template

## Test Categories

### Read-Only Tests (Safe)

These tests only read data and don't modify your Moodle instance:

- `test_get_course_groups`
- `test_get_assignments`
- `test_get_grades`
- `test_check_username_exists`

### Write Tests (Skipped by Default)

These tests modify data and are skipped by default:

- `test_create_user` (requires admin)
- `test_add_grade` (modifies grades)
- `test_update_grade` (modifies grades)
- `test_send_notification` (sends real notification)

To run write tests:

```bash
pytest tests/ -v --run-write-tests
```

## v0.2.0 Specific Tests

### Breaking Changes Tested

1. **`get_course_grades()` requires user_id**
   ```python
   def test_get_course_grades_requires_user_id(self, moodle, test_config):
       result = moodle.grades.get_course_grades(
           course_id=test_config['course_id'],
           user_id=test_config['user_id']  # Now required!
       )
   ```

2. **Removed functions verified**
   ```python
   def test_get_assignment_submissions_removed(self, moodle):
       assert not hasattr(moodle.assignments, 'get_assignment_submissions')
   
   def test_get_grade_items_removed(self, moodle):
       assert not hasattr(moodle.grades, 'get_grade_items')
   ```

### Optimization Validation

Tests verify optimized response structures:

- **Groups:** 15+ fields → 6 fields
- **Assignments:** 50+ fields → 11 fields
- **Submissions:** 30+ fields → 8 fields
- **Grades:** 30+ fields → 10 fields per item

Example:
```python
def test_get_assignments(self, moodle, test_config):
    assignments = moodle.assignments.get_assignments(
        course_ids=[test_config['course_id']]
    )
    
    if assignments:
        assert len(assignments[0].keys()) <= 15, "Should return ~11 fields (optimized)"
```

## Troubleshooting

### Common Issues

**1. Missing .env file**
```
SKIPPED - MOODLE_URL and MOODLE_TOKEN must be set
```
→ Copy `.env.example` to `.env` and configure

**2. Invalid credentials**
```
MoodleAPIError: Authentication failed
```
→ Verify MOODLE_TOKEN in your .env

**3. Course/Group not found**
```
MoodleAPIError: Course not found
```
→ Update COURSE_ID in .env with valid course

**4. Permission denied**
```
MoodleAPIError: Permission denied
```
→ Ensure your token has required capabilities

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest python-dotenv
      - name: Run tests
        env:
          MOODLE_URL: ${{ secrets.MOODLE_URL }}
          MOODLE_TOKEN: ${{ secrets.MOODLE_TOKEN }}
          COURSE_ID: ${{ secrets.COURSE_ID }}
        run: pytest tests/ -v
```

## Contributing

When adding new tests:

1. Follow existing test structure
2. Use descriptive test names
3. Add docstrings explaining what is tested
4. Mark destructive tests with `@pytest.mark.skip`
5. Update this README with new test coverage

## Support

For issues with tests:
1. Check [GUIDE_TESTS.md](GUIDE_TESTS.md) for detailed testing guide
2. Review [CHANGELOG.md](../CHANGELOG.md) for v0.2.0 changes
3. Open an issue on GitHub

---

**Version:** Tests for edutools-moodle v0.2.0  
**Last Updated:** December 29, 2024
