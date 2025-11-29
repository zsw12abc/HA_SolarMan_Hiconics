import sys
import os
import time
from datetime import datetime

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import utils
from src.constants import PRIORITY_ADDRESSES
from src.zero_addresses import ZERO_ADDRESSES

SEARCH_TIMEOUT = 300  # 搜索超时时间
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    client = utils.get_client()

    # --- 阶段1: 扫描高优先级地址 ---
    priority_filename = os.path.join(PROJECT_ROOT, "priority_scan_result.txt")
    print(f"📋 [阶段1] 正在扫描 {len(PRIORITY_ADDRESSES)} 个高优先级地址...")
    
    start_time_dt = datetime.now()
    with open(priority_filename, "w", encoding="utf-8") as f:
        f.write(f"扫描开始时间: {start_time_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        header = f"{'地址':<8} | {'Raw':<6} | {'Signed':<7} | {'/10':<8} | {'/100':<8}\n"
        f.write("-" * 75 + "\n")
        f.write(header)
        f.write("-" * 75 + "\n")
        
        utils.print_header()

        for addr in PRIORITY_ADDRESSES:
            try:
                val = client.read_holding_registers(addr, 1)[0]
                s_val = utils.signed(val)
                line = f"0x{addr:04X}   | {val:<6} | {s_val:<7} | {s_val / 10:<8} | {s_val / 100:<8}\n"
                f.write(line)
                utils.print_record(addr, val)
            except Exception:
                pass

        end_time_dt = datetime.now()
        f.write(f"\n扫描结束时间: {end_time_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"✅ [阶段1] 扫描完成, 结果已保存至: {priority_filename}")
    print("-" * 75)

    # --- 阶段2: 扫描零值地址 ---
    zero_filename = os.path.join(PROJECT_ROOT, "zero_scan_result.txt")
    print(f"📋 [阶段2] 正在扫描 {len(ZERO_ADDRESSES)} 个零值地址...")
    print(f"⏳ 超时设置: {SEARCH_TIMEOUT}秒")
    
    start_time_dt_zero = datetime.now()
    with open(zero_filename, "w", encoding="utf-8") as f:
        f.write(f"扫描开始时间: {start_time_dt_zero.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        header = f"{'地址':<8} | {'Raw':<6} | {'Signed':<7} | {'/10':<8} | {'/100':<8}\n"
        f.write("-" * 75 + "\n")
        f.write(header)
        f.write("-" * 75 + "\n")
        
        utils.print_header()

        start_time_timeout = time.time()
        found_count = 0

        for addr in ZERO_ADDRESSES:
            elapsed_time = time.time() - start_time_timeout
            if elapsed_time > SEARCH_TIMEOUT:
                print(f"\n🛑 扫描超时! 已运行 {elapsed_time:.1f} 秒。")
                break

            try:
                val = client.read_holding_registers(addr, 1)[0]
                if val != 0:
                    found_count += 1
                    s_val = utils.signed(val)
                    line = f"0x{addr:04X}   | {val:<6} | {s_val:<7} | {s_val / 10:<8} | {s_val / 100:<8}\n"
                    f.write(line)
                    utils.print_record(addr, val, prefix="🔥 新发现!")
            except Exception:
                pass

        end_time_dt_zero = datetime.now()
        f.write(f"\n扫描结束时间: {end_time_dt_zero.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"共发现 {found_count} 个新地址。\n")

    print(f"✅ [阶段2] 扫描完成, 结果已保存至: {zero_filename}")
    print("\n✅ 程序运行结束。")

if __name__ == "__main__":
    main()
