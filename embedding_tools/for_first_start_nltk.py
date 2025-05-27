import nltk

# 아주 명확하게 재설치 + 정확한 경로 지정
nltk.download("punkt_tab", download_dir="./.venv/nltk_data", force=True)
nltk.data.path.clear()
nltk.data.path.append("C:/Users/hnn07/Documents/Gptrip//.venv/nltk_data")


from nltk.tokenize import sent_tokenize

print(sent_tokenize("광화문은 경복궁의 정문이다. 조선왕조의 상징이다."))
