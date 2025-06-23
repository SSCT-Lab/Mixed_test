import inspect

from pythonfuzz import tracer
from pythonfuzz.Coverages.LineCoverage import LineCoverage
from pythonfuzz.utils import htmlpaser
from pythonfuzz import config
import glob
import coverage
import numpy as np
import json
import subprocess
import shutil

global_pnac_map={}
class PNAC():
    def __init__(self) -> None:
        self.lineCoverage = LineCoverage()
    def get_PNAC(self, batch):
        cur_iter_nac_vec = None
        cur_iter_line_vector=None
        total_line_rate, total_1_count, total_1_and_0_count = 0,0,0

        model_path = '/media/lzq/D/lzq/pylot_test/pylot/dependencies/models/obstacle_detection/frozen_graph.pb'
        x_path = '/media/lzq/D/lzq/pylot_test/pylot/dependencies/models/obstacle_detection/x.npy'
        x_i_path = '/media/lzq/D/lzq/pylot_test/pylot/dependencies/models/obstacle_detection/x_i.npy'
        vec_path = '/media/lzq/D/lzq/pylot_test/pylot/dependencies/models/obstacle_detection/vec_i.json'
        x = np.load(x_path, allow_pickle=True)
        print('一共的批次：', batch)
        for i in range(batch):
            pattern1 = f'{config.COV_FILE_PATH}/.coverage.{i}*'
            pattern2 = f'{config.COV_FILE_PATH}/.coverage.main*'
            files1, files2 = glob.glob(pattern1), glob.glob(pattern2)
            files = files1 + files2
            # print('files', files)
            if not files:
                continue

            # 创建 Coverage 实例，指定输出合并后的 data_file
            # print(f'读取了第{i}轮的覆盖文件')
            cov = coverage.Coverage(data_file=f'.coverage.combined.{i}')
            cov.start()
            # cov.exclude('@coverage_decorator')
            # cov.exclude('def coverage_decorator')
            cov.stop()
            cov.save()
            # 合并这一组 data files
            cov.combine(data_paths=files, keep=True)
            # 生成 HTML 报告到目录 html_report_i
            cov.html_report(directory=f'html_report_{i}')
            total_line_rate, total_1_count, total_1_and_0_count, cur_seed_line_vector,_,cur_line_status_vector_map,_ = self.lineCoverage.get_line_coverage(f'html_report_{i}')
            # print('cur_seed_line_vector', cur_seed_line_vector)
            line_vec_sim = []
            for j in range(len(cur_seed_line_vector)):
                if cur_seed_line_vector[j]==1:
                    line_vec_sim.append(j)

            ### 计算整个迭代轮次中batch_size个图片的行覆盖：cur_iter_line_vec##############33
            if cur_iter_line_vector is None:
                cur_iter_line_vector = cur_seed_line_vector
            else:
                cur_iter_line_vector = [a | b for a, b in zip(cur_iter_line_vector, cur_seed_line_vector)]
            ################################################################
            # print(f'第{i}轮计算的行覆盖向量:{cur_iter_line_vector}')
            np.save(x_i_path, np.expand_dims(x[i], axis=0))
            subprocess.run(['python', '/media/lzq/D/lzq/pylot_test/pythonfuzz/pythonfuzz/Coverages/NacCoverage.py', '--model_path', model_path, '--data_path', x_i_path, '--vec_path', vec_path])

            with open(vec_path, 'r') as f:
                cur_seed_nac_vec = json.load(f)
            nac_rate = sum(cur_seed_nac_vec)/float(len(cur_seed_nac_vec))

            # 计算整个迭代轮次中batch_size个图片的nac：cur_iter_nac_vec#############################
            if cur_iter_nac_vec is None:
                cur_iter_nac_vec = cur_seed_nac_vec
            else:
                cur_iter_nac_vec = [a | b for a, b in zip(cur_iter_nac_vec, cur_seed_nac_vec)]
            ##################################################################################
            for key in cur_line_status_vector_map:
                cur_line_status_vector_map[key] = [x for x in cur_line_status_vector_map[key] if x != -1]
            for key in cur_line_status_vector_map:
                cur_line_status_vector_map[key] = [i for i, val in enumerate(cur_line_status_vector_map[key]) if val == 1]
            k = json.dumps(cur_line_status_vector_map, sort_keys=True)
            if k not in global_pnac_map.keys():
                global_pnac_map[k] = cur_seed_nac_vec
            else:
                global_pnac_map[k]=[a | b for a, b in zip(global_pnac_map[k], cur_seed_nac_vec)]
            shutil.rmtree(f'html_report_{i}')
            # print('global_pnac_map的长度', len(global_pnac_map))
        # print('cur_iter_line_vector',cur_iter_line_vector)
        cur_iter_line_cov = calculate_coverage(cur_iter_line_vector)
        
        one_pnac_rates=[]
        for nv in global_pnac_map.values():
            one_pnac_rates.append(sum(nv)/len(nv))

        pnac_rate = np.mean(one_pnac_rates)
        return global_pnac_map, pnac_rate,cur_iter_nac_vec, sum(cur_iter_nac_vec)/float(len(cur_iter_nac_vec)), total_line_rate, total_1_count, total_1_and_0_count, cur_iter_line_vector, cur_iter_line_cov
        ##返回 PNAC、 当前轮次batch_size个图片的nac、全部的行覆盖、当前轮次batch_size个图片的行覆盖


            
def calculate_coverage(function_vectors):
    total_1_count = 0  # 统计所有向量中1的总数
    total_1_and_0_count = 0  # 统计所有向量中1和0的总数

    # 遍历函数状态向量map
    for v in function_vectors:
        if v==1:
            total_1_count+=1
            total_1_and_0_count+=1
        elif v==0:
            total_1_and_0_count+=1

    # 计算覆盖率：1的总数 / (1和0的总数)
    if total_1_and_0_count == 0:
        return 0  # 避免除以0的情况
    coverage = total_1_count / total_1_and_0_count
    return coverage

