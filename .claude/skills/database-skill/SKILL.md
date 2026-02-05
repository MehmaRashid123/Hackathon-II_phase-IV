---
name: database-skill
description: Create tables, manage migrations, and design database schemas effectively. Use for building structured data storage in apps.
---

# Database Skill – Tables, Migrations, Schema Design

## Instructions

1. **Schema Design**
   - Plan tables based on entities and relationships
   - Identify primary keys and foreign keys
   - Normalize data to reduce redundancy

2. **Creating Tables**
   - Use SQL `CREATE TABLE` statements
   - Define data types for each column
   - Apply constraints (PRIMARY KEY, UNIQUE, NOT NULL, etc.)

3. **Migrations**
   - Use migration tools (e.g., Alembic for Python, Rails migrations, Sequelize for Node.js)
   - Version control your database schema
   - Apply incremental changes safely

4. **Relationships**
   - One-to-One, One-to-Many, Many-to-Many
   - Use foreign keys to maintain referential integrity
   - Join tables where necessary

## Best Practices
- Keep table and column names clear and consistent
- Avoid storing redundant data
- Use indexes for frequently queried columns
- Backup database before migrations
- Keep migrations small and reversible

