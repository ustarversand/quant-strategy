#!/bin/bash
# 每天收盘前(14:30)运行杨永兴十步法监控

cd ~/quant-strategy/short-term

# 激活虚拟环境
source ~/quant-strategy/venv/bin/activate

# 运行监控
python3 yang_yongxing_enhanced.py >> ~/quant-strategy/logs/yang_yongxing_$(date +\%Y\%m\%d).log 2>&1

# 输出结果
echo "--- 监控完成 $(date) ---"
