from __future__ import annotations

from models import TaskType


TASK_TYPE_MAP = {
    "generate_code": TaskType.CODE,
    "debug": TaskType.CODE,
    "refactor": TaskType.CODE,
    "scaffold_project": TaskType.CODE,
    "git_commit": TaskType.CODE,
    "git_push": TaskType.CODE,
    "deploy_vercel": TaskType.CODE,
    "deploy_netlify": TaskType.CODE,
    "run_tests": TaskType.CODE,
    "fix_lint": TaskType.CODE,
    "create_tweet": TaskType.SOCIAL,
    "create_post": TaskType.SOCIAL,
    "schedule_content": TaskType.SOCIAL,
    "analyze_engagement": TaskType.SOCIAL,
    "reply_mentions": TaskType.SOCIAL,
    "generate_hashtags": TaskType.SOCIAL,
    "scrape_page": TaskType.WEB,
    "monitor_url": TaskType.WEB,
    "search_web": TaskType.WEB,
    "summarize_article": TaskType.WEB,
    "download_file": TaskType.WEB,
    "check_broken_links": TaskType.WEB,
    "organize_folder": TaskType.FILE,
    "search_files": TaskType.FILE,
    "convert_format": TaskType.FILE,
    "compress_files": TaskType.FILE,
    "sync_folder": TaskType.FILE,
    "clean_duplicates": TaskType.FILE,
    "run_automation": TaskType.SYSTEM,
    "monitor_system": TaskType.SYSTEM,
    "clean_temp_files": TaskType.SYSTEM,
    "optimize_performance": TaskType.SYSTEM,
    "manage_processes": TaskType.SYSTEM,
}


def get_task_type(task_description: str) -> TaskType:
    for keyword, task_type in TASK_TYPE_MAP.items():
        if keyword in task_description.lower():
            return task_type
    return TaskType.GENERAL
