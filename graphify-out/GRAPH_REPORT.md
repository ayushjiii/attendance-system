# Graph Report - ATTENDENCE  (2026-05-15)

## Corpus Check
- 91 files · ~1,646,877 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 621 nodes · 1260 edges · 48 communities detected
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 146 edges (avg confidence: 0.66)
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
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
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
- [[_COMMUNITY_Community 83|Community 83]]

## God Nodes (most connected - your core abstractions)
1. `J` - 89 edges
2. `Nk()` - 33 edges
3. `Ak()` - 32 edges
4. `Employee` - 21 edges
5. `LeaveRequest` - 18 edges
6. `t()` - 17 edges
7. `LeaveBalance` - 16 edges
8. `y()` - 15 edges
9. `c()` - 14 edges
10. `Qc()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `AttendanceRecordAdmin` --uses--> `AttendanceRecord`  [INFERRED]
  attendance\admin.py → attendance\models.py
- `AttendanceRecord` --uses--> `Main page after login.     Shows today's check-in status and last 7 days of att`  [INFERRED]
  attendance\models.py → attendance\views.py
- `AttendanceRecord` --uses--> `Handle the Check In button.          Security checks (in order):     1. Must`  [INFERRED]
  attendance\models.py → attendance\views.py
- `AttendanceRecord` --uses--> `Handle the Check Out button.          Validation:     - Must have checked in`  [INFERRED]
  attendance\models.py → attendance\views.py
- `AttendanceRecord` --uses--> `Employee's personal attendance history.     Can be filtered by month using ?mon`  [INFERRED]
  attendance\models.py → attendance\views.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (26): load_cache(), _(), A(), b, c(), f(), g(), h() (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (54): AbstractUser, EmployeeAdmin, HolidayAdmin, LeaveBalanceAdmin, LeaveRequestAdmin, EditProfileForm, EmployeeCreationForm, HolidayForm (+46 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (33): aT(), Ax(), bg(), Bk(), Bx(), Cg(), Eg(), fm() (+25 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (24): AttendanceRecordAdmin, AttendanceRecord, Stores one attendance record per employee per day.          Fields:     - emp, Calculate total hours worked.         Called automatically when the employee ch, calculate_distance_meters(), get_client_ip(), get_device_info(), is_office_ip() (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (24): bfs_paths(), find_start_nodes(), graph_search(), hybrid_search(), merge_results(), normalize_results(), apply_edit(), backup_file() (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (31): aC(), Ak(), aO(), bE(), BO(), DE(), eC(), eO() (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.13
Nodes (22): d(), a(), C(), eT(), f(), FS(), gE(), h() (+14 more)

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (20): ab(), _b(), bb(), cb(), db(), Eb(), fb(), gb() (+12 more)

### Community 8 - "Community 8"
Cohesion: 0.17
Nodes (19): Ay(), em(), Fy(), Gc(), im(), Jc(), jy(), Kc() (+11 more)

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (14): e(), bC(), BS(), cm(), e(), hm(), Hv(), i() (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (14): AE(), cO(), $d(), GO(), jE(), jx(), KO(), My() (+6 more)

### Community 11 - "Community 11"
Cohesion: 0.26
Nodes (4): add_edge(), add_node(), extract_urls(), GraphVisitor

### Community 12 - "Community 12"
Cohesion: 0.21
Nodes (12): Dy(), Ig(), jg(), Kv(), mg(), pg(), py(), qg() (+4 more)

### Community 13 - "Community 13"
Cohesion: 0.18
Nodes (6): AppConfig, AccountsConfig, AttendanceConfig, HolidaysConfig, LeaveManagementConfig, ReportsConfig

### Community 14 - "Community 14"
Cohesion: 0.54
Nodes (7): calculate_metadata_score(), fuzzy_match(), load_index(), metadata_search(), normalize(), score_word_match(), tokenize()

### Community 15 - "Community 15"
Cohesion: 0.29
Nodes (2): get_file_hash(), read_file_content()

### Community 16 - "Community 16"
Cohesion: 0.33
Nodes (2): FunctionModelVisitor, Detect patterns like:          AttendanceRecord.objects.filter()         Empl

### Community 17 - "Community 17"
Cohesion: 0.6
Nodes (5): filterHighlight(), highlightFilter(), neighbourhoodHighlight(), selectNode(), selectNodes()

### Community 18 - "Community 18"
Cohesion: 0.4
Nodes (1): Migration

### Community 19 - "Community 19"
Cohesion: 0.4
Nodes (1): CodeChunkVisitor

### Community 20 - "Community 20"
Cohesion: 0.7
Nodes (4): boost_important_results(), diversify_results(), remove_duplicate_results(), rerank_results()

### Community 21 - "Community 21"
Cohesion: 0.5
Nodes (2): apply_intent_boost(), detect_query_intent()

### Community 22 - "Community 22"
Cohesion: 0.4
Nodes (1): CallGraphVisitor

### Community 24 - "Community 24"
Cohesion: 0.83
Nodes (3): clear_cache(), main(), run_indexer()

### Community 25 - "Community 25"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 26 - "Community 26"
Cohesion: 0.67
Nodes (2): format_hours(), Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (1): Migration

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (1): ASGI config for attendance_system project.  It exposes the ASGI callable as a

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): Django settings for attendance_system project.  Generated by 'django-admin sta

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (1): URL configuration for attendance_system project.  The `urlpatterns` list route

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (1): WSGI config for attendance_system project.  It exposes the WSGI callable as a

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): Migration

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (1): True if employee has checked in today.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): True if employee has checked out today.

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (1): RAG Testing Level 1

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (1): RAG Testing Level 2

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (1): RAG Testing Level 3

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): RAG Testing Level 4

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): RAG Testing Level 5

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): RAG Testing Level 6

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): RAG Testing V3

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (1): Feature Analyzer Modification Logs

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): Architecture Overview Report

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Global Navigation Bar

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (1): GPS-based Check-in Workflow

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (1): Leave Request Rules (36h Notice)

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Monthly Report Export Actions

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (1): Employee Attendance Analytics Charts

## Knowledge Gaps
- **33 isolated node(s):** `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp`, `Calculate total hours worked.         Called automatically when the employee ch`, `True if employee has checked in today.` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 15`** (7 nodes): `create_chunks()`, `detect_file_type()`, `detect_module()`, `extract_python_metadata()`, `get_file_hash()`, `read_file_content()`, `auto_indexer.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 16`** (6 nodes): `FunctionModelVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `Detect patterns like:          AttendanceRecord.objects.filter()         Empl`, `model_usage_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 18`** (5 nodes): `Migration`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 19`** (5 nodes): `CodeChunkVisitor`, `.__init__()`, `.visit_ClassDef()`, `.visit_FunctionDef()`, `code_chunk_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 21`** (5 nodes): `retrieval_ranker.py`, `apply_intent_boost()`, `deduplicate_results()`, `detect_query_intent()`, `should_ignore_file()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (5 nodes): `CallGraphVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `call_graph_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (3 nodes): `main()`, `manage.py`, `Run administrative tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (3 nodes): `format_hours()`, `Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75`, `attendance_filters.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `Migration`, `0002_alter_employee_options_alter_employee_department_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `ASGI config for attendance_system project.  It exposes the ASGI callable as a`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `settings.py`, `Django settings for attendance_system project.  Generated by 'django-admin sta`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (2 nodes): `urls.py`, `URL configuration for attendance_system project.  The `urlpatterns` list route`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (2 nodes): `wsgi.py`, `WSGI config for attendance_system project.  It exposes the WSGI callable as a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (2 nodes): `Migration`, `0002_leavebalance.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `True if employee has checked in today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `True if employee has checked out today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `RAG Testing Level 1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `RAG Testing Level 2`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `RAG Testing Level 3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `RAG Testing Level 4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `RAG Testing Level 5`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `RAG Testing Level 6`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `RAG Testing V3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `Feature Analyzer Modification Logs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `Architecture Overview Report`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `Global Navigation Bar`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `GPS-based Check-in Workflow`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `Leave Request Rules (36h Notice)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Monthly Report Export Actions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (1 nodes): `Employee Attendance Analytics Charts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `J` connect `Community 0` to `Community 1`, `Community 4`?**
  _High betweenness centrality (0.208) - this node is a cross-community bridge._
- **Why does `d()` connect `Community 6` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `t()` connect `Community 9` to `Community 0`, `Community 2`, `Community 6`, `Community 8`, `Community 10`, `Community 12`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 17 inferred relationships involving `Employee` (e.g. with `EmployeeAdmin` and `EmployeeCreationForm`) actually correct?**
  _`Employee` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `LeaveRequest` (e.g. with `LeaveRequestAdmin` and `LeaveBalanceAdmin`) actually correct?**
  _`LeaveRequest` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp` to the rest of the system?**
  _33 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._