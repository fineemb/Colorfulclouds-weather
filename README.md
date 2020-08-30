<!--
 * @Author        : fineemb
 * @Github        : https://github.com/fineemb
 * @Description   : 
 * @Date          : 2020-08-26 16:20:12
 * @LastEditors   : fineemb
 * @LastEditTime  : 2020-08-30 22:17:49
-->

# 彩云天气

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

使用最新的v2.5彩云api, [自己去申请key](https://www.caiyunapp.com/dev_center/login.html)

模拟了官方天气的格式

在这个基础上,返回了彩云能够提供的所有数据.

## 更新

+ v1.1
  + 支持前端UI配置
  
## 安装配置

```yaml
weather: 
  - platform: colorfulclouds
    api_key: !secret colorfulclouds_key  
    latitude: 31.55
    longitude: 121.09

```