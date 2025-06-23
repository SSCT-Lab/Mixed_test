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

