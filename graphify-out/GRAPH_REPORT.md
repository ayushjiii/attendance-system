# Graph Report - ATTENDENCE  (2026-05-16)

## Corpus Check
- 91 files · ~1,646,999 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 664 nodes · 1306 edges · 47 communities detected
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 155 edges (avg confidence: 0.68)
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
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
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
6. `LeaveRequest` - 16 edges
7. `AttendanceRecord` - 15 edges
8. `y()` - 15 edges
9. `LeaveBalance` - 14 edges
10. `c()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `monthly_report_view()` --rationale_for--> `Reports as Most Central App`  [INFERRED]
  reports\views.py → project_mapper/outputs/reports/ARCHITECTURE_REPORT.md
- `monthly_report_view()` --conceptually_related_to--> `Reporting Engine`  [INFERRED]
  reports\views.py → README.md
- `AttendanceRecordAdmin` --uses--> `AttendanceRecord`  [INFERRED]
  attendance\admin.py → attendance\models.py
- `Main page after login.     Shows today's check-in status and last 7 days of att` --uses--> `AttendanceRecord`  [INFERRED]
  attendance\views.py → attendance\models.py
- `Handle the Check In button.          Security checks (in order):     1. Must` --uses--> `AttendanceRecord`  [INFERRED]
  attendance\views.py → attendance\models.py

## Hyperedges (group relationships)
- **Reports Cross App Data Aggregation** — views_monthly_report_view, views_attendance_record, views_leave_request, views_employee [EXTRACTED 1.00]
- **Employee Detail Reporting Flow** — views_employee_detail_report_view, views_employee_daily_data, views_employee_report_charts, views_attendance_record [EXTRACTED 1.00]
- **Project Intelligence Layer** — readme_graphify, readme_project_mapper, readme_hybrid_retrieval, tester_rag_testing [INFERRED 0.86]
- **Attendance Self-Service Flow** — dashboard_today_attendance_card, dashboard_check_in_gps_capture, dashboard_check_out_workflow, history_attendance_history [INFERRED 0.86]
- **Leave Request Lifecycle** — submit_leave_apply_for_leave, my_leaves_my_leave_requests, admin_leaves_all_leave_requests, approve_reject_leave_request_decision [INFERRED 0.90]
- **Monthly Reporting Workflow** — monthly_report_monthly_attendance_report, monthly_report_export_actions, monthly_report_employee_drilldown, employee_detail_employee_report [EXTRACTED 1.00]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (24): load_cache(), _(), A(), c(), e(), g(), h(), I() (+16 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (55): AbstractUser, EmployeeAdmin, HolidayAdmin, LeaveBalanceAdmin, LeaveRequestAdmin, EditProfileForm, EmployeeCreationForm, HolidayForm (+47 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (31): aT(), Ax(), _b(), Bk(), Bx(), eT(), fm(), Gd() (+23 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (29): AttendanceRecordAdmin, AttendanceRecord, Stores one attendance record per employee per day.          Fields:     - emp, Calculate total hours worked.         Called automatically when the employee ch, calculate_distance_meters(), get_client_ip(), get_device_info(), is_office_ip() (+21 more)

### Community 4 - "Community 4"
Cohesion: 0.1
Nodes (25): bfs_paths(), find_start_nodes(), graph_search(), hybrid_search(), merge_results(), normalize_results(), apply_edit(), backup_file() (+17 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (33): aC(), AE(), Ak(), aO(), bE(), BO(), DE(), eC() (+25 more)

### Community 6 - "Community 6"
Cohesion: 0.16
Nodes (20): Ay(), cm(), em(), Fy(), Gc(), im(), Jc(), jy() (+12 more)

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (20): d(), R(), a(), C(), f(), FS(), gE(), l() (+12 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (20): bC(), BS(), Dy(), e(), hm(), Hv(), Ig(), jg() (+12 more)

### Community 9 - "Community 9"
Cohesion: 0.24
Nodes (18): ab(), bb(), cb(), db(), Eb(), fb(), gb(), hb() (+10 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (17): All Attendance Records, Attendance Admin Filters, Attendance Status Badges, Check-In GPS Capture, Check-Out Workflow, Employee Attendance Dashboard, Recent Attendance, Today's Attendance Card (+9 more)

### Community 11 - "Community 11"
Cohesion: 0.13
Nodes (15): cO(), $d(), GO(), i(), jx(), KO(), My(), Pk() (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.26
Nodes (4): add_edge(), add_node(), extract_urls(), GraphVisitor

### Community 13 - "Community 13"
Cohesion: 0.18
Nodes (6): AppConfig, AccountsConfig, AttendanceConfig, HolidaysConfig, LeaveManagementConfig, ReportsConfig

### Community 14 - "Community 14"
Cohesion: 0.28
Nodes (9): All Leave Requests, Leave Approval Actions, Leave Status Filter, Admin Comment, Leave Request Decision, Apply for Leave Link, My Leave Requests, 36 Hour Leave Notice Rule (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.54
Nodes (7): calculate_metadata_score(), fuzzy_match(), load_index(), metadata_search(), normalize(), score_word_match(), tokenize()

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (8): bg(), Cg(), Eg(), _g(), kg(), Og(), wg(), xg()

### Community 17 - "Community 17"
Cohesion: 0.25
Nodes (8): Application Dependency Graph, Holidays as Isolated App, Reports as Most Central App, Project Mapper Automated Edit Log, Graphify Codebase Knowledge Graph, Hybrid Retrieval, Project Mapper Local RAG Engine, RAG Testing Results

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (2): get_file_hash(), read_file_content()

### Community 19 - "Community 19"
Cohesion: 0.48
Nodes (1): b

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (2): FunctionModelVisitor, Detect patterns like:          AttendanceRecord.objects.filter()         Empl

### Community 21 - "Community 21"
Cohesion: 0.6
Nodes (5): filterHighlight(), highlightFilter(), neighbourhoodHighlight(), selectNode(), selectNodes()

### Community 22 - "Community 22"
Cohesion: 0.4
Nodes (1): Migration

### Community 23 - "Community 23"
Cohesion: 0.4
Nodes (1): CodeChunkVisitor

### Community 24 - "Community 24"
Cohesion: 0.7
Nodes (4): boost_important_results(), diversify_results(), remove_duplicate_results(), rerank_results()

### Community 25 - "Community 25"
Cohesion: 0.5
Nodes (2): apply_intent_boost(), detect_query_intent()

### Community 26 - "Community 26"
Cohesion: 0.4
Nodes (1): CallGraphVisitor

### Community 28 - "Community 28"
Cohesion: 0.83
Nodes (3): clear_cache(), main(), run_indexer()

### Community 29 - "Community 29"
Cohesion: 0.5
Nodes (4): Employee Leave Balances, Remaining Leave Threshold Colors, My Leave Balance, Leave Balance Progress Visualization

### Community 30 - "Community 30"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 31 - "Community 31"
Cohesion: 0.67
Nodes (2): format_hours(), Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75

### Community 32 - "Community 32"
Cohesion: 0.67
Nodes (3): Django CSRF Login Form, Employee Login, Login Message Alerts

### Community 33 - "Community 33"
Cohesion: 0.67
Nodes (3): Employee Identity Fields, Employee Profile, Profile Edit and Password Actions

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (3): Add Holiday Form, Admin Holiday Actions, Public Holidays List

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Migration

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): ASGI config for attendance_system project.  It exposes the ASGI callable as a

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): Django settings for attendance_system project.  Generated by 'django-admin sta

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (1): URL configuration for attendance_system project.  The `urlpatterns` list route

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (1): WSGI config for attendance_system project.  It exposes the WSGI callable as a

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (1): Migration

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (1): True if employee has checked in today.

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (1): True if employee has checked out today.

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): Calculate the distance between two GPS coordinates in meters.     Uses the Have

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Return True if the given GPS coordinates are within     the allowed office radi

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (1): Extract browser and OS info from the HTTP User-Agent header.     Stored for aud

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (1): AttendanceRecord Impact Query

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Invalid Checkout Rules Query

## Knowledge Gaps
- **48 isolated node(s):** `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp`, `Calculate total hours worked.         Called automatically when the employee ch`, `True if employee has checked in today.` (+43 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 18`** (7 nodes): `create_chunks()`, `detect_file_type()`, `detect_module()`, `extract_python_metadata()`, `get_file_hash()`, `read_file_content()`, `auto_indexer.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (7 nodes): `b`, `.constructor()`, `.getScoreFunction()`, `.getSortFunction()`, `.prepareSearch()`, `.search()`, `.tokenize()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (6 nodes): `FunctionModelVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `Detect patterns like:          AttendanceRecord.objects.filter()         Empl`, `model_usage_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (5 nodes): `Migration`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (5 nodes): `CodeChunkVisitor`, `.__init__()`, `.visit_ClassDef()`, `.visit_FunctionDef()`, `code_chunk_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (5 nodes): `retrieval_ranker.py`, `apply_intent_boost()`, `deduplicate_results()`, `detect_query_intent()`, `should_ignore_file()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (5 nodes): `CallGraphVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `call_graph_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (3 nodes): `main()`, `manage.py`, `Run administrative tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (3 nodes): `format_hours()`, `Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75`, `attendance_filters.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `Migration`, `0002_alter_employee_options_alter_employee_department_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (2 nodes): `ASGI config for attendance_system project.  It exposes the ASGI callable as a`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (2 nodes): `settings.py`, `Django settings for attendance_system project.  Generated by 'django-admin sta`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (2 nodes): `urls.py`, `URL configuration for attendance_system project.  The `urlpatterns` list route`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (2 nodes): `wsgi.py`, `WSGI config for attendance_system project.  It exposes the WSGI callable as a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (2 nodes): `Migration`, `0002_leavebalance.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `True if employee has checked in today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `True if employee has checked out today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `Calculate the distance between two GPS coordinates in meters.     Uses the Have`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `Return True if the given GPS coordinates are within     the allowed office radi`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `Extract browser and OS info from the HTTP User-Agent header.     Stored for aud`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `AttendanceRecord Impact Query`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Invalid Checkout Rules Query`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `J` connect `Community 0` to `Community 1`, `Community 4`?**
  _High betweenness centrality (0.190) - this node is a cross-community bridge._
- **Why does `d()` connect `Community 7` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `t()` connect `Community 8` to `Community 0`, `Community 2`, `Community 6`, `Community 7`, `Community 11`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Employee` (e.g. with `EmployeeAdmin` and `EmployeeCreationForm`) actually correct?**
  _`Employee` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `t()` (e.g. with `.clear()` and `.on()`) actually correct?**
  _`t()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp` to the rest of the system?**
  _48 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._