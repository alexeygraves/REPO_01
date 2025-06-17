
#!/usr/bin/env python3
"""fs_info.py — вывод сведений о файловой системе и выбранном объекте.

Запуск:
    python fs_info.py <путь/к/файлу_или_каталогу>
Если путь не указан — берётся текущий каталог.
"""

import os
import stat
import sys
import platform
from pathlib import Path
from datetime import datetime


def human(n: int, base: int = 1024) -> str:
    """Преобразовать байты в человекочитаемый формат."""
    for unit in ("", "K", "M", "G", "T", "P"):
        if abs(n) < base:
            return f"{n:.0f} {unit}B"
        n /= base
    return f"{n:.0f} EB"


def ts(epoch: float) -> str:
    return datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")


def file_type(mode: int) -> str:
    """Определить тип файла по st_mode."""
    if stat.S_ISREG(mode):
        return "обычный файл"
    if stat.S_ISDIR(mode):
        return "каталог"
    if stat.S_ISLNK(mode):
        return "символическая ссылка"
    if stat.S_ISCHR(mode):
        return "символьное устройство"
    if stat.S_ISBLK(mode):
        return "блочное устройство"
    if stat.S_ISFIFO(mode):
        return "FIFO (канал)"
    if stat.S_ISSOCK(mode):
        return "сокет"
    return "неизвестный"


def show_fs_info(path: Path) -> None:
    """Вывести общую информацию о файловой системе для заданного пути."""
    vfs = os.statvfs(path)

    blksize = vfs.f_frsize or vfs.f_bsize
    total   = vfs.f_blocks * blksize
    free    = vfs.f_bavail * blksize
    used    = total - free
    pct     = used / total * 100 if total else 0

    print("📁  Информация о файловой системе")
    print(f"  • ФС для пути          : {path.resolve()}")
    print(f"  • Платформа            : {platform.system()} {platform.release()}")
    print(f"  • Размер блока         : {blksize} байт")
    print(f"  • Всего блоков         : {vfs.f_blocks}")
    print(f"  • Свободных блоков     : {vfs.f_bavail}")
    print(f"  • Всего объём          : {human(total)}")
    print(f"  • Использовано         : {human(used)}  ({pct:.1f} %)")
    print(f"  • Свободно             : {human(free)}")
    print(f"  • Inode всего          : {vfs.f_files}")
    print(f"  • Inode свободно       : {vfs.f_favail}\n")


def show_file_info(path: Path) -> None:
    """Вывести информацию о конкретном файле или каталоге."""
    st = path.lstat()  # не разыменовываем символические ссылки

    print("📄  Информация о выбранном объекте")
    print(f"  • Путь                 : {path.resolve()}")
    print(f"  • inode                : {st.st_ino}")
    print(f"  • Размер               : {human(st.st_size)}")
    print(f"  • Права (oct)          : {oct(st.st_mode & 0o777)}")
    print(f"  • Тип                  : {file_type(st.st_mode)}")
    print(f"  • Владелец (uid/gid)   : {st.st_uid}/{st.st_gid}")
    print(f"  • Время доступа        : {ts(st.st_atime)}")
    print(f"  • Время модификации    : {ts(st.st_mtime)}")
    print(f"  • Время изменения inode: {ts(st.st_ctime)}\n")


def main() -> None:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser()
    if not target.exists():
        sys.exit(f"Путь не существует: {target}")

    show_fs_info(target)
    show_file_info(target)


if __name__ == "__main__":
    main()
