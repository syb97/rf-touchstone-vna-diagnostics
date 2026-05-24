实验室这边记录了一批VNA导出的Touchstone文件，先放了4个公开样本在environment/data/public_touchstone里。里面有一端口匹配件，也有两端口传输线和滤波路径。这里有点麻烦的地方不是文件多，而是他们导出格式都不统一：GHz/MHz/Hz单位、RI/MA/DB三种写法、行内注释、拆行记录、点数和频段都不统一，会变。现在工具只够扫一点文件头，后面的RF诊断还没补上，我需要你把这块补上去。

主要看一下src/rfdiag/analyze.py就行。run_report.py这个入口py文件先别改，还是这样跑：

python run_report.py --input-dir <目录> --output output/report.json

输出写到output/report.json这个json文件中。顶层schema_version填rfdiag.v1，files下面按文件名放每个Touchstone文件的结果。公开样本可以反复跑，用来对字段和数量级；后面会换另一批同源文件检查，不会只看这4个公开样本。

先把解析做好了。Touchstone选项行、频率单位、数据格式、参考阻抗、端口数和复数S参数都要读对。基础字段这几个key名跟我写的后面的脚本对上就行：n_ports、n_points、frequency_unit、data_format、reference_ohm、freq_start_hz、freq_stop_hz、monotonic_frequency。

一端口文件主要看S11。dB值要给最小、最大、均值、中位数、10分位、90分位和标准差，最小/最大点对应的频率也要带上。还要算S11幅度均值和最大值、最好/最差return loss、低于-10dB的连续频段数、点数、起止频率和带宽，以及VSWR的最小、最大、中位数。没有低于-10dB的点时，带宽写0，起止频率写null。
两端口文件多看几个量。S21给均值、最小、最大、ripple、标准差和极值频率；S12给均值；再算S12/S21平均dB差、S11/S22最大dB和均值、互易误差最大值和均值。相位这块别直接拿跳变后的角度，要先展开S21相位，再给起点、终点、span，线性拟合群时延，以及相邻点差分群时延的均值、最小、最大、标准差。最后给max_power_balance和mean_power_balance，也要大致看一下无源性。

别联网，也别把公开文件的数值写死。后面会换目录、换文件名、换频段，也会用不同Touchstone表示方式。MA/DB/RI转换、端口矩阵顺序、相位展开、null和0这些地方一错，分数会掉得比较明显。先让公开样本跑出完整报告，再自己造几个小文件查边界。
