#!/usr/bin/env python3
"""
🎮 FF PROXY BACKEND - RAILWAY READY
- Handles all proxy traffic
- Session management
- Header stripping
- Always on
"""

import os, sys, json, time, random, base64, hashlib, threading, re, logging
from datetime import datetime
from flask import Flask, request, Response, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== CONFIG ====================
CLIENT_SECRET = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'
PROXY_PORT = int(os.environ.get("PORT", 5031))

print(f"📡 Backend running on port: {PROXY_PORT}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== IMPORT PB2 FILES ====================
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Pb2'))

USE_PB2 = False
try:
    from Pb2 import MajoRLoGinrEq_pb2
    from Pb2 import MajoRLoGinrEs_pb2
    from Pb2 import PorTs_pb2
    USE_PB2 = True
    print("✅ PB2 loaded successfully")
except ImportError as e:
    print(f"⚠️ PB2 import error: {e}")
    USE_PB2 = False

# ==================== DEVICE POOL ====================
DEVICE_POOL = [
    {"model": "SM-G998B", "brand": "samsung", "android": "13", "user_agent": "Dalvik/2.1.0 (Linux; U; Android 13; SM-G998B Build/TP1A.220624.014)"},
    {"model": "SM-G991B", "brand": "samsung", "android": "13", "user_agent": "Dalvik/2.1.0 (Linux; U; Android 13; SM-G991B Build/TP1A.220624.014)"},
    {"model": "M2101K7AG", "brand": "Xiaomi", "android": "12", "user_agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2101K7AG Build/SKQ1.210908.001)"},
]

def get_random_device():
    return random.choice(DEVICE_POOL)

# ==================== STRIP PROXY HEADERS ====================
def strip_proxy_headers(headers):
    PROXY_HEADERS = [
        'Via', 'X-Forwarded-For', 'X-Forwarded-Proto', 'X-Forwarded-Host',
        'X-Real-IP', 'X-Proxy-ID', 'Forwarded', 'Proxy-Connection',
        'X-Original-Forwarded-For', 'X-Originating-IP', 'X-Remote-IP',
        'X-Remote-Addr', 'X-Client-IP', 'X-Host', 'X-Forwarded-Server',
        'CF-Connecting-IP', 'True-Client-IP', 'X-Forwarded-For-Original',
        'X-Forwarded-For-Source', 'X-Forwarded-For-Server'
    ]
    
    for header in PROXY_HEADERS:
        headers.pop(header, None)
        headers.pop(header.lower(), None)
    
    headers.pop('Server', None)
    return headers

# ==================== ENCRYPTION ====================
def encrypt_proto(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    padded = pad(data, AES.block_size)
    return cipher.encrypt(padded)

# ==================== PROTOBUF FUNCTIONS ====================
def build_major_login_proto(open_id, access_token, region="IND"):
    if USE_PB2:
        try:
            major_login = MajoRLoGinrEq_pb2.MajorLogin()
            
            major_login.event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            major_login.game_name = "free fire"
            major_login.platform_id = 1
            major_login.client_version = "1.126.9"
            major_login.system_software = "Android OS 13 / API-33 (TP1A.220905.001/R.206769c-2)"
            major_login.system_hardware = "Handheld"
            major_login.telecom_operator = "45403"
            major_login.network_type = "WIFI"
            major_login.screen_width = 1280
            major_login.screen_height = 720
            major_login.screen_dpi = "320"
            major_login.processor_details = "ARM64 FP ASIMD AES | 2352 | 8"
            major_login.memory = 128
            major_login.gpu_renderer = "Mali-G610"
            major_login.gpu_version = "OpenGL ES 3.2 v1.g18p0-01eac0.2d5e200a1514bdef1a4909db66e37e28"
            major_login.unique_device_id = f"Google|{random.getrandbits(128):032x}"
            major_login.client_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            major_login.language = "en"
            major_login.open_id = open_id
            major_login.open_id_type = "4"
            major_login.device_type = "Handheld"
            major_login.device_model = "OPPO CPH2217"
            
            if region and region != "auto":
                major_login.region = region
            
            major_login.access_token = access_token
            major_login.platform_sdk_id = 1
            major_login.network_operator_a = "45403"
            major_login.network_type_a = "WIFI"
            major_login.client_using_version = "1ac4b80ecf0478a44203bf8fac6120f5"
            major_login.external_storage_total = 20660
            major_login.external_storage_available = 17445
            major_login.internal_storage_total = 2663
            major_login.internal_storage_available = 1500
            major_login.game_disk_storage_available = 17573
            major_login.game_disk_storage_total = 20660
            major_login.external_sdcard_avail_storage = 17573
            major_login.external_sdcard_total_storage = 20660
            major_login.login_by = 3
            major_login.library_path = "/data/app/~~xHaSHUdUBlxvhJaRWh018A==/com.dts.freefireth-4OBn7-sLMoPuswIfmgixhA==/lib/arm64"
            major_login.reg_avatar = 1
            major_login.library_token = f"{hashlib.md5(str(random.random()).encode()).hexdigest()}|/data/app/~~xHaSHUdUBlxvhJaRWh018A==/com.dts.freefireth-4OBn7-sLMoPuswIfmgixhA==/base.apk"
            major_login.channel_type = 6
            major_login.cpu_type = 2
            major_login.cpu_architecture = "64"
            major_login.client_version_code = "2019120816"
            major_login.graphics_api = "OpenGLES2"
            major_login.supported_astc_bitset = 16383
            major_login.login_open_id_type = 4
            major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
            major_login.loading_time = 25777
            major_login.release_channel = "3rd_party"
            major_login.extra_info = "KqsHTz+zAigQ0BOzKhQHN8ae/IefLXcroDjaj4QY+OF71nTuiQh+myDUqCZFPJQ5gyC9LfEeKoon9d461764VIGguRHcIyKfExGAh4bvxFZRgp2X"
            major_login.extra_json = '{"cur_rate":null,"support_etc2":false}'
            major_login.android_engine_init_flag = 110009
            major_login.if_push = 1
            major_login.is_vpn = 1
            major_login.origin_platform_type = "4"
            major_login.primary_platform_type = "4"
            major_login.unknown_bytes102 = b"E1JMTwcJXjA2"
            
            return major_login.SerializeToString()
            
        except Exception as e:
            print(f"PB2 error: {e}")
    
    return build_simple_proto(open_id, access_token, region)

def build_simple_proto(open_id, access_token, region="IND"):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def encode_varint(n):
        result = []
        while True:
            b = n & 0x7F
            n >>= 7
            if n:
                result.append(b | 0x80)
            else:
                result.append(b)
                break
        return bytes(result)
    
    def build_field(field_num, value):
        if isinstance(value, int):
            tag = (field_num << 3) | 0
            return encode_varint(tag) + encode_varint(value)
        elif isinstance(value, (str, bytes)):
            data = value.encode() if isinstance(value, str) else value
            tag = (field_num << 3) | 2
            return encode_varint(tag) + encode_varint(len(data)) + data
        return b''
    
    fields = {
        3: now, 4: "free fire", 5: 1,
        7: "1.126.9",
        8: "Android OS 13 / API-33",
        9: "Handheld", 10: "45403",
        11: "WIFI", 22: open_id,
        29: access_token, 26: region.upper()
    }
    
    payload = b''
    for k, v in fields.items():
        payload += build_field(k, v)
    
    return payload

def parse_major_login_response(data):
    try:
        if USE_PB2:
            try:
                response = MajoRLoGinrEs_pb2.MajorLoginRes()
                response.ParseFromString(data)
                if response.token:
                    return response.token
            except:
                pass
        
        text = data.decode('utf-8', errors='ignore')
        jwt_match = re.search(r'eyJ[a-zA-Z0-9\-_=]+\.[a-zA-Z0-9\-_=]+\.?[a-zA-Z0-9\-_.+/=]*', text)
        if jwt_match:
            return jwt_match.group()
    except:
        pass
    return None

# ==================== FLASK APP ====================
app = Flask(__name__)
sessions = {}
user_sessions = {}

# ==================== PROXY HANDLER ====================
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_handler(path=""):
    parts = path.split('/')
    session_id = parts[0] if parts and parts[0] in sessions else None
    if not session_id:
        return jsonify({"error": "No active session"}), 404
    
    session_data = sessions[session_id]
    device = get_random_device()
    
    if "MajorLogin" in path:
        if not session_data.get('open_id'):
            return jsonify({"error": "No open_id"}), 400
        
        print(f"[Proxy] MajorLogin with open_id: {session_data['open_id'][:10]}...")
        
        proto_data = build_major_login_proto(
            session_data['open_id'],
            session_data['access_token'],
            session_data.get('region', 'IND')
        )
        encrypted = encrypt_proto(proto_data)
        
        headers = {
            "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2022.3.47f1",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "loginbp.ggpolarbear.com",
            "ReleaseVersion": "OB54",
            "X-GA": "v1 1",
            "Authorization": "Bearer"
        }
        
        headers = strip_proxy_headers(headers)
        
        try:
            resp = requests.post(
                "https://loginbp.ggpolarbear.com/MajorLogin",
                headers=headers,
                data=encrypted,
                verify=False,
                timeout=15
            )
            print(f"[Proxy] MajorLogin Status: {resp.status_code}")
            
            if resp.status_code == 200:
                jwt = parse_major_login_response(resp.content)
                if jwt:
                    session_data['jwt_token'] = jwt
                    print(f"[Proxy] ✅ JWT: {jwt[:30]}...")
                return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
            else:
                return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
        except Exception as e:
            print(f"[Proxy] MajorLogin error: {e}")
            return jsonify({"error": str(e)}), 500
    
    elif "GetLoginData" in path:
        if not session_data.get('jwt_token'):
            return jsonify({"error": "No JWT"}), 400
        
        print(f"[Proxy] GetLoginData with JWT: {session_data['jwt_token'][:30]}...")
        
        proto_data = build_major_login_proto(
            "24adf2d6806cf61bd95d4cd3b57a0bd9",
            session_data['jwt_token'],
            session_data.get('region', 'IND')
        )
        encrypted = encrypt_proto(proto_data)
        
        if session_data.get('region', 'IND').upper() == "IND":
            url = "https://client.ind.freefiremobile.com/GetLoginData"
            host = "client.ind.freefiremobile.com"
        else:
            url = "https://clientbp.ggpolarbear.com/GetLoginData"
            host = "clientbp.ggpolarbear.com"
        
        headers = {
            "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
            "X-Unity-Version": "2022.3.47f1",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": host,
            "ReleaseVersion": "OB54",
            "X-GA": "v1 1",
            "Authorization": f"Bearer {session_data['jwt_token']}"
        }
        
        headers = strip_proxy_headers(headers)
        
        try:
            resp = requests.post(url, headers=headers, data=encrypted, verify=False, timeout=15)
            print(f"[Proxy] GetLoginData Status: {resp.status_code}")
            return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
        except Exception as e:
            print(f"[Proxy] GetLoginData error: {e}")
            return jsonify({"error": str(e)}), 500
    
    elif "GetAccountBriefInfoBeforeLogin" in path:
        return Response(status=200)
    
    elif "Ping" in path:
        return Response(status=200)
    
    else:
        print(f"[Proxy] Unknown endpoint: {path}")
        return Response(status=200)

# ==================== SESSION MANAGEMENT ====================
@app.route('/create_session', methods=['POST'])
def create_session():
    data = request.json or {}
    access_token = data.get('access_token')
    open_id = data.get('open_id', '')
    region = data.get('region', 'IND')
    uid = data.get('uid', '')
    user_id = data.get('user_id', '')
    
    if not access_token:
        return jsonify({"error": "access_token required"}), 400
    
    if user_id and user_id in user_sessions:
        return jsonify({
            "status": "error",
            "message": "You already have an active session! Please use /stop to end it first."
        }), 409
    
    session_id = base64.b64encode(access_token[:16].encode()).decode()[:8]
    sessions[session_id] = {
        'access_token': access_token,
        'open_id': open_id,
        'region': region.upper(),
        'uid': uid,
        'jwt_token': None,
        'created': datetime.now().isoformat()
    }
    
    if user_id:
        user_sessions[user_id] = session_id
    
    return jsonify({
        "status": "success",
        "session_id": session_id,
        "open_id": open_id
    })

@app.route('/get_session/<session_id>', methods=['GET'])
def get_session(session_id):
    if session_id in sessions:
        return jsonify(sessions[session_id])
    return jsonify({"error": "Session not found"}), 404

@app.route('/delete_session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    if session_id in sessions:
        del sessions[session_id]
        for user_id, sid in list(user_sessions.items()):
            if sid == session_id:
                del user_sessions[user_id]
                break
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Session not found"}), 404

@app.route('/stop_user_session', methods=['POST'])
def stop_user_session():
    data = request.json or {}
    user_id = data.get('user_id')
    
    if user_id and user_id in user_sessions:
        session_id = user_sessions[user_id]
        if session_id in sessions:
            del sessions[session_id]
        del user_sessions[user_id]
        return jsonify({"status": "stopped"})
    
    return jsonify({"error": "No active session found"}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(sessions),
        "active_users": len(user_sessions)
    })

@app.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        "total_sessions": len(sessions),
        "total_users": len(user_sessions),
        "sessions": list(sessions.keys())[:10]
    })

# ==================== MAIN ====================
def main():
    print("🎮 FF PROXY BACKEND - RAILWAY READY")
    print(f"🔌 Port: {PROXY_PORT}")
    print(f"🛡️ Proxy Headers: STRIPPED")
    print(f"📦 PB2: {'✅' if USE_PB2 else '⚠️'}")
    
    app.run(host='0.0.0.0', port=PROXY_PORT, debug=False, threaded=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Stopped")
        sys.exit(0)
