# Graph Report - .  (2026-05-14)

## Corpus Check
- Large corpus: 119 files · ~1,646,205 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder, or use --no-semantic to run AST-only.

## Summary
- 619 nodes · 1252 edges · 49 communities detected
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 138 edges (avg confidence: 0.67)
- Token cost: 1,500 input · 800 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Frontend Library (TomSelect)|Frontend Library (TomSelect)]]
- [[_COMMUNITY_Django Admin & Core Logic|Django Admin & Core Logic]]
- [[_COMMUNITY_Graph Visualization (Vis.js)|Graph Visualization (Vis.js)]]
- [[_COMMUNITY_Search & Retrieval Utils|Search & Retrieval Utils]]
- [[_COMMUNITY_Attendance Logic & Views|Attendance Logic & Views]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Code Parsing (AST)|Code Parsing (AST)]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_App Lifecycle (apps.py)|App Lifecycle (apps.py)]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Metadata Retrieval|Metadata Retrieval]]
- [[_COMMUNITY_File Detection & Indexing|File Detection & Indexing]]
- [[_COMMUNITY_ORM Model Usage Mapper|ORM Model Usage Mapper]]
- [[_COMMUNITY_UI Search Highlighting|UI Search Highlighting]]
- [[_COMMUNITY_Initial Database Schema|Initial Database Schema]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Search Result Reranking|Search Result Reranking]]
- [[_COMMUNITY_Retrieval Intent Filtering|Retrieval Intent Filtering]]
- [[_COMMUNITY_Call Graph Analysis|Call Graph Analysis]]
- [[_COMMUNITY_RAG System Management|RAG System Management]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Human-Readable Formatting|Human-Readable Formatting]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_System Configurations|System Configurations]]
- [[_COMMUNITY_Global Routing|Global Routing]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_RAG Evaluation Suite|RAG Evaluation Suite]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Project Templates & UI|Project Templates & UI]]
- [[_COMMUNITY_GPS Integration logic|GPS Integration logic]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]

## God Nodes (most connected - your core abstractions)
1. `J` - 89 edges
2. `Nk()` - 33 edges
3. `Ak()` - 32 edges
4. `Employee` - 19 edges
5. `t()` - 17 edges
6. `LeaveRequest` - 16 edges
7. `y()` - 15 edges
8. `LeaveBalance` - 14 edges
9. `c()` - 14 edges
10. `Qc()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `AttendanceRecordAdmin` --uses--> `AttendanceRecord`  [INFERRED]
  E:\WORK\python\ATTENDENCE\attendance\admin.py → E:\WORK\python\ATTENDENCE\attendance\models.py
- `Main page after login.     Shows today's check-in status and last 7 days of att` --uses--> `AttendanceRecord`  [INFERRED]
  E:\WORK\python\ATTENDENCE\attendance\views.py → E:\WORK\python\ATTENDENCE\attendance\models.py
- `Handle the Check In button.          Security checks (in order):     1. Must` --uses--> `AttendanceRecord`  [INFERRED]
  E:\WORK\python\ATTENDENCE\attendance\views.py → E:\WORK\python\ATTENDENCE\attendance\models.py
- `Handle the Check Out button.          Validation:     - Must have checked in` --uses--> `AttendanceRecord`  [INFERRED]
  E:\WORK\python\ATTENDENCE\attendance\views.py → E:\WORK\python\ATTENDENCE\attendance\models.py
- `Employee's personal attendance history.     Can be filtered by month using ?mon` --uses--> `AttendanceRecord`  [INFERRED]
  E:\WORK\python\ATTENDENCE\attendance\views.py → E:\WORK\python\ATTENDENCE\attendance\models.py

## Communities

### Community 0 - "Frontend Library (TomSelect)"
Cohesion: 0.06
Nodes (23): load_cache(), _(), A(), c(), e(), g(), h(), I() (+15 more)

### Community 1 - "Django Admin & Core Logic"
Cohesion: 0.05
Nodes (52): AbstractUser, EmployeeAdmin, HolidayAdmin, LeaveBalanceAdmin, LeaveRequestAdmin, EditProfileForm, EmployeeCreationForm, HolidayForm (+44 more)

### Community 2 - "Graph Visualization (Vis.js)"
Cohesion: 0.05
Nodes (33): aT(), Ax(), bg(), Bk(), Bx(), Cg(), Eg(), fm() (+25 more)

### Community 3 - "Search & Retrieval Utils"
Cohesion: 0.1
Nodes (25): bfs_paths(), find_start_nodes(), graph_search(), hybrid_search(), merge_results(), normalize_results(), apply_edit(), backup_file() (+17 more)

### Community 4 - "Attendance Logic & Views"
Cohesion: 0.09
Nodes (24): AttendanceRecordAdmin, AttendanceRecord, Stores one attendance record per employee per day.          Fields:     - emp, Calculate total hours worked.         Called automatically when the employee ch, calculate_distance_meters(), get_client_ip(), get_device_info(), is_office_ip() (+16 more)

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
Nodes (13): bC(), BS(), cm(), e(), hm(), Hv(), i(), IC() (+5 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (14): AE(), cO(), $d(), GO(), jE(), jx(), KO(), My() (+6 more)

### Community 11 - "Code Parsing (AST)"
Cohesion: 0.26
Nodes (4): add_edge(), add_node(), extract_urls(), GraphVisitor

### Community 12 - "Community 12"
Cohesion: 0.21
Nodes (12): Dy(), Ig(), jg(), Kv(), mg(), pg(), py(), qg() (+4 more)

### Community 13 - "App Lifecycle (apps.py)"
Cohesion: 0.18
Nodes (6): AppConfig, AccountsConfig, AttendanceConfig, HolidaysConfig, LeaveManagementConfig, ReportsConfig

### Community 14 - "Community 14"
Cohesion: 0.33
Nodes (3): b, R(), u()

### Community 15 - "Metadata Retrieval"
Cohesion: 0.54
Nodes (7): calculate_metadata_score(), fuzzy_match(), load_index(), metadata_search(), normalize(), score_word_match(), tokenize()

### Community 16 - "File Detection & Indexing"
Cohesion: 0.29
Nodes (2): get_file_hash(), read_file_content()

### Community 17 - "ORM Model Usage Mapper"
Cohesion: 0.33
Nodes (2): FunctionModelVisitor, Detect patterns like:          AttendanceRecord.objects.filter()         Empl

### Community 18 - "UI Search Highlighting"
Cohesion: 0.6
Nodes (5): filterHighlight(), highlightFilter(), neighbourhoodHighlight(), selectNode(), selectNodes()

### Community 19 - "Initial Database Schema"
Cohesion: 0.4
Nodes (1): Migration

### Community 20 - "Community 20"
Cohesion: 0.4
Nodes (1): CodeChunkVisitor

### Community 21 - "Search Result Reranking"
Cohesion: 0.7
Nodes (4): boost_important_results(), diversify_results(), remove_duplicate_results(), rerank_results()

### Community 22 - "Retrieval Intent Filtering"
Cohesion: 0.5
Nodes (2): apply_intent_boost(), detect_query_intent()

### Community 23 - "Call Graph Analysis"
Cohesion: 0.4
Nodes (1): CallGraphVisitor

### Community 25 - "RAG System Management"
Cohesion: 0.83
Nodes (3): clear_cache(), main(), run_indexer()

### Community 26 - "Community 26"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 27 - "Human-Readable Formatting"
Cohesion: 0.67
Nodes (2): format_hours(), Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (1): Migration

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (1): ASGI config for attendance_system project.  It exposes the ASGI callable as a

### Community 32 - "System Configurations"
Cohesion: 1.0
Nodes (1): Django settings for attendance_system project.  Generated by 'django-admin sta

### Community 33 - "Global Routing"
Cohesion: 1.0
Nodes (1): URL configuration for attendance_system project.  The `urlpatterns` list route

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): WSGI config for attendance_system project.  It exposes the WSGI callable as a

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): Migration

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (1): True if employee has checked in today.

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (1): True if employee has checked out today.

### Community 71 - "RAG Evaluation Suite"
Cohesion: 1.0
Nodes (1): RAG Testing Level 1

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (1): RAG Testing Level 2

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): RAG Testing Level 3

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): RAG Testing Level 4

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): RAG Testing Level 5

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): RAG Testing Level 6

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (1): RAG Testing V3

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (1): Feature Analyzer Modification Logs

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Architecture Overview Report

### Community 80 - "Project Templates & UI"
Cohesion: 1.0
Nodes (1): Global Navigation Bar

### Community 81 - "GPS Integration logic"
Cohesion: 1.0
Nodes (1): GPS-based Check-in Workflow

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (1): Leave Request Rules (36h Notice)

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (1): Monthly Report Export Actions

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (1): Employee Attendance Analytics Charts

## Knowledge Gaps
- **33 isolated node(s):** `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp`, `Calculate total hours worked.         Called automatically when the employee ch`, `True if employee has checked in today.` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `File Detection & Indexing`** (7 nodes): `create_chunks()`, `detect_file_type()`, `detect_module()`, `extract_python_metadata()`, `get_file_hash()`, `read_file_content()`, `auto_indexer.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `ORM Model Usage Mapper`** (6 nodes): `FunctionModelVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `Detect patterns like:          AttendanceRecord.objects.filter()         Empl`, `model_usage_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Initial Database Schema`** (5 nodes): `Migration`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 20`** (5 nodes): `CodeChunkVisitor`, `.__init__()`, `.visit_ClassDef()`, `.visit_FunctionDef()`, `code_chunk_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Retrieval Intent Filtering`** (5 nodes): `retrieval_ranker.py`, `apply_intent_boost()`, `deduplicate_results()`, `detect_query_intent()`, `should_ignore_file()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Call Graph Analysis`** (5 nodes): `CallGraphVisitor`, `.__init__()`, `.visit_Call()`, `.visit_FunctionDef()`, `call_graph_mapper.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (3 nodes): `main()`, `manage.py`, `Run administrative tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Human-Readable Formatting`** (3 nodes): `format_hours()`, `Converts decimal hours to human readable format.     0.75 -> '45 min'     4.75`, `attendance_filters.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `Migration`, `0002_alter_employee_options_alter_employee_department_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `ASGI config for attendance_system project.  It exposes the ASGI callable as a`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `System Configurations`** (2 nodes): `settings.py`, `Django settings for attendance_system project.  Generated by 'django-admin sta`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Global Routing`** (2 nodes): `urls.py`, `URL configuration for attendance_system project.  The `urlpatterns` list route`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (2 nodes): `wsgi.py`, `WSGI config for attendance_system project.  It exposes the WSGI callable as a`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (2 nodes): `Migration`, `0002_leavebalance.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `True if employee has checked in today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `True if employee has checked out today.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `RAG Evaluation Suite`** (1 nodes): `RAG Testing Level 1`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `RAG Testing Level 2`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `RAG Testing Level 3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `RAG Testing Level 4`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `RAG Testing Level 5`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `RAG Testing Level 6`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `RAG Testing V3`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `Feature Analyzer Modification Logs`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `Architecture Overview Report`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Project Templates & UI`** (1 nodes): `Global Navigation Bar`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `GPS Integration logic`** (1 nodes): `GPS-based Check-in Workflow`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `Leave Request Rules (36h Notice)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (1 nodes): `Monthly Report Export Actions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (1 nodes): `Employee Attendance Analytics Charts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `J` connect `Frontend Library (TomSelect)` to `Community 9`, `Search & Retrieval Utils`, `Django Admin & Core Logic`?**
  _High betweenness centrality (0.208) - this node is a cross-community bridge._
- **Why does `d()` connect `Community 6` to `Frontend Library (TomSelect)`, `Django Admin & Core Logic`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Why does `t()` connect `Community 9` to `Frontend Library (TomSelect)`, `Graph Visualization (Vis.js)`, `Community 6`, `Community 8`, `Community 10`, `Community 12`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Employee` (e.g. with `EmployeeAdmin` and `EmployeeCreationForm`) actually correct?**
  _`Employee` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `t()` (e.g. with `.clear()` and `.on()`) actually correct?**
  _`t()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Run administrative tasks.`, `Migration`, `Stores one attendance record per employee per day.          Fields:     - emp` to the rest of the system?**
  _33 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Frontend Library (TomSelect)` be split into smaller, more focused modules?**
  _Cohesion score 0.06 - nodes in this community are weakly interconnected._