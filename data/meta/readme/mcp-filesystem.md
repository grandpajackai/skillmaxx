# Filesystem MCP Server

Node.js server implementing Model Context Protocol (MCP) for filesystem operations.

Published on npm as [`@modelcontextprotocol/server-filesystem`](https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem).

## Features

- Read/write files
- Create/list/delete directories
- Move files/directories
- Search files
- Get file metadata
- Directory access control from command-line arguments, with [Roots](https://modelcontextprotocol.io/docs/learn/client-concepts#roots) as a deprecated, 2025-era convenience
- Serves both protocol eras on stdio: 2026-07-28 clients (`server/discover`, no handshake) and 2025-era clients (`initialize`)

## Directory Access Control

The server may touch only its **allowed directories**. Pass them on the command line. A 2025-era client that supports [Roots](https://modelcontextprotocol.io/docs/learn/client-concepts#roots) can also replace them at runtime, but Roots is [deprecated as of protocol version 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/deprecated) and a 2026-07-28 connection cannot use it.

### Method 1: Command-line Arguments (Recommended)
Specify Allowed directories when starting the server:
```bash
mcp-server-filesystem /path/to/dir1 /path/to/dir2
```

This is the only method that works on every protocol version, so it is the one to use.

### Method 2: MCP Roots (Deprecated, 2025-era clients only)
A client that connects with a 2025-era protocol version (the `initialize` handshake) and supports [Roots](https://modelcontextprotocol.io/docs/learn/client-concepts#roots) can dynamically update the Allowed directories.

Roots notified by Client to Server, completely replace any server-side Allowed directories when provided.

**Important**: If server starts without command-line arguments AND a 2025-era client doesn't support roots protocol, the server fails at initialization: it logs the reason to stderr, closes the connection and exits with status 1. A client that supports roots but provides none (or none that are valid) keeps the connection, with no allowed directories until it sends `roots/list_changed` with valid roots.

The 2026-07-28 protocol has no `initialize` handshake and no server-to-client `roots/list` request, so a 2026-07-28 client's roots are never asked for: the command-line directories are the whole allow-list. A server started with none answers every tool call on such a connection with an error saying so.

### How It Works

The server's directory access control follows this flow:

1. **Server Startup**
   - Server starts with directories from command-line arguments (if provided)
   - If no arguments provided, server starts with empty allowed directories

2. **Client Connection**
   - The client's first message picks the protocol era of the connection
   - A **2026-07-28** client sends `server/discover` (or any request carrying the per-request `_meta` envelope): the server uses the command-line directories, and steps 3 and 4 do not apply
   - A **2025-era** client sends `initialize` with its capabilities, and the server checks whether it supports roots (`capabilities.roots`)
   
3. **Roots Protocol Handling** (2025-era clients that support roots)
   - **On initialization**: Server requests roots from client via `roots/list`
   - Client responds with its configured roots
   - Server replaces ALL allowed directories with client's roots
   - Tool calls that arrive before the initial roots are loaded wait for them, so they are checked against the client's roots
   - **On runtime updates**: Client can send `notifications/roots/list_changed`
   - Server requests updated roots and replaces allowed directories again
   - Tool calls that arrive while an update is being fetched wait for it, so none runs against a root the client has just withdrawn
   - Once the client's roots are in force, an update with no valid roots revokes access: every path is refused ("Access denied - no allowed directories") until the client exposes a root again. Before any root has been in force, such an update keeps the command-line directories

4. **Fallback Behavior** (2025-era clients that don't support roots)
   - Server continues using command-line directories only
   - No dynamic updates possible
   - With no command-line directories either, the server logs an error, closes the connection and exits with status 1

5. **Access Control**
   - All filesystem operations are restricted to allowed directories
   - Use `list_allowed_directories` tool to see current directories
   - Server requires at least ONE allowed directory to operate

**Note**: The server will only allow operations within directories specified either via `args` or, for a 2025-era client, via Roots.



## API

### Tools

- **read_text_file**
  - Read complete contents of a file as text
  - Inputs:
    - `path` (string)
    - `head` (number, optional): First N lines
    - `tail` (number, optional): Last N lines
  - Always treats the file as UTF-8 text regardless of extension
  - Cannot specify both `head` and `tail` simultaneously

- **read_media_file**
  - Read a file and return it as a base64-encoded content block with its MIME type
  - Inputs:
    - `path` (string)
  - Streams the file and returns base64 data with the corresponding MIME type. Image and
    audio files are returned as `image`/`audio` content; any other file type is returned as
    an embedded `resource` (a valid MCP content block for arbitrary binary data)

- **read_multiple_files**
  - Read multiple files simultaneously
  - Input: `paths` (string[])
  - Failed reads won't stop the entire operation

- **write_file**
  - Create new file or overwrite existing (exercise caution with this)
  - Inputs:
    - `path` (string): File location
    - `content` (string): File content
  - An existing file is overwritten in place, so it keeps its inode, creation
    time, hard links and permissions (`edit_file` writes the same way). The
    overwrite is not crash-atomic: a crash mid-write can leave the file partly
    written. A read-only file is refused rather than replaced

- **edit_file**
  - Make selective edits using advanced pattern matching and formatting
  - Features:
    - Line-based and multi-line content matching
    - Whitespace normalization with indentation preservation
    - Multiple simultaneous edits with correct positioning
    - Indentation style detection and preservation: when only whitespace differs, each replacement line takes the indentation of the line it replaces
    - Preserves the file's line endings (LF or CRLF)
    - Git-style diff output with context
    - Preview changes with dry run mode
  - Inputs:
    - `path` (string): File to edit
    - `edits` (array): List of edit operations
      - `oldText` (string): Text to search for (can be substring)
      - `newText` (string): Text to replace with
    - `dryRun` (boolean): Preview changes without applying (default: false)
  - Returns detailed diff and match information for dry runs, otherwise applies changes
  - Best Practice: Always use dryRun first to preview changes before applying them

- **create_directory**
  - Create new directory or ensure it exists
  - Input: `path` (string)
  - Creates parent directories if needed
  - Succeeds silently if directory exists

- **list_directory**
  - List directory contents with [FILE] or [DIR] prefixes
  - Input: `path` (string)

- **list_directory_with_sizes**
  - List directory contents with [FILE] or [DIR] prefixes, including file sizes
  - Inputs:
    - `path` (string): Directory path to list
    - `sortBy` (string, optional): Sort entries by "name" or "size" (default: "name")
  - Returns detailed listing with file sizes and summary statistics
  - Shows total files, directories, and combined size

- **move_file**
  - Move or rename files and directories
  - Inputs:
    - `source` (string)
    - `destination` (string)
  - Fails if destination exists

- **search_files**
  - Recursively search for files/directories that match or do not match patterns
  - Inputs:
    - `path` (string): Starting directory
    - `pattern` (string): Search pattern
    - `excludePatterns` (string[]): Exclude any patterns.
  - Glob-style pattern matching
  - Returns full paths to matches

- **directory_tree**
  - Get recursive JSON tree structure of directory contents
  - Inputs:
    - `path` (string): Starting directory
    - `excludePatterns` (string[]): Exclude any patterns. Glob formats are supported.
  - Returns:
    - JSON array where each entry contains:
      - `name` (string): File/directory name
      - `type` ('file'|'directory'): Entry type
      - `children` (array): Present only for directories
        - Empty array for empty directories
        - Omitted for files
  - Output is formatted with 2-space indentation for readability
    
- **get_file_info**
  - Get detailed file/directory metadata
  - Input: `path` (string)
  - Returns:
    - Size
    - Creation time
    - Modified time
    - Access time
    - Type (file/directory)
    - Permissions

- **list_allowed_directories**
  - List all directories the server is allowed to access
  - No input required
  - Returns:
    - Directories that this server can read/write from

### Tool annotations (MCP hints)

This server sets [MCP ToolAnnotations](https://modelcontextprotocol.io/specification/2025-03-26/server/tools#toolannotations)
on each tool so clients can:

- Distinguish **read‑only** tools from write‑capable tools.
- Understand which write operations are **idempotent** (safe to retry with the same arguments).
- Highlight operations that may be **destructive** (overwriting or heavily mutating data).
- Signal that a tool does **not** reach an open or external world (every filesystem tool sets `openWorldHint: false`).

The mapping for filesystem tools is:

| Tool                        | readOnlyHint | idempotentHint | destructiveHint | Notes                                            |
|-----------------------------|--------------|----------------|-----------------|--------------------------------------------------|
| `read_text_file`            | `true`       | –              | –               | Pure read                                       |
| `read_media_file`           | `true`       | –              | –               | Pure read                                       |
| `read_multiple_files`       | `true`       | –              | –               | Pure read                                       |
| `list_directory`            | `true`       | –              | –               | Pure read                                       |
| `list_directory_with_sizes` | `true`       | –              | –               | Pure read                                       |
| `directory_tree`            | `true`       | –              | –               | Pure read                                       |
| `search_files`              | `true`       | –              | –               | Pure read                                       |
| `get_file_info`             | `true`       | –              | –               | Pure read                                       |
| `list_allowed_directories`  | `true`       | –              | –               | Pure read                                       |
| `create_directory`          | `false`      | `true`         | `false`         | Re‑creating the same dir is a no‑op             |
| `write_file`                | `false`      | `true`         | `true`          | Overwrites existing files                       |
| `edit_file`                 | `false`      | `false`        | `true`          | Re‑applying edits can fail or double‑apply      |
| `move_file`                 | `false`      | `false`        | `true`          | Deletes source file                             |

> Note: `idempotentHint` and `destructiveHint` are meaningful only when `readOnlyHint` is `false`, as defined by the MCP spec. Every tool also sets `openWorldHint: false` — this server only accesses the local filesyste