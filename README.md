# VNA Touchstone S参数批量诊断报告生成

这个仓库放的是一个射频测量后处理小项目：给定一批VNA导出的Touchstone文件，补全Python脚本，生成统一的S参数诊断报告。

仓库里的.s1p和.s2p样本是我们自己生成和整理的。样本覆盖一端口匹配件、两端口传输线、滤波路径等常见场景，也刻意保留了Touchstone文件里容易写错的地方，比如GHz/MHz单位、RI/MA/DB三种复数表示、行内注释、拆行记录和不同点数。

公开版仓库只保留对外可看的内容：

1. `instruction.md`：任务说明。
2. `environment/data/public_touchstone/`：公开Touchstone样本。
3. `src/rfdiag/analyze.py`：可运行的基础实现，目前只做元数据解析，完整诊断指标留给任务实现。
4. `run_report.py`：命令行入口。
5. `docs/DATA_PROVENANCE.txt`：数据说明。

公开仓库只保留说明、公开样本和基础代码。

本地运行：

```bash
python3 run_report.py --input-dir environment/data/public_touchstone --output output/report.json
```

输出文件是`output/report.json`，结构为`schema_version`和按文件名组织的`files`字段。当前公开版能先读出端口数、频率单位、数据格式、参考阻抗和频率范围。完整任务里还要继续补一端口的S11、return loss、VSWR、-10dB带宽，以及两端口的S21/S12/S11/S22、互易性、相位展开、群时延和power balance等指标。
