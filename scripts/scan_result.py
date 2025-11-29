import sys
import os

# 将项目根目录添加到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pysolarmanv5 import PySolarmanV5
from src import config, utils

# ================= 配置区域 =================
# 扫描范围: 0x0000 - 0x5000 (覆盖所有可能区域)
START_ADDR = 0x0000
END_ADDR = 0x5000

# 批量读取大小 (越大越快，但如果设备响应慢容易报错)
BLOCK_SIZE = 100

# 结果保存文件名
OUTPUT_FILE = "scan_result.txt"


# ===========================================

def log(message, file_handle):
    """同时打印到屏幕和写入文件"""
    print(message)
    file_handle.write(message + "\n")
    file_handle.flush()


def main():
    # 打开文件准备写入
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        log(f"🚀 连接设备: {config.IP}...", f)

        try:
            client = PySolarmanV5(config.IP, config.SN, port=config.PORT, mb_slave_id=config.SLAVE_ID, verbose=False)
        except Exception as e:
            log(f"❌ 连接失败: {e}", f)
            return

        log(f"📋 开始全量扫描: 0x{START_ADDR:04X} - 0x{END_ADDR:04X}", f)
        log("-" * 80, f)
        log(f"{ '地址':<8} | {'Raw':<6} | {'Signed':<7} | {'/10':<8} | {'/100':<8}", f)
        log("-" * 80, f)

        current = START_ADDR
        valid_count = 0

        while current < END_ADDR:
            count = min(BLOCK_SIZE, END_ADDR - current)
            scan_success = False

            # 1. 尝试【批量】读取 (高速)
            try:
                values = client.read_holding_registers(current, count)
                for i, val in enumerate(values):
                    addr = current + i
                    s_val = utils.signed(val)

                    # 计算比例
                    v_10 = round(s_val / 10, 1)
                    v_100 = round(s_val / 100, 2)

                    # 记录每一行数据
                    log(f"0x{addr:04X}   | {val:<6} | {s_val:<7} | {v_10:<8} | {v_100:<8}", f)
                    valid_count += 1
                scan_success = True

            except Exception:
                # 批量读取失败，说明这一段里可能有空地址，不做处理，交给下面单点扫描
                pass

            # 2. 如果批量失败，切换【单点】读取 (补漏)
            if not scan_success:
                for i in range(count):
                    single_addr = current + i
                    try:
                        val_list = client.read_holding_registers(single_addr, 1)
                        val = val_list[0]
                        s_val = utils.signed(val)

                        v_10 = round(s_val / 10, 1)
                        v_100 = round(s_val / 100, 2)

                        log(f"0x{single_addr:04X}   | {val:<6} | {s_val:<7} | {v_10:<8} | {v_100:<8}", f)
                        valid_count += 1
                    except:
                        pass  # 确实读不到的空地址，直接跳过

            current += count

            # 进度提示
            if current % 1000 == 0:
                print(f"--- 进度: 已处理至 0x{current:04X} ---")

        log("-" * 80, f)
        log(f"✅ 扫描完成。共获取 {valid_count} 个有效数据点。", f)
        log(f"📁 结果已保存至: {OUTPUT_FILE}", f)


if __name__ == "__main__":
    main()
