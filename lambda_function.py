import json
import boto3
import os


s3_client = boto3.client('s3')
translate_client = boto3.client('translate')

sourceLanguageCode = "zh"
targetLanguageCode = "en"


# 读取srt格式的字幕文件
def read_srt(filename):
    id_list = []
    time_list = []
    subtitles_list = []
    with open(filename, encoding='utf-8') as srt_file:
        content = srt_file.read()
        content_split = content.split("\n\n")
        # print(content_split)
        for one_content in content_split:
            if one_content != '':
                id_list.append(one_content.split("\n")[0])
                time_list.append(one_content.split("\n")[1])
                subtitles_list.append(one_content.split("\n")[2])
    return id_list, time_list, subtitles_list

# 调用Amazan Translate进行翻译
def translate_text(text, sourceLanguageCode, targetLanguageCode):
    response1 = translate_client.translate_text(
        Text = text,
        SourceLanguageCode = sourceLanguageCode,
        TargetLanguageCode = targetLanguageCode
    )
    translation_text = response1['TranslatedText']
    return translation_text

# 翻译字幕列表
def translate_subtitles(subtitles_list, sourceLanguageCode, targetLanguageCode):
    translate_subtitles_list = []
    for subtitle in subtitles_list:
        translated_subtitle = translate_text(subtitle,sourceLanguageCode, targetLanguageCode)
        translate_subtitles_list.append(translated_subtitle)

    return translate_subtitles_list

# 生成srt字幕文件
def get_translated_srt_content(id_list, time_list, translate_subtitles_list):
    result = ""
    for i in range(len(id_list)):
        result = result + id_list[i] + "\n" + time_list[i] + "\n" + translate_subtitles_list[i] + "\n\n"
    return result


#lambda entry point
def lambda_handler(event, context):
    region = os.environ['AWS_DEFAULT_REGION']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    sourceS3Key = event['Records'][0]['s3']['object']['key']

    # 下载S3的字幕文件到本地
    input_file_name = sourceS3Key.split("/")[-1]
    local_input_file = "/tmp/" + input_file_name
    s3_client.download_file(bucket_name, sourceS3Key, local_input_file)
    
    # 读取字幕文件的内容
    id_list, time_list, subtitles_list = read_srt(local_input_file)
    
    # 对字幕进行翻译
    translate_subtitles_list = translate_subtitles(subtitles_list, sourceLanguageCode, targetLanguageCode)
    
    # 把翻译的结果集成到srt字幕文件里
    result = get_translated_srt_content(id_list, time_list, translate_subtitles_list)

    # 上传文件到S3
    output_filename = "translated_" + input_file_name
    outputS3Key = "output/translated-subtitles/" + output_filename
    s3_client.put_object(Body=result, Bucket=bucket_name, Key=outputS3Key)
    # s3_client.upload_file(local_file, bucket_name, outputS3Key)
    
    # 删除下载的临时文件
    os.remove(local_input_file)
    
    return {
        'statusCode': 200,
        'body': json.dumps('process complete')
    }
