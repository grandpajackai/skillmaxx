#!/usr/bin/env python3
"""Unit tests for npx package parsing used by the npm-cache pre-warm."""
import os,sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_tests as rt

cases = [
  ("npx -y @benborla29/mcp-server-mysql", "@benborla29/mcp-server-mysql"),
  ("npx -y mcp-local-rag", "mcp-local-rag"),
  ("npx --yes --package=@cyanheads/pubmed-mcp-server -- pubmed-mcp", "@cyanheads/pubmed-mcp-server"),
  ("npx -y --package foo -- bar", "foo"),
  ("npx -p bar -y", "bar"),
  ("uvx mcp-server-time", None),
  ("", None),
  (None, None),
]
failed=0
for cmd,want in cases:
  got=rt.npx_package(cmd)
  if got!=want:
    print(f"FAIL npx_package({cmd!r}) = {got!r}, want {want!r}")
    failed+=1
if failed:
    sys.exit(1)
print("ok npx_prewarm unit tests")
