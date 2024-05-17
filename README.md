# USMT-Helper

## 概述 / Overview:
USMT Helper 被设计为辅助用户使用USMT减轻负担，它侧重于迁移应用程序，但也会顺便迁移用户状态。  
The USMT Helper is designed to assist users in reducing the burden of using USMT. It focuses on migrating applications, but also migrates user states as a secondary function.  
它侧重于脱机迁移，主要应用场景为不能启动的Windows系统。  
It is primarily intended for offline migration, with the main application scenario being non-bootable Windows systems.  
它支持中英双语。  
It supports both Chinese and English.  

## 大体程序逻辑 / General Program Logic:
1. 自动设置语言。  
   Automatically set the language.  
2. 提供生成offline.xml所需信息。盘符等。  
   Provide the necessary information for generating offline.xml, such as drive letters.  
3. 生成offline.xml。  
   Generate offline.xml.  
4. 扫描脱机系统上所有应用程序。  
   Scan all applications on the offline system.  
5. 将应用程序保存到txt。  
   Save the applications to a txt file.  
6. 提示用户修改txt，保留需要迁移的并按回车继续。  
   Prompt the user to edit the txt file, keeping the applications to be migrated and pressing Enter to continue.  
7. 检查这些应用程序是否在当前电脑上存在，如果存在则输出到txt并打印一条简略的文本提示。  
   Check if these applications exist on the current computer; if they do, output them to a txt file and print a brief text prompt.  
8. 分别搜索这些应用程序的安装路径、用户数据、注册表项。  
   Search for the installation paths, user data, and registry entries of these applications.  
9. 依据搜索结果分别生成以应用程序命名的，用于迁移应用程序的USMT自定义xml文件。  
   Based on the search results, generate USMT custom XML files named after the applications for migration.  
10. 引导用户下一步操作。  
    Guide the user through the next steps.  
```