#!/bin/bash
# 每天早上9点检查Dual Thrust信号

cd ~/quant-strategy/strategies/momentum

# 激活虚拟环境并运行
source ~/quant-strategy/venv/bin/activate
python3 dual_thrust_live.py >> ~/quant-strategy/logs/dual_thrust_$(date +\%Y\%m\%d).log 2>&1

# 如果有信号变化，可以发送通知（需要配置）
