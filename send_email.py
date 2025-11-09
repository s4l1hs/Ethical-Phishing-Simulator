#!/usr/bin/env python3

import smtplib
import ssl
import argparse
from email.message import EmailMessage
from email.utils import formataddr

def send_simulation_email(smtp_server, smtp_port, sender_email, sender_name, sender_password, receiver_email, subject, body_text, file_path=None):
    """
    Kimlik doğrulaması yaparak SMTP üzerinden etik phishing simülasyonu e-postası gönderir.
    """
    
    # --- 1. E-posta Mesajını Oluştur (Modern Yöntem) ---
    msg = EmailMessage()
    
    # Başlıklar
    msg['Subject'] = subject
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = receiver_email
    
    # Mesaj gövdesi (HTML veya plain text olabilir, HTML linkler için daha iyidir)
    # Bu örnekte plain text kullanıldı, HTML için add_alternative kullanabilirsiniz.
    msg.set_content(body_text)

    # --- 2. Eklentiyi (Attachment) Güvenli Yoldan Ekle ---
    if file_path:
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_name = f.name.split('/')[-1] # Sadece dosya adını al
            
            msg.add_attachment(file_data, 
                               maintype='application', 
                               subtype='octet-stream', 
                               filename=file_name)
            print(f"[*] Eklenti başarıyla yüklendi: {file_name}")
        except FileNotFoundError:
            print(f"[!] Hata: Eklenti dosyası bulunamadı: {file_path}")
            return
        except Exception as e:
            print(f"[!] Hata: Eklenti yüklenemedi: {e}")
            return

    # --- 3. Sunucuya Bağlan ve Gönder (Güvenli 'with' bloğu ile) ---
    context = ssl.create_default_context()
    
    try:
        print(f"[*] SMTP sunucusuna bağlanılıyor: {smtp_server}:{smtp_port}")
        # 'with' bloğu, bağlantının hata verse bile (server.quit()) güvenle kapanmasını sağlar
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)  # Güvenli bağlantıya yükselt (STARTTLS)
            server.ehlo()
            
            # --- ÖNEMLİ: Etik simülasyon için kimlik doğrulama ---
            try:
                server.login(sender_email, sender_password)
                print("[*] Kimlik doğrulama başarılı.")
            except smtplib.SMTPAuthenticationError:
                print("[!] Hata: Kimlik doğrulama başarısız. Kullanıcı adı veya şifre yanlış.")
                return

            # E-postayı gönder
            server.send_message(msg)
            print(f"[*] Simülasyon e-postası başarıyla gönderildi -> {receiver_email}")
            
    except smtplib.SMTPServerDisconnected:
        print("[!] Hata: Sunucu bağlantısı kesildi.")
    except ssl.SSLError:
        print("[!] Hata: SSL Hatası. Port 587 (STARTTLS) yerine 465 (SSL) mi denemelisiniz?")
    except Exception as e:
        print(f"[!] Genel bir hata oluştu: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ethical Phishing Simulator - Yetkili Testler İçin E-posta Gönderme Aracı",
        epilog="UYARI: Sadece eğitim ve yetkili penetrasyon testleri için kullanın."
    )
    
    # SMTP Ayarları
    parser.add_argument("--server", required=True, help="SMTP sunucu adresi (örn: smtp.gmail.com)")
    parser.add_argument("--port", type=int, default=587, help="SMTP port (örn: 587 STARTTLS için)")
    
    # Gönderen Kimlik Bilgileri (Yetkilendirme için)
    parser.add_argument("--user", required=True, help="Gönderen e-posta adresi (kimlik doğrulama için)")
    parser.add_argument("--name", required=True, help="Gönderen olarak görünecek isim (örn: 'IT Destek')")
    parser.add_argument("--password", "--pass", dest="password", required=True, help="Gönderen e-posta şifresi veya uygulama şifresi")
    
    # Hedef ve İçerik
    parser.add_argument("--to", required=True, help="Hedef e-posta adresi")
    parser.add_argument("--subject", required=True, help="E-posta konusu")
    parser.add_argument("--body", required=True, help="E-posta gövdesi (metin)")
    parser.add_argument("--attach", help="Eklenecek dosyanın yolu (opsiyonel)")
    
    args = parser.parse_args()
    
    send_simulation_email(
        smtp_server=args.server,
        smtp_port=args.port,
        sender_email=args.user,
        sender_name=args.name,
        sender_password=args.password,
        receiver_email=args.to,
        subject=args.subject,
        body_text=args.body,
        file_path=args.attach
    )