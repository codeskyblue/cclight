"""PID 文件工具"""

import os


def read_pid(pid_file):
    """读取 PID 文件。

    Returns:
        (pid, None) 成功
        (None, str) 失败，str 为错误信息
    """
    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        return pid, None
    except FileNotFoundError:
        return None, "PID 文件不存在"
    except (ValueError, OSError) as e:
        return None, "读取 PID 文件失败: {}".format(e)


def is_running(pid):
    """检测进程是否存活（通过 os.kill(pid, 0)）。"""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def cleanup_if_stale(pid_file):
    """检测 PID 文件是否 stale 并清理。

    如果文件对应的进程已不存在，删除 PID 文件。

    Returns:
        True  - 可以安全启动（文件不存在或已清理 stale 文件）
        False - 进程仍在运行，不应启动
    """
    if not os.path.exists(pid_file):
        return True

    pid, err = read_pid(pid_file)
    if err:
        try:
            os.remove(pid_file)
        except OSError:
            pass
        return True

    if is_running(pid):
        return False

    try:
        os.remove(pid_file)
    except OSError:
        pass
    return True
