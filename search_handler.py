from webdav_handler import list_files, read_file

def search_files(query):
    results = []
    files = list_files()

    for file in files:
        content = read_file(file)
        if not content:
            continue

        lines = content.splitlines()
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                context = "\n".join(lines[max(0, i-1):min(len(lines), i+2)])
                results.append({
                    "file": file,
                    "match": context.strip()
                })
    return results