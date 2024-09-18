import json

# 排行榜文件名
HIGH_SCORE_FILE = "high_score.json"

# 函数用于创建并初始化 high_score.json 文件
def create_high_score_file():
    try:
        with open(HIGH_SCORE_FILE, 'x') as file:  # 'x' 模式会创建新文件，如果文件已存在则不执行
            json.dump(0, file)  # 初始化最高分为 0
    except FileExistsError:
        print("High score file already exists.")
    except Exception as e:
        print(f"An error occurred while creating the high score file: {e}")

# 调用函数
create_high_score_file()