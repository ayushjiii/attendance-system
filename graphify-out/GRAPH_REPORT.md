# Graph Report - ATTENDENCE  (2026-05-16)

## Corpus Check
- 94 files · ~1,648,004 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 709 nodes · 1380 edges · 48 communities detected
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 185 edges (avg confidence: 0.67)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]

## God Nodes (most connected - your core abstractions)
1. `J` - 89 edges
2. `Nk()` - 33 edges
3. `Ak()` - 32 edges
4. `Employee` - 19 edges
5. `t()` - 17 edges
6. `AttendanceRecord` - 16 edges
7. `BreakRecordTests` - 16 edges
8. `LeaveRequest` - 16 edges
9. `y()` - 15 edges
10. `LeaveBalance` - 14 edges

## Surprising Connections (you probably didn't know these)
- `monthly_report_view()` --conceptually_related_to--> `Reporting Engine`  [INFERRED]
  reports\views.py → README.md
- `monthly_report_view()` --rationale_for--> `Reports as Most Central App`  [INFERRED]
  reports\views.py → project_mapper/outputs/reports/ARCHITECTURE_REPORT.md
- `AttendanceRecord` --uses--> `Main page after login.     Shows today's check-in status and last 7 days of att`  [INFERRED]
  attendance\models.py → attendance\views.py
- `AttendanceRecord` --uses--> `Handle the Check In button.          Security checks (in order):     1. Must`  [INFERRED]
  attendance\models.py → attendance\views.py
- `AttendanceRecord` --uses--> `Handle the Check Out button.          Validation:     - Must have checked in`  [INFERRED]
  attendance\models.py → attendance\views.py

## Hyperedges (group relationships)
- **Reports Cross App Data Aggregation** — views_monthly_report_view, views_attendance_record, views_leave_request, views_employee [EXTRACTED 1.00]
- **Employee Detail Reporting Flow** — views_employee_detail_report_view, views_employee_daily_data, views_employee_report_charts, views_attendance_record [EXTRACTED 1.00]
- **Project Intelligence Layer** — readme_graphify, readme_project_mapper, readme_hybrid_retrieval, tester_rag_testing [INFERRED 0.86]
- **Attendance Self-Service Flow** — dashboard_today_attendance_card, dashboard_check_in_gps_capture, dashboard_check_out_workflow, history_attendance_history [INFERRED 0.86]
- **Leave Request Lifecycle** — submit_leave_apply_for_leave, my_leaves_my_leave_requests, admin_leaves_all_leave_requests, approve_reject_leave_request_decision [INFERRED 0.90]
- **Monthly Reporting Workflow** — monthly_report_monthly_attendance_report, monthly_report_export_actions, monthly_report_employee_drilldown, employee_detail_employee_report [EXTRACTED 1.00]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.03
Nodes (148): d(), R(), a(), aC(), AE(), Ak(), aO(), aT() (+140 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (25): load_cache(), _(), A(), b, c(), e(), f(), g() (+17 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (49): AbstractUser, EmployeeAdmin, HolidayAdmin, LeaveBalanceAdmin, LeaveRequestAdmin, EditProfileForm, EmployeeCreationForm, HolidayForm (+41 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (39): AttendanceRecordAdmin, BreakRecordAdmin, CompanyPolicyAdmin, EmployeeShiftAdmin, AttendanceRecord, BreakRecord, CompanyPolicy, EmployeeShift (+31 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (24): bfs_paths(), find_start_nodes(), graph_search(), hybrid_search(), merge_results(), normalize_results(), apply_edit(), backup_file() (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.13
Nodes (17): Application Dependency Graph, Holidays as Isolated App, Reports as Most Central App, format_hours(), format_hours_value(), Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75 -, Project Mapper Automated Edit Log, Attendance Management System (+9 more)

### Community 6 - "Community 6"
Cohesion: 0.24
Nodes (18): ab(), bb(), cb(), db(), Eb(), fb(), gb(), hb() (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (17): All Attendance Records, Attendance Admin Filters, Attendance Status Badges, Check-In GPS Capture, Check-Out Workflow, Employee Attendance Dashboard, Recent Attendance, Today's Attendance Card (+9 more)

### Community 8 - "Community 8"
Cohesion: 0.26
Nodes (4): add_edge(), add_node(), extract_urls(), GraphVisitor

### Community 9 - "Community 9"
Cohesion: 0.18
Nodes (6): AppConfig, AccountsConfig, AttendanceConfig, HolidaysConfig, LeaveManagementConfig, ReportsConfig

### Community 10 - "Community 10"
Cohesion: 0.28
Nodes (9): All Leave Requests, Leave Approval Actions, Leave Status Filter, Admin Comment, Leave Request Decision, Apply for Leave Link, My Leave Requests, 36 Hour Leave Notice Rule (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.54
Nodes (7): calculate_metadata_score(), fuzzy_match(), load_index(), metadata_search(), normalize(), score_word_match(), tokenize()

### Community 12 - "Community 12"
Cohesion: 0.29
Nodes (2): get_file_hash(), read_file_content()

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (2): FunctionModelVisitor, Detect patterns like:          AttendanceRecord.objects.filter()         Empl

### Community 14 - "Community 14"
Cohesion: 0.6
Nodes (5): filterHighlight(), highlightFilter(), neighbourhoodHighlight(), selectNode(), selectNodes()

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (1): Migration

### Community 16 - "Community 16"
Cohesion: 0.4
Nodes (1): CodeChunkVisitor

### Community 17 - "Community 17"
Cohesion: 0.7
Nodes (4): boost_important_results(), diversify_results(), remove_duplicate_results(), rerank_results()

### Community 18 - "Community 18"
Cohesion: 0.5
Nodes (2): apply_intent_boost(), detect_query_intent()

### Community 19 - "Community 19"
Cohesion: 0.4
Nodes (1): CallGraphVisitor

### Community 21 - "Community 21"
Cohesion: 0.83
Nodes (3): clear_cache(), main(), run_indexer()

### Community 22 - "Community 22"
Cohesion: 0.5
Nodes (4): Employee Leave Balances, Remaining Leave Threshold Colors, My Leave Balance, Leave Balance Progress Visualization

### Community 23 - "Community 23"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 24 - "Community 24"
Cohesion: 0.67
Nodes (3): Django CSRF Login Form, Employee Login, Login Message Alerts

### Community 25 - "Community 25"
Cohesion: 0.67
Nodes (3): Employee Identity Fields, Employee Profile, Profile Edit and Password Actions

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (3): Add Holiday Form, Admin Holiday Actions, Public Holidays List

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Migration

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): Migration

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Migration

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): Migration

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): ASGI config for attendance_system project.  It exposes the ASGI callable as a

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Django settings for attendance_system project.  Generated by 'django-admin sta

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): URL configuration for attendance_system project.  The `urlpatterns` list route

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): WSGI config for attendance_system project.  It exposes the WSGI callable as a

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Migration

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (1): True if employee has checked in today.

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (1): True if employee has checked out today.

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (1): Stores one attendance record per employee per day.          Fields:     - emp

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): Calculate total hours worked.         Called automatically when the employee ch

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): True if employee has checked in today.

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): True if employee has checked out today.

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): Check if an IP address is in the allowed office network.          Supports:

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (1): Calculate the distance between two GPS coordinates in meters.     Uses the Have

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): Return True if the given GPS coordinates are within     the allowed office radi

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Extract browser and OS info from the HTTP User-Agent header.     Stored for aud

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (1): Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (1): AttendanceRecord Impact Query

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Invalid Checkout Rules Query

## Knowledge Gaps
- **57 isolated node(s):** `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp`, `Calculate net hours worked.          - Caps duration at 10 hours total.`, `True if employee has checked in today.` (+52 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 12`** (7 nodes): `create_chunks()`, `detect_file_type()`, `detect_module()`, `extract_python_metadata()`, `get_file_hash()`, `read_file_content()`, `auto_indexer.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 13`** (6 nodes): `FunctionModelVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `Detect patterns like:          AttendanceRecord.objects.filter()         Empl`, `model_usage_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 15`** (5 nodes): `Migration`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (5 nodes): `CodeChunkVisitor`, `.__init__()`, `.visit_ClassDef()`, `.visit_FunctionDef()`, `code_chunk_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (5 nodes): `retrieval_ranker.py`, `apply_intent_boost()`, `deduplicate_results()`, `detect_query_intent()`, `should_ignore_file()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (5 nodes): `CallGraphVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `call_graph_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (3 nodes): `main()`, `manage.py`, `Run administrative tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `Migration`, `0002_alter_employee_options_alter_employee_department_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `Migration`, `0002_breakrecord.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `Migration`, `0003_companypolicy.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (2 nodes): `Migration`, `0004_employeeshift.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (2 nodes): `ASGI config for attendance_system project.  It exposes the ASGI callable as a`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (2 nodes): `settings.py`, `Django settings for attendance_system project.  Generated by 'django-admin sta`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (2 nodes): `urls.py`, `URL configuration for attendance_system project.  The `urlpatterns` list route`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `wsgi.py`, `WSGI config for attendance_system project.  It exposes the WSGI callable as a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (2 nodes): `Migration`, `0002_leavebalance.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `True if employee has checked in today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `True if employee has checked out today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `Stores one attendance record per employee per day.          Fields:     - emp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `Calculate total hours worked.         Called automatically when the employee ch`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `True if employee has checked in today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `True if employee has checked out today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `Check if an IP address is in the allowed office network.          Supports:`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `Calculate the distance between two GPS coordinates in meters.     Uses the Have`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `Return True if the given GPS coordinates are within     the allowed office radi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `Extract browser and OS info from the HTTP User-Agent header.     Stored for aud`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `AttendanceRecord Impact Query`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Invalid Checkout Rules Query`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `J` connect `Community 1` to `Community 2`, `Community 4`?**
  _High betweenness centrality (0.186) - this node is a cross-community bridge._
- **Why does `d()` connect `Community 0` to `Community 1`, `Community 2`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `t()` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Employee` (e.g. with `EmployeeAdmin` and `EmployeeCreationForm`) actually correct?**
  _`Employee` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `t()` (e.g. with `.clear()` and `.on()`) actually correct?**
  _`t()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp` to the rest of the system?**
  _57 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.03 - nodes in this community are weakly interconnected._