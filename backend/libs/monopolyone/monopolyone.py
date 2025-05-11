import json
import time
import random
import string
import rel
import requests
import websocket
from backend.libs.monopolyone.utils import objects


class Client:

    def __init__ (self, email: str = None, password: str = None, access_token: str = None, websocket: bool = False):
        self.access_token = access_token
        self.api = "https://monopoly-one.com/api/"
        if email:
            self.sign_in(email, password)
        if websocket:
            self.create_connection()

    def on_message(self, ws, message):
        try:
            json_start = message.find("{")
            if json_start != -1:
                clean_json = message[json_start:]
                data = json.loads(clean_json)
                print(json.dumps(data, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")

    def on_error(self, ws, error):
        print("Ошибка WebSocket:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print(f"Соединение закрыто с кодом: {close_status_code}, сообщение: {close_msg}")

    def on_open(self, ws):
        print("Соединение успешно открыто")

    def create_connection(self, subs: str = "rooms"):
        self.ws_url = f"wss://monopoly-one.com/ws?subs={subs}&access_token={self.access_token}"
        self.headers = {
            'Upgrade': 'websocket',
            'Origin': 'https://monopoly-one.com',
            'Cache-Control': 'no-cache',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,af;q=0.6,tr;q=0.5',
            'Pragma': 'no-cache',
            'Connection': 'Upgrade',
            'Sec-WebSocket-Key': 'i3mtNlmC01SlbOOhQIrpxA==',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Sec-WebSocket-Version': '13',
            'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits'
        }
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            header=self.headers,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )

    def listen(self):
        try:
            self.ws.run_forever(dispatcher=rel, reconnect=5)
            rel.signal(2, rel.abort)
            rel.dispatch()
        except KeyboardInterrupt:
            print("Прослушивание WebSocket завершено вручную.")

    def sign_up(self, email: str, nickname: str, password: str, recaptcha_token: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "email": email,
            "password": password,
            "sct": int(time.time()),
            "nick": nickname,
            "recaptcha_token": recaptcha_token
        }
        response = requests.post(f"{self.api}auth.signup", json=data, proxies=proxies).json()
        if response["code"] == 0:
            self.user_id = response["data"]["user_id"]
            self.access_token = response["data"]["access_token"]
            self.expires = response["data"]["expires"]
            self.expires_in = response["data"]["expires_in"]
            self.refresh_token = response["data"]["refresh_token"]
            return objects.SessionGet(response["data"]).SessionGet
        return objects.SessionGet(response).SessionGet

    def sign_in(self, email: str, password: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "email": email,
            "password": password,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}auth.signin", json=data, proxies=proxies).json()
        if response["code"] == 0:
            self.user_id = response["data"].get("user_id", None)
            self.access_token = response["data"].get("access_token", None)
            self.expires = response["data"].get("expires", None)
            self.expires_in = response["data"].get("expires_in", None)
            self.refresh_token = response["data"].get("refresh_token", None)
            self.totp_session_token = response["data"].get("totp_session_token", None)
            if self.totp_session_token:
                return self.totp_verify(self.totp_session_token)
            return objects.SessionGet(response["data"]).SessionGet
        return objects.SessionGet(response).SessionGet

    def account_update_password(self, password_current: str, password_new: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "password_current": password_current,
            "password_new": password_new,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}account.updatePassword", json=data, proxies=proxies).json()
        if response["code"] == 0:
            self.user_id = response["data"].get("user_id", None)
            self.access_token = response["data"].get("access_token", None)
            self.expires = response["data"].get("expires", None)
            self.expires_in = response["data"].get("expires_in", None)
            self.refresh_token = response["data"].get("refresh_token", None)
            self.totp_session_token = response["data"].get("totp_session_token", None)
            return objects.SessionGet(response["data"]).SessionGet
        return objects.SessionGet(response).SessionGet
    
    def totp_verify(self, totp_session_token: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        totp_code = input("Введите TOTP-код: ")
        data = {
            "totp_session_token": totp_session_token,
            "code": totp_code,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}auth.totpVerify", json=data, proxies=proxies).json()
        if response["code"] == 0:
            self.user_id = response["data"].get("user_id", None)
            self.access_token = response["data"].get("access_token", None)
            self.expires = response["data"].get("expires", None)
            self.expires_in = response["data"].get("expires_in", None)
            self.refresh_token = response["data"].get("refresh_token", None)
            self.totp_session_token = response["data"].get("totp_session_token", None)
            return objects.SessionGet(response["data"]).SessionGet
        return objects.SessionGet(response).SessionGet
    
    def refresh(self, refresh_token: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "refresh_token": refresh_token,
            "sct": int(time.time()) 
            }
        response = requests.post(f"{self.api}auth.refresh", json=data, proxies=proxies).json()
        if response["code"] == 0:
            self.user_id = response["data"].get("user_id", None)
            self.access_token = response["data"].get("access_token", None)
            self.expires = response["data"].get("expires", None)
            self.expires_in = response["data"].get("expires_in", None)
            self.refresh_token = response["data"].get("refresh_token", None)
            self.totp_session_token = response["data"].get("totp_session_token", None)
            return objects.SessionGet(response["data"]).SessionGet
        return objects.SessionGet(response).SessionGet

    def users_get(self, user_ids: str = None, type: str = "short", short: bool = True, access_token: str = None, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        if access_token is None:
            access_token = self.access_token
        data = {
            "user_ids": str(user_ids),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        if short:
            data["type"] = type

        response = requests.post(f"{self.api}users.get", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.UsersGet(response["data"]).UsersGet
        return objects.UsersGet(response).UsersGet

    def account_info(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}account.info", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.AccountInfo(response["data"]).AccountInfo
        return objects.AccountInfo(response).AccountInfo

    def account_update_info(self, nickname: str = None, gender: int = None, domain: str = None, social_vk_show: int = None, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }

        if nickname:
            data["nick"] = str(nickname)
        if gender in [0, 1]:
            data["gender"] = int(gender)
        if social_vk_show in [0, 1]:
            data["social_vk_show"] = int(social_vk_show)
        if domain:
            data["domain"] = str(domain)
        
        response = requests.post(f"{self.api}account.updateInfo", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def account_update_email(self, email: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "email": email,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}account.updateEmail", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def wallet_promocode_activate(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "promocode": "FREEVIP",
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}wallet.promocodeActivate", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def account_social_get(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}account.socialGet", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.AccountSocialGet(response["data"]).AccountSocialGet
        return objects.AccountSocialGet(response).AccountSocialGet

    def account_social_remove(self, vk: bool = False, discord: bool = False, twitch: bool = False, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        if vk:
            data["type"] = "vk"
        if discord:
            data["type"] = "discord"
        if twitch:
            data["type"] = "twitch"

        response = requests.post(f"{self.api}account.socialRemove", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def privacy_get(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}privacy.get", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.PrivacyGet(response["data"]).PrivacyGet
        return objects.PrivacyGet(response).PrivacyGet

    def privacy_update(self, stream_autoplay: bool = True, trades_income: int = 0, trades_income_gifts: bool = False, trades_income_from_friends: bool = False, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time()),
            "stream_autoplay": "1" if stream_autoplay else "0",
            "trades_income": str(trades_income)
        }

        if trades_income_gifts:
            data["trades_income_gifts"] = "1"
        if trades_income_from_friends:
            data["trades_income_from_friends"] = "1"

        response = requests.post(f"{self.api}privacy.update", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def dialogs_get(self, offset: int = 0, count: int = 30, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "id_last": 419729250000,
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}im.dialogsGet", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.DialogsGet(response["data"]).DialogsGet
        return objects.DialogsGet(response).DialogsGet

    def history_get(self, user_id: int, offset: int = 0, count: int = 30, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "id_last": 419729250000,
            "offset": offset,
            "count": count,
            "user_id": int(user_id),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}im.historyGet", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.HistoryGet(response["data"]).HistoryGet
        return objects.HistoryGet(response).HistoryGet

    def trades_get_income(self, offset: int = 0, count: int = 20, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}trades.getIncome", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.TradesGetIncome(response["data"]).TradesGetIncome
        return objects.TradesGetIncome(response).TradesGetIncome

    def trades_get_outbound(self, offset: int = 0, count: int = 20, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}trades.getOutbound", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.TradesGetOutbound(response["data"]).TradesGetOutbound
        return objects.TradesGetOutbound(response).TradesGetOutbound

    def trades_history(self, offset: int = 0, count: int = 20, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}trades.history", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.TradesHistory(response["data"]).TradesHistory
        return objects.TradesHistory(response).TradesHistory

    def profile_get(self, user_id: int, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "user_id": user_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}execute.profile", json=data, proxies=proxies).json()
        if response["result"]:
            return objects.ProfileGet(response["result"]).ProfileGet
        return objects.ProfileGet(response).ProfileGet

    def info_get(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "logged_in": 1,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}execute.games", json=data, proxies=proxies).json()
        if response["result"]:
            return objects.InfoGet(response["result"]).InfoGet
        return objects.InfoGet(response).InfoGet

    def gchat_get(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}gchat.get", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.GchatGet(response["data"])
        return objects.GchatGet(response["data"])

    def friends_get(self, offset: int = 0, count: int = 30, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "add_user_info": 1,
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}friends.get", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.FriendsProfile(response["data"])
        return objects.FriendsProfile(response)

    def friends_add(self, user_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "user_id": str(user_id),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}friends.add", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def friends_delete(self, user_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "user_id": str(user_id),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}friends.delete", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def friends_get_requests(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}friends.getRequests", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return response["data"]
        return response

    def blacklist_get(self, offset: int = 0, count: int = 20, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}blacklist.get", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.BlacklistGet(response["data"]).BlacklistGet
        return objects.BlacklistGet(response).BlacklistGet
    
    def blacklist_add(self, user_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "user_id": str(user_id),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}blacklist.add", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def blacklist_remove(self, user_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "user_id": str(user_id),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}blacklist.remove", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def global_chat_send(self, message: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "message": message,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}gchat.send", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return response
        return response
 
    def rooms_get(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.get", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomsGet(response["data"]).RoomsGet
        return objects.RoomsGet(response).RoomsGet    
    
    def room_create(self, maxplayers: int = 5, option_private: bool = False, game_submode: int = 0, option_autostart: bool = True, access_token: str = None, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        if access_token is None:
            access_token = self.access_token
        data = {
            "maxplayers": maxplayers,
            "option_private": int(option_private),
            "game_submode": game_submode,
            "option_autostart": int(option_autostart),
            "access_token": access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.create", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomPatch(response["data"])
        return objects.RoomPatch(response)

    def rooms_start_game(self, room_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "room_id": room_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.startGame", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomPatch(response)
        return objects.RoomPatch(response)

    def rooms_settings_change(self, room_id: str, maxplayers: int = None, autostart: int = None, game_timers: int = None, br_corner: int = None, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "room_id": room_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }

        if maxplayers in [2, 3, 4, 5]:
            data["param"] = "maxplayers"
            data["value"] = maxplayers
        elif autostart in [0, 1]:
            data["param"] = "autostart"
            data["value"] = str(autostart)
        elif game_timers in [0, 1]:
            data["param"] = "game_timers"
            data["value"] = str(game_timers)
        if br_corner in [0, 1, 2, 3]:
            data["param"] = "br_corner"
            data["value"] = br_corner
        
        response = requests.post(f"{self.api}rooms.settingsChange", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomPatch(response)
        return objects.RoomPatch(response)

    def rooms_delete(self, room_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "room_id": room_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.delete", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomPatch(response)
        return objects.RoomPatch(response)

    def rooms_kick(self, room_id: str, user_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "room_id": room_id,
            "user_id": user_id,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.kick", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomPatch(response)
        return objects.RoomPatch(response)

    def room_join(self, room_id: str, access_token: str = None, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        if access_token is None:
            access_token = self.access_token
        data = {
            "room_id": room_id,
            "access_token": access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.join", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomPatch(response)
        return objects.RoomPatch(response)

    def room_leave(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}rooms.leave", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.RoomPatch(response)
        return objects.RoomPatch(response)

    def games_get_live(self, offset: int = 0, count: int = 25, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "offset": offset,
            "count": count,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}games.getLive", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.GamesGetLive(response["data"]).GamesGetLive
        return objects.GamesGetLive(response).GamesGetLive

    def games_my(self, offset: int = 0, count: int = 30, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}games.my", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.GamesMy(response["data"]).GamesMy
        return objects.GamesMy(response).GamesMy

    def games_resolve(self, gs_game_id: str, gs_id: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "gs_game_id": str(gs_game_id),
            "gs_id": str(gs_id),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}games.resolve", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.GamesResolve(response["data"]).GamesResolve
        return objects.GamesResolve(response).GamesResolve

    def games_report(self, gs_game_id: str, gs_id: str, game_time: str, user_id: str, reasons: str, comment: str, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "gs_game_id": str(gs_game_id),
            "gs_id": str(gs_id),
            "game_time": str(game_time),
            "user_id": str(user_id),
            "reasons": str(reasons),
            "comment": str(comment),
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}games.report", json=data, proxies=proxies).json()
        if response["code"] != 0:
            return response

    def streams_get_live(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}streams.getLive", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.StreamsGetLive(response["data"]).StreamsGetLive
        return objects.StreamsGetLive(response).StreamsGetLive

    def status_health(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}status.health", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.StatusHealth(response["data"]).StatusHealth
        return objects.StatusHealth(response).StatusHealth
    
    def users_get_top_week(self, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}users.getTopWeek", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.UsersGetTopWeek(response["data"]).UsersGetTopWeek
        return objects.UsersGetTopWeek(response).UsersGetTopWeek

    def users_search(self, query: str, offset: int = 0, count: int = 15, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "query": query,
            "offset": offset,
            "count": count,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}users.search", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.UsersSearch(response["data"]).UsersSearch
        return objects.UsersSearch(response).UsersSearch

    def users_notes_get(self, offset: int = 0, count: int = 20, proxy: str = None):
        proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"} if proxy else None
        data = {
            "offset": offset,
            "count": count,
            "access_token": self.access_token,
            "sct": int(time.time())
        }
        response = requests.post(f"{self.api}users.notesGet", json=data, proxies=proxies).json()
        if response["code"] == 0:
            return objects.UsersNotesGet(response["data"]).UsersNotesGet
        return objects.UsersNotesGet(response).UsersNotesGet