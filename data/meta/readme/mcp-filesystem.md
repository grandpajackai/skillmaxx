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

### Read-only Mode
Add `--read-only` to serve only the tools that cannot change the filesystem:
```bash
mcp-server-filesystem --read-only /path/to/dir1 /path/to/dir2
```

The server then registers only the tools annotated `readOnlyHint: true` in the [Tool annotations](#tool-annotations-mcp-hints) table, the ones that read and list. Every tool not annotated `readOnlyHint: true`, that is every tool that writes (such as `write_file` and `edit_file`), is left out, so a client never lists it and a call to it fails as an unknown tool. A tool added later follows the same rule through its annotation. The server enforces this, whatever the client is configured to allow, and it works the same with `npx` as with Docker. It applies on both protocol eras, and to directories that come from a client's Roots.

The flag may appear anywhere among the arguments. `--` ends the options, so a directory literally named `--read-only` can be given after it.

Read-only mode covers every allowed directory. To make only some of them read-only, run two servers: one with `--read-only` for the directories to protect, and one without it for the rest. That separation holds only while the writable server keeps its command-line directories: a 2025-era client that supports Roots replaces them (see Method 2), so it could expose a protected directory to the writable server, unless that server is started with `--confine-roots` (see below). Where that matters, make the protected directories read-only at the operating-system level as well, with file permissions or, with Docker, a bind mount's `ro` flag.

### Method 2: MCP Roots (Deprecated, 2025-era clients only)
A client that connects with a 2025-era protocol version (the `initialize` handshake) and supports [Roots](https://modelcontextprotocol.io/docs/learn/client-concepts#roots) can dynamically update the Allowed directories.

Roots notified by Client to Server, completely replace any server-side Allowed directories when provided.

#### Confining Roots to the command-line directories
To keep a client's Roots inside the directories you gave on the command line, add `--confine-roots`:
```bash
mcp-server-filesystem --confine-roots /path/to/dir1 /path/to/dir2
```

The client's Roots can then narrow the command-line directories but never replace or widen them. The server allows the overlap of the two:

- A root inside a command-line directory is allowed as given, so a client can narrow access to one project.
- A root that contains a command-line directory (for example `/`) is narrowed to that directory.
- A root outside every command-line directory is ignored and logged. If every root is ignored, the server treats the update as one with no valid roots: before any root has been in force the command-line directories stay; once one has, access is revoked until the client exposes a root inside them again.

This suits an operator who decides what may be shared (the command line) while letting a client say what it wants to work on (its Roots), and it keeps a client from discarding the command-line directories by advertising its working directory. Without command-line directories the flag has no effect, and the server warns at startup. Without the flag, Roots replace the command-line directories as described above.

A Root reached through a symlink is allowed in both its advertised form and its resolved form, as a command-line directory is: a Root of `file:///tmp/project` on macOS allows `/tmp/project` and `/private/tmp/project`. Every requested path is still resolved and checked against the resolved directories, so a symlink inside a Root that points outside it is refused.

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
   - Server replaces ALL allowed directories with client's roots (with `--confine-roots`, with their overlap with the command-line directories)
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
   - The server also logs the effective allowed directories to stderr, with where they came from (the command line, or the client's Roots and whether those replaced the command-line directories), at startup and whenever they change: after `initialize`, after each Roots update, and when a withdrawal leaves none. For example:
     ```
     Effective allowed directories (from the client's Roots, which replaced the command-line directories):
       /Users/username/project
     ```
   - Server requires at least ONE allowed directory to operate

**Note**: The server will only allow operations within directories specified either via `args` or, for a 2025-era client, via Roots.



## API

### Resources

Files inside the allowed directories are also [resources](https://modelcontextprotocol.io/specification/2026-07-28/server/resources), so a client application can read one with `resources/read` and decide itself what to do with it (attach it to the model's context, show it to the user), rather than relaying it through a tool result.

- **Resource template** `file://{+path}` (name `file`)
  - Read any file by its absolute `file://` URI, for example `file:///home/user/project/README.md`. A path with spaces or other reserved characters is percent-encoded, as in any `file://` URL.
  - Text files are returned as `text`, with a MIME type from the extension (`text/plain` for an unknown extension whose bytes are UTF-8). Images, audio, PDFs and other binary files are returned as a base64 `blob` with their MIME type (`application/octet-stream` when unknown).
  - Confined exactly as the tools are: a URI outside the allowed directories, or a symlink whose target is outside them, is refused with an `Access denied` error (`-32602`). A missing file is "resource not found" (`-32602` with the URI in the error data), and a directory is not a resource.
  - `resources/list` returns nothing: the server never enumerates the disk. Find files with `list_directory`, `directory_tree` or `search_files`, then read them by URI.
  - Results carry a cache hint of `ttlMs: 0`, `cacheScope: "private"` (2026-07-28), since a file can change at any time.

### Tools

- **read_text_file**
  - Read complete contents of a file as text
  - Inputs:
    - `path` (string)
    - `head` (non-negative integer, optional): First N lines; `0` returns no lines
    - `tail` (non-negative integer, optional): Last N lines; `0` returns no lines
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
  - Allowed-directory checks are path-based: they check the name you pass,
    not every name the file has. A hard link is a real name of the same file,
    so when a file inside an allowed directory is also hard-linked from
    somewhere else (pnpm, for example, hard-links package files into
    `node_modules` from its store), overwriting or editing it changes the
    content at every name, inside the allowed directories or not.
    `get_file_info` reports a file's `hardLinks` count; more than 1 means
    the file has other names

- **append_file**
  - Append text