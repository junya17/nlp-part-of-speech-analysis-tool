from flask import Flask, request, jsonify, render_template
import spacy
import time

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# 品詞ごとの色と日本語表記＋説明
POS_INFO = {
    "NOUN": {"color": "#007bff", "label": "名詞", "desc": "物・人・概念を表す"},
    "VERB": {"color": "#ff4d4d", "label": "動詞", "desc": "動作や状態を表す"},
    "ADJ": {"color": "#28a745", "label": "形容詞", "desc": "名詞を修飾する"},
    "ADV": {"color": "#ff8c00", "label": "副詞", "desc": "動詞や形容詞を修飾する"},
    "PRON": {"color": "#6f42c1", "label": "代名詞", "desc": "名詞の代わりになる"},
    "DET": {"color": "#d63384", "label": "限定詞", "desc": "名詞を特定する（the, my）"},
    "ADP": {"color": "#ffc107", "label": "前置詞", "desc": "名詞の前に置かれる（in, on）"},
    "CONJ": {"color": "#17a2b8", "label": "接続詞", "desc": "語や文をつなぐ"},
    "NUM": {"color": "#6610f2", "label": "数詞", "desc": "数を表す"},
    "PART": {"color": "#20c997", "label": "助詞", "desc": "文の構造を補助する"},
    "AUX": {"color": "#e83e8c", "label": "助動詞", "desc": "動詞の意味を補助する"},
    "PUNCT": {"color": "#6c757d", "label": "句読点", "desc": "文の区切りを示す"},
    "SYM": {"color": "#fd7e14", "label": "記号", "desc": "数式や特殊記号"},
    "X": {"color": "#dc3545", "label": "その他", "desc": "分類できない単語"},
    "INTJ": {"color": "#17a2b8", "label": "感動詞", "desc": "感情を表す"}
}

POS_CORRECTIONS = {
    "how": "ADV",  # 🔹 `SCONJ` を `ADV` に修正
    "what": "PRON",
    "who": "PRON",
    "which": "PRON",
    "whose": "PRON",
    "why": "ADV",
    "where": "ADV",
    "when": "ADV",
    "my": "DET",
    "your": "DET",
    "his": "DET",
    "her": "DET",
    "our": "DET",
    "their": "DET",
    "'s": "VERB"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "").strip()

    print(f"Received text: {text}")
    doc = nlp(text)
    print(f"Processed text: {doc}")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    doc = nlp(text)
    result = []
    word_count = len([token for token in doc if token.is_alpha])  # 🔹 記号やスペースを除外した単語数

    # 品詞のカウント（正しく `token.pos_` が一致するように修正）
    pos_counts = {"VERB": 0, "ADJ": 0, "ADV": 0, "CONJ": 0}

    for token in doc:
        word_lower = token.text.lower()  # 小文字に変換して比較
        pos = POS_CORRECTIONS.get(word_lower, token.pos_)  # 🔹 修正された品詞を適用
        pos_data = POS_INFO.get(pos, {"label": pos, "color": "#000000", "desc": "説明なし"})

        result.append({
            "word": token.text,
            "pos": pos_data["label"],  
            "color": pos_data["color"],
            "desc": pos_data["desc"]
        })
    
    return jsonify({"words": result})

if __name__ == "__main__":
    app.run(debug=True)
