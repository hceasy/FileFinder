#!/usr/bin/env python
# coding=UTF-8
'''
@Description: 文件查找
@Author: hceasy
LastEditors: hceasy
@Date: 2020-11-20 15:22:39
LastEditTime: 2020-11-20 18:31:51
'''
# -*- coding: utf-8 -*-
import sys
import os
import time
import datetime
import json

htmlTemplate = '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>File finder</title><meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1"><meta name="viewport"        content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no"><script src="https://cdn.bootcdn.net/ajax/libs/vue/2.6.12/vue.min.js"></script><link rel="stylesheet" href="https://cdn.bootcdn.net/ajax/libs/element-ui/2.14.0/theme-chalk/index.min.css"><script src="https://cdn.bootcdn.net/ajax/libs/element-ui/2.14.0/index.min.js"></script></head><body><div id="app"><el-card class="box-card"><div slot="header" class="clearfix"><el-row><el-col :span="18"><span>File finder</span></el-col><el-col :span="6"><el-input v-model="searchTxt" size="mini" placeholder="请输入文件名称"></el-input></el-col></el-row></div><el-table size="mini" v-if="searchTxt.length > 0" stripe :data="targetFiles" style="width: 100%"><el-table-column prop="fileName" label="文件名"></el-table-column><el-table-column prop="createDate" label="创建日期"></el-table-column><el-table-column prop="fileSrc" label="位置"></el-table-column><el-table-column label="操作"><template slot-scope="scope"><el-button size="mini" @click="window.open(scope.row.fileSrc)">下载</el-button></template></el-table-column></el-table><el-table size="mini" v-else stripe :data="files" style="width: 100%"><el-table-column prop="fileName" label="文件名"></el-table-column><el-table-column prop="createDate" label="创建日期"></el-table-column><el-table-column prop="fileSrc" label="位置"></el-table-column><el-table-column label="操作"><template slot-scope="scope"><el-button size="mini" @click="window.open(scope.row.fileSrc)">下载</el-button></template></el-table-column></el-table></el-card></div></body><script>    new Vue({        el: "#app",        data: {            files: $files,            targetFiles: [],            searchTxt: ""        },        methods: {        },        mounted() {        },        watch: {            searchTxt: function (val, oldVal) {                const _that = this;                _that.targetFiles = [];                _that.files.forEach(file => {                    if (file.fileSrc.search(val) > -1) {                        _that.targetFiles.push(file);                    }                });            }        },    })</script><style></style></html>'

dir = 'C:\\Users\\xxx\\Desktop'  # 目标目录
out = 'C:\\Users\\xxx\\Desktop\\index2.html' # 生成文件地址
cut = 'C:\\' # 需要替换的路径
rep = 'file://' # 替换为   C:\\xxx\xxx.dat => file:\\xxx\xxx.dat

def main():
    files = os.walk(dir)
    filesMap = []
    filesJson = ''
    for path,dir_list,file_list in files:
        for file_name in file_list:
            # print(os.path.join(path, file_name) )
            filePath = os.path.join(path, file_name)
            fileCreateDate =time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(os.path.getctime(filePath)))
            file = {'fileName': file_name, 'createDate': fileCreateDate, 'fileSrc': filePath.replace(cut,rep).replace('\\','/')}
            filesMap.append(file)
    filesJson = json.dumps(filesMap)
    html = htmlTemplate.replace('$files',filesJson)
    f = open(out,'w',encoding="utf-8")
    f.write(html)
    f.close()


if __name__ == "__main__":
   main()