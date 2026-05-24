# VNA Touchstone S参数批量诊断报告生成

这个目录是VNA数据后处理工具的起始代码。要做的事很直接：读一批Touchstone .s1p/.s2p文件，把每个文件的端口数、频率范围、S参数诊断指标整理成统一JSON。

公开样本在environment/data/public_touchstone里，都是本题自建样本，覆盖一端口匹配件、两端口滤波路径、传输线和夹具损耗。文件格式故意没有写成同一个模板：GHz/MHz/Hz单位、RI/MA/DB复数表示、行内注释、拆行记录、点数和频段都会变。

主要看instruction.md和src/rfdiag/analyze.py。起始实现能跑，但只做了很少的基础解析。后面要补Touchstone解析、S参数复数转换、一端口S11诊断、两端口传输指标、相位展开、群时延和无源性相关统计。

几个文件先认一下：

1. instruction.md，具体任务说明。
2. run_report.py，命令行入口。
3. src/rfdiag/analyze.py，主要修改位置。
4. environment/data/public_touchstone，公开开发样本。
5. docs/DATA_PROVENANCE.txt，自建数据说明。

先跑公开样本，看入口和JSON写出是否正常：

```bash
python3 run_report.py --input-dir environment/data/public_touchstone --output output/report.json
```

后续会换一批同源样本检查，不会只看这几个公开文件。实现时别依赖文件名、点数或固定频段。
