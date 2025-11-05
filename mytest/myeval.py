##!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   myeval.py
@Time    :   2025/11/04 15:15:49
@Author  :   wlj 
'''

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from myutils.yml_utils import yaml_load, write_yaml
from argparse import Namespace
from lm_eval.__main__ import cli_evaluate
from myutils.write_xlsx import write_xlsx_eval_preface, set_style, write_llm_content
from openpyxl import Workbook
from myutils.log import logger
from myutils.file_utils import read_json, get_subfolder, get_exclude_list

config_path = "./mytest/test_config.yml"


'''
该脚本与位于/path/to/lm-evaluation-harness-main/lm_eval/__main__.py脚本的区别是：
将参数写进yml配置文件中，并将结果整合进一个excel文件中，其它算法和代码完全相同

'''
if __name__ == '__main__':

    # ====================== write out ====================== 
    workbook = Workbook()
    # 删除默认生成的 "Sheet" 表格
    default_sheet = workbook['Sheet']
    workbook.remove(default_sheet)
    style = set_style("style", bold=False,italic=False, horizontal='left')
    mysheet = workbook.create_sheet(title="Qwen performance")  
    mysheet, rows = write_xlsx_eval_preface(mysheet, style, start_row=1, max_column=14)
    
    save_xlsx_path = "./docs/acc.xlsx"

    
    # ====================== get all models ====================== 
    # pretrained_path = "/data/wlj/pretrained/Qwen"
    # model_list = get_subfolder(pretrained_path)

    # # exclude_list = ['Qwen3-1.7B', 'Qwen3-4B', 'Qwen3-30B']
    # exclude_list = ['Qwen3-30B']
    # model_list = get_exclude_list(model_list, exclude_list, exclude_flag=True)
    # # model_list = ['Qwen3-0.6B', 'Qwen3-1.7B', 'Qwen3-30B-A3B-Instruct-2507', 'Qwen3-30B-A3B-Instruct-2507-FP8', 
    # #               'Qwen3-30B-A3B-Thinking-2507', 'Qwen3-30B-A3B-Thinking-2507-FP8', 
    # #               'Qwen3-4B-Instruct-2507', 'Qwen3-4B-Instruct-2507-FP8', 
    # #               'Qwen3-4B-Thinking-2507', 'Qwen3-4B-Thinking-2507-FP8']
    # print(model_list)
    model_list = ['Qwen3-0.6B', 
                  'Qwen3-1.7B', 
                #   'Qwen3-4B-Instruct-2507', 'Qwen3-4B-Instruct-2507-FP8',
                #   'Qwen3-4B-Thinking-2507', 'Qwen3-4B-Thinking-2507-FP8'
                  ]
    model_root_path = [
                       '/data/wlj/pretrained/Qwen', #"hf"
                       '/data/wlj/pretrained/Qwen', #"vlm"
                       '/data/wlj/pretrained/Qwen', #"vlm FP8"
                       '/data/wlj/pretrained/Qwen_quantize-awq-sym',# "vllm AWQ"
                       ]
    model = [
             "hf", 
             "vllm", 
             "vllm", 
             "vllm",
            ]
    

    for j, model_root in enumerate(model_root_path):
        for i, model_name in enumerate(model_list):
            
            # 读进来，更新，写出去
            conifgs = yaml_load(config_path)
            conifgs['model'] = model[j]
            if j == 2:
                conifgs['model_args'] = f"pretrained={os.path.join(model_root, model_name)},quantization=fp8,dtype=bfloat16,gpu_memory_utilization=0.8"
            else:
                conifgs['model_args'] = f"pretrained={os.path.join(model_root, model_name)}"
            write_yaml(config_path, conifgs)
        
            # ====================== get configs ====================== 
            conifgs = yaml_load(config_path)
            # 将一个字典（dict）转换为 Namespace，使其可以像命令行参数一样通过点号访问（如 args.model）
            args = Namespace(**conifgs)
            print(args)

            # ====================== inference ====================== 
            start_time = time.time()
            results = cli_evaluate(args)
            for k,v in results.items():
                print(k, v)
            end_time = time.time()
            elaspe = "%.2fS" % (end_time - start_time)
            results['results'][args.tasks]['runtime'] = elaspe #注意只能单个数据集跑

            write_llm_content(mysheet, style, results, row=rows+1 + i, col=3 + j * 3)


    workbook.save(save_xlsx_path)  
    logger.info("save results to %s" % save_xlsx_path) 