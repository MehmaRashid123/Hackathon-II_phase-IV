# Feature Tasks: Advanced SaaS Layout & Premium UI/UX

**Feature Branch**: `005-saas-layout`
**Created**: 2026-02-05
**Status**: Draft
**Spec Reference**: `specs/005-saas-layout/spec.md`
**Plan Reference**: `specs/005-saas-layout/plan.md`

## Dependencies

- User Story 1 (P1): Professional Sidebar Navigation
- User Story 2 (P1): Persistent Theme Toggle
- User Story 3 (P2): Global Command Palette
- User Story 4 (P2): Animated Landing Page
- User Story 5 (P3): Loading Skeleton States

## Implementation Strategy

The implementation will follow an MVP-first approach, prioritizing core navigation and theming (P1 user stories), then moving to productivity and visual enhancements (P2 stories), and finally polish (P3 story). Each user story is designed to be independently testable.

## Phase 1: Setup

Goal: Install necessary frontend libraries.
Independent Test: Verify packages are installed in `package.json` and dependencies are resolved.

- [X] T001 Install `next-themes` for theme management in `frontend/package.json`
- [X] T002 Install `cmdk` for command palette in `frontend/package.json`
- [X] T003 Install `lucide-react` for icons in `frontend/package.json`

## Phase 2: Foundational

Goal: Refactor the root layout to support the new SaaS sidebar-main structure.
Independent Test: Verify `frontend/app/layout.tsx` is updated to include a flexible layout container suitable for sidebar and main content.

- [X] T004 Refactor `frontend/app/layout.tsx` to establish the base SaaS sidebar-main layout, ensuring responsiveness for mobile and desktop.

## Phase 3: User Story 1 - Professional Sidebar Navigation (Priority: P1)

Goal: Implement a collapsible sidebar with workspace/project navigation and profile section.
Independent Test: Load the dashboard and verify the sidebar displays correctly, collapses/expands, and is responsive on mobile.

- [X] T005 [P] [US1] Create `frontend/components/Sidebar.tsx` with dummy workspace switcher, navigation links (Dashboard, Tasks), and user profile section.
- [X] T006 [P] [US1] Implement sidebar collapse/expand functionality for desktop, including animation.
- [X] T007 [P] [US1] Implement mobile overlay sidebar with backdrop and smooth slide-in/out animations.
- [X] T008 [US1] Integrate `Sidebar.tsx` into `frontend/app/layout.tsx`.
- [X] T009 [US1] Implement active navigation link highlighting based on current route.
- [X] T010 [US1] Ensure `Lucide React` icons are used for navigation items.

## Phase 4: User Story 2 - Persistent Theme Toggle (Priority: P1)

Goal: Implement a persistent light/dark theme toggle.
Independent Test: Toggle themes, refresh the page, and verify persistence and smooth transitions.

- [X] T011 [P] [US2] Set up `frontend/providers/ThemeProvider.tsx` using `next-themes` to manage theme state.
- [X] T012 [P] [US2] Create `frontend/components/ThemeToggle.tsx` component with a switch to toggle between light/dark/system themes.
- [X] T013 [US2] Integrate `ThemeProvider` into `frontend/app/layout.tsx` to wrap the application.
- [X] T014 [US2] Place `ThemeToggle.tsx` in `frontend/components/TopBar.tsx` (to be created next, but prepare for placement).
- [X] T015 [US2] Verify theme persistence in `localStorage` and system preference detection.
- [X] T016 [US2] Ensure smooth theme transition animations for UI elements (300ms target).

## Phase 5: User Story 3 - Global Command Palette (Priority: P2)

Goal: Build a keyboard-activated global command palette.
Independent Test: Press Ctrl+K/Cmd+K, type queries, navigate results, and verify functionality.

- [X] T017 [P] [US3] Create `frontend/components/CommandSearch.tsx` using `cmdk` for the command palette modal.
- [X] T018 [P] [US3] Implement search functionality for navigation items and dummy tasks, including real-time debounced input.
- [X] T019 [P] [US3] Add keyboard navigation (arrow keys, Enter to select, Escape to close) within `CommandSearch.tsx`.
- [X] T020 [US3] Implement global keyboard shortcut (Ctrl+K / Cmd+K) to open the command palette.
- [X] T021 [US3] Integrate `CommandSearch.tsx` into `frontend/app/layout.tsx` or a relevant top-level component.
- [X] T022 [US3] Ensure `Lucide React` icons are used for command palette results.

## Phase 6: User Story 4 - Animated Landing Page (Priority: P2)

Goal: Implement a visually impressive landing page with particle background animation.
Independent Test: Visit the landing page and verify smooth particle animation and glassmorphism effects.

- [X] T023 [P] [US4] Create `frontend/components/ParticleBackground.tsx` using Framer Motion or a lightweight canvas library for the animated background.
- [X] T024 [P] [US4] Implement logic for configurable particle count (150 desktop, 50 mobile) and graceful degradation for performance.
- [X] T025 [US4] Apply `AnimatePresence` wrapper to the dashboard content for smooth layout shifts.
- [X] T026 [US4] Integrate `ParticleBackground.tsx` into the landing page layout (`frontend/app/page.tsx` or similar).
- [X] T027 [US4] Ensure glassmorphism cards on the landing page render correctly with `backdrop-filter` and appropriate fallbacks.

## Phase 7: User Story 5 - Loading Skeleton States (Priority: P3)

Goal: Display skeleton loading placeholders during data fetching.
Independent Test: Simulate slow network and verify skeleton placeholders appear during task list loading and new task creation.

- [X] T028 [P] [US5] Create generic `frontend/components/SkeletonCard.tsx` component for task list placeholders.
- [X] T029 [US5] Implement logic to display skeleton placeholders for task list loading (`frontend/app/(dashboard)/tasks/page.tsx`).
- [X] T030 [US5] Implement optimistic UI for new task creation, showing a skeleton state until confirmed.

## Phase 8: UI Refinement & Polish

Goal: Apply consistent UI refinements across the application.
Independent Test: Visually inspect all buttons and inputs for rounded corners, soft shadows, and subtle gradients.

- [X] T031 Refine all buttons and inputs with rounded corners (12px+), soft shadows, and subtle gradients across the application (`frontend/components/**/*.tsx` and global CSS).
- [X] T032 Create `frontend/components/TopBar.tsx` including a placeholder for Global Search and the `ThemeToggle`.
- [X] T033 Integrate `TopBar.tsx` into `frontend/app/layout.tsx`.

## Parallel Execution Examples

### For User Story 1 (P1): Professional Sidebar Navigation

- **T005 & T006 (Parallel)**: `Sidebar.tsx` creation and desktop collapse functionality can be developed in parallel as they operate on distinct aspects of the sidebar's behavior and UI.
- **T005 & T007 (Parallel)**: `Sidebar.tsx` creation and mobile overlay implementation can be done concurrently if working on separate files/branches for each.

### For User Story 2 (P1): Persistent Theme Toggle

- **T011 & T012 (Parallel)**: `ThemeProvider.tsx` setup and `ThemeToggle.tsx` component creation can be done in parallel as they handle different parts of the theming system.

### For User Story 3 (P2): Global Command Palette

- **T017, T018 & T019 (Parallel)**: `CommandSearch.tsx` component, search logic, and keyboard navigation can be developed concurrently within the `CommandSearch.tsx` file or related helper files.

### For User Story 4 (P2): Animated Landing Page

- **T023 & T024 (Parallel)**: `ParticleBackground.tsx` creation and performance degradation logic can be developed in parallel.

### For User Story 5 (P3): Loading Skeleton States

- **T028 & T029 (Parallel)**: `SkeletonCard.tsx` creation and integration into the task list page can be done in parallel.