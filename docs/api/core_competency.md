# Core Competency API

Documentation for core_competency web service functions.

## Table of Contents

- [core_competency_add_competency_to_course](#core-competency-add-competency-to-course)
- [core_competency_add_competency_to_plan](#core-competency-add-competency-to-plan)
- [core_competency_add_competency_to_template](#core-competency-add-competency-to-template)
- [core_competency_add_related_competency](#core-competency-add-related-competency)
- [core_competency_approve_plan](#core-competency-approve-plan)
- [core_competency_competency_framework_viewed](#core-competency-competency-framework-viewed)
- [core_competency_competency_viewed](#core-competency-competency-viewed)
- [core_competency_complete_plan](#core-competency-complete-plan)
- [core_competency_count_competencies](#core-competency-count-competencies)
- [core_competency_count_competencies_in_course](#core-competency-count-competencies-in-course)
- [core_competency_count_competencies_in_template](#core-competency-count-competencies-in-template)
- [core_competency_count_competency_frameworks](#core-competency-count-competency-frameworks)
- [core_competency_count_course_module_competencies](#core-competency-count-course-module-competencies)
- [core_competency_count_courses_using_competency](#core-competency-count-courses-using-competency)
- [core_competency_count_templates](#core-competency-count-templates)
- [core_competency_count_templates_using_competency](#core-competency-count-templates-using-competency)
- [core_competency_create_competency](#core-competency-create-competency)
- [core_competency_create_competency_framework](#core-competency-create-competency-framework)
- [core_competency_create_plan](#core-competency-create-plan)
- [core_competency_create_template](#core-competency-create-template)
- [core_competency_create_user_evidence_competency](#core-competency-create-user-evidence-competency)
- [core_competency_delete_competency](#core-competency-delete-competency)
- [core_competency_delete_competency_framework](#core-competency-delete-competency-framework)
- [core_competency_delete_evidence](#core-competency-delete-evidence)
- [core_competency_delete_plan](#core-competency-delete-plan)
- [core_competency_delete_template](#core-competency-delete-template)
- [core_competency_delete_user_evidence](#core-competency-delete-user-evidence)
- [core_competency_delete_user_evidence_competency](#core-competency-delete-user-evidence-competency)
- [core_competency_duplicate_competency_framework](#core-competency-duplicate-competency-framework)
- [core_competency_duplicate_template](#core-competency-duplicate-template)
- [core_competency_get_scale_values](#core-competency-get-scale-values)
- [core_competency_grade_competency](#core-competency-grade-competency)
- [core_competency_grade_competency_in_course](#core-competency-grade-competency-in-course)
- [core_competency_grade_competency_in_plan](#core-competency-grade-competency-in-plan)
- [core_competency_list_competencies](#core-competency-list-competencies)
- [core_competency_list_competencies_in_template](#core-competency-list-competencies-in-template)
- [core_competency_list_competency_frameworks](#core-competency-list-competency-frameworks)
- [core_competency_list_course_competencies](#core-competency-list-course-competencies)
- [core_competency_list_course_module_competencies](#core-competency-list-course-module-competencies)
- [core_competency_list_plan_competencies](#core-competency-list-plan-competencies)
- [core_competency_list_templates](#core-competency-list-templates)
- [core_competency_list_templates_using_competency](#core-competency-list-templates-using-competency)
- [core_competency_list_user_plans](#core-competency-list-user-plans)
- [core_competency_move_down_competency](#core-competency-move-down-competency)
- [core_competency_move_up_competency](#core-competency-move-up-competency)
- [core_competency_plan_cancel_review_request](#core-competency-plan-cancel-review-request)
- [core_competency_plan_request_review](#core-competency-plan-request-review)
- [core_competency_plan_start_review](#core-competency-plan-start-review)
- [core_competency_plan_stop_review](#core-competency-plan-stop-review)
- [core_competency_read_competency](#core-competency-read-competency)
- [core_competency_read_competency_framework](#core-competency-read-competency-framework)
- [core_competency_read_plan](#core-competency-read-plan)
- [core_competency_read_template](#core-competency-read-template)
- [core_competency_read_user_evidence](#core-competency-read-user-evidence)
- [core_competency_remove_competency_from_course](#core-competency-remove-competency-from-course)
- [core_competency_remove_competency_from_plan](#core-competency-remove-competency-from-plan)
- [core_competency_remove_competency_from_template](#core-competency-remove-competency-from-template)
- [core_competency_remove_related_competency](#core-competency-remove-related-competency)
- [core_competency_reopen_plan](#core-competency-reopen-plan)
- [core_competency_reorder_course_competency](#core-competency-reorder-course-competency)
- [core_competency_reorder_plan_competency](#core-competency-reorder-plan-competency)
- [core_competency_reorder_template_competency](#core-competency-reorder-template-competency)
- [core_competency_request_review_of_user_evidence_linked_competencies](#core-competency-request-review-of-user-evidence-linked-competencies)
- [core_competency_search_competencies](#core-competency-search-competencies)
- [core_competency_set_course_competency_ruleoutcome](#core-competency-set-course-competency-ruleoutcome)
- [core_competency_set_parent_competency](#core-competency-set-parent-competency)
- [core_competency_template_has_related_data](#core-competency-template-has-related-data)
- [core_competency_template_viewed](#core-competency-template-viewed)
- [core_competency_unapprove_plan](#core-competency-unapprove-plan)
- [core_competency_unlink_plan_from_template](#core-competency-unlink-plan-from-template)
- [core_competency_update_competency](#core-competency-update-competency)
- [core_competency_update_competency_framework](#core-competency-update-competency-framework)
- [core_competency_update_course_competency_settings](#core-competency-update-course-competency-settings)
- [core_competency_update_plan](#core-competency-update-plan)
- [core_competency_update_template](#core-competency-update-template)
- [core_competency_user_competency_cancel_review_request](#core-competency-user-competency-cancel-review-request)
- [core_competency_user_competency_plan_viewed](#core-competency-user-competency-plan-viewed)
- [core_competency_user_competency_request_review](#core-competency-user-competency-request-review)
- [core_competency_user_competency_start_review](#core-competency-user-competency-start-review)
- [core_competency_user_competency_stop_review](#core-competency-user-competency-stop-review)
- [core_competency_user_competency_viewed](#core-competency-user-competency-viewed)
- [core_competency_user_competency_viewed_in_course](#core-competency-user-competency-viewed-in-course)
- [core_competency_user_competency_viewed_in_plan](#core-competency-user-competency-viewed-in-plan)

---

## core_competency_add_competency_to_course

**Description:** No description available

**Parameters:** None documented

---

## core_competency_add_competency_to_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_add_competency_to_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_add_related_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_approve_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_competency_framework_viewed

**Description:** No description available

**Parameters:** None documented

---

## core_competency_competency_viewed

**Description:** No description available

**Parameters:** None documented

---

## core_competency_complete_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_competencies_in_course

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_competencies_in_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_competency_frameworks

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_course_module_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_courses_using_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_templates

**Description:** No description available

**Parameters:** None documented

---

## core_competency_count_templates_using_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_create_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_create_competency_framework

**Description:** No description available

**Parameters:** None documented

---

## core_competency_create_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_create_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_create_user_evidence_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_delete_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_delete_competency_framework

**Description:** No description available

**Parameters:** None documented

---

## core_competency_delete_evidence

**Description:** No description available

**Parameters:** None documented

---

## core_competency_delete_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_delete_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_delete_user_evidence

**Description:** No description available

**Parameters:** None documented

---

## core_competency_delete_user_evidence_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_duplicate_competency_framework

**Description:** No description available

**Parameters:** None documented

---

## core_competency_duplicate_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_get_scale_values

**Description:** No description available

**Parameters:** None documented

---

## core_competency_grade_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_grade_competency_in_course

**Description:** No description available

**Parameters:** None documented

---

## core_competency_grade_competency_in_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_competencies_in_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_competency_frameworks

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_course_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_course_module_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_plan_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_templates

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_templates_using_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_list_user_plans

**Description:** No description available

**Parameters:** None documented

---

## core_competency_move_down_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_move_up_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_plan_cancel_review_request

**Description:** No description available

**Parameters:** None documented

---

## core_competency_plan_request_review

**Description:** No description available

**Parameters:** None documented

---

## core_competency_plan_start_review

**Description:** No description available

**Parameters:** None documented

---

## core_competency_plan_stop_review

**Description:** No description available

**Parameters:** None documented

---

## core_competency_read_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_read_competency_framework

**Description:** No description available

**Parameters:** None documented

---

## core_competency_read_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_read_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_read_user_evidence

**Description:** No description available

**Parameters:** None documented

---

## core_competency_remove_competency_from_course

**Description:** No description available

**Parameters:** None documented

---

## core_competency_remove_competency_from_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_remove_competency_from_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_remove_related_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_reopen_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_reorder_course_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_reorder_plan_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_reorder_template_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_request_review_of_user_evidence_linked_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_search_competencies

**Description:** No description available

**Parameters:** None documented

---

## core_competency_set_course_competency_ruleoutcome

**Description:** No description available

**Parameters:** None documented

---

## core_competency_set_parent_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_template_has_related_data

**Description:** No description available

**Parameters:** None documented

---

## core_competency_template_viewed

**Description:** No description available

**Parameters:** None documented

---

## core_competency_unapprove_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_unlink_plan_from_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_update_competency

**Description:** No description available

**Parameters:** None documented

---

## core_competency_update_competency_framework

**Description:** No description available

**Parameters:** None documented

---

## core_competency_update_course_competency_settings

**Description:** No description available

**Parameters:** None documented

---

## core_competency_update_plan

**Description:** No description available

**Parameters:** None documented

---

## core_competency_update_template

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_cancel_review_request

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_plan_viewed

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_request_review

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_start_review

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_stop_review

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_viewed

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_viewed_in_course

**Description:** No description available

**Parameters:** None documented

---

## core_competency_user_competency_viewed_in_plan

**Description:** No description available

**Parameters:** None documented

---
