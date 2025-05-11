import os
import datetime
import requests
import json
import time
from typing import Optional, Dict, Any, List

EMAIL = os.getenv('MONOPOLY_EMAIL')
PASSWORD = os.getenv('MONOPOLY_PASSWORD')
PROXY = os.getenv('MONOPOLY_PROXY')
if not EMAIL or not PASSWORD:
    raise ValueError("MONOPOLY_EMAIL и MONOPOLY_PASSWORD должны быть установлены в переменных окружения")

AUTH_URL = 'https://monopoly-one.com/api/auth.signin'
USER_DATA_URL = 'https://monopoly-one.com/api/users.get'
RESOLVE_URL = 'https://monopoly-one.com/api/games.resolve'
GAME_ACTION_URL = "https://gs{}.monopoly-one.com/api/game.action"
GAME_TABLE_URL_TEMPLATE = "https://monopoly-one.com/table/#/{}/{}"
GAME_M1TV_URL_TEMPLATE = "https://monopoly-one.com/m1tv/#/{}/{}"
GAME_DATA_URL_TEMPLATE = "https://demos.monopoly-one.com/dl/{}/{}.mid"

def get_auth_data(email: str, password: str) -> Dict[str, Any]:
    auth_headers = {"Content-Type": "application/json", "Host": "monopoly-one.com"}
    auth_data = {"email": email, "password": password}
    proxies = {"http": f"http://{PROXY}", "https": f"http://{PROXY}"} if PROXY else None
    response = requests.post(AUTH_URL, headers=auth_headers, json=auth_data, proxies=proxies)
    response.raise_for_status()
    return response.json()

def get_user_data(user_id: str, access_token: str) -> Dict[str, Any]:
    user_headers = {"Authorization": f"Bearer {access_token}"}
    user_params = {"user_ids": user_id, "type": "short"}
    proxies = {"http": f"http://{PROXY}", "https": f"http://{PROXY}"} if PROXY else None
    response = requests.get(USER_DATA_URL, headers=user_headers, params=user_params, proxies=proxies)
    response.raise_for_status()
    return response.json()

def get_resolve_data(gs_id: str, gs_game_id: str, access_token: str) -> Dict[str, Any]:
    resolve_headers = {"Authorization": f"Bearer {access_token}"}
    resolve_params = {"gs_id": gs_id, "gs_game_id": gs_game_id, "access_token": access_token}
    proxies = {"http": f"http://{PROXY}", "https": f"http://{PROXY}"} if PROXY else None
    response = requests.get(RESOLVE_URL, headers=resolve_headers, params=resolve_params, proxies=proxies)
    response.raise_for_status()
    return response.json()

# def clear_console() -> None:
#     os.system('cls' if os.name == 'nt' else 'clear')

def convert_unix_time_to_hhmmss(unix_time_ms: int) -> str:
    unix_time_sec = unix_time_ms / 1000
    return datetime.datetime.fromtimestamp(unix_time_sec).strftime("%H:%M:%S")

def get_seconds_word(seconds: int) -> str:
    if seconds % 10 == 1 and seconds % 100 != 11:
        return "секунда"
    elif 2 <= seconds % 10 <= 4 and not (12 <= seconds % 100 <= 14):
        return "секунды"
    else:
        return "секунд"

def search_for_game_data() -> None:
    data_found = False
    global user_id
    print("[-] Идет поиск игры...")

    while True:
        try:
            auth_response_data = get_auth_data(EMAIL, PASSWORD)
            user_id = auth_response_data["data"]["user_id"]
            access_token = auth_response_data["data"]["access_token"]
            refresh_token = auth_response_data['data']['refresh_token']
            users_response_data = get_user_data(user_id, access_token)
            nick = users_response_data['data'][0]['nick']
            current_game = users_response_data["data"][0].get("current_game")
            gs_id = current_game.get("gs_id") if current_game else None
            gs_game_id = current_game.get("gs_game_id") if current_game else None
            url_game_table = GAME_TABLE_URL_TEMPLATE.format(gs_id, gs_game_id) if gs_id and gs_game_id else None
            url_game_m1tv = GAME_M1TV_URL_TEMPLATE.format(gs_id, gs_game_id) if gs_id and gs_game_id else None
            url = GAME_DATA_URL_TEMPLATE.format(gs_id, gs_game_id) if gs_id and gs_game_id else None

            if gs_id and gs_game_id:
                if not data_found:
                    # clear_console()
                    resolve_response_data = get_resolve_data(gs_id, gs_game_id, access_token)
                    gs_token = resolve_response_data['data']['gs_token']

                    authorization_message = (
                        f"Авторизация прошла успешно:\n"
                        f"- nick: {nick}\n"
                        f"- user_id: {user_id}\n"
                        f"- access_token: {access_token}\n"
                        f"- refresh_token: {refresh_token}\n"
                        f"- gs_id: {gs_id}\n"
                        f"- gs_game_id: {gs_game_id}\n"
                        f"- gs_token: {gs_token}\n"
                        f"- game_table: {url_game_table}\n"
                        f"- game_m1tv: {url_game_m1tv}\n"
                        f"- game_data: {url}\n"
                    )
                    print(authorization_message)
                    data_found = True
                    process_game_stream(nick, user_id, access_token, refresh_token, gs_id, gs_game_id, gs_token, url)

            else:
                if data_found:
                    # clear_console()
                    print("[-] Идет поиск игры...")
                    data_found = False

        except Exception as e:
            print(f"[-] Произошла ошибка: {e}. Ожидание...")

        time.sleep(1)

def display_game_info(data: Dict[str, Any], access_token: str) -> None:
    players = data.get("status", {}).get("players", [])
    time_data = data.get("time", {})
    global config_data
    config_data = data.get("config", {})
    settings = data.get("settings", {})
    
    ts_start = time_data.get("ts_start")

    packet_info = (
        f"Игра началась в: {convert_unix_time_to_hhmmss(ts_start)}\n"
        f"- Наличие турнира: {'да' if settings.get('is_tournament') else 'нет'}\n"
        f"- Играть с таймерами: {'да' if settings.get('timers') else 'нет'}\n"
        f"- Личные сообщения разрешены: {'да' if settings.get('pm_allowed') else 'нет'}\n"
        f"- Протесты по контракту: {'да' if settings.get('contract_protests') else 'нет'}"
    )
    print(packet_info)

    if settings.get('timers'):
        timer_info = (
            f"- Время для броска кубиков: {config_data.get('TIME_FOR_ROLL_DICES')} {get_seconds_word(config_data.get('TIME_FOR_ROLL_DICES'))}\n"
            f"- Время для покупки: {config_data.get('TIME_FOR_PAY')} {get_seconds_word(config_data.get('TIME_FOR_PAY'))}\n"
            f"- Время для реакции контракта: {config_data.get('TIME_FOR_CONTRACT_REACTION')} {get_seconds_word(config_data.get('TIME_FOR_CONTRACT_REACTION'))}\n"
            f"- Время для реакции аукциона: {config_data.get('TIME_FOR_AUCTION_REACTION')} {get_seconds_word(config_data.get('TIME_FOR_AUCTION_REACTION'))}\n"
            f"- Время для выбора поля: {config_data.get('TIME_FOR_CHOOSE_FIELD')} {get_seconds_word(config_data.get('TIME_FOR_CHOOSE_FIELD'))}\n"
            f"- Дополнительное время (только vip): {config_data.get('TIME_ADDITIONAL')} {get_seconds_word(config_data.get('TIME_ADDITIONAL'))}"
        )
        print(timer_info)

    player_info_lines = []
    for player in players:
        user_id = player.get("user_id")
        players_data = get_user_data(user_id, access_token)
        players_nick = players_data["data"][0].get("nick")
        vip = player.get("vip")
        money = player.get("money")

        s_vip = "есть" if vip else "нет"
        
        player_info_lines.append(
            f"- игрок: {players_nick} (id{user_id}), vip: {s_vip}, баланс: {money}k"
        )

    if player_info_lines:
        print("\n".join(player_info_lines).strip())

def handle_roll_dices_event(event: Dict[str, Any], access_token) -> None:
    dices = event.get("dices")
    mean_position = event.get("mean_position")
    roll_user_data = get_user_data(event['user_id'], access_token)
    roll_user_nick = roll_user_data["data"][0].get("nick")
    
    if isinstance(dices, list):
        total = sum(dices)
        output = (
            f"{roll_user_nick} выбрасывает {dices}, сумма: {total}, поле: {mean_position}"
        )

        if len(dices) == 2 and dices[0] == dices[1]:
            output += " - Это дубль! Получает еще один ход."

        print(output)


def handle_other_event(event: Dict[str, Any]) -> None:
    event_type = event.get("type")
    print(f"{event_type}")

def handle_game_over_event(event: Dict[str, Any], gs_id) -> None:
    print(f"Игра №{gs_id} завершилась")

def handle_message_event(event, access_token, gs_token, gs_id, user_id) -> None:
    sender_id = event.get("user_id")
    message_text = event.get("text")
    sender_data = get_user_data(sender_id, access_token)
    sender_nick = sender_data["data"][0].get("nick")
    sender_gender = sender_data["data"][0].get("gender")

    if sender_gender == 1:
        action = "написала"
    elif sender_gender == 0:
        action = "написал"
    else:
        action = "написал(а)"
    
    if "private" in event:
        receiver_id = event["private"].get("user")
        receiver_data = get_user_data(receiver_id, access_token)
        receiver_nick = receiver_data["data"][0].get("nick")

        if sender_id != user_id and receiver_id != user_id:
            headers = {"Authorization": f"Bearer {access_token}"}            
            text = f"[{sender_nick}] {action} [{receiver_nick}]: {message_text}"
            tex = f"Больше двух говорят вслух Doge"
            param = {"text": f"{tex}", "channel": "all", "action": f"message", "gs_token": f"{gs_token}"}
            params = {"text": f"{text}", "channel": "all", "action": f"message", "gs_token": f"{gs_token}"}
            response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=param)
            response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
            print(f"{sender_nick} {action} {receiver_nick}: {message_text}")
        else:
            print(f"{sender_nick} {action} {receiver_nick}: {message_text}")

    else:
        print(f"{sender_nick} {action} в чат: {message_text}")

def handle_leave_event(event: Dict[str, Any], user_id: str) -> bool:
    if event.get("user_id") == user_id:
        return True
    else:
        print(f"Игрок с id {event.get(user_id)} покинул игру.")
        return False
    































def have_groups(data):
    config = config_data
    status = data.get('status')
    group_fields = {}
    for index, field in enumerate(config['fields']):
        if 'group' in field:
            group_id = field['group']
            if group_id in (0, 9):
                continue  
            if group_id not in group_fields:
                group_fields[group_id] = []
            group_fields[group_id].append(str(index))

    user_fields = {key for key, details in status['fields'].items() if details['owner'] == user_id}

    completed_groups = [
        group_id for group_id, fields in group_fields.items()
        if set(fields).issubset(user_fields)
    ]

    return completed_groups

def handle_level_up(access_token: str, gs_id: str, gs_token: str, data: Dict[str, Any]) -> None:
    config = config_data
    status = data.get('status')
    fields = status.get("fields", {})
    players = status.get("players", [])

    groups = config.get("groups", {})
    
    current_player = next(
        (player for player in players if str(player.get("user_id")) == str(user_id)), 
        None
    )
    if not current_player:
        return
    
    money = current_player.get("money", 0)

    completed_groups = have_groups(data)
    
    for group_id in completed_groups:
        group_info = groups.get(str(group_id), {})
        if not group_info:
            print(f"Группа {group_id} не найдена в конфиге")
            continue
        
        level_up_cost = group_info.get("levelUpCost", 0)
        if not level_up_cost:
            print(f"У группы {group_id} нет стоимости улучшения")
            continue
        
        group_fields = [
            field for field in config_data["fields"] 
            if str(field.get("group")) == str(group_id)
        ]

        if not group_fields:
            print(f"В группе {group_id} нет полей")
            continue
        
        for field in group_fields:
            field_index = str(config_data["fields"].index(field))
            field_data = fields.get(field_index, {})
            
            current_level = field_data.get("level", 0)
            max_level = len(group_info.get("levels", [])) - 1
            
            if current_level < max_level and money >= level_up_cost:
                headers = {"Authorization": f"Bearer {access_token}"}
                params = {
                    "field_id": field_index,
                    "action": "levelUp",
                    "gs_token": gs_token,
                }
                response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
                if response.status_code == 200:
                    print(f"Улучшено поле {field_index} (уровень {current_level + 1})")
                    money -= level_up_cost
                else:
                    print(f"Ошибка: {response.status_code} при улучшении поля {field_index}")

def handle_level_down(access_token: str, gs_id: str, gs_token: str, data: Dict[str, Any], price: int) -> None:
    status = data.get('status', {})
    players = status.get("players", [])
    config = config_data
    completed_groups = have_groups(data)

    current_player = next(
        (player for player in players if str(player.get("user_id")) == str(user_id)), 
        None
    )
    
    if not current_player:
        return
    
    money = current_player.get("money", 0)
    
    levels_lowered = False  # Флаг, чтобы отслеживать, были ли понижены уровни
    
    for group_id in completed_groups:
        group_info = config.get("groups", {}).get(str(group_id), {})
        if not group_info:
            continue
        
        level_down_cost = group_info.get("levelUpCost", 0)
        if not level_down_cost:
            continue
        
        group_fields = [
            field for field in config_data["fields"] 
            if str(field.get("group")) == str(group_id)
        ]

        if not group_fields:
            continue
        
        for field in group_fields:
            field_index = str(config_data["fields"].index(field))
            field_data = status.get("fields", {}).get(field_index, {})
            
            current_level = field_data.get("level", 0)
            if current_level > 0:
                headers = {"Authorization": f"Bearer {access_token}"}
                params = {
                    "field_id": field_index,
                    "action": "levelDown",
                    "gs_token": gs_token,
                }
                response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
                
                if response.status_code == 200:
                    money += level_down_cost
                    levels_lowered = True
                    print(f"Понижен уровень поля {field_index} (уровень {current_level - 1}), получено +{level_down_cost}k")
                    print(f"Новый баланс: {money}k")
                    
                    if money >= price:
                        print("Денег достаточно, прекращаем понижение уровней")
                        return
                else:
                    print(f"Ошибка: {response.status_code} при понижении уровня поля {field_index}")
    
    if not levels_lowered:
        print("Нет полей с уровнями для понижения.")

def get_my_fields_with_prices(data: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    status = data.get("status", {})
    fields = status.get("fields", {})
    groups = config_data.get("groups", {})
    
    my_fields = {}
    
    for field_id_str, field_data in fields.items():
        if str(field_data.get("owner")) != str(user_id):
            continue
            
        field_id = int(field_id_str)
        field_config = config_data["fields"][field_id]
        group_id = str(field_config.get("group"))
            
        group_data = groups[group_id]
        is_last = bool(field_config.get("is_last"))
        
        buy_price = group_data.get("buy_last" if is_last else "buy", 0)
        
        my_fields[field_id] = buy_price
    print(my_fields)
    return my_fields

def handle_mortgage(access_token: str, gs_id: str, gs_token: str, data: Dict[str, Any], price) -> None:
    status = data.get('status')
    my_fields_with_price = get_my_fields_with_prices(data)
    players = status.get("players", [])

    current_player = next(
        (player for player in players if str(player.get("user_id")) == str(user_id)), 
        None
    )
    
    if not current_player:
        return
    
    money = current_player.get("money", 0)
    fields = status.get("fields", {})
    
    for field_index, field_data in fields.items():
        if field_data.get("owner") == user_id and not field_data.get("mortgaged"):
            field_price = my_fields_with_price.get(int(field_index), 0)
            mortgage_value = field_price // 2
            
            headers = {"Authorization": f"Bearer {access_token}"}
            params = {
                "field_id": field_index,
                "action": "mortgage",
                "gs_token": gs_token,
            }
            response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
            
            if response.status_code == 200:
                print(f"Заложено поле {field_index} за {mortgage_value}k")
                money += mortgage_value
                print(f"Новый баланс: {money}k")
                
                if money >= price:
                    break
            else:
                print(f"Ошибка: {response.status_code} при залоге поля {field_index}")
                
def handle_unmortgage(access_token: str, gs_id: str, gs_token: str, data: Dict[str, Any]) -> None:
    status = data.get('status', {})
    fields = status.get("fields", {})
    players = status.get("players", [])
    
    current_player = next(
        (player for player in players if str(player.get("user_id")) == str(user_id)), 
        None
    )
    
    if not current_player:
        print("Ошибка: текущий игрок не найден.")
        return
    
    money = current_player.get("money", 0)
    my_fields_with_prices = get_my_fields_with_prices(data)  # Используем существующую функцию
    
    coeff_unmortgage = 1.2  # Коэффициент выкупа
    unmortgaged_fields = False  # Флаг для отслеживания выкупа
    
    for field_index, field_data in fields.items():
        if field_data.get("owner") == user_id and field_data.get("mortgaged"):
            field_price = my_fields_with_prices.get(int(field_index), 0)
            unmortgage_cost = int(field_price * coeff_unmortgage / 2)  # Цена выкупа = (цена поля / 2) * 1.2
            
            if money >= unmortgage_cost:
                headers = {"Authorization": f"Bearer {access_token}"}
                params = {
                    "field_id": field_index,
                    "action": "unmortgage",
                    "gs_token": gs_token,
                }
                response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
                
                if response.status_code == 200:
                    unmortgaged_fields = True
                    money -= unmortgage_cost
                    print(f"Выкуплено поле {field_index} за {unmortgage_cost}k")
                    print(f"Новый баланс: {money}k")
                else:
                    print(f"Ошибка: {response.status_code} при выкупе поля {field_index}")
            else:
                print(f"Недостаточно денег ({money}k) для выкупа поля {field_index} ({unmortgage_cost}k)")
    
    if not unmortgaged_fields:
        print("Нет заложенных полей для выкупа или недостаточно денег.")

def handle_need_money(data, event, access_token: str, gs_id: str, gs_token: str, gs_game_id) -> None:
    event_user_id = event.get('user_id')  # ID игрока, связанного с событием
    if str(event_user_id) != str(user_id):  # Проверяем, что событие относится к вашему игроку
        # Если это не ваш игрок, просто логируем событие и выходим
        event_type = event.get('type')
        money = event.get('money', 'неизвестно')
        user_data = get_user_data(event_user_id, access_token)
        nick = user_data["data"][0].get("nick", "неизвестный игрок")
        print(f"Событие '{event_type}' для {nick} (id: {event_user_id}), сумма: {money}k - не относится к вам.")
        return

    # Если событие относится к вашему игроку, продолжаем обработку
    status = data.get('status')
    players = status.get("players", [])
    completed_groups = have_groups(data)
    price = event.get('money')

    if price is None or not isinstance(price, int):
        return
        
    current_player = next(
        (player for player in players if str(player.get("user_id")) == str(user_id)), 
        None
    )

    if not current_player:
        return
    
    money = current_player.get("money", 0)
    event_type = event.get('type')
    chance_list = ['5', '6', '7', '8', '9', '15']
    chance_type = str(event.get('chance_id'))

    if (event_type in ['payRent', 'tax_income', 'tax_luxury', 'payForUnjail', 'repair', 'insurance'] or 
        (chance_type in chance_list)):
        if price > money:
            if completed_groups:
                print("У вас есть монополия, но не хватает денег. Пытаемся понизить уровни.")
                handle_level_down(access_token, gs_id, gs_token, data, price)
                
                response = requests.get(GAME_DATA_URL_TEMPLATE.format(gs_id, gs_game_id))
                if response.status_code == 200:
                    data = json.loads(response.text.splitlines()[-1])
                
                updated_player = next(
                    (p for p in data.get("status", {}).get("players", []) if str(p.get("user_id")) == str(user_id)), 
                    None
                )
                money = updated_player.get("money", 0) if updated_player else money

                if money < price:
                    print("Понижение уровней не дало достаточно денег. Пытаемся заложить поля.")
                    handle_mortgage(access_token, gs_id, gs_token, data, price)
            else:
                print("У вас нет монополии и не хватает денег. Пытаемся заложить поля.")
                handle_mortgage(access_token, gs_id, gs_token, data, price)

            response = requests.get(GAME_DATA_URL_TEMPLATE.format(gs_id, gs_game_id))
            if response.status_code == 200:
                data = json.loads(response.text.splitlines()[-1])
            
            updated_player = next(
                (p for p in data.get("status", {}).get("players", []) if str(p.get("user_id")) == str(user_id)), 
                None
            )
            money = updated_player.get("money", 0) if updated_player else money

            if money >= price:
                headers = {"Authorization": f"Bearer {access_token}"}
                if event_type == "payRent":
                    params = {"action": "payRent", "gs_token": gs_token}
                    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
                    print(f"Успешно оплачена аренда в размере {price}k")
                elif event_type in ["tax_income", "tax_luxury"] or (chance_type in chance_list):
                    params = {"action": "payToBank", "gs_token": gs_token}
                    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
                    print(f"Успешно оплачен налог/штраф в размере {price}k")
                elif event_type == "payForUnjail":
                    params = {"action": "payForUnjail", "gs_token": gs_token}
                    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
                    print(f"Успешно оплачено освобождение из тюрьмы за {price}k")
            else:
                print(f"Не удалось собрать достаточно денег ({money}k) для оплаты {price}k")
        else:
            print(f"У вас достаточно денег ({money}k) для оплаты {price}k. Оплата производится.")
            headers = {"Authorization": f"Bearer {access_token}"}
            if event_type == "payRent":
                params = {"action": "payRent", "gs_token": gs_token}
                response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
            elif event_type in ["tax_income", "tax_luxury"] or (chance_type in chance_list):
                params = {"action": "payToBank", "gs_token": gs_token}
                response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
            elif event_type == "payForUnjail":
                params = {"action": "payForUnjail", "gs_token": gs_token}
                response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)


























def handle_can_buy_event(event: Dict[str, Any], access_token: str, gs_id: str, gs_token: str, data: Dict[str, Any,]) -> None:
    field_can_buy = event.get("field")
    field_price = event.get('money')
    players = data.get("status", {}).get('players',{})

    for player in players:
        player_user_id = player.get('user_id')
        if user_id == player_user_id:
            money = player.get("money")
    
    can_buy_data = get_user_data(event['user_id'], access_token)
    roll_user_nick = can_buy_data["data"][0].get("nick")
    print(f"{roll_user_nick} попадает на {field_can_buy} поле и задумывается о покупке")

    if money >= field_price:
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"action": "buy", "gs_token": f"{gs_token}"}
        response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)
    else:
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"action": "toAuction", "gs_token": f"{gs_token}"}
        print(f"{roll_user_nick} выставляет поле на аукцион")
        response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)

def handle_to_auction(event: Dict[str, Any], access_token: str, gs_id: str, gs_token: str, data: Dict[str, Any,]) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"action": "auctionDecline", "gs_token": f"{gs_token}"}
    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)

def handle_contract_decline(event: Dict[str, Any], access_token: str, gs_id: str, gs_token: str, data: Dict[str, Any,]) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"action": "contract_decline", "gs_token": f"{gs_token}"}
    print(f"контракт был отклонен")
    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)

def handle_buy_event(event: Dict[str, Any], access_token: str) -> None:
    money_buy = event.get("money")
    field_buy = event.get("field")
    buy_data = get_user_data(event['user_id'], access_token)
    roll_user_nick = buy_data["data"][0].get("nick")
    print(f"{roll_user_nick} покупает {field_buy} поле за {money_buy}k")

def handle_pay_to_bank(event: Dict[str, Any], access_token: str, gs_id: str, gs_token: str) -> None:
    money_pay_to_bank = event.get("money")
    pay_to_bank_data = get_user_data(event['user_id'], access_token)
    roll_user_nick = pay_to_bank_data["data"][0].get("nick")
    print(f"{roll_user_nick} платит банку {money_pay_to_bank}k")
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"action": "payToBank", "gs_token": f"{gs_token}"}
    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)

def handle_pay_for_unjail(event: Dict[str, Any], access_token: str, gs_id: str, gs_token: str) -> None:
    money_for_unjail = event.get("money")
    unjail_data = get_user_data(event['user_id'], access_token)
    roll_user_nick = unjail_data["data"][0].get("nick")
    print(f"{roll_user_nick} платит за освобождение {money_for_unjail}k")
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"action": "payForUnjail", "gs_token": f"{gs_token}"}
    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)

def handle_jackpot_decline(event: Dict[str,Any], access_token: str, gs_id: str, gs_token: str) -> None:
    jacpot_data = get_user_data(event['user_id'], access_token)
    roll_user_nick = jacpot_data["data"][0].get("nick")
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"action": "jackpotDecline", "gs_token": f"{gs_token}"}
    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)

def handle_go_to_jail_event(event: Dict[str, Any], access_token: str) -> None:
    goto_jail_data = get_user_data(event['user_id'], access_token)
    goto_jail_nick = goto_jail_data["data"][0].get("nick")
    print(f"{goto_jail_nick} арестован(a) полицией и отправляется в тюрьму")

def handle_pay_rent_event(event: Dict[str, Any], access_token: str, gs_id: str, gs_token: str) -> None:
    field_pay_rent = event.get("field")
    money_pay_rent = event.get("money")
    to_rent_data = get_user_data(event['to'], access_token)
    pay_rent_data = get_user_data(event['user_id'], access_token)
    nick_first = pay_rent_data["data"][0].get("nick")
    to_nick = to_rent_data["data"][0].get("nick")
    print(f"{nick_first} попадает на {field_pay_rent} поле и должен(должна) заплатить игроку {to_nick} аренду в размере {money_pay_rent}k")
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"action": "payRent", "gs_token": f"{gs_token}"}
    response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=params)

def handle_pay_rent_success_event(event: Dict[str, Any], access_token: str) -> None:
    money_pay_rent_success = event.get("money")
    pay_rent_success_data = get_user_data(event['user_id'], access_token)
    nick_first = pay_rent_success_data["data"][0].get("nick")
    print(f"{nick_first} заплатил(a) аренду {money_pay_rent_success}k")

def process_game_stream(nick: str, user_id: str, access_token: str, refresh_token: str, gs_id: str, gs_game_id: str, gs_token: str, url: str) -> None:
    last_processed_id = None
    exit_game = False 

    event_handlers = {
        "leave": lambda event: handle_leave_event(event, user_id),
        "gameOver": lambda event: handle_game_over_event(event, gs_id), 
        "rollDices": lambda event: handle_roll_dices_event(event, access_token),
        "message": lambda event: handle_message_event(event, access_token, gs_token, gs_id, user_id),
        "canBuy": lambda event: handle_can_buy_event(event, access_token, gs_id, gs_token, data),
        "buy": lambda event: handle_buy_event(event, access_token),
        "goToJail": lambda event: handle_go_to_jail_event(event, access_token),
        "payRent": lambda event: handle_need_money(data, event, access_token, gs_id, gs_token, gs_game_id),
        "payRentSuccess": lambda event: handle_pay_rent_success_event(event, access_token),
        "chance": lambda event: handle_need_money(data, event, access_token, gs_id, gs_token, gs_game_id),
        "tax_income": lambda event: handle_need_money(data, event, access_token, gs_id, gs_token, gs_game_id),
        "tax_luxury": lambda event: handle_need_money(data, event, access_token, gs_id, gs_token, gs_game_id),
        "jackpot": lambda event: handle_jackpot_decline(event, access_token, gs_id, gs_token),
        "payForUnjail": lambda event:handle_need_money(data, event, access_token, gs_id, gs_token, gs_game_id),
        "toAuction": lambda event:handle_to_auction(event, access_token, gs_id, gs_token, data),
        "contract_details": lambda event:handle_contract_decline(event, access_token, gs_id, gs_token, data),
        "contract": lambda event:handle_contract_decline(event, access_token, gs_id, gs_token, data),
    }

    while not exit_game:
        try:
            response = requests.get(url)
            response.encoding = response.apparent_encoding
            if response.status_code == 200:
                raw_data = response.text
                lines = raw_data.splitlines()
                last_event = None

                for line in lines:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            json_id = data.get("id")
                            
                            if last_processed_id is None or json_id > last_processed_id:
                                last_processed_id = json_id
                                if json_id == 0:
                                    display_game_info(data, access_token)
                                    print()

                                last_event = data

                        except json.JSONDecodeError as e:
                            print(f"[-] Ошибка декодирования JSON: {e} в строке: {line}")
                
                if last_event:

                    if 'events' in last_event:

                        for event in last_event['events']:
                            event_type = event.get("type")
                            handler = event_handlers.get(event_type, handle_other_event)
                            exit_game = handler(event)

                            if exit_game:
                                break

                    if 'status' in last_event:
                        player_owner_of_move = last_event["status"]["player_ownerOfMove"]
                        if player_owner_of_move == user_id:
                            handle_level_up(access_token, gs_id, gs_token, data)
                            handle_unmortgage(access_token, gs_id, gs_token, data)
                            # time.sleep(1)
                            data = {
                                'action': 'rollDices',
                                'gs_token': f'{gs_token}',
                            }
                            headers = {"Authorization": f"Bearer {access_token}"}
                            response = requests.post(GAME_ACTION_URL.format(gs_id), headers=headers, data=data)

            elif response.status_code == 404:
                print("[-] Ошибка 404: Игра не найдена. Ожидание перед повторной попыткой...")
                break
            else:
                print(f"[-] Ошибка: {response.status_code}. Ожидание перед повторной попыткой...")
                break

        except Exception as e:
            print(f"[-] Произошла ошибка при получении данных: {e}. Ожидание перед повторной попыткой...")
            time.sleep(1)


if __name__ == "__main__":
    search_for_game_data()