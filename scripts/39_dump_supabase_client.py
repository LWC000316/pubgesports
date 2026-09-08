with open("intermediate_results/supabaseClient-BuEEPi6L.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("sqsouczuiycvtjnfztqs")
if idx != -1:
    start = max(0, idx - 200)
    end = min(len(text), idx + 500)
    with open("intermediate_results/supabase_client_snippet.txt", "w", encoding="utf-8") as out:
        out.write(text[start:end])
    print("스니펫 저장 완료")
else:
    print("문자열 못 찾음")
