You are responsible for creating a MINOR release.

Tasks:

1. Analyze all changes since the last git tag.
2. Verify that the changes introduce new functionality while maintaining backward compatibility.
3. Determine the latest semantic version tag in the repository.
4. Increment the MINOR version number and reset PATCH to zero.
   Example:
   - 0.1.3 -> 0.2.0
   - 1.4.8 -> 1.5.0
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