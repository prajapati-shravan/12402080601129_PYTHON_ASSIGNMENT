"""Q8: Build/search an inverted token index, pickle it, and zip logs + index."""
import pickle, re, sys, zipfile
from collections import defaultdict
from pathlib import Path

TOKEN = re.compile(r"\b\w+\b", re.UNICODE)

def build(folder, archive_name):
    folder = Path(folder)
    if not folder.is_dir(): raise ValueError("folder does not exist")
    logs = sorted(p for p in folder.rglob("*.txt") if p.is_file())
    index = defaultdict(list); total_lines = 0
    for path in logs:
        try: display = str(path.relative_to(folder))
        except ValueError: display = path.name
        with path.open(encoding="utf-8", errors="replace") as stream:
            for line_no, line in enumerate(stream, 1):
                total_lines += 1
                for token in TOKEN.findall(line.lower()):
                    index[token].append((display, line_no))
    archive_path = Path(archive_name)
    index_path = archive_path.with_suffix(".pkl")
    with index_path.open("wb") as stream: pickle.dump(dict(index), stream, protocol=pickle.HIGHEST_PROTOCOL)
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in logs: archive.write(path, arcname=f"logs/{path.relative_to(folder)}")
        archive.write(index_path, arcname=index_path.name)
    return len(logs), total_lines, len(index), str(index_path), str(archive_path)

def search(index_path, queries):
    # Only load pickle files from a trusted source: pickle can execute code when loaded.
    with open(index_path, "rb") as stream: index = pickle.load(stream)
    output = []
    for query in queries:
        hits = index.get(query.lower(), [])
        output.append(f"{query}: " + (", ".join(f"{name}:{line}" for name, line in hits) if hits else "NOT_FOUND"))
    return "\n".join(output)

def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if not lines: print("Usage: BUILD folder archive.zip OR SEARCH index.pkl token1 token2"); return
    parts = lines[0].split()
    try:
        if parts[0].upper() == "BUILD" and len(parts) == 3:
            files, line_count, tokens, index_path, archive = build(parts[1], parts[2])
            print(f"FILES {files}\nLINES {line_count}\nTOKENS {tokens}\nINDEX {index_path}\nARCHIVE {archive}")
        elif parts[0].upper() == "SEARCH" and len(parts) >= 3:
            print(search(parts[1], parts[2:]))
        else: raise ValueError("invalid command")
    except (OSError, ValueError, pickle.PickleError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); sys.exit(1)
if __name__ == "__main__": main()
