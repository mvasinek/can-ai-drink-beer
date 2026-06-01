You are responsible for creating a PATCH release.

Tasks:

1. Analyze all changes since the last git tag.
2. Verify that the changes correspond to bug fixes, refactoring, documentation updates, tests, or other backward-compatible changes.
3. Determine the latest semantic version tag in the repository.
4. Increment the PATCH version number.
   Example:
   - 0.1.0 -> 0.1.1
   - 1.4.2 -> 1.4.3
5. Create a concise release summary.
6. Create a git commit using the format:

   release: v<new-version>

7. Create a git tag:

   v<new-version>

8. Do not push any commits or tags to a remote repository.

Before executing any git commands, display:
- Current version
- New version
- Release summary

Ask for confirmation before proceeding.