<!--
 * @Author        : fineemb
 * @Github        : https://github.com/fineemb
 * @Description   : 
 * @Date          : 2020-08-26 16:20:12
 * @LastEditors   : fineemb
 * @LastEditTime  : 2021-04-08 18:45:28
-->

# 彩云天气

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

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
+ ### v1.2.4
  + 适配hass规范

+ ### v1.2.5
  + 修复配置页面错误 [#11](https://github.com/fineemb/Colorfulclouds-weather/issues/11)
+ ### v1.2.6
  + 适配HASS v2022.3+ [#21](https://github.com/fineemb/Colorfulclouds-weather/issues/21)
+ ### v1.2.7
  + 修复系统单位获取问题 [#32](https://github.com/fineemb/Colorfulclouds-weather/issues/32)
  + 极端天气预警修复 [#14](https://github.com/fineemb/Colorfulclouds-weather/issues/14)
+ ### v2.0.0
  + 重新适配更高版本的HASS [#52](https://github.com/fineemb/Colorfulclouds-weather/issues/52)
  [#47](https://github.com/fineemb/Colorfulclouds-weather/issues/47)
  [#50](https://github.com/fineemb/Colorfulclouds-weather/issues/50)
  [#51](https://github.com/fineemb/Colorfulclouds-weather/issues/51)
  [#49](https://github.com/fineemb/Colorfulclouds-weather/issues/49)
  [#48](https://github.com/fineemb/Colorfulclouds-weather/issues/48)
  [#46](https://github.com/fineemb/Colorfulclouds-weather/issues/46)
  [#45](https://github.com/fineemb/Colorfulclouds-weather/issues/45)
  + 天气预报和小时预报不再写入状态机,[前端卡片](https://github.com/fineemb/lovelace-colorfulclouds-weather-card)将会同步更新
+ ### v2.0.1
  + 修复因彩云api返回数据不完整导致的崩溃 [#53](https://github.com/fineemb/Colorfulclouds-weather/issues/53)
+ ### v2.0.2
  + 彩云api不返回分钟预报数据 [#54](https://github.com/fineemb/Colorfulclouds-weather/issues/54)
  + 添加自定义api请求间隔时间（默认是10分钟）
  
## 安装配置

建议使用HACS安装和配置
