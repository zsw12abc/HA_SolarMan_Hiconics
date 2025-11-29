# HA SolarMan Hiconics

用于 SolarMan/Hiconics 逆变器的 Home Assistant 集成工具。

## 目标 (Goal)

本项目的核心目标是创建一个 Python 脚本，用于生成 Home Assistant 的 `custom_hiconics.yaml` 配置文件，以便 Solarman 插件能够读取和展示逆变器的各项关键数据。

需要实现以下功能：

1.  **数据匹配**: 分析用户提供的设备运行截图和通过 Python 脚本获取的原始 Modbus 数据（包含地址和数值）。
2.  **地址映射**: 将截图中显示的以下关键信息与脚本返回的具体 Modbus 地址进行智能匹配：
    *   光伏发电功率 (PV generation power)
    *   电池电量 (Battery SOC)
    *   电池充放电功率 (Battery charge/discharge power)
    *   电网输电并电功率 (Grid power)
    *   家庭用电功率 (Home consumption power)
    *   今日总用电量 (Total consumption today)
    *   今日总发电量 (Total generation today)
    *   今日并电量 (Grid feed-in today)
    *   今日购电量 (Grid import today)
    *   今日充电量 (Battery charge today)
    *   今日放电量 (Battery discharge today)
3.  **YAML 生成**: 根据成功匹配的地址，生成格式正确的 `custom_hiconics.yaml` 文件。

## 项目结构

```
.
├── .gitignore
├── .venv/
├── Info.md
├── README.md
├── requirements.txt
├── scan_result.txt
├── scripts/
│   ├── hiconics_full_scan.py
│   ├── scan_result.py
│   └── search_address.py
└── src/
    ├── config.py
    ├── constants.py
    └── utils.py
```

## 安装

1.  **创建并激活虚拟环境**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # on Windows, use `.venv\Scripts\activate`
    ```

2.  **安装依赖**

    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

### 1. 扫描逆变器数据 (可选)

你可以运行 `scripts` 目录下的扫描脚本来获取逆变器的数据。

*   **`hiconics_full_scan.py`**: 扫描已知和未知的地址。
*   **`search_address.py`**: 在指定范围内扫描地址。
*   **`scan_result.py`**: 全量扫描地址并将结果保存到 `scan_result.txt`。

例如，运行 `hiconics_full_scan.py`:

```bash
python scripts/hiconics_full_scan.py
```

### 2. 生成 `custom_hiconics.yaml`

(此功能待开发)

当脚本开发完成后，你将可以通过以下方式运行：

```bash
python scripts/generate_yaml.py --scan-file <scan_result.txt> --screenshot <screenshot.png>
```

脚本会自动分析输入文件，匹配数据并生成 `custom_hiconics.yaml`。