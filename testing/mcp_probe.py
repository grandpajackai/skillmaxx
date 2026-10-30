#!/usr/bin/env python3
"""Minimal MCP stdio handshake: initialize + tools/list. Used for Codex, whose CLI has no MCP health check.
usage: mcp_probe.py <command> [args...]   prints 'PROBE OK <n> tools' or 'PROBE FAIL <reason>'"""
import json,subprocess,sys,threading,queue
p=subprocess.Popen(sys.argv[1:],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True)
q=queue.Queue();threading.Thread(target=lambda:[q.put(l) for l in p.stdout],daemon=True).start()
def send(m): p.stdin.write(json.dumps(m)+"\n");p.stdin.flush()
def wait(i,t=90):
  while True:
    try: l=q.get(timeout=t)
    except queue.Empty: return None
    try: m=json.loads(l)
    except Exception: continue
    if m.get("id")==i: return m
try:
  send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"skillmaxx-probe","version":"1"}}})
  r=wait(1)
  if not r or "result" not in r: print("PROBE FAIL no initialize result");sys.exit(1)
  send({"jsonrpc":"2.0","method":"notifications/initialized"});send({"jsonrpc":"2.0","id":2,"method":"tools/list"})
  r=wait(2,30);n=len((r or {}).get("result",{}).get("tools",[]))
  print(f"PROBE OK {n} tools (protocol {r and 'ok'})" if r and "result" in r else "PROBE FAIL no tools/list result")
except Exception as e: print("PROBE FAIL",e)
finally: p.kill()
