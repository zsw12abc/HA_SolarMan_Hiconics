import sys
import os

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import utils

# 扫描范围
START_ADDR = 0x3000
END_ADDR = 0x4000
BLOCK_SIZE = 20

def main():
    client = utils.get_client()

    print(f"📋 正在地毯式扫描 0x{START_ADDR:04X} - 0x{END_ADDR:04X}...")
    utils.print_header()

    current = START_ADDR
    while current < END_ADDR:
        count = min(BLOCK_SIZE, END_ADDR - current)

        try:
            # 1. 尝试成块读取
            values = client.read_holding_registers(current, count)
            for i, val in enumerate(values):
                utils.print_record(current + i, val)

        except Exception:
            # 2. 失败则切换单点扫描
            for i in range(count):
                single_addr = current + i
                try:
                    val = client.read_holding_registers(single_addr, 1)[0]
                    utils.print_record(single_addr, val)
                except Exception:
                    pass # 无效地址跳过

        if current % 200 == 0:
            print(f"... 已扫描至 0x{current:04X}")
        current += count

    print("-" * 75)
    print("✅ 全域扫描完成。")

if __name__ == "__main__":
    main()
