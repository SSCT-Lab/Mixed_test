# 项目结构

		|-- Mixed_test
	
		    |-- pylot
	
			|-- mutilprocess
	
			|-- pythonfuzz
	
				|-- PTtool 
	
				|-- ATS
	
				|-- traj-dist
	
				|-- pythonfuzz


# 配置
1. 百度网盘中dependencies目录是pylot的依赖模型等，需要放置在Mixed_test/pylot/目录下，如果不能直接使用请按照pylot/install.sh配置一下（一般情况是能直接用的）
2. 百度网盘中pylot38里面是conda环境

链接：https://pan.baidu.com/s/1Ly2E7sHaiBEZXhBqtVf9Qg 
提取码：0k9u

# 运行
要运行测试程序，需要在pylot目录下运行如下命令
```
conda activate pylot38
export PYLOT_HOME=`pwd`/
export CARLA_HOME=$PYLOT_HOME/dependencies/CARLA_0.9.10.1/
cd $PYLOT_HOME/scripts/
source ./set_pythonpath.sh
cd  $PYLOT_HOME/
python fuzz_list.py dirs seed_list2.txt --has-model True --use-nc True --batch-size 10
```
其中
    fuzz_list.py为接口函数，
    seed_list2.txt为种子配置文件，根据需要进行配置，需要与fuzz_list.py中接口函数的参数一一对应，
    has-model标识被测系统是否使用了智能模型，对于pylot的测试，has-model恒为True，
    use-nc标识模型覆盖率使用Pt还是神经元覆盖率，使用神经元覆盖率为True，使用Pt为False
    batch-size是指一次运行pylot使用多少个种子

## 种子说明
请在txt文件中指定初始种子，需要为被测接口函数的每个参数指定初始值在txt文件中，一个参数占一行，并且是 **key=value** 的形式。

pylot测试的种子文件示例如下：
```
imgs=/home/lzq/experiment_datatset/fuzz_test_dataset/town1/obstacles_dataset_datax
y=/home/lzq/experiment_datatset/fuzz_test_dataset/town1/obstacles_y.npy
planning_label=/home/lzq/experiment_datatset/fuzz_test_dataset/town1/plannings/town1_obstacle/planning_rs_label_y.npy
control_label=/home/lzq/experiment_datatset/fuzz_test_dataset/town1/controls/town1_obstacle/control_rs_label_y.npy
perfect_depth_estimation=False
perfect_segmentation=False
log_detector_output=False
log_lane_detection_camera=False
log_traffic_light_detector_output=False
```
其中图片文件夹命名必须以_datax结尾，在种子构建时，会依次取文件夹中的一个图像与其它参数构成种子；
对于标签类型的种子参数，参数名称请以y或者label结尾，在该项目中，感知模块标签命名为"y"，规划模块标签命名为"planning_label"，控制模块标签命名为"control_label"。

# 结果
1. 最终的实验结果信息被存于OUTPUT_DIR中，包含迭代轮次、行覆盖率、神经元覆盖率、Global Weight、Path-Neuron、系统错误、感知错误、规划错误、控制错误、感知输出ious、规划输出tdist、控制输出steer_diff、行覆盖向量、神经元覆盖向量、Path-Neuron覆盖map、行覆盖map等信息；
2. LOCAL_SEED_POOL 存储种子池中的变异种子；
3. ERROR_INFOS_DIR 记录每轮迭代的具体报错信息；
4. ERROR_SEEDS_VECTOR 记录报错轮次的覆盖向量；
5. COV_REPORT_PATH 记录代码行覆盖报告；
6. COV_HTML_PATH 记录代码行覆盖html报告详细信息；
7. CRASH_SEED_PATH、PREDICT_ERROR_SEED_PATH、PLANNING_ERROR_SEED_PATH、CONTROL_ERROR_SEED_PATH分别记录触发系统、感知、规划、控制错误的种子信息。

**以上地址变量均在pythonfuzz/pythonfuzz/config.py中设置**

8. tmp/error_result.py与tmp/coverage_result.py中根据OUTPUT_DIR中的实验结果画图。

