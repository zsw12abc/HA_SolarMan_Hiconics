from pysolarmanv5 import PySolarmanV5
import config

def get_client(verbose=False):
    """创建并返回连接客户端"""
    print(f"🚀 连接设备: {config.IP} (SN: {config.SN})...")
    return PySolarmanV5(
        config.IP, config.SN,
        port=config.PORT,
        mb_slave_id=config.SLAVE_ID,
        verbose=verbose
    )

def signed(val):
    """转换 16 位有符号整数"""
    return val if val < 32768 else val - 65536

def print_header():
    """打印统一的表头"""
    print("-" * 75)
    print(f"{'地址':<8} | {'Raw':<6} | {'Signed':<7} | {'/10':<8} | {'/100':<8}")
    print("-" * 75)

def print_record(addr, val, prefix=""):
    """打印单行记录"""
    s_val = signed(val)
    # 格式化输出
    line = f"0x{addr:04X}   | {val:<6} | {s_val:<7} | {s_val / 10:<8} | {s_val / 100:<8}"
    if prefix:
        line = f"{prefix} {line}"
    print(line)