import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 获取配置，如果没有设置则报错或使用默认值
IP = os.getenv("SOLARMAN_IP")
SN = int(os.getenv("SOLARMAN_SN", 0))
PORT = int(os.getenv("SOLARMAN_PORT", 8899))
SLAVE_ID = int(os.getenv("SOLARMAN_SLAVE_ID", 1))

if not IP or not SN:
    raise ValueError("请在 .env 文件中配置 SOLARMAN_IP 和 SOLARMAN_SN")