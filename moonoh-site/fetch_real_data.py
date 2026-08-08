import requests
import json
import os

s = requests.Session()
r_login = s.post("http://52.44.113.58:8080/admin.do", data={"kind": "login", "id": "admin", "password": "1234"})

r_data = s.post("http://52.44.113.58:8080/admin.do", data={
    "kind": "getProductArray",
    "page": 0,
    "viewCount": 500  # fetch up to 500 items
})
data = r_data.json()

items = []
town_names = {
    1: "Flushing",
    2: "Bayside",
    3: "Palisades Park",
    4: "Fort Lee",
    5: "Upper Manhattan"
}

if data.get("productArray"):
    for item in data["productArray"]:
        if item.get("isShow") == "N":
            continue
            
        town_no = item.get("townNo", 0)
        town_name = town_names.get(town_no, "etc")
        
        picture_url = item.get("pictureUrl", "")
        img_url = "images/common/ico_profile_empty.png" # default
        if picture_url:
            last_index = picture_url.rfind("/")
            path = picture_url[:last_index+1]
            file_name = picture_url[last_index+1:]
            dot_index = file_name.rfind(".")
            if dot_index != -1:
                thumbnail_name = "thumbnail_" + file_name[:dot_index] + ".jpg"
            else:
                thumbnail_name = "thumbnail_" + file_name + ".jpg"
            img_url = f"http://52.44.113.58:8080/file/{path}{thumbnail_name}"
            
        items.append({
            "title": item.get("title", ""),
            "price": item.get("price", 0),
            "location": f"1mi · {town_name}",  # mock distance
            "image": img_url,
            "category": item.get("categoryName", "")
        })

with open("/Users/thomaskim/Cryptocasinomedia/moonoh-site/data.json", "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"Fetched {len(items)} real items and saved to data.json")
