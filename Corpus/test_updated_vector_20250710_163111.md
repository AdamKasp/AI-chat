# Test Updated VectorDocument

This is a longer test document to verify that the refactored VectorDocument works correctly with summary instead of content and without file_path.

## Summary Testing
- The summary should be created from the first 500 characters
- File path should no longer be stored in Qdrant
- All operations should work seamlessly

## Additional Content
This content will likely be truncated in the summary but the full content will still be stored in PostgreSQL for retrieval through the regular document endpoints.
