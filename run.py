#!/usr/bin/env python
# coding=UTF-8
'''
@Description: 文件查找
@Author: hceasy
LastEditors: hceasy
@Date: 2020-11-20 15:22:39
LastEditTime: 2021-08-04 10:05:08
'''
# -*- coding: utf-8 -*-
import sys
import os
import time
import datetime
import json
import argparse

htmlTemplate = '''
<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <title>File finder</title>
    <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
    <meta name="viewport"
        content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no">
    <!-- VUE -->
    <script src="https://cdn.jsdelivr.net/npm/vue@3.0.2/dist/vue.global.min.js"></script>
    <!-- element-ui 样式 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/element-plus@1.0.1-alpha.15/lib/theme-chalk/index.css">
    <!-- element-ui -->
    <script src="https://cdn.jsdelivr.net/npm/element-plus@1.0.1-alpha.15/lib/index.js"></script>
</head>

<body>
    <div id="app">

        <el-container>
            <el-header>
                <el-row>
                    <el-col :span="18">
                        <b>File finder</b>
                    </el-col>
                    <el-col :span="6">
                        <el-input v-model="searchTxt" size="mini" placeholder="请输入文件名称">
                            <template v-slot:append>
                                <el-button icon="el-icon-search" v-on:click="search"></el-button>
                            </template>
                        </el-input>
                    </el-col>
                </el-row>
                <el-row>
                    <i style="font-size: 12px;">Last update: {{updateTime}}</i>
                </el-row>
            </el-header>
            <el-container>
                <el-aside style="width: 200px;">
                    <el-card>
                        <div slot="header" class="clearfix">
                        </div>
                        <el-tree @node-click="fileFilter" style="overflow: auto;" :data="files"></el-tree>
                    </el-card>
                </el-aside>
                <el-main>
                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <el-row>

                                <el-breadcrumb separator="/">
                                    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
                                    <el-breadcrumb-item><a href="/">活动管理</a></el-breadcrumb-item>
                                    <el-breadcrumb-item>活动列表</el-breadcrumb-item>
                                    <el-breadcrumb-item>活动详情</el-breadcrumb-item>
                                </el-breadcrumb>
                            </el-row>
                        </div>
                        <el-table size="mini" stripe :data="targetFiles"
                            style="width: 100%">
                            <el-table-column prop="name" label="文件名">
                            </el-table-column>
                            <el-table-column prop="time" label="创建日期">
                            </el-table-column>
                            <el-table-column prop="size" label="文件大小">
                            </el-table-column>
                            <!-- <el-table-column prop="fileSrc" label="位置">
                            </el-table-column> -->
                            <!-- <el-table-column label="操作">
                                <template slot-scope="scope">
                                    <el-button size="mini" @click="window.open(scope.row.fileSrc)">下载</el-button>
                                </template>
                            </el-table-column> -->
                        </el-table>
                    </el-card>
                </el-main>
            </el-container>
        </el-container>

    </div>
</body>
<script>
    const App = {
        data() {
            return {
                updateTime: '2020-11-24 11:30:24',
                files:$filesJson, 
                targetFiles: [],
                searchTxt: ""
            }
        },
        methods: {
            search() {
                console.log(this.searchTxt)
            },
            fileFilter(data) {
                // data.files.forEach(file => {
                //     let obj = {
                //         name: file.name,
                //         size: file.size,
                //         time: file.time,
                //         src: file.src
                //     }
                //     this.targetFiles.push(obj)

                // });
                this.targetFiles = data.files
                // console.log(this.targetFiles)
            }
        }
    }
    Vue.createApp(App)
        .use(ElementPlus)
        .mount('#app')
</script>
<style>
    .el-main {
        padding: 5px 0px 5px 0;
    }

    .el-header {
        padding-top: 10px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
    }

    .el-aside {
        padding: 5px 5px 5px 0;
    }

    .el-tree>.el-tree-node {
        min-width: 100%;
        display: inline-block;
    }

    .clearfix:before,
    .clearfix:after {
        display: table;
        content: "";
    }

    .clearfix:after {
        clear: both
    }
</style>

</html>'''

DIR = ''
OUT = ''
cut = 'G:\\'  # 需要替换的路径
rep = 'file://'  # 替换为   C:\\xxx\xxx.dat => file:\\xxx\xxx.dat
floderTree = []

def main():
    global OUT,DIR
    parser = argparse.ArgumentParser(description="""
    File finder v0.0.1
    """)
    parser.add_argument("dir", help="folder")
    parser.add_argument("out", help="file out")
    args = parser.parse_args()
    DIR = args.dir
    OUT = args.out
    files = os.walk(DIR)
    flodersList = {}
    for path, dir_list, file_list in files:
        floder = []
        for file_name in file_list:
            # print(os.path.join(path, file_name))
            filePath = os.path.join(path, file_name)
            fileCreateDate = time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(os.path.getctime(filePath)))
            file = {
                    'label': file_name,
                    'createDate': fileCreateDate,
                    'fileSrc': filePath.replace(cut, rep).replace('\\', '/')
                    }
            floder.append(file)
        if(len(floder)>0):
            flodersList[path] = floder
    createFloderTreeList(flodersList)


def createFloderTreeList(flodersList):
    fileCache = []
    for floders in flodersList:
        floderPathArray = floders.split('\\')
        fileTree = {}
        for index in range(len(floderPathArray)):
            if(index == 0):
                fileTree = {
                        'label':floderPathArray[len(floderPathArray) - index - 1],
                        'children':flodersList[floders]
                        }
            else:
                fileTree = {
                        'label':floderPathArray[len(floderPathArray) - index - 1],
                        'children':[fileTree]
                        }
        fileCache.append(fileTree)
    createFloderTree(fileCache)

def createFloderTree(floderTreeList):
    while (len(floderTreeList)>0):
        nextFloder = floderTreeList.pop()
        treeCheck(floderTree,nextFloder)
    outPutFile(floderTree)

def treeCheck(targetTree,nextFloder):
    targetFloder = None
    for floder in targetTree:
        if(floder['label'] == nextFloder['label']):
            targetFloder = floder
            break 
    if (targetFloder is None):
        targetTree.append(nextFloder)
    else:
        if(('children' in nextFloder.keys()) & ('children' in targetFloder.keys())):
            if(len(nextFloder['children'])==0):
                targetFloder['children'].append(nextFloder)
            else:
                targetFloder = targetFloder['children']
                nextFloder = nextFloder['children'][0]
                treeCheck(targetFloder,nextFloder)
        elif('children' in nextFloder.keys()):
            targetFloder['children'] = [nextFloder]
        elif('children' in targetFloder.keys()):
            targetFloder['children'].append(nextFloder)

def outPutFile(floderTree):
    global OUT
    filesJson = json.dumps(floderTree)
    html = htmlTemplate.replace('$filesJson', filesJson)
    f = open(OUT, 'w', encoding="utf-8")
    f.write(html)
    f.close()



if __name__ == "__main__":
    main()
