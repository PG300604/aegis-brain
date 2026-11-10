import urllib.request
import json
import sys

def check_runs():
    url = "https://api.github.com/repos/PG300604/aegis-brain/actions/runs?per_page=10"
    req = urllib.request.Request(url, headers={"User-Agent": "AegisBot"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            runs = data.get("workflow_runs", [])
            print(f"Total runs: {len(runs)}")
            for r in runs:
                msg = r.get("head_commit", {}).get("message", "").split("\n")[0]
                print(f"Run ID: {r['id']} | Status: {r['status']} | Conclusion: {r['conclusion']} | SHA: {r['head_sha'][:7]} | {msg}")
                if r['conclusion'] == 'failure':
                    # fetch jobs
                    jobs_url = r['jobs_url']
                    j_req = urllib.request.Request(jobs_url, headers={"User-Agent": "AegisBot"})
                    with urllib.request.urlopen(j_req) as j_resp:
                        j_data = json.loads(j_resp.read().decode())
                        for job in j_data.get('jobs', []):
                            print(f"   Job: {job['name']} | Conclusion: {job['conclusion']}")
                            if job['conclusion'] == 'failure':
                                for step in job.get('steps', []):
                                    if step.get('conclusion') == 'failure':
                                        print(f"      Failed Step: {step['name']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_runs()
