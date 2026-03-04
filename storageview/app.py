print("starting...", flush=True)

from flask import Flask, render_template
import shutil
import os

app = Flask(__name__)

def get_volumes():
    volumes = {}
    raw = os.environ.get("VOLUMES", "")
    if raw:
        for pair in raw.split(","):
            name, path = pair.strip().split(":", 1)  # the "1" limits to first colon only
            volumes[name.strip()] = path.strip()
    return volumes

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            try:
                if entry.is_file(follow_symlinks=False):
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_dir_size(entry.path)
            except PermissionError:
                pass
    return total

@app.route("/")
def index():
    data = []
    for name, path in get_volumes().items():
        try:
            used_bytes = get_dir_size(path)
            used_gb = used_bytes / (1024 ** 3)
            data.append({"name": name, "path": path, "used": used_gb})
        except Exception as e:
            data.append({"name": name, "path": path, "error": str(e)})
    return render_template("index.html", volumes=data)

if __name__ == "__main__":
    print("calling app.run...", flush=True)
    app.run(host="0.0.0.0", port=5000, debug=False)
