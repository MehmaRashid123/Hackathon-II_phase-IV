---
id: 0003
title: Suggest Clean Build for SkeletonCard Error
stage: green
date: 2026-02-05
surface: agent
model: gemini-2.5-flash
feature: saas-layout
branch: 005-saas-layout
user: User
command: null
labels: ["bug-fix", "frontend", "environment", "caching"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: []
tests_yaml: []
prompt_text: |
  ## Error Type
  Runtime ReferenceError

  ## Error Message
  SkeletonCard is not defined


      at DashboardPage (app/dashboard/page.tsx:185:16)

  ## Code Frame
    183 |           {loading && tasks.length === 0 ? (
    184 |             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  > 185 |               <SkeletonCard />
        |                ^
    186 |               <SkeletonCard />
    187 |               <SkeletonCard />
    188 |             </div>

  Next.js version: 16.1.6 (Turbopack)
response_text: |
  The `tsconfig.json` confirms the path alias for `@/components` is correctly configured. Since the `SkeletonCard` component is properly imported and defined, and a server restart didn't resolve the issue, it suggests a caching problem within the Next.js environment. I recommend performing a clean build by deleting the `.next` and `node_modules` folders, then reinstalling dependencies and restarting the development server.
outcome: Suggested a clean build process (delete .next, node_modules, reinstall, restart) to address persistent ReferenceError despite correct code.
evaluation: All code-related aspects have been verified; the issue points to a development environment caching problem.
---