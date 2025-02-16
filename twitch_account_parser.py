# pip install requests — бібліотека для роботи з HTTP-запитами (для взаємодії з API Twitch).
# pip install csv  — стандартна бібліотека для роботи з CSV-файлами (для збереження даних).

import requests
import csv

# Дані для Twitch API
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
BASE_URL = "https://api.twitch.tv/helix/"

# Список токенів акаунтів
TOKENS = ["token1", "token2", "token3"]

# Функція для перевірки токена і отримання даних про акаунт
def get_user_data(token):
    headers = {"Authorization": f"Bearer {token}", "Client-Id": CLIENT_ID}
    response = requests.get(BASE_URL + "users", headers=headers)
    
    if response.status_code == 200 and "data" in response.json():
        return response.json()["data"][0]
    return None

# Функція перевірки можливості дарувати саби (тільки для Twitch-партнерів)
def can_gift_subs(user_id, token):
    headers = {"Authorization": f"Bearer {token}", "Client-Id": CLIENT_ID}
    url = f"{BASE_URL}subscriptions?broadcaster_id={user_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return True  # Успішний запит → акаунт має доступ до сабів
    elif response.status_code == 403:
        return "Not a Partner"  # Акаунт не партнерський
    return False  # Інші помилки → саби недоступні

# Функція зміни мови акаунта
def change_language(token, user_id, new_language):
    headers = {"Authorization": f"Bearer {token}", "Client-Id": CLIENT_ID}
    data = {"language": new_language}
    response = requests.patch(BASE_URL + "users", headers=headers, json=data)
    return response.status_code == 204  # 204 означає успішне оновлення

# Функція зміни відображуваного імені
def change_display_name(token, user_id, new_display_name):
    headers = {"Authorization": f"Bearer {token}", "Client-Id": CLIENT_ID}
    data = {"display_name": new_display_name}
    response = requests.patch(BASE_URL + "users", headers=headers, json=data)
    return response.status_code == 204

# Запуск парсингу акаунтів і збереження результатів
results = []

for token in TOKENS:
    user_data = get_user_data(token)
    
    if user_data:
        user_id = user_data["id"]
        display_name = user_data["display_name"]
        email = user_data.get("email", "No Access")  # Доступний тільки з OAuth-дозволом
        language = user_data.get("broadcaster_language", "Unknown")
        
        # Перевірка саб-гівтів
        can_gift = can_gift_subs(user_id, token)
        
        # Змінюємо мову
        language_changed = change_language(token, user_id, "en")
        
        # Змінюємо ім'я (наприклад, додаємо "_new" до старого)
        new_display_name = display_name + "_new"
        name_changed = change_display_name(token, user_id, new_display_name)

        results.append([user_id, display_name, new_display_name, email, language, can_gift, language_changed, name_changed])
        print(f"✅ {display_name} → {new_display_name} | Email: {email} | Мова: {language} | Саб-гівт: {can_gift}")
    
    else:
        print("❌ Помилка: акаунт недоступний або токен неправильний.")

# Збереження результатів у CSV
with open("twitch_accounts.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["User ID", "Old Display Name", "New Display Name", "Email", "Language", "Can Gift Subs", "Language Changed", "Name Changed"])
    writer.writerows(results)

print("📄 Дані збережено у twitch_accounts.csv")