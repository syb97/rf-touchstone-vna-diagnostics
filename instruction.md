这批VNA导出的Touchstone样本放在environment/data/public_touchstone里。里面既有一端口匹配件，也有两端口传输线、滤波路径。文件不是一个模板倒出来的：GHz/MHz/Hz单位、RI/MA/DB三种写法、行内注释、拆行记录、点数和频段都会变。现在这个后处理工具只搭了个架子，你把它补到能批量出诊断报告。

主要改src/rfdiag/analyze.py。入口别改，仍然用：

python run_report.py --input-dir <目录> --output output/report.json

输出就写output/report.json。顶层schema_version填rfdiag.v1，files下面按文件名放每个Touchstone文件的结果。公开样本可以反复跑，用来对字段和数量级；我后面会换另一批同一套方式生成但不公开的文件检查，不会只看这4个公开样本。

解析先做扎实。每个文件都要读对Touchstone选项行、频率单位、数据格式、参考阻抗、端口数和复数S参数。基础字段这些key名要对上：n_ports、n_points、frequency_unit、data_format、reference_ohm、freq_start_hz、freq_stop_hz、monotonic_frequency。

一端口文件看S11。要算出S11的最小、最大、均值、中位数、10分位、90分位dB值，最小和最大对应的频率，S11幅度均值和最大值，最好/最差return loss，低于-10dB的连续频段数、点数、起止频率和带宽，还有VSWR的最小、最大和中位数。没有低于-10dB的点时，带宽写0，起止频率写null。

两端口文件多看几个量。S21要有均值、最小、最大、ripple、标准差和极值频率；S12要有均值；还要给S12/S21平均dB差、S11/S22最大dB和均值、互易误差最大值和均值。相位这块别直接拿跳变后的角度，要给S21相位展开后的起点、终点、span，线性拟合群时延，以及相邻点差分群时延的均值、最小、最大、标准差。最后再给max_power_balance和mean_power_balance，粗看一下无源性。

别联网，也别把公开文件的数值写死。测试这边会换目录、换文件名、换频段，也会用不同Touchstone表示方式。MA/DB/RI转换、端口矩阵顺序、相位展开、null和0这些地方一错，分数会掉得很明显。先让公开样本跑出完整报告，再自己造几个小文件查边界，会更稳。
