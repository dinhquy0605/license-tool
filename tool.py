import sys
import subprocess
import requests
import uuid

# ================= CẤU HÌNH TOOL =================
CURRENT_VERSION = "v1.0.0"  # Phiên bản hiện tại của tool
SERVER_URL = "https://wandering-snow-c84a.seothgroup6868.workers.dev"
# =================================================

def check_update():
    """Kiểm tra xem máy chủ có phiên bản mới hơn không"""
    try:
        res = requests.get(f"{SERVER_URL}/api/check-update", timeout=5)
        if res.status_code == 200:
            data = res.json()
            latest_version = data.get("latestVersion")
            if latest_version and latest_version != CURRENT_VERSION:
                print("=" * 60)
                print(f"⚠️  CẢNH BÁO: ĐÃ CÓ BẢN CẬP NHẬT MỚI: {latest_version} (Bản hiện tại: {CURRENT_VERSION})")
                print(f"🔗 Tải bản mới tại: {data.get('downloadUrl')}")
                print(f"📝 Nội dung mới: {data.get('changelog')}")
                print("=" * 60)
                print()
    except Exception:
        # Nếu mất mạng hoặc lỗi server kiểm tra update thì bỏ qua để tiếp tục
        pass

def get_hwid():
    """Lấy Hardware ID duy nhất của máy Windows"""
    try:
        output = subprocess.check_output("wmic csproduct get uuid", shell=True).decode()
        hwid = output.split("\n")[1].strip()
        if hwid:
            return hwid
    except Exception:
        pass
    return str(uuid.getnode())

def verify_license(key):
    """Gửi Key + HWID lên Cloudflare để kích hoạt hoặc kiểm tra"""
    hwid = get_hwid()
    try:
        res = requests.post(
            f"{SERVER_URL}/api/verify-license",
            json={"key": key, "hwid": hwid, "currentVersion": CURRENT_VERSION},
            timeout=10
        )
        return res.json()
    except Exception as e:
        return {"success": False, "message": f"Không thể kết nối máy chủ xác thực: {e}"}

def main():
    print(f"==================================================")
    print(f"          TOOL QUẢN LÝ TỰ ĐỘNG - {CURRENT_VERSION}")
    print(f"==================================================\n")

    # 1. Tự động kiểm tra bản v1 hay v2
    check_update()

    # 2. Bắt buộc nhập Key bản quyền
    user_key = input("👉 Vui lòng nhập License Key: ").strip()
    if not user_key:
        print("❌ Key không được để trống!")
        sys.exit(1)

    print("\n⏳ Đang kiểm tra bản quyền (HWID + IP)...")
    result = verify_license(user_key)

    if result.get("success"):
        print("✅ KÍCH HOẠT THÀNH CÔNG! BẢN QUYỀN HỢP LỆ.")
        print(f"Thông báo: {result.get('message')}\n")
        
        # BẮT ĐẦU CHẠY CÁC CHỨC NĂNG CỦA TOOL TẠI ĐÂY
        print("🎉 Chào mừng bạn! Tool đang bắt đầu thực thi nhiệm vụ...")
        input("\nNhấn Enter để thoát tool...")
    else:
        print(f"❌ XÁC THỰC THẤT BẠI: {result.get('message')}")
        input("\nNhấn Enter để thoát...")
        sys.exit(1)

if __name__ == "__main__":
    main()
