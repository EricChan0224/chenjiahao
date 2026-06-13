import json
import os
from openai import OpenAI
import pdfplumber

# ==================== 配置区域 ====================
# 1. 填入你刚刚复制的阿里云百炼 API Key
MY_API_KEY = "sk-ws-H.REHLIYH.1ZuE.MEYCIQCLJzYZ73xJh3tBEvqenaLEkFmyE5pt_khEJjkAlZBaUgIhAJaSPHnYOGwN4ehs9J97JTcoeLQDubVgB_p89MlhDV5g" 

# 2. 指定你要读取的病例 PDF 文件名
PDF_FILE_NAME = "A case of portal vein recanalization and symptomatic heart failure.pdf"
# ==================================================

def extract_pdf_text(filepath):
    """第一步：把 PDF 里面的文字全部读取出来"""
    print(f"正在读取 PDF 文件: {filepath} ...")
    text_content = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content += text + "\n"
    return text_content

def call_qwen_api(medical_text):
    """第二步：把文字发送给通义千问，让它按结构抽取并返回 JSON"""
    print("正在呼叫通义千问大模型进行实体抽取，请稍候...")
    
    client = OpenAI(
        api_key=MY_API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    # 设计精密的 Prompt，强制要求大模型只输出 JSON 字符串
    prompt = f"""
    你是一个高年资的医疗数据处理专家。请从以下给定的病例报告（Case Report）中，
    准确提取关键医学实体。你必须严格以 JSON 格式输出结果，不要包含任何 markdown 标记（如 ```json）、不要包含任何解释性文字。

    【病例内容】
    {medical_text}

    【JSON 输出格式模板】
    {{
        "患者基本信息": {{ "年龄": "", "性别": "", "其他": "" }},
        "主要症状": [],
        "既往史": [],
        "诊断结果": [],
        "治疗方案": []
    }}
    """
    
    completion = client.chat.completions.create(
        model="qwen-plus",  # 选用百炼平台针对复杂文本表现优异的 plus 模型
        messages=[
            {"role": "system", "content": "你是一个严格执行指令的医疗数据结构化助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1  # 低随机性，保证严谨
    )
    
    return completion.choices[0].message.content

def main():
    # 检查本地有没有这个 PDF 文件
    if not os.path.exists(PDF_FILE_NAME):
        print(f"❌ 错误：在当前目录下没有找到【{PDF_FILE_NAME}】文件，请检查文件名或移动路径！")
        return
        
    # 1. 提取文字
    pdf_text = extract_pdf_text(PDF_FILE_NAME)
    
    # 2. 调用大模型
    raw_result = call_qwen_api(pdf_text)
    
    # 3. 解析并保存为标准的 JSON 文件
    try:
        # 去除可能残留的空白字符
        clean_result = raw_result.strip()
        # 将字符串转化为标准的 python 字典
        parsed_json = json.loads(clean_result)
        
        # 将数据写入本地 json 文件
        output_filename = "extracted_report.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, ensure_ascii=False, indent=4)
            
        print(f"\n✅ 任务成功完成！")
        print(f"🎉 结构化数据已成功保存至: {output_filename}")
        
    except Exception as e:
        print(f"\n❌ JSON 解析失败。大模型返回的原始文本可能夹带了多余字符。")
        print(f"报错原因: {e}")
        print("大模型返回的原始文本如下：")
        print(raw_result)

if __name__ == "__main__":
    main()