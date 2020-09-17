<!--
 * @Author        : fineemb
 * @Github        : https://github.com/fineemb
 * @Description   : 
 * @Date          : 2020-08-26 16:20:12
 * @LastEditors   : fineemb
 * @LastEditTime  : 2020-09-17 19:22:49
-->

# 彩云天气

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

使用最新的v2.5彩云api, [自己去申请key](https://www.caiyunapp.com/dev_center/login.html)

模拟了官方天气的格式

在这个基础上,返回了彩云能够提供的所有数据.

配合此集成的[前端卡片](https://github.com/fineemb/lovelace-colorfulclouds-weather-card)

## 更新

+ ### v1.1
  + 支持前端UI配置
+ ### v1.2
  + 支持多个地点(设备)
  + 支持历史信息(比如昨天或前天天气情况)
  + 支持自定义天级预报和小时级预报的数量
+ ### v1.2.1
  + 修复预报数据获取的问题
  + 修复气压单位不对的问题
+ ### v1.2.2
  + 尝试修复 #1
+ ### v1.2.3
  + 修复百分比单位
  
## 安装配置

建议使用HACS安装和配置