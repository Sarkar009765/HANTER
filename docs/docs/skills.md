---
sidebar_position: 5
---

# Skills

Skills are the building blocks of agent capabilities. They are lazy-loaded to minimize RAM usage.

## Built-in Skills

### Dev Skill
Full-stack development capabilities including code generation, git operations, and deployment.

**RAM:** 100MB | **Network:** Required

### Social Skill
Social media management including content creation and scheduling.

**RAM:** 80MB | **Network:** Required

### Web Skill
Web automation including scraping and monitoring.

**RAM:** 60MB | **Network:** Required

### File Skill
File operations including organization and search.

**RAM:** 40MB | **Network:** Not required

### System Skill
System operations including monitoring and automation.

**RAM:** 50MB | **Network:** Not required

## Skill Lifecycle

1. **Registered** - Skill class loaded into registry at startup
2. **Lazy Loaded** - Skill instantiated only when needed
3. **Auto-Unloaded** - Skill freed after 300 seconds of inactivity
4. **RAM Pressure Unload** - Oldest skill freed when RAM is needed
