import sys
sys.path.append('/media/lzq/D/lzq/pylot_test/pylot')
sys.path.append('/media/lzq/D/lzq/pylot_test/pylot/pylot')
sys.path.append('/media/lzq/D/lzq/pylot_test/pythonfuzz')
sys.path.append('/media/lzq/D/lzq/pylot_test/pythonfuzz/PTtool')
sys.path.append('/media/lzq/D/lzq/pylot_test/pythonfuzz/ATS')

import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
from pythonfuzz.main import PythonFuzz
from pylot3 import run_pylot_with_flags
import pylot.flags
import random
import subprocess
import time
import multiprocessing as mp
import shutil
import coverage
config_path = '/media/lzq/D/lzq/pylot_test/pylot/configs/mpc2.conf'

def update_config(file_path, updates):
    # 读取配置文件内容
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for param_name, new_value in updates.items():
        found = False  # 标记参数是否在文件中找到
        for i in range(len(lines)):
            if lines[i] is not None and lines[i].startswith(param_name):
                found = True
                if new_value is False:
                    # 如果参数值为 False，删除该参数
                    lines[i] = None  # 标记为删除
                elif new_value is not True:
                    lines[i] = f"{param_name}={new_value}\n"
                break  # 找到后退出内层循环

        # 如果参数未找到且值为 True，则添加该参数
        if new_value is True and not found:
            lines.append(f"{param_name}\n")  # 添加参数行

    # 过滤掉标记为删除的行
    lines = [line for line in lines if line is not None]

    # 将更新后的内容写回文件
    with open(file_path, 'w') as file:
        file.writelines(lines)


@PythonFuzz
def fuzz_interface(imgs:list,y:list,planning_label:list,control_label:list,
                   perfect_depth_estimation:bool,
                   perfect_segmentation:bool, 
                   log_detector_output:bool,
                   log_lane_detection_camera:bool,log_traffic_light_detector_output:bool):
    import psutil
    import os
    import signal
    # print(visualize_detected_traffic_lights, visualize_rgb_camera)

    updates = {
    '--perfect_depth_estimation':perfect_depth_estimation,
    '--perfect_segmentation':perfect_segmentation,
    # '--planning_type':planning_type_enum,
    # '--simulator_mode':simulator_mode_enum,
    '--log_detector_output':log_detector_output,
    '--log_lane_detection_camera':log_lane_detection_camera,
    '--log_traffic_light_detector_output':log_traffic_light_detector_output

    }
    update_config(config_path, updates)
    time.sleep(2)
    traffic_light_path = '/home/lzq/experiment_datatset/inputs/obstacles'

    # 检查文件夹是否存在
    if os.path.exists(traffic_light_path):
        # 删除现有文件夹
        shutil.rmtree(traffic_light_path)
     # 创建新的文件夹
    os.makedirs(traffic_light_path)
    img_arrays = []
    for ind, img in enumerate(imgs):
        img = img.resize((1920, 1080))

        img.save(os.path.join(traffic_light_path, f'{ind}.png'))
        img_array = np.array(img)

        img_arrays.append(img_array)
    img_arrays = np.array(img_arrays)
    target_process = mp.Process(target=run_pylot_with_flags, args=(config_path,))

    # run_pylot_with_flags(config_path)
    target_process.start()
    target_process.join()
    

    return img_arrays




if __name__ == '__main__':
    fuzz_interface()



# def run_pylot_process(config_path, coverage_queue):
#     """在子进程中运行 run_pylot_with_flags 并收集覆盖率"""
#     try:
#         # 在子进程中启动覆盖率收集
#         child_cov = coverage.Coverage()
#         child_cov.start()
        
#         # 运行目标函数
#         run_pylot_with_flags(config_path)
        
#         # 停止覆盖率收集
#         child_cov.stop()
        
#         # 将覆盖率数据保存到临时文件
#         temp_file = f'coverage_{os.getpid()}.data'
#         child_cov.save(temp_file)
        
#         # 将临时文件路径发送到队列
#         coverage_queue.put(temp_file)
#    except Exception as e:
#         print(f"Error in child process: {e}")
#         coverage_queue.put(None)