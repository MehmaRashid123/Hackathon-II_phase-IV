---
name: spec-analysis-skill
description: Parse Spec-Kit Plus markdown files to extract requirements, user stories, and acceptance criteria. Use for analyzing project specs.
---

# Spec Analysis Skill – Parse Requirements, User Stories, Acceptance Criteria

## Instructions

1. **File Parsing**
   - Load Spec-Kit Plus markdown files
   - Identify sections by headings and bullet points
   - Recognize metadata (name, description, tags)

2. **Extract Requirements**
   - Detect functional and non-functional requirements
   - Capture details for features, constraints, and conditions
   - Organize requirements by priority

3. **Identify User Stories**
   - Parse “As a [user], I want [feature], so that [benefit]” statements
   - Map stories to corresponding requirements
   - Capture acceptance criteria for each story

4. **Acceptance Criteria**
   - Extract clear, testable conditions
   - Ensure criteria are measurable and specific
   - Associate with relevant user stories or requirements

## Best Practices
- Maintain structured output (JSON or tables)
- Preserve section hierarchy from markdown
- Handle multiple files in batch
- Validate extracted data for completeness
- Keep extraction logic modular for reuse

