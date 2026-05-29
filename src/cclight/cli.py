"""CLI 入口"""

import argparse
import logging
import sys

from cclight.config import VALID_STATES
from cclight.client import client_run
from cclight.daemon import daemon_start, daemon_status, daemon_stop


def main():
    parser = argparse.ArgumentParser(description="CCLight 状态指示器（CS 模式）")
    sub = parser.add_subparsers(dest="command")

    # cclight state <name>
    state_parser = sub.add_parser("state", help="设置状态（idle/working/input）")
    state_parser.add_argument("name", choices=VALID_STATES, help="目标状态")
    state_parser.add_argument("--port", help="指定串口设备（可选）")

    # cclight daemon <action>
    daemon_parser = sub.add_parser("daemon", help="管理 daemon 进程")
    daemon_sub = daemon_parser.add_subparsers(dest="action")

    start_p = daemon_sub.add_parser("start", help="启动 daemon")
    start_p.add_argument("--port", help="指定串口设备（可选）")
    start_p.add_argument("--fg", action="store_true", help="前台运行（调试用）")

    daemon_sub.add_parser("stop", help="停止 daemon")
    daemon_sub.add_parser("status", help="查看 daemon 状态")

    # 兼容旧用法：cclight idle / working / input
    parser.add_argument(
        "legacy_state", nargs="?", choices=VALID_STATES, help=argparse.SUPPRESS
    )
    parser.add_argument("--port", help="指定串口设备（可选）")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.WARNING, format="%(levelname)s: %(message)s"
        )

    if args.command == "state":
        client_run(args.name, port=args.port)
    elif args.command == "daemon":
        if args.action == "start":
            daemon_start(port=args.port, fg=args.fg)
        elif args.action == "stop":
            daemon_stop()
        elif args.action == "status":
            sys.exit(0 if daemon_status() else 1)
        else:
            daemon_parser.print_help()
            sys.exit(1)
    elif args.legacy_state:
        client_run(args.legacy_state, port=args.port)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
