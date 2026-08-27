#!/usr/bin/env python3
"""Ad-hoc OpenVAS (Greenbone) domain scanner driven over gvmd's GMP socket.

Runs inside the greenbone `gvm-tools` container, which mounts the gvmd and
ospd UNIX sockets and bundles the `gvm` client library (and therefore lxml).
"""

import os
import sys
import time

from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp

domains = os.environ["TARGETS"]
gate = os.environ.get("SEVERITY_GATE", "").strip().lower()

LEVEL_ORDER = {
    "critical": 5, "high": 4, "medium": 3, "low": 2, "info": 1, "": 0,
}


def level(value):
    return LEVEL_ORDER.get((value or "").strip().lower(), 0)


conn = UnixSocketConnection(path="/run/gvmd/gvmd.sock")
gmp = Gmp(connection=conn)
gmp.connect()
try:
    # Wait for gvmd to come up and finish importing the shipped feed before
    # resuming the scan config set. Bounded by the job timeout.
    config = None
    for attempt in range(60):
        try:
            gmp.authenticate("admin", "openvas")
            config = next(
                (c for c in gmp.get_configs().xpath("//config")
                 if c.get("name") == "Full and fast"),
                None,
            )
            if config is not None:
                break
        except Exception:
            pass
        time.sleep(10)

    if config is None:
        sys.exit("No 'Full and fast' scan config available (gvmd feed not ready?).")

    port_lists = gmp.get_port_lists().xpath(
        "//port_list[@name='All IANA assigned TCP']"
    )

    hosts = ",".join(domains.split(","))
    target_id = gmp.create_target(
        name="adhoc-target",
        hosts=hosts,
        port_list_id=port_lists[0].get("id") if port_lists else None,
    ).xpath(".//@id")[0]

    task_id = gmp.create_task(
        name="adhoc-scan",
        config_id=config.get("id"),
        target_id=target_id,
    ).xpath(".//@id")[0]

    gmp.start_task(task_id)

    # Poll until the task leaves the running state.
    report_id = None
    while True:
        task = gmp.get_task(task_id)
        status = task.xpath("//task/@status")[0]
        rid = task.xpath("//task/report/@id")
        if rid:
            report_id = rid[0]
        if status in ("Done", "Stopped", "Stop Requested", "Failed"):
            break
        time.sleep(30)

    if not report_id:
        sys.exit("Scan finished but no report was generated.")

    report = gmp.get_report(report_id)

    rows = []
    for host in report.xpath("//report//host"):
        name = host.xpath("string(.//asset/text)") or host.get("host")
        for res in host.xpath(".//result"):
            level_str = res.xpath("string(.//severity/level)")
            cvss = res.xpath("string(.//severity)")
            nvt = res.xpath("string(.//nvt/name)")
            cve = ", ".join(res.xpath(".//nvt/cve/text()"))
            rows.append((name, cvss, level_str, nvt, cve))

    rows.sort(key=lambda r: level(r[2]), reverse=True)

    print("HOST\tCVSS\tLEVEL\tNVT\tCVE")
    for row in rows:
        print("\t".join(row))

    # Report-only by default; an optional severity gate blocks the run.
    if gate and gate in LEVEL_ORDER:
        worst = max((level(r[2]) for r in rows), default=0)
        if worst < LEVEL_ORDER[gate]:
            print(f"\nGate: worst severity below '{gate}', not failing.")
        else:
            print(f"\nGate: findings at or above '{gate}', failing.")
            sys.exit(1)

finally:
    gmp.disconnect()