整理好的Touchstone文件已经放在environment/data/public_touchstone里。现在这批数据里有一端口匹配件，也有两端口传输线和滤波路径，文件格式不完全一样：有GHz/MHz单位、RI/MA/DB表示、行内注释、拆行记录，还有不同点数和不同频段。你把这个小工具补完整，后面我会拿另一批同一套脚本生成但不公开的Touchstone文件跑同一套检查。

你要改的是src/rfdiag/analyze.py，入口保持python run_report.py --input-dir <目录> --output output/report.json可用。输出是一份JSON，schema_version写rfdiag.v1，files下面按文件名放每个Touchstone文件的诊断结果。公开数据可以自己反复跑，用来确认字段和数量级；另一批文件不会放在开发目录里。

每个文件先要正确解析Touchstone选项行、频率单位、数据格式、参考阻抗、端口数和复数S参数。基础字段包括n_ports、n_points、frequency_unit、data_format、reference_ohm、freq_start_hz、freq_stop_hz、monotonic_frequency。

一端口文件要给出S11相关指标：最小/最大/均值/中位数/10分位/90分位的dB值，最小和最大对应频率，S11幅度均值和最大值，最好/最差return loss，低于-10dB的连续频段数、点数、起止频率和带宽，VSWR的最小、最大和中位数。没有低于-10dB的点时，带宽给0，起止频率给null。

两端口文件要给出S21、S12、S11、S22和相位/群时延相关指标：S21的均值、最小、最大、ripple、标准差和极值频率，S12均值，S12/S21平均dB差，S11/S22最大dB和均值，互易误差最大值和均值，S21相位展开后的起点、终点、span，线性拟合群时延，以及相邻点差分群时延的均值、最小、最大、标准差。还要给max_power_balance和mean_power_balance，用来粗看无源性。

别联网，也别把公开文件的数值硬编码进去。测试这边会换目录跑，文件名和频段都可能变。解析失败、漏字段、把MA/DB/RI搞混、相位没展开、端口矩阵顺序弄错，都会直接掉分。建议先让公开样本全部能出完整报告，再做一些自己的小样本检查格式边界。
