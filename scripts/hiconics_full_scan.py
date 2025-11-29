import sys
import os
import time

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import utils
from src.constants import PRIORITY_ADDRESSES
from src.zero_addresses import ZERO_ADDRESSES

SEARCH_TIMEOUT = 300  # 搜索超时时间

def main():
    client = utils.get_client()

    # 直接使用从 zero_addresses.py 导入的列表
    zero_addresses = ZERO_ADDRESSES

    print(f"📋 [阶段1] 正在快速扫描 {len(PRIORITY_ADDRESSES)} 个有效数据点 (High Priority)...")
    utils.print_header()

    # 1. 扫描高优先级
    for addr in PRIORITY_ADDRESSES:
        try:
            val = client.read_holding_registers(addr, 1)[0]
            utils.print_record(addr, val)
        except Exception:
            pass

    print("-" * 75)
    print(f"📋 [阶段2] 正在后台扫描 {len(zero_addresses)} 个未知/零值地址 (Low Priority)...")
    print(f"⏳ 超时设置: {SEARCH_TIMEOUT}秒")
    print("-" * 75)

    start_time = time.time()

    # 2. 扫描低优先级
    for addr in zero_addresses:
        elapsed_time = time.time() - start_time
        if elapsed_time > SEARCH_TIMEOUT:
            print(f"\n🛑 扫描超时! 已运行 {elapsed_time:.1f} 秒。")
            break

        try:
            val = client.read_holding_registers(addr, 1)[0]
            if val != 0:
                utils.print_record(addr, val, prefix="🔥 新发现!")
        except Exception:
            pass

    print("\n✅ 程序运行结束。")

if __name__ == "__main__":
    main()
