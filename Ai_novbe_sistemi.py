import streamlit as st
import numpy as np
import pandas as pd
import random
import os 
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import gizli
from datetime import datetime, timedelta
import time  
import matplotlib.pyplot as plt

# Moderator və Administratorun məlumatları (username → password)
USERS = {
    "moderator": "moderator123",
    "administrator": "administrator123"
}

# İstifadəçi rolunu yadda saxla
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

# İstifadəçilər üçün giriş ekranı
if not st.session_state.authenticated:
    st.title("🔒 Giriş")

    username = st.text_input("İstifadəçi adı")
    password = st.text_input("Şifrə", type="password")

    if st.button("🔑 Giriş"):
        if username in USERS and USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.user_role = username  # İstifadəçi rolunu təyin et
            st.rerun()  # Səhifəni yenilə, yeni vəziyyəti göstər
        else:
                st.error("❌ Yanlış istifadəçi adı və ya şifrə.")
   
    st.stop()  # Əgər giriş edilməyibsə, tətbiq davam etmir

# Giriş uğurludursa: İstifadəçi roluna görə mesaj göstər
st.success(f"✅ Giriş uğurla tamamlandı! Xoş gəldiniz, **{st.session_state.user_role}**.")

if st.session_state.user_role == "moderator":
    st.info("🔹 Moderatorsunuz, müəyyən əməliyyatları yerinə yetirə bilərsiniz.")
elif st.session_state.user_role == "administrator":
    st.warning("⚡ Administratorsunuz, bütün səlahiyyətlərə maliksiniz.")

# Fayl yollarını təyin edirik
april_file_path = r"Datalar\april.xlsx"
may_file_path = r"Datalar\may.xlsx"
june_file_path = r"Datalar\iyun.xlsx"
july_file_path = r"Datalar\iyul.xlsx"
august_file_path = r"Datalar\avqust.xlsx"
september_file_path = r"Datalar\sentyabr.xlsx"
october_file_path = r"Datalar\oktyabr.xlsx"
november_file_path = r"Datalar\noyabr.xlsx"
december_file_path = r"Datalar\dekabr.xlsx"

employes_file_path = r"Datalar\employes.xlsx"
old_file_path = r"Datalar\old.xlsx"

# Excel fayllarını oxuyuruq
april_df = pd.read_excel(april_file_path)
may_df = pd.read_excel(may_file_path)
june_df = pd.read_excel(june_file_path)
july_df = pd.read_excel(july_file_path)
august_df = pd.read_excel(august_file_path)
september_df = pd.read_excel(september_file_path)
october_df = pd.read_excel(october_file_path)
november_df = pd.read_excel(november_file_path)
december_df = pd.read_excel(december_file_path)

employes_df = pd.read_excel(employes_file_path)
old_df = pd.read_excel(old_file_path)

# Əgər session_state-də ay seçilməyibsə, onu təyin edirik
if "selected_month" not in st.session_state:
    st.session_state.selected_month = None

# **Giriş Ekranı:**
if st.session_state.selected_month is None:
    st.title("📅 Ay Seçim Ekranı")

    # Selectbox - Ay seçimi
    selected_month = st.selectbox(
        "Hansı ayın məlumatlarını görmək istəyirsiniz?",
        ["Aprel", "May", "İyun", "İyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]
    )

    # Davam et düyməsi
    if st.button("⏩ Davam et"):
        st.session_state.selected_month = selected_month  # Seçilən ayı yadda saxlayırıq
        st.rerun()  # Səhifəni yeniləyirik ki, yeni vəziyyət əks olunsun

    st.stop()  # Əgər ay seçilməyibsə, buradan aşağıdakı kod işləməyəcək

# **Əsas Ekran - Ay seçildikdən sonra görünəcək**
st.success(f"✅ Seçilmiş ay: **{st.session_state.selected_month}**")

# Seçilən aya uyğun cədvəli təyin edirik
if st.session_state.selected_month == "Aprel":
    all_days = april_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "May":
    all_days = may_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "İyun":
    all_days = june_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "İyul":
    all_days = july_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "Avqust":
    all_days = august_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "Sentyabr":
    all_days = september_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "Oktyabr":
    all_days = october_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "Noyabr":
    all_days = november_df[['Tarix', 'Gün']]
elif st.session_state.selected_month == "Dekabr":
    all_days = december_df[['Tarix', 'Gün']]

def main():
    # Başlıq 
    st.markdown(
        """
        <h2 style='color: red; text-align: center; white-space: nowrap;'> 
            Süni İntellekt əsaslı növbə planlaşdırma sistemi 
        </h2>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='color: green; text-align: center; font-size: 16px; white-space: nowrap;'> 
             Bu sistem keçmiş ayları nəzərə alaraq gələcək aylar üçün avtomatik növbə təyin edir.
        </p>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

# **Ayı dəyişmək üçün düymə əlavə edirik**
if st.button("🔄 Ayı dəyiş"):
    st.session_state.selected_month = None  # Seçimi sıfırlayırıq
    st.rerun()  # Səhifəni yeniləyirik ki, seçim ekranı yenidən gəlsin

# Cədvəli göstər
st.dataframe(all_days)

# İşçi məlumatlarını bir listə əlavə edirik.
workers = employes_df['İşçi'].tolist()

# Keçmiş verilənlər 
past_data = dict(zip(old_df['Tarix'].astype(str), old_df['İşçi']))

# Keçmiş iş sayı
past_assignments = {worker: list(past_data.values()).count(worker) for worker in workers}

# İstisna günlər üçün istifadəçi interfeysi
st.sidebar.title("📅 İşçi Məzuniyyət və Ezamiyyət Planı")
apply_changes = st.sidebar.button("🔄 Cədvəli yenilə", key='apply_changes')

unavailable_workers = {}
for worker in workers:
    unavailable_dates = st.sidebar.multiselect(f"{worker} üçün işləmək mümkün olmayan günlər:", all_days['Tarix'].dt.strftime('%Y-%m-%d').tolist(), key=worker)
    unavailable_workers[worker] = set(unavailable_dates)  # Daha sürətli yoxlama üçün set istifadə edirik
    
# Genetik alqoritm funksiyası 
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
GENERATIONS = 200

def fitness(schedule):
    worker_counts = {worker: 0 for worker in workers}
    penalty = 0
    for worker in schedule:
        worker_counts[worker] += 1
    max_count = max(worker_counts.values())
    min_count = min(worker_counts.values())
    fairness = max_count - min_count
    return -fairness - penalty

def generate_population():
    population = []
    for _ in range(POPULATION_SIZE):
        schedule = []
        for date in all_days['Tarix'].astype(str):
            available_workers = [w for w in workers if date not in unavailable_workers.get(w, set())]
            if available_workers:
                schedule.append(random.choice(available_workers))
            else:
                schedule.append(random.choice(workers))  # Alternativ tapılmasa, təsadüfi işçi seçilir
        population.append(schedule)
    return population

def crossover(parent1, parent2):
    point = random.randint(0, len(all_days) - 1)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(schedule):
    if random.random() < MUTATION_RATE:
        index = random.randint(0, len(schedule) - 1)
        available_workers = [w for w in workers if str(all_days.iloc[index]['Tarix']) not in unavailable_workers.get(w, set())]
        if available_workers:
            schedule[index] = random.choice(available_workers)
    return schedule

def genetic_algorithm():
    population = generate_population()
    for _ in range(GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        new_population = population[:10]  # Ən yaxşı fərdlər
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:20], 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        population = new_population
    return population[0]

# Ən yaxşı cədvəli tap
best_schedule = genetic_algorithm()

# Cədvəli dataframe-ə çevirək
schedule_df = pd.DataFrame(zip(all_days['Tarix'], all_days['Gün'], best_schedule),
                           columns=['Tarix', 'Gün', 'İşçi'])

# **Final yoxlama: məhdudiyyət pozuntularını düzəltmək**
invalid_entries = []

# Yoxlama - işçilərin təyin olunduğu günlərdə işçinin işləməməli olduğu günlərin olub-olmaması
for index, row in schedule_df.iterrows():
    date = str(row['Tarix'])
    worker = row['İşçi']
    
    # İstisna günlərini yoxlama
    if worker in unavailable_workers:
        if date in unavailable_workers[worker]:
            # Bu işçi həmin tarixdə işləməməlidir, alternativ işçi tapmalıyıq
            available_workers = [w for w in workers if date not in unavailable_workers.get(w, set())]
            
            if available_workers:
                # Alternativ işçi tapılıb, təyin edilir
                schedule_df.at[index, 'İşçi'] = random.choice(available_workers)
                invalid_entries.append(f"{worker} işçisi {date} tarixində işləyə bilməz, yeni işçi təyin olundu.")
            else:
                # Alternativ işçi tapılmırsa, heç bir məhdudiyyəti olmayan işçi ilə əvəz edilir
                available_workers = [w for w in workers if not unavailable_workers.get(w, set())]
                if available_workers:
                    schedule_df.at[index, 'İşçi'] = random.choice(available_workers)
                    invalid_entries.append(f"{worker} işçisi {date} tarixində işləyə bilməz, heç bir məhdudiyyəti olmayan işçi ilə əvəz olundu.")
                else:
                    # Heç bir işçi tapılmadıqda, təkrar işçi seçirik
                    schedule_df.at[index, 'İşçi'] = random.choice(workers)
                    invalid_entries.append(f"{worker} işçisi {date} tarixində işləyə bilməz, heç bir alternativ tapılmadı, yeni işçi təyin olundu.")

# Unikal işçiləri saxlamaq üçün set
unique_workers_for_special_days = set()

# "Bazar" və "İstirahət günü" günlərinin tarixlərini tapırıq
special_days = schedule_df[schedule_df['Gün'].isin(['Bazar', 'İstirahət günü'])]

# Mövcud işçilər
all_workers = set(employes_df['İşçi'])

# Təkrarlanan işçilər üçün siyahı
repeated_workers = []

# Hər "Bazar" və "İstirahət günü" üçün işçi təyini
for index, row in special_days.iterrows():
    # "Bazar" və "İstirahət günü" üçün hələ təyin edilməmiş işçilərdən seçim edirik
    available_workers = list(all_workers - unique_workers_for_special_days)

    # Təkrarlanmayan və həmin gün işləyə bilməyən işçiləri filtIrləyirik
    available_workers = [worker for worker in available_workers if row['Tarix'].strftime('%Y-%m-%d') not in unavailable_workers.get(worker, set())]

    # Yalnız mövcud işçilərdən təkrarlanmayacaq birini seçirik
    if available_workers:
        selected_worker = random.choice(available_workers)  # Mövcud işçilərdən təsadüfi seçim
        schedule_df.at[index, 'İşçi'] = selected_worker
        unique_workers_for_special_days.add(selected_worker)  # Seçilmiş işçini əlavə edirik
    else:
        # Təkrarlanan işçi tapıldıqda siyahıya əlavə edirik
        repeated_workers.append(f"Tekrarlanan işçi tapıldı: {row['Tarix']} tarixində, işçi {schedule_df.at[index, 'İşçi']} təkrarlanır.")

# Yadda saxlanacaq faylın adı
LAST_DF_FILE = "last_schedule.xlsx"

# Əgər fayl varsa, içindəki məlumatı oxu, yoxdursa, boş dataframe yarat
if os.path.exists(LAST_DF_FILE):
    last_df = pd.read_excel(LAST_DF_FILE)
else:
    last_df = pd.DataFrame(columns=["Tarix", "Gün", "İşçi"])

# Session state-də last_df yoxdursa, fayldan oxunanı ora yaz
st.session_state.setdefault('last_df', last_df.copy())

# **Cədvəli dataframe-ə çevirək**
schedule_df = pd.DataFrame(zip(all_days['Tarix'], all_days['Gün'], schedule_df['İşçi']),
                           columns=['Tarix', 'Gün', 'İşçi'])

# **Final yoxlama və dəyişikliklərin yadda saxlanması**
if apply_changes:
    st.session_state['last_df'] = schedule_df

# **Yadda saxla düyməsi**
save_button = st.button("💾 Yadda Saxla")

# **Mövcud Cədvəl (Dəyişiklik edilə bilər)**
st.write("### 📑 Mövcud Cədvəl ✍️ – Redaktə edə bilərsən!")
edited_schedule = st.data_editor(st.session_state['last_df'], num_rows="dynamic", key="editable_table_1")

# **Dəyişiklik olduqda avtomatik yadda saxla və yaxud Yadda saxla düyməsinə basanda yadda saxlanılması**
if save_button or not edited_schedule.equals(st.session_state['last_df']):
    st.session_state['last_df'] = edited_schedule
    edited_schedule.to_excel(LAST_DF_FILE, index=False)  # Excel faylına yalnız dəyişiklik olduqda yaz
    st.success("✅ Cədvəl dərhal yadda saxlandı!")

# **Son Yadda Saxlanmış Cədvəl (Dəyişiklik edilə bilməz)**
st.write("### 📁Yadda Saxlanmış Cədvəl 🔒(Dəyişiklik mümkün deyil)")
if os.path.exists(LAST_DF_FILE):
    last_saved_df = pd.read_excel(LAST_DF_FILE)
    st.dataframe(last_saved_df)
else:
    st.warning("⚠️ Hələ ki, yadda saxlanmış cədvəl yoxdur.")

# Cədvəl üçün işçiləri toplayırıq
worker_duties_all = last_saved_df['İşçi'].value_counts()

if st.button("📊 Qrafiki göstər"):
    fig, ax = plt.subplots()
    worker_duties_all.plot(kind='bar', ax=ax)
    
    ax.set_title("Hər İşçinin Ümumi Növbətçilik Günləri")
    ax.set_xlabel("İşçi")
    ax.set_ylabel("Növbətçilik Günlərinin Sayı")
    
    st.pyplot(fig)

# Bazar günü növbətçi olan işçiləri tapırıq
bazar_day = last_saved_df[last_saved_df['Gün'] == 'Bazar']

# Bazar günü növbətçi olan işçilərə növbəti iş günü üçün istirahət veririk
rest_for_next_day = []

for _, row in bazar_day.iterrows():
    # Bazar günü növbətçi olan işçinin növbəti günü tapırıq
    next_day = last_saved_df[last_saved_df['Tarix'] == row['Tarix'] + pd.Timedelta(days=1)]
    
    if not next_day.empty and next_day['Gün'].iloc[0] == 'İş günü':
        # Bazar günü sonrakı gündə iş günü varsa, istirahət veririk
        next_day['Nəzarət'] = f"{row['İşçi']} bazar gününə növbə düşdüyü üçün, {next_day['Tarix'].iloc[0].strftime('%Y-%m-%d')} tarixində istirahət verilir."
        rest_for_next_day.append(next_day)

# Streamlit-də göstərmək üçün nəticəni birləşdiririk
rest_for_next_day_df = pd.concat(rest_for_next_day)

# "İşçi" sütununu silirik
rest_for_next_day_df = rest_for_next_day_df.drop(columns=['İşçi'])

# Streamlit ekranında nəticəni göstəririk
st.write("☀️ Bazar günü növbətçi olduqları üçün bazar ertəsi istirahət verilən işçilər")
st.dataframe(rest_for_next_day_df)

# **Fayla əlavə etmə funksiyası**
def append_to_old_file(last_df, old_file_path):
    # Tarix və İşçi sütunlarını seçirik
    new_data = last_df[['Tarix', 'İşçi']]
    
    # Əgər `old.xlsx` faylı mövcuddursa, onu oxuyuruq, yoxdursa boş dataframe yaradırıq
    if os.path.exists(old_file_path):
        old_df = pd.read_excel(old_file_path)
    else:
        old_df = pd.DataFrame(columns=["Tarix", "İşçi"])

    # Yeni məlumatları `old_df` cədvəlinə əlavə edirik
    updated_old_df = pd.concat([old_df, new_data], ignore_index=True)

    # Yenilənmiş məlumatları `old.xlsx` faylına yazırıq
    updated_old_df.to_excel(old_file_path, index=False)
    st.success("✅ Cari ayın məlumatları süni intellekt modelinin inkişafı üçün istifadəyə göndərildi!")

# **"Keçmiş verilənlərə əlavə et" düyməsi**
if st.button("💡 Süni intellekt modelini inkişaf etdir"):
    append_to_old_file(last_df, old_file_path)

# **Faylı e-poçtla göndərmək funksiyası**
def send_email_with_attachment(file_path, subject, message, sendto):
    mymail = gizli.mail
    password = gizli.password

    # E-poçt mesajını qur
    msg_mime = MIMEMultipart()
    msg_mime['From'] = mymail
    msg_mime['To'] = ", ".join(sendto)  # Bir neçə alıcı varsa, onları birləşdiririk
    msg_mime['Subject'] = subject

    # Mesaj mətnini əlavə et
    msg_mime.attach(MIMEText(message, 'plain'))

    # Excel faylını əlavə et
    with open(file_path, 'rb') as f:
        part = MIMEApplication(f.read(), _subtype="xlsx")
        part.add_header('Content-Disposition', 'attachment', filename=file_path)
        msg_mime.attach(part)

    # E-poçtu göndər
    mail = SMTP("smtp.gmail.com", 587)
    mail.ehlo()
    mail.starttls()
    mail.login(mymail, password)
    mail.sendmail(mymail, sendto, msg_mime.as_string())  # MIME mesajını göndəririk
    mail.quit()
    st.write("📨✅  E-poçt göndərildi.")
# **Faylı Göndər düyməsi**
if st.button("✉️ Növbə cədvəlini hərkəsə göndər"):
    # E-poçt göndərmək üçün məlumatları təyin et
    subject = "Növbə cədvəli"
    message = "Salam, yeni ayın növbə cədvəli sizə göndərilmişdir"
    sendto = gizli.kime  # Burada əlavə etmək istədiyiniz e-poçt ünvanlarını təyin edin

    # Yadda saxlanmış faylı e-poçtla göndər
    send_email_with_attachment(LAST_DF_FILE, subject, message, sendto)

# **Son Yadda Saxlanmış Cədvəli Yükləmə Düyməsi**
if os.path.exists(LAST_DF_FILE):
    with open(LAST_DF_FILE, "rb") as file:
        st.download_button(
            label="📥 Son Saxlanılmış Cədvəli Yüklə",
            data=file,
            file_name="last_schedule.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


# Məlumatları birləşdiririk
merged_df = pd.merge(last_saved_df, employes_df[['İşçi', 'Email']], on='İşçi', how='left')

# Email ünvanı olmayan işçilər üçün email ünvanı tapılmadı məlumatını əlavə edirik.
merged_df['Email'] = merged_df['Email'].fillna('Email tapılmadı')

# final_df
final_df = merged_df[['Tarix', 'İşçi', 'Email']]

# Streamlit ekranına məlumatları yazırıq
st.title("İşçi ve Email məlumatları")

edited_df = st.data_editor(final_df)

# E-poçt məlumatları gizli.py faylından alınır
sender_email = gizli.mail
password = gizli.password
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Mail ünvanlarını listə çeviririk
# final_df DataFrame-dən e-poçt ünvanlarını çıxararaq mails dəyişəninə təyin edin
mails = final_df['Email'].tolist()  # Mail ünvanlarını listə çeviririk

# Tarix sütununu datetime formatına çeviririk (əgər deyilsə)
final_df['Tarix'] = pd.to_datetime(final_df['Tarix']).dt.date

# E-poçt mesajını göndərən funksiya
def send_email(subject, message, sendto):
    # E-poçt mesajını qur
    msg_mime = MIMEMultipart()
    msg_mime['From'] = sender_email
    msg_mime['To'] = ", ".join(sendto)  # Birdən çox alıcı üçün
    msg_mime['Subject'] = subject

    # Mesaj mətnini əlavə et
    msg_mime.attach(MIMEText(message, 'plain'))

    # E-poçtu göndər
    mail = SMTP(smtp_server, smtp_port)
    mail.ehlo()
    mail.starttls()
    mail.login(sender_email, password)
    mail.sendmail(sender_email, sendto, msg_mime.as_string())  # MIME mesajını göndəririk
    mail.quit()

# Streamlit ilə interfeys
st.title("📧 Növbətçi email göndərmə sistemi")

# Başlama tarixini daxil etmək üçün Streamlit inputu
start_date = st.date_input("Başlama tarixini daxil edin:", datetime.today())

# Proqramın işləməsi üçün düymə
if st.button("🚀📨 Gündəlik email göndərmə prosesini başlat (Qeyd olunmuş tarixdən etibarən)"):
    # Hər 1 gün üçün tarixi yoxlamaq və mail göndərmək
    while True:
        today = datetime.today().date()
        if today == start_date - timedelta(days=1):  # Sabah növbətçi olanlar üçün
            # final_df-dəki tarixləri yoxlamaq
            uygun_emails = final_df[final_df['Tarix'] == start_date]['Email'].tolist()
            
            if uygun_emails:  # Əgər uyğun e-poçt ünvanları varsa
                subject = "Salam"
                message = "Salam, Sabah növbətçisiniz"
                
                # Mail ünvanlarına Salam mesajı göndər
                send_email(subject, message, uygun_emails)
                st.write(f"✅ E-poçt göndərildi: {', '.join(uygun_emails)}")
            else:
                st.write("⚠️ Bu gün növbətçi göndərilməsi üçün uyğun tarix deyil.")
            
            # Növbəti günün tarixini təyin et və proqramı 24 saat sonra işlət
            start_date = start_date + timedelta(days=1)  # Yeni tarix təyin edilir
            time.sleep(2)  # 24 saat gözləyirik (86400 saniyə)
        else:
            st.write("⚠️ Bu gün növbətçi göndərilməsi üçün uyğun tarix deyil.")
            time.sleep(2)  # 1 saat gözləyirik (3600 saniyə)
