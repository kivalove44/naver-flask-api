from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

CLIENT_ID = "YJ_fiRJhVXWGLxXABuSh"
CLIENT_SECRET = "Mtk8JWBRyI"

NAVER_ENDPOINTS = {
    "shop": "shop.json",
    "news": "news.json",
    "blog": "blog.json",
    "book": "book.json",
    "image": "image.json",
    "movie": "movie.json",
    "kin": "kin.json",
    "web": "webkr.json"
}

@app.route("/search")
def search():
    query = request.args.get("query")
    search_type = request.args.get("type", "shop")

    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    if search_type not in NAVER_ENDPOINTS:
        return jsonify({"error": "Invalid search type"}), 400

    # ✅ count 파라미터 (1~100 자유 입력)
    count = request.args.get("count")
    try:
        count = int(count)
        if count < 1 or count > 100:
            count = 30
    except:
        count = 30

    url = f"https://openapi.naver.com/v1/search/{NAVER_ENDPOINTS[search_type]}"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": count
    }

    res = requests.get(url, headers=headers, params=params)
    items = res.json().get("items", [])

    simplified = []
    for item in items:
        simplified.append({
            "title": item.get("title", "").replace("<b>", "").replace("</b>", ""),
            "link": item.get("link", ""),
            "description": item.get("description", "").replace("<b>", "").replace("</b>", "")
        })

    return Response(json.dumps(simplified, ensure_ascii=False), mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
