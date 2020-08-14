# 在 AWS 上实现无服务器视频字幕自动翻译架构

## 简介
随着媒体行业的全球化发展，越来越多的用户（包括企业和个人）都会有视频字幕的自动化翻译的需求。本文使用Amazon S3作为视频和字幕文件的存储，使用 Amazon Translate 实现了字幕的机器翻译，并且使用Amazon Lambda来调用 Amazon Translate 构建了一套无服务器的视频字幕翻译架构。利用本文实现的方案，您只需要将视频和字幕文件上传至Amazon S3，就可以自动获得翻译后的视频和字幕文件。

## 整体架构
![image](https://github.com/nwcd-samples/ServerlessSubtitleTranslation/blob/master/Translate_Lambda.png)

1. 用户上传视频和原语言的SRT格式的字幕文件到 S3 存储桶；
2. 监测到 S3 存储桶的事件变化（put object操作），自动触发执行 Lambda 函数；
3. Lambda 函数调用 Translate 服务对字幕文件的内容进行翻译；
4. Lambda 函数集成翻译结果形成一个目标语言的 SRT 字幕文件；
5. Lambda 函数将新的字幕文件上传到S3存储桶；
6. 用户可以利用原来的视频文件和目标语言的 SRT 字幕文件

## 构建步骤
1.创建S3存储桶
2.创建 IAM 角色
3.创建Lambda函数
4.配置Lambda触发条件
5. Lambda内存和超时配置
6.导入Lambda函数
7.测试

具体参考博客：https://amazonaws-china.com/cn/blogs/china/realize-serverless-video-subtitle-automatic-translation-architecture-on-aws/