import os
from db import *

DB = "sample.db"
if os.path.exists(DB):
    os.remove(DB)

with db_connection(DB) as cur:
    init_db(cur)
    add_defect(cur, "Login crash", "auth", "coding error", "high", "2026-10-06", 8.0)
    add_defect(cur, "Typo on form", "ui", "design flaw", "low", "2026-10-06", 0.5)
    add_defect(cur, "Slow query", "database", "coding error", "medium", "2026-10-08", 3.5)
    add_defect(cur, "Wrong total", "billing", "requirement gap", "high", "2026-10-13", 12.0)
    add_defect(cur, "Button misaligned", "ui", "design flaw", "low", "2026-10-13", 1.0)
    add_defect(cur, "Open bug", "auth", "coding error", "medium")

with db_connection(DB) as cur:
    print("all:", list_defects(cur))
    print("by cause:", count_by_cause(cur))
    print("fix times:", fix_times(cur))
    print("per week:", count_by_defects_per_week(cur))
    print("severity vs fix:", severity_vs_fix_time(cur))
    print("cause and module:", count_by_cause_and_module(cur))