#!/usr/bin/env python3
import os
import json
from typing import Dict, List, Optional

# ARES-TRON SYS_KERNEL V1.1
# Agnostic Project Awareness & Dynamic Resolution

class AresKernel:
    def __init__(self, fallback_root: str = "/home/daniel/tron/programas/TR"):
        self.current_cwd = os.getcwd()
        self.project_root = self._detect_project_root() or fallback_root
        self.system_docs = "/home/daniel/tron/programas/TR/docs" # Global Docs location

    def _detect_project_root(self) -> Optional[str]:
        """Climbs up from CWD to find the nearest project root (marked by LEEME.md)."""
        curr = self.current_cwd
        while curr != "/":
            if os.path.exists(os.path.join(curr, "LEEME.md")):
                return curr
            curr = os.path.dirname(curr)
        return None

    def resolve(self, symbol: str) -> Optional[str]:
        """Resolves a @symbol to a real file path based on the ACTIVE project."""
        mapping = {
            "@ROOT": self.project_root,
            "@SKILLS": os.path.join(self.system_docs, "skills"),
            "@MEMORY": os.path.join(self.system_docs, "ALMAS-IAS/IA-MEMORY.md"),
            "@TODO": os.path.join(self.project_root, "docs/TODO"),
            "@MODULES": os.path.join(self.project_root, "modules"),
            "@SCRIPTS": os.path.join(self.project_root, "scripts")
        }
        if symbol in mapping:
            return mapping[symbol]
        return None

    def list_projects(self) -> List[Dict]:
        """Scans the system for other ARES-compliant projects."""
        search_paths = ["/home/daniel/tron/programas", "/home/daniel/tron/programas/TR/AGENTES/sub-agentes"]
        projects = []
        for path in search_paths:
            if not os.path.exists(path): continue
            for d in os.listdir(path):
                full_path = os.path.join(path, d)
                if os.path.isdir(full_path) and os.path.exists(os.path.join(full_path, "LEEME.md")):
                    projects.append({"name": d, "path": full_path})
        return projects

    def audit(self) -> Dict:
        """Audits the current project structure."""
        required = ["modules", "docs/TODO", "scripts", "LEEME.md"]
        missing = [r for root in [self.project_root] for r in required if not os.path.exists(os.path.join(self.project_root, r))]
        return {
            "project": os.path.basename(self.project_root),
            "root": self.project_root,
            "status": "ARES-COMPLIANT" if not missing else "INCOMPLETE",
            "missing": missing
        }

if __name__ == "__main__":
    import sys
    kernel = AresKernel()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "resolve": print(kernel.resolve(sys.argv[2]))
        elif cmd == "list-projects": print(json.dumps(kernel.list_projects(), indent=2))
        elif cmd == "audit": print(json.dumps(kernel.audit(), indent=2))
        elif cmd == "where": print(kernel.project_root)
