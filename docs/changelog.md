# Changelog

All notable changes to Collagraph will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation skeleton with guides, API reference, and examples
- More resilient error handling in PySideRenderer

### Fixed
- Signal blocking when setting attributes directly to prevent unwanted triggers
- Unnecessary remounts of fragments in `v-if` directives

## [0.8.11] - 2026-01-19

### Added
- Support for template refs via `ref` attribute to access underlying widgets
- Dynamic slot content no longer requires a template wrapper element

### Fixed
- Issue with removing items from form layouts
- Error in `v-bind` within `v-for` when different numbers of props are used
- Signal blocking for `QTreeWidget` when inserting and removing items

### Changed
- Minimum PyGfx version bumped to 0.13.0

## [0.8.8] - 2025-12-01

### Fixed
- Setting selected and expanded state of `QTreeWidgetItem` elements
- Signal restoration after setting attributes to prevent trigger issues

## [0.8.7] - 2025-11-28

### Added
- Support for component classes in dynamic tags (e.g., `<component :is="SomeComponent" />`)
- Keyed reconciliation for more efficient list rendering with `:key` attribute

### Fixed
- Name clash issues in `v-for` directives
- Unwanted signal triggers in PySide components
- End location parsing of self-closing elements in templates

## [0.8.0] - 2025-10-26

### Added
- Fine-grained reactivity system for more efficient updates
- `init()` lifecycle hook as the recommended initialization method
- Support for Python 3.14 in CI

### Fixed
- Problem with using form layouts in components
- Callback triggers when watchers are destroyed

### Changed
- Refactored `cgx` package to `sfc` (Single File Component) package with better module names
- Migrated from Black to Ruff for code formatting
- Migrated from Poetry to uv for dependency management

## [0.7.0] - 2024-03-06

### Added
- CLI script to run `.cgx` component files directly with `collagraph` command
- Support for `QScrollArea` widgets in PySide renderer
- Custom widget registration and custom layout support

### Fixed
- Bug where root-level comments would break the `.cgx` parser
- Text element handling in templates

### Changed
- Improved handling of custom widgets and layouts

## [0.6.0] - 2023-06-14

### Added
- Support for PySide 6.4 and later versions
- Better `.cgx` file discovery from projects that include Collagraph

### Changed
- Made PySide truly optional - can install without PySide for PyGfx-only usage
- Updated PyGfx examples for compatibility

### Fixed
- Counter example in README to reflect current best practices

---

For detailed information about each release, see the [GitHub Releases](https://github.com/fork-tongue/collagraph/releases) page.

## Previous Versions

Versions prior to 0.6.0 are not documented in this changelog. Please refer to the [commit history](https://github.com/fork-tongue/collagraph/commits/main) for details on earlier changes.
