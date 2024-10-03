import paddle
paddle.enable_static()
import jieba
import requests
from bs4 import BeautifulSoup
import re
jieba.enable_paddle()
# 假设这是用户输入的诗句
user_poem = input("请输入需要处理的诗句：")
# 使用jieba进行分词
words = jieba.cut(user_poem, cut_all=True)  # 使用lcut可以直接得到列表

# 存储查询结果的字典
query_results = {}

# 假设每个词对应的查询页面的URL
query_url = "https://www.gushiwen.cn/shiwenv_bb008be421f3.aspx"  # 示例URL, 需要替换为真实可查询的URL

try:
    # 发送HTTP GET请求并获取页面内容（HTML）
    response = requests.get(query_url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析HTML页面内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找包含译文和注释的div
        annotation_div = soup.find('div', class_='contyishang')

        if annotation_div:
            # 提取所有的段落<p>
            paragraphs = annotation_div.find_all('p')

            # 初始化注释文本
            full_annotation = ""

            # 查找包含“注释”的段落
            for paragraph in paragraphs:
                if "注释" in paragraph.get_text():
                    full_annotation = paragraph.get_text(strip=True)
                    break  # 找到后退出循环

            # 清除拼音部分
            cleaned_annotation = re.sub(r'（.*?）', '', full_annotation)  # 去掉所有拼音部分

            # 调试输出

            # 处理每个词并查找相关注释
            for word in words:
                if word in cleaned_annotation:
                    # 使用正则表达式查找与词语相关的句子
                    pattern = re.compile(rf'{word}[^。]*')  # 匹配词语后直到句号
                    match = pattern.search(cleaned_annotation)

                    if match:
                        annotation = match.group(0).strip()  # 提取与词相关的句子
                    else:
                        annotation = '无相关注释信息'
                else:
                    annotation = '无相关注释信息'

                # 将查询结果存储到字典中
                query_results[word] = annotation

        else:
            print("未找到注释部分")

    else:
        print(f"查询失败，状态码：{response.status_code}")

except Exception as e:
    print(f"请求或解析时发生错误: {e}")

# 打印查询结果
for word, annotation in query_results.items():
    if word not in ["，", "。", "！", "？"]:  # 过滤掉标点符号
        print(f"词语: {word}, 注释: {annotation}")







