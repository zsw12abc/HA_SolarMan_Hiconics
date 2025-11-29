import sys
import os
import time
from datetime import datetime

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import utils
from src.constants import PRIORITY_ADDRESSES
from src.zero_addresses import ZERO_ADDRESSES

# --- 配置 ---
SEARCH_TIMEOUT = 300  # 搜索超时时间
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONSTANTS_PATH = os.path.join(PROJECT_ROOT, "src", "constants.py")
ZERO_ADDRESSES_PATH = os.path.join(PROJECT_ROOT, "src", "zero_addresses.py")

def update_address_files(found_addresses, all_zero_addresses):
    """
    将发现的地址从 zero_addresses.py 移动到 constants.py。
    """
    if not found_addresses:
        print("\nℹ️ 未发现新地址，无需更新文件。")
        return

    print(f"\n🔄 发现 {len(found_addresses)} 个新地址，正在更新地址文件...")

    # 1. 更新 constants.py
    try:
        with open(CONSTANTS_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        last_bracket_index = content.rfind(']')
        if last_bracket_index == -1:
            raise ValueError("在 constants.py 中未找到列表的结束符号 ']'。")

        # 格式化要添加的新地址字符串
        new_addresses_str = f",\n\n    # --- {datetime.now().strftime('%Y-%m-%d')} 新发现的地址 ---\n"
        for i, addr in enumerate(sorted(found_addresses)):
            if i % 8 == 0:
                new_addresses_str += "    "
            new_addresses_str += f"0x{addr:04X}, "
            if (i + 1) % 8 == 0 and i < len(found_addresses) - 1:
                new_addresses_str += "\n"
        
        # 插入新地址
        updated_content = content[:last_bracket_index] + new_addresses_str.rstrip(", ") + "\n]"

        with open(CONSTANTS_PATH, "w", encoding="utf-8") as f:
            f.write(updated_content)
            
        print(f"✅ 'constants.py' 已更新，添加了 {len(found_addresses)} 个新地址。")
    except Exception as e:
        print(f"❌ 更新 'constants.py' 失败: {e}")

    # 2. 更新 zero_addresses.py
    try:
        # 从零值列表中移除已找到的地址
        remaining_zeroes = sorted(list(set(all_zero_addresses) - set(found_addresses)))
        
        with open(ZERO_ADDRESSES_PATH, "w", encoding="utf-8") as f:
            f.write("ZERO_ADDRESSES = [\n")
            for i, addr in enumerate(remaining_zeroes):
                if i > 0 and i % 8 == 0:
                    f.write("\n")
                if i % 8 == 0:
                    f.write("    ")
                f.write(f"0x{addr:04X}, ")
            f.write("\n]\n")
        print(f"✅ 'zero_addresses.py' 已更新，移除了 {len(found_addresses)} 个地址。")
    except Exception as e:
        print(f"❌ 更新 'zero_addresses.py' 失败: {e}")


def main():
    client = utils.get_client()

    # --- 阶段1: 扫描高优先级地址 ---
    priority_filename = os.path.join(PROJECT_ROOT, "priority_scan_result.txt")
    print(f"📋 [阶段1] 正在扫描 {len(PRIORITY_ADDRESSES)} 个高优先级地址...")
    
    start_time_dt = datetime.now()
    with open(priority_filename, "w", encoding="utf-8") as f:
        f.write(f"扫描开始时间: {start_time_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
        header = f"{'地址':<8} | {'Raw':<6} | {'Signed':<7} | {'/10':<8} | {'/100':<8}\n"
        f.write("-" * 75 + "\n" + header + "-" * 75 + "\n")
        
        utils.print_header()

        for addr in PRIORITY_ADDRESSES:
            try:
                val = client.read_holding_registers(addr, 1)[0]
                s_val = utils.signed(val)
                line = f"0x{addr:04X}   | {val:<6} | {s_val:<7} | {s_val / 10:<8} | {s_val / 100:<8}\n"
                f.write(line)
                # 即使是0也打印
                utils.print_record(addr, val)
            except Exception:
                pass

        f.write(f"\n扫描结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✅ [阶段1] 扫描完成, 结果已保存至: {priority_filename}")
    print("-" * 75)

    # --- 阶段2: 扫描零值地址 ---
    zero_filename = os.path.join(PROJECT_ROOT, "zero_scan_result.txt")
    print(f"📋 [阶段2] 正在扫描 {len(ZERO_ADDRESSES)} 个零值地址...")
    print(f"⏳ 超时设置: {SEARCH_TIMEOUT}秒")
    
    start_time_dt_zero = datetime.now()
    found_addresses = []

    with open(zero_filename, "w", encoding="utf-8") as f:
        f.write(f"扫描开始时间: {start_time_dt_zero.strftime('%Y-%m-%d %H:%M:%S')}\n")
        header = f"{'地址':<8} | {'Raw':<6} | {'Signed':<7} | {'/10':<8} | {'/100':<8}\n"
        f.write("-" * 75 + "\n" + header + "-" * 75 + "\n")
        
        utils.print_header()
        start_time_timeout = time.time()

        for addr in ZERO_ADDRESSES:
            if time.time() - start_time_timeout > SEARCH_TIMEOUT:
                print(f"\n🛑 扫描超时! 已运行 {time.time() - start_time_timeout:.1f} 秒。")
                break
            try:
                val = client.read_holding_registers(addr, 1)[0]
                if val != 0:
                    found_addresses.append(addr)
                    s_val = utils.signed(val)
                    line = f"0x{addr:04X}   | {val:<6} | {s_val:<7} | {s_val / 10:<8} | {s_val / 100:<8}\n"
                    f.write(line)
                    utils.print_record(addr, val, prefix="🔥 新发现!")
            except Exception:
                pass

        f.write(f"\n扫描结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"共发现 {len(found_addresses)} 个新地址。\n")

    print(f"✅ [阶段2] 扫描完成, 结果已保存至: {zero_filename}")
    
    # --- 阶段3: 更新地址文件 ---
    update_address_files(found_addresses, ZERO_ADDRESSES)

    print("\n✅ 程序运行结束。")

if __name__ == "__main__":
    main()
