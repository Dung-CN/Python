from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import json, os, sys
import re
# ========== PYINSTALLER ==========
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS 
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
#============================================ FORMAT =======================================
# ===== VARIABLE GLOBAL ====
error_pw_label_1 = None
error_email_label_2 = None
error_pw_label_2 = None
error_email_label_3 = None
error_dob_label_3 = None
# ================================ INFORMATION FORMATH ================================
def check_password_1(password):
    is_valid = bool(re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#_]).+$', password))
    return is_valid
def check_email_2(email):
    is_valid = bool(re.fullmatch(r'\w+@\w+\.\w+$', email))
    return is_valid
def check_password_2(password):
    is_valid = bool(re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#_]).+$', password))
    return is_valid
def check_email_3(email):
    is_valid = bool(re.fullmatch(r'\w+@\w+\.\w+$', email))
    return is_valid
def check_dob_3(dob):
    is_valid = bool(re.fullmatch(r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/[0-9]{4}$', dob))
    return is_valid
def check_score(score):
    is_valid = bool(re.fullmatch(r'^(10(\.0+)?)|([0-9](\.\d+)?)$', score))
    return is_valid
def check_year(year):
    is_valid = re.fullmatch(r'(20\d{2}-(20\d{2}))', year)
    if not is_valid:
        return False
    y1, y2 = map(int, year.split('-'))
    return y2 == y1 + 1
#============================================DATABASE=======================================
WINDOWN_WIDTH = 700
WINDOWN_HEIGHT = 500
WINDOWN_POSION_RIGHT = 420
WINDOWN_POSION_DOWN = 110

USERS_FILE = "users.json"
PROFILE_FILE = "profile.json"
STUDY_RESULT = "study_result.json"
LEARNING_STATISTICS =  "learning_statistics.json"

DEFAULT_AVATAR = resource_path(os.path.join("Images", "nv.png"))


#============================================HÀM CHUNG=======================================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf8') as f:
            try:
                data = json.load(f)
                return data
            except:
                return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def load_user_data(file, username):
    if not os.path.exists(file):
        return {}
    with open(file, 'r', encoding='utf8') as f:
        try:
            data = json.load(f)
        except:
            return {}
    if isinstance(data, dict):
        return data.get(username, {})
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                if item.get("username") == username:
                    return item
        return {}
    return {}

# ===========PROFILE========
def _ensure_profile_file():
    if not os.path.exists(PROFILE_FILE):
        with open(PROFILE_FILE, "w", encoding="utf8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
            
def load_profile_for_user(username):
    _ensure_profile_file()
    with open(PROFILE_FILE, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if isinstance(data, dict):
        return data.get(username, {})
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("username") == username:
                return item
    return {}

def save_profile_for_user(username, profile_dict):
    _ensure_profile_file()
    with open(PROFILE_FILE, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if isinstance(data, list):
        tmp = {}
        for item in data:
            if isinstance(item, dict) and "username" in item:
                tmp[item["username"]] = item
        data = tmp
    data[username] = profile_dict
    with open(PROFILE_FILE, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =====================STUDY=============
def _ensure_study_file():
    if not os.path.exists(STUDY_RESULT):
        with open(STUDY_RESULT, "w", encoding="utf8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def load_study_courses(username):
    _ensure_study_file()
    with open(STUDY_RESULT, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if not isinstance(data, dict):
        data = {}
    return data.get(username, [])

def save_study_courses(username, courses_list):
    _ensure_study_file()
    with open(STUDY_RESULT, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if not isinstance(data, dict):
        data = {}
    data[username] = courses_list
    with open(STUDY_RESULT, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===============LEARNING=========
def _ensure_learning_file():
    if not os.path.exists(LEARNING_STATISTICS):
        with open(LEARNING_STATISTICS, "w", encoding="utf8") as f:
            json.dump({}, f, ensure_ascii=False, indent=2)

def load_learning_courses(username):
    _ensure_learning_file()
    with open(LEARNING_STATISTICS, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if not isinstance(data, dict):
        data = {}
    return data.get(username, [])

def save_learning_courses(username, courses_list):
    _ensure_learning_file()
    with open(LEARNING_STATISTICS, "r", encoding="utf8") as f:
        try:
            data = json.load(f)
        except:
            data = {}
    if not isinstance(data, dict):
        data = {}
    data[username] = courses_list
    with open(LEARNING_STATISTICS, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ====Calculate gpa====
def grade_to_4scale(gpa_10):
    gpa_10 = float(gpa_10)
    if gpa_10 >= 9: return 4.0
    if gpa_10 >= 8: return 3.5
    if gpa_10 >= 7: return 3.0
    if gpa_10 >= 6: return 2.5
    if gpa_10 >= 5: return 2.0
    if gpa_10 >= 4: return 1.5
    return 0.0

def calculate_gpa4(courses):       
    total_point = 0
    total_credit = 0
    for c in courses:
        try:
            credit = float(c.get("credit", 0))
            gpa_10 = float(c.get("average_score", 0))
            gpa_4 = grade_to_4scale(gpa_10)
            total_point += gpa_4 * credit
            total_credit += credit
        except:
            continue
    if total_credit == 0:
        return 0
    return round(total_point / total_credit, 2)

def generate_feedback(username, score_data):
    try:
        with open(LEARNING_STATISTICS, 'r', encoding="utf8") as f:
            data = json.load(f)
            user_data = data.get(username, [])
            if user_data:
                gpa = float(user_data[-1].get("gpa", 0))
            else:
                gpa = 0.0
    except:
        gpa = 0.0
    if not score_data:
        return "Không có dữ liệu để nhận xét"
    max_score = max(score_data.values())
    max_subjects = [subj for subj, s in score_data.items() if s == max_score]
    max_subjects_str = ", ".join(max_subjects)

    nhan_xet = f"**BÁO CÁO TỔNG QUAN HỌC TẬP:**\n\n"
    nhan_xet += f"Điểm GPA học kỳ 1 là **{gpa}**.\n"
    nhan_xet += (f"Điểm trung bình cao nhất là môn **{max_subjects_str}** với **{max_score}**.\n"
                 f"Bạn đã thể hiện sự nỗ lực và khả năng tốt ở lĩnh vực này.\n")
    try:
        with open(STUDY_RESULT, 'r', encoding="utf8") as f:
            data = json.load(f)
            course_average_score = data.get(username, [])
    except (FileNotFoundError, json.JSONDecodeError):
        course_average_score = []
    excellent, good, fair, average = [], [], [], []
    for item in course_average_score:
        avg = float(item.get("average_score", 0))
        name = item.get("course_name", "Unknown")
        if avg >= 9.0:
            excellent.append((name, avg))
        elif avg >= 8.0:
            good.append((name, avg))
        elif avg >= 6.5:
            fair.append((name, avg))
        else:
            average.append((name, avg))
    if excellent:
        nhan_xet += "Các môn Xuất sắc: " + ", ".join([s[0] for s in excellent]) + ". Thành tích học tập **RẤT TỐT**. Tiếp tục duy trì phong độ xuất sắc này và thử thách bản thân với những môn nâng cao!\n"
    if good:
        nhan_xet += "Các môn Giỏi: " + ", ".join([s[0] for s in good]) + ". Thành tích học tập **TỐT**, bạn học tốt nhưng vẫn còn cơ hội để đạt xuất sắc. Hãy tập trung vào những chi tiết nhỏ và luyện tập thêm để nâng cao.\n"
    if fair:
        nhan_xet += "Các môn Khá: " + ", ".join([s[0] for s in fair]) + ". Môn này có thành tích khá, bạn nên ôn tập kỹ hơn, làm thêm bài tập và tham khảo tài liệu để nâng điểm lên mức Giỏi.\n"
    if average:
        nhan_xet += "Cần chú ý cải thiện môn: " + ", ".join([s[0] for s in average]) + ". Bạn phải dành thời gian nhiều hơn cho môn này, sắp xếp lại lịch học của mình sao cho hợp lý, học đúng cách để cải thiện tốt nhất\n"
    return nhan_xet

#============================================LEARNING STATISTICS=======================================
def open_learning_statistics(root, username):
    root.withdraw()
    lst_win = Toplevel()
    lst_win.title("Thống kê học tập")
    lst_win.geometry("{}x{}+{}+{}".format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    lst_win.resizable(False, False)
    lst_win.configure(bg="#f5f5f5")
    # ====Scroolbar====
    main_canvas = Canvas(lst_win, bg="#f5f5f5")
    main_canvas.pack(side='left', fill='both', expand=True)
    y_scrollbar = ttk.Scrollbar(lst_win, orient="vertical", command=main_canvas.yview)
    y_scrollbar.pack(side='right', fill='y')
    main_canvas.configure(yscrollcommand=y_scrollbar.set)
    frame_content = Frame(main_canvas)
    frame_content_window = main_canvas.create_window((0,10), window=frame_content, anchor='nw')

    # ---- Cập nhật vùng cuộn, giữ frame_content rộng bằng canvas ----
    def update_scrollregion(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.itemconfig(frame_content_window, width=main_canvas.winfo_width())
    frame_content.bind("<Configure>", update_scrollregion)

    # ---- Cuộn chuột ----
    def on_mousewheel(event):
        main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    main_canvas.bind_all("<MouseWheel>", on_mousewheel)

    # ==== Frame Avatar + name + mssv ====
    frame = Frame(frame_content, relief="flat", bg="#CCFF99")
    frame.pack(padx=5, pady=5, fill="x")
    # ----Avatar----
    try:
        with open(PROFILE_FILE, 'r', encoding="utf8") as f:
            data = json.load(f)
            user_data = data.get(username, {})
            name = user_data.get("name", "Unknown Student")
            mssv = user_data.get("mssv", "Unknown MSSV")
            avatar_path = user_data.get("avatar_path", "")
    except:
        name = "Unknown Name"
        mssv = "Unknown Mssv"
        avatar_path = ""
    if avatar_path and os.path.exists(avatar_path):
        avatar_img = Image.open(avatar_path)
    elif os.path.exists(DEFAULT_AVATAR):
        avatar_img = Image.open(DEFAULT_AVATAR)
    else:
        avatar_img = Image.new("RGB", (160, 160), color="lightgray")
    avatar_img = avatar_img.resize((50, 50), Image.LANCZOS)
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = Label(frame, image=avatar_photo, bg='white', relief='flat')
    avatar_label.image = avatar_photo
    avatar_label.pack(side='left', padx=20)
    # ----Name + Mssv----
    info_frame = Frame(frame, relief='flat', bg="#CCFF99")
    info_frame.pack(side='left', anchor='w')
    name_label = Label(info_frame, bg="#CCFF99", text=name, font=('Abadi', 16, 'bold'))
    name_label.pack(anchor='w')
    mssv_label = Label(info_frame, bg="#CCFF99", text=mssv, font=('Abadi', 16, 'bold'))
    mssv_label.pack(anchor='w')

    # ====Treeview====
    cols = ('Năm học', 'HK', 'GPA', 'Tỷ lệ đạt môn', 'Xếp loại')
    tree_frame = Frame(frame_content, bg="#f5f5f5")
    tree_frame.pack(padx=10, pady=0, fill='both', expand=True)
    tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse', height=6)
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=100, anchor='center')
    tree.pack(side='left', fill='both', expand=True)

    # ----Điều chỉnh theo chiều rộng cửa sổ ----
    def resize_tree_columns(event):
        total_width = tree.winfo_width()
        col_width = total_width // len(cols)
        for c in cols:
            tree.column(c, width=col_width)
    tree.bind("<Configure>", resize_tree_columns)

    # ==== Đưa dl lên bảng ====
    courses = load_study_courses(username)
    school_years = sorted({c.get("school_year") for c in courses})
    semesters = sorted({c.get("semester") for c in courses})
    all_data = []
    for year in school_years:
        for sem in semesters:
            semesters_course = [c for c in courses if c.get("school_year")==year and c.get("semester")==sem]
            if not semesters_course:
                continue
            gpa_sem = calculate_gpa4(semesters_course)
            passed = sum(1 for c in semesters_course if float(c.get("average_score",0)) >= 5)
            total = len(semesters_course)
            pass_rate = f"({passed/total*100:.0f}%)"
            rank = "Xuất Sắc" if gpa_sem >= 3.6 else "Giỏi" if gpa_sem >= 3.2 else "Khá" if gpa_sem >= 2.5 else "Trung bình"
            tree.insert("", "end", values=(year, sem, gpa_sem, pass_rate, rank))
            stat_item = {"school_year": year, "semester": sem, "gpa": gpa_sem, "pass_rate": pass_rate, "rank": rank}
            all_data.append(stat_item)
    save_learning_courses(username, all_data)
    
    # ====Frame chứa chart====
    chart_frame = Frame(frame_content, bg="#f5f5f5")
    chart_frame.pack(pady=(10,40), anchor='center')
    chart_widget = None
    def chart():
        nonlocal chart_widget
        if chart_widget is None:
            courses = load_study_courses(username)
            course_names = [i.get("course_name", "Unknown") for i in courses]
            average_scores = [float(i.get("average_score", 0)) for i in courses]

            fig, ax = plt.subplots(figsize=(5.6, 3.68))
            ax.plot(course_names, average_scores, marker='o', color='red', linewidth=2)
            ax.set_ylim(0,10)
            ax.set_title("Điểm trung bình", fontsize=11, fontweight='bold')
            ax.set_xlabel("Môn học", fontsize=8)
            ax.set_ylabel("Điểm", fontsize=8)
            ax.grid(True, linestyle='--', alpha=0.6)
            for i, v in enumerate(average_scores):
                ax.text(i, v+0.1, f"{v:.1f}", ha='center', fontsize=8)
            canvas_chart = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas_chart.draw()
            chart_widget = canvas_chart.get_tk_widget()
            chart_widget.pack(anchor='w', pady=(5,0))
        else:
            chart_widget.destroy()
            chart_widget = None
    buton_chart = Button(chart_frame, text='Biểu đồ trực quan', font=('Abadi', 10, 'bold'), bg="#3498db", command=chart)
    buton_chart.pack(padx=10 ,pady=(10, 5), anchor='center')

    # ====Frame comment====
    comment_frame = Frame(frame_content, bg="#f5f5f5")
    comment_frame.pack(padx=10, pady=(0, 20), fill='x', expand=True)
    comment_text = Text(comment_frame, height=10, wrap='word', font=('Arial', 10))
    comment_text.pack(fill='both', expand=True)
    def show_feedback():
        try:
            with open(STUDY_RESULT, 'r', encoding="utf8") as f:
                data = json.load(f)
                score_data_list = data.get(username, [])
        except:
            score_data_list = []
        score_data = {item.get("course_name", "Unknown"): float(item.get("average_score", 0)) 
                  for item in score_data_list}
        feeback = generate_feedback(username, score_data)
        comment_text.delete('0.0', END)
        comment_text.insert(END, feeback)
    button_feedback = Button(comment_frame, text="Hiển thị nhận xét", font=('Abadi', 10, 'bold'),bg="#f39c12", command=show_feedback)
    button_feedback.pack(pady=5)

    def back_to_main():
        lst_win.destroy()
        root.deiconify()
    Button(lst_win, text="⬅ Quay lại", font=('Arial', 12), bg="#f44336", fg="white", command=back_to_main).place(x=10, y=460)
    lst_win.protocol("WM_DELETE_WINDOW", back_to_main) 

#============================================STUDY RESULT=======================================
def open_study_result(root, username):
    root.withdraw()
    std_win = Toplevel()

    std_win.title("Kết quả học tập")
    std_win.geometry("{}x{}+{}+{}".format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    std_win.resizable(False, False)
    std_win.configure(bg="#f5f5f5")
    # ====Frame avatar + name + mssv =====
    frame = Frame(std_win, relief="flat", bg="#CCFF99")
    frame.pack(padx=5, pady=5, fill='x')
    # ---- Avatar ----
    try:
        with open(PROFILE_FILE, 'r', encoding="utf8") as f:
            data = json.load(f)
            user_data = data.get(username, {})
            name = user_data.get("name", "Unknown Student")
            mssv = user_data.get("mssv", "Unknown MSSV")
            avatar_path = user_data.get("avatar_path", "")
    except:
        name = "Unknown Student"
        mssv = "Unknown MSSV"
        avatar_path = ""
    if avatar_path and os.path.exists(avatar_path):
        avatar_img = Image.open(avatar_path)
    elif os.path.exists(DEFAULT_AVATAR):
        avatar_img = Image.open(DEFAULT_AVATAR)
    else:
        avatar_img = Image.new("RGB", (160, 160), color="lightgray")
    avatar_img = avatar_img.resize((50, 50), Image.LANCZOS)
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = Label(frame, image=avatar_photo, bg="#CCFF99", relief="flat")
    avatar_label.image = avatar_photo
    avatar_label.pack(side="left", padx=20)
    # ---- Frame con chứa Tên + MSSV ----
    info_frame = Frame(frame, bg="#CCFF99")
    info_frame.pack(side="left", anchor="w")
    name_label = Label(info_frame, bg="#CCFF99", text=name, font=('Abadi', 16, 'bold'))
    name_label.pack(anchor="w")
    mssv_label = Label(info_frame, bg="#CCFF99", text=mssv, font=('Abadi', 12, 'bold'))
    mssv_label.pack(anchor="w")
    
    def calculate_average_score(att, mid, fin):
        try:
            att = float(att)    
            mid = float(mid)
            fin = float(fin)
            asc = att*0.1 + mid*0.2 + fin*0.7
            return round(asc, 2)
        except:
            return 0

    # ==== Thêm inf vào bảng ====
    def add_record():
        attendance_score = attendance_score_entry.get().strip()
        midterm_score = midterm_score_entry.get().strip()
        final_score = final_score_entry.get().strip()
        school_year = school_year_entry.get().strip()

        if not check_score(attendance_score):
            messagebox.showerror("", "Điểm chuyên cần không hợp lệ!")
            return
        elif not check_score(midterm_score):
            messagebox.showerror("", "Điểm GK không hợp lệ!")
            return
        elif not check_score(final_score):
            messagebox.showerror("", "Điểm CK không hợp lệ!")
            return
        if not check_year(school_year):
            messagebox.showerror("", "Năm học không hợp lệ!")
            return

        average_score = calculate_average_score(attendance_score_entry.get(), midterm_score_entry.get(), final_score_entry.get())
        data = (
            course_code_entry.get().strip(),
            course_name_entry.get().strip(),
            semester_entry.get().strip(),
            credit_entry.get().strip(),
            attendance_score_entry.get().strip(),
            midterm_score_entry.get().strip(),
            final_score_entry.get().strip(),
            average_score,
            school_year_entry.get().strip()
        )
        if not data[0] or not data[1]:
            return
        tree.insert("", "end", values=data)
        data_1 = (
            course_code_entry,
            course_name_entry,
            semester_entry,
            credit_entry,
            attendance_score_entry,
            midterm_score_entry,
            final_score_entry,
            school_year_entry
            )
        for i in data_1:
            i.delete(0, END)
    # ==== Save Json ====
    def save_json():
        all_data = []
        for item in tree.get_children():
            values = tree.item(item, "values")
            all_data.append(
                {
                "course_code": values[0],
                "course_name": values[1],
                "semester": values[2],
                "credit": values[3],
                "attendance_score": values[4],
                "midterm_score": values[5],
                "final_score": values[6],
                "average_score": values[7],
                "school_year": values[8]
                }
            )
        save_study_courses(username, all_data)
        messagebox.showinfo("Thông báo","Lưu dữ liệu thành công!")
    # ====Load json->tree ====
    def load_inf():
        courses = load_study_courses(username)
        for item in courses:
            tree.insert("","end", values=(
                item["course_code"],
                item["course_name"],
                item["semester"],
                item["credit"],
                item["attendance_score"],
                item["midterm_score"],
                item["final_score"],
                item.get("average_score", calculate_average_score(item["attendance_score"], item["midterm_score"], item["final_score"])),
                item["school_year"]
            ))
    # ==== Delete record =====
    def delete_record():
        selected = tree.focus()
        if not selected:
            return
        messagebox.showwarning("Thông báo", "Bạn chắc chắn muốn xóa Không!")
        tree.delete(selected)
        for e in [course_code_entry, course_name_entry, semester_entry, credit_entry,attendance_score_entry, midterm_score_entry, final_score_entry, school_year_entry]:
            e.delete(0, END)
        messagebox.showinfo("Thông báo", "Xóa thành công!")
    # ====Update record====
    def update_record():
        selected = tree.focus()
        if not selected:
            return
        average_score = calculate_average_score(attendance_score_entry.get(), midterm_score_entry.get(), final_score_entry.get())
        new_data = (
            course_code_entry.get().strip(),
            course_name_entry.get().strip(),
            semester_entry.get().strip(),
            credit_entry.get().strip(),
            attendance_score_entry.get().strip(),
            midterm_score_entry.get().strip(),
            final_score_entry.get().strip(),
            average_score,
            school_year_entry.get().strip()
        )
        tree.item(selected, values=new_data)
        data_1 = (
            course_code_entry,
            course_name_entry,
            semester_entry,
            credit_entry,
            attendance_score_entry,
            midterm_score_entry,
            final_score_entry,
            school_year_entry
            )
        for i in data_1:
            i.delete(0, END)
        messagebox.showinfo("Thông Báo", "Cập nhật thành công!")
          
    # ==== Frame Content ====
    frame_1 = Frame(std_win, relief="groove", bd=2, bg="#f5f5f5")
    frame_1.pack(padx=5, pady=5, fill='x')
    course_code_label = Label(frame_1, bg="#f5f5f5", text='Mã môn học',width=10,anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=0, padx=(10, 0), pady=10)
    course_code_entry = Entry(frame_1, width=15)
    course_code_entry.grid(row=1, column=1, pady=10)
    course_name_label = Label(frame_1, bg="#f5f5f5", text='Môn học',width=14, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=2, padx=(10, 0), pady=10)
    course_name_entry = Entry(frame_1, width=15)
    course_name_entry.grid(row=1, column=3, pady=10)
    semester_label = Label(frame_1, bg="#f5f5f5", text='Học kỳ',width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=4, padx=(10, 0), pady=10)
    semester_entry = Entry(frame_1, width=15)
    semester_entry.grid(row=1, column=5, pady=10)

    credit_label = Label(frame_1, bg="#f5f5f5", text='Số tín chỉ',width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=0, padx=(10, 0), pady=10)
    credit_entry = Entry(frame_1, width=15)
    credit_entry.grid(row=2, column=1, pady=10)
    attendance_score_label = Label(frame_1, bg="#f5f5f5", text='Điểm chuyên cần',width=14, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=2, padx=(10, 0), pady=10)
    attendance_score_entry = Entry(frame_1, width=15)
    attendance_score_entry.grid(row=2, column=3, pady=10)
    midterm_score_label = Label(frame_1, bg="#f5f5f5", text='Điểm GK',width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=4, padx=(10, 0), pady=10)
    midterm_score_entry = Entry(frame_1, width=15)
    midterm_score_entry.grid(row=2, column=5, pady=10)

    final_score_label = Label(frame_1, bg="#f5f5f5", text="Điểm CK",width=10, anchor='w', font=('Abadi', 12, 'bold')).grid(row=3, column=0, padx=(10, 0), pady=10)
    final_score_entry = Entry(frame_1, width=15)
    final_score_entry.grid(row=3, column=1, pady=10)
    school_year_label = Label(frame_1, bg="#f5f5f5", text='Năm học',width=14, anchor='w', font=('Abadi', 12, 'bold')).grid(row=3, column=2, padx=(10, 0) , pady=10)
    school_year_entry = Entry(frame_1, width=15)
    school_year_entry.grid(row=3, column=3, pady=10)

    # ====Treeview====
    cols = ('Mã môn học', 'Môn học', 'Học kỳ', 'Số TC','Điểm chuyên cần', 'Điểm GK', 'Điểm CK', 'Điểm TB', 'Năm học')
    tree_frame = Frame(std_win)
    tree_frame.pack(padx=10, pady=50, fill='both', expand=True)

    tree = ttk.Treeview(tree_frame, columns=cols, show='headings', selectmode='browse')
    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=len(c)*5, anchor='center')
    tree.pack(side='left', fill='both', expand=True)

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # === Khi click chọn dòng trong TreeView ===
    def on_tree_select(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        entries = [course_code_entry, course_name_entry, semester_entry, credit_entry,attendance_score_entry, midterm_score_entry, final_score_entry, school_year_entry]
        for e, v in zip(entries, [values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[8]]):
            e.delete(0, END)
            e.insert(0, v)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # ==== Nút Tùy Chỉnh ====
    button_1 = Button(std_win, bg="#27ae60", text='🆕 Thêm', width=9, font=('Abadi', 13, 'bold'), command=add_record).place(x=100, y=220)
    button_2 = Button(std_win, bg="#2980b9", text='💾 Lưu', width=9, font=('Abadi', 13, 'bold'), command=save_json).place(x=230, y=220)
    button_3 = Button(std_win, bg="#f39c12", text='🖉Cập Nhật', width=9, font=('Abadi', 13, 'bold'), command=update_record).place(x=360, y=220)
    button_3 = Button(std_win, bg="#e74c3c", text='🗑 Xóa', width=9, font=('Abadi', 13, 'bold'), command=delete_record).place(x=490, y=220)
    
    load_inf()
    def back_to_main():
        std_win.destroy()
        root.deiconify()
    Button(std_win, text="⬅ Quay lại", font=('Arial', 12), bg="#f44336", fg="white", command=back_to_main).place(x=10, y=460)
    std_win.protocol("WM_DELETE_WINDOW", back_to_main)

#============================================PROFILE=======================================
def open_profile(root, username):
    root.withdraw()
    pro_win = Toplevel()
    # ====Pro windown====
    pro_win.title('HỒ SƠ CÁ NHÂN')
    pro_win.geometry('{}x{}+{}+{}'.format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    pro_win.resizable(False, False)
    pro_win.configure(bg="#f5f5f5")
    # ====CONTENT====
    heading = Label(pro_win, text='Hồ Sơ Cá Nhân', font=('Arial', 20, 'bold'), bg="#f5f5f5")
    heading.pack(padx=10, pady=40)
    frame = Frame(pro_win, bg="#f5f5f5", relief=GROOVE, bd=2, pady=5)
    frame.pack(padx=15, fill='x')

    # ========================================================== AVATAR FRAME ==========================================================
    avatar_frame = Frame(frame, bg="#ffffff")
    avatar_frame.grid(row=0, column=0, rowspan=5, sticky='nw', padx=(10, 0))
    # ==== Hiển thị avatar mặc định ====
    try:
        if os.path.exists(DEFAULT_AVATAR):
            avatar_img = Image.open(DEFAULT_AVATAR)
        else:
            raise FileNotFoundError
    except Exception:
        avatar_img = Image.new('RGB', (160, 160), color='lightgray')

    avatar_img = avatar_img.resize((160, 160), Image.LANCZOS)
    avatar_photo = ImageTk.PhotoImage(avatar_img)
    avatar_label = Label(avatar_frame, image=avatar_photo, bg="#f5f5f5", relief="groove")
    avatar_photo.photo_default = avatar_photo
    avatar_photo.photo_current = avatar_photo
    avatar_label.image = avatar_photo
    avatar_label.pack(pady=5)

    # ==== Load Avatar ====
    def load_avatar():
        profile = load_profile_for_user(username)
        path = profile.get("avatar_path", DEFAULT_AVATAR)
        if not os.path.exists(path):
            path = DEFAULT_AVATAR if os.path.exists(DEFAULT_AVATAR) else ""
        try:
            new_img = Image.open(path).resize((160, 160), Image.LANCZOS)
        except:
            new_img = Image.new("RGB", (160, 160), color="lightgray")
        new_photo = ImageTk.PhotoImage(new_img)
        avatar_label.configure(image=new_photo)
        avatar_label.image = new_photo

    # ==== Change Avatar ====
    def change_avatar():
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh đại diện",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.ico")]
            )
        if file_path:
            new_img = Image.open(file_path).resize((160, 160), Image.LANCZOS)
            new_photo = ImageTk.PhotoImage(new_img)
            avatar_label.configure(image=new_photo)
            avatar_label.image = new_photo

            profile = load_profile_for_user(username) or {}
            profile["avatar_path"] = file_path
            save_profile_for_user(username, profile)
            load_avatar()

    # ========================================================== Save Inf ==========================================================
    def save_inf():
        global error_email_label_3, error_dob_label_3
        name = name_entry.get().strip()
        mssv = mssv_entry.get().strip()
        email = email_entry.get().strip()
        dob = date_of_birth_entry.get().strip()
        address = address_text.get("1.0", "end").strip()

        if not name or not mssv or not email or not dob or not address:
            messagebox.showerror("", "Vui lòng nhập thông tin đầy đủ!")
            return

        if error_email_label_3:
            error_email_label_3.destroy()
            error_email_label_3 = None
        if error_dob_label_3:
            error_dob_label_3.destroy()
            error_dob_label_3 = None
        if not check_dob_3(dob):
            error_dob_label_3 = Label(pro_win, text="Ngày sinh không hợp lệ!", fg="red")
            error_dob_label_3.place(x=315, y=260)
            return

        if not check_email_3(email):
            error_email_label_3 = Label(pro_win, text="Email không hợp lệ!", fg="red", relief='flat', bd=0)
            error_email_label_3.place(x=530, y=260)
            return
        profile = load_profile_for_user(username) or {}
        avatar_path = profile.get("avatar_path", DEFAULT_AVATAR)
        profile = {
            "avatar_path": avatar_path,
            "name": name_entry.get(),
            "mssv": mssv_entry.get(),
            "dob": date_of_birth_entry.get(),
            "email": email_entry.get(),
            "sex": gender.get(),
            "address": address_text.get("1.0", END).strip(),
        }
        save_profile_for_user(username, profile)
        messagebox.showinfo("Thành công", "Hồ sơ đã được lưu!")
    def load_inf():
        profile = load_profile_for_user(username)
        name_entry.insert(0, profile.get("name",""))
        mssv_entry.insert(0, profile.get("mssv",""))
        date_of_birth_entry.insert(0, profile.get("dob",""))
        email_entry.insert(0, profile.get("email",""))
        gender.set(profile.get("sex","Nam"))
        address_text.insert("1.0", profile.get("address",""))
    
    # ========================================================== Delete Profile ==========================================================
    def delete_inf():
        cofirm = messagebox.askyesno("Xác nhận","Bạn có chắc chắn muốn xóa tài khoản chứ?")
        if cofirm:
            with open(PROFILE_FILE, "w", encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            name_entry.delete(0, END)
            mssv_entry.delete(0, END)
            date_of_birth_entry.delete(0, END)
            email_entry.delete(0, END)
            gender.set('Nam')
            address_text.delete("1.0", END)

            with open(STUDY_RESULT, 'w', encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            with open(LEARNING_STATISTICS, 'w', encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
            with open(USERS_FILE, 'w', encoding="utf8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

        if os.path.exists(DEFAULT_AVATAR):
            default_img = Image.open(DEFAULT_AVATAR)
        else:
            default_img = Image.new("RGB", (160, 160), color="lightgray")

        default_img  = Image.open(DEFAULT_AVATAR).resize((160,160), Image.LANCZOS)
        avatar_photo = ImageTk.PhotoImage(default_img)
        avatar_label.configure(image=avatar_photo)
        avatar_label.photo_default = avatar_photo
        avatar_label.photo_current = avatar_photo
        avatar_label.image = avatar_photo

    Button(avatar_frame, text="🖼 Thay đổi ảnh", font=('Arial', 10, 'bold'),
        bg="#4CAF50", fg="white", command=change_avatar).pack(pady=5, fill='x')

    Button(avatar_frame, text="💾 Lưu hồ sơ", font=('Arial', 10, 'bold'),
        bg="#2196F3", fg="white", command=save_inf).pack(pady=5, fill='x')
    
    Button(avatar_frame, text="🗑 Xóa tài khoản", font=('Arial', 10, 'bold'),
        bg="#f44336", fg="white", command=delete_inf).pack(pady=5, fill='x')
    
    # ========================================================== INFORMATION ==========================================================
    # ====ROW 1====
    name_label = Label(frame,bg="#f5f5f5", text='Họ và tên:',width=8, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=1, pady=10)
    name_entry = Entry(frame, width=22)
    name_entry.grid(row=1, column=2, pady=10 )
    mssv_label = Label(frame,bg="#f5f5f5", text='MSSV:',width=5, anchor='w', font=('Abadi', 12, 'bold')).grid(row=1, column=3, pady=10)
    mssv_entry = Entry(frame, width=22)
    mssv_entry.grid(row=1, column=4, pady=10)
    # ====ROW 2====
    date_of_birth_label = Label(frame,bg="#f5f5f5", text='Ngày sinh:',width=8, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=1, pady=10)
    date_of_birth_entry = Entry(frame, width=22)
    date_of_birth_entry.grid(row=2, column=2, pady=10)
    email_label = Label(frame,bg="#f5f5f5", text='Email:',width=5, anchor='w', font=('Abadi', 12, 'bold')).grid(row=2, column=3, pady=10)
    email_entry = Entry(frame, width=22)
    email_entry.grid(row=2, column=4, pady=10)
    # ====ROW 3====
    gender = StringVar()
    gender.set('Nam')   
    gender_label = Label(frame,bg="#f5f5f5", text='Giới tính:',width=10, font=('Abadi', 12, 'bold')).grid(row=3, column=1,padx=5, pady=10)
    Radiobutton(frame,bg="#f5f5f5", text='Nam', variable=gender, value='Nam').grid(row=3, column=2, pady=10, sticky='w', padx=5)
    Radiobutton(frame,bg="#f5f5f5", text='Nữ', variable=gender, value='Nữ').grid(row=3, column=2, pady=10, sticky='w', padx=55)
    # ====ROW 4====
    address_label = Label(frame,bg="#f5f5f5", text='Địa chỉ:',width=10, font=('Abadi', 12, 'bold')).grid(row=4, column=1,padx=5, pady=5)
    address_text = Text(frame, width=30, height=3)
    address_text.grid(row=4, column=1, columnspan=6, padx=120, sticky='w')

    def back_to_main():
        pro_win.destroy()
        root.deiconify()
    Button(pro_win, text="⬅ Quay lại", font=('Arial', 12), bg="#f44336", fg="white", command=back_to_main).place(x=10, y=460)
    pro_win.protocol("WM_DELETE_WINDOW", back_to_main)
    load_inf()
    load_avatar()

#============================================MAIN=======================================
def open_main(pw_win, username):
    pw_win.withdraw()
    root = Toplevel()
    root.title('Student Care')
    root.geometry('{}x{}+{}+{}'.format(WINDOWN_WIDTH, WINDOWN_HEIGHT, WINDOWN_POSION_RIGHT, WINDOWN_POSION_DOWN))
    root.resizable(False, False)
    root.configure(bg="#f5f5f5")
    profile = load_user_data("profile.json", username) or {}
    study_result = load_user_data("study_result.json", username) or {}
    learning_stats = load_user_data("learning_statistics.json", username) or {}
    style = {
        "font": ("Arial", 14, "bold"),
        "width": 18,
        "relief": "raised",
        "bd": 2,
    }
    # ====Icon====
    try:
        icon_path = r"C:\Users\Nga\Desktop\APP STUDENTS CARE\Images\icon_students_care.png"
        icon = Image.open(icon_path).resize((32, 32), Image.LANCZOS)
        icon_tk = ImageTk.PhotoImage(icon)
        root.iconphoto(True, icon_tk)
        root.icon_tk = icon_tk
    except:
        icon_path = ''
    # ====HEADING====
    frame = Frame(root, relief='flat')
    frame.pack(pady=0 ,anchor='center', fill='x')
    heading = Label(frame, height=3, text="🎓 Student Care", font=("Helvetica", 22, "bold"), bg="#2c3e50", fg="white")
    heading.pack(anchor='center', fill='both', expand=True)
    # ====CONTENT====
    button_1 = Button(root, text='Hồ Sơ Cá Nhân', **style, bg="#428bca", fg='black', activebackground="#3498db", activeforeground="white", command=lambda: open_profile(root, username))
    button_1.pack(anchor='center', pady=(50, 20))
    button_2 = Button(root, text='Kết Quả Học Tập', **style, bg="#5cb85c", fg='black', activebackground="#2ecc71", activeforeground="white", command=lambda: open_study_result(root, username))
    button_2.pack(anchor='center', pady=20)
    button_3 = Button(root, text='Thống Kê Học Tập', **style, bg="#f0ad4e", fg='black', activebackground="#f39c12", activeforeground="white", command=lambda: open_learning_statistics(root, username))
    button_3.pack(anchor='center', pady=20)
    button_4 = Button(root, text='Thoát', **style, bg="#d9534f", fg='black', activebackground="#e74c3c", activeforeground="white", command=root.quit)
    button_4.pack(anchor='center', pady=20)
    root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))

#============================================SIGN UP=======================================
def open_signup(pw_win):
    pw_win.withdraw()
    sgn = Toplevel()
    sgn.title('SIGN UP')
    sgn.geometry("350x290+580+140")
    sgn.resizable(False, False)

    signup = Label(sgn, text="SIGN UP", font=('Arial', 18, 'bold'))
    signup.place(x=120, y=10)
    username = Label(sgn, text="Username", font=("Arial", 11, 'bold'))
    username.place(x=10, y=60)
    username_entry = Entry(sgn, text="Username", width=30)
    username_entry.place(x=150, y=60)

    email = Label(sgn, text="Email", font=("Arial", 11, 'bold'))
    email.place(x=10, y=95)
    email_entry = Entry(sgn, width=30)
    email_entry.place(x=150, y=95)

    password = Label(sgn, text="Password", font=("Arial", 11, 'bold'))
    password.place(x=10, y=130)
    password_entry = Entry(sgn, text="Password", width=30, show="*")
    password_entry.place(x=150, y=130)

    confirm_password = Label(sgn, text="Confirm Password", font=("Arial", 11, 'bold'))
    confirm_password.place(x=10, y=165)
    confirm_password_entry = Entry(sgn, text="Confirm Password", width=30, show="*")
    confirm_password_entry.place(x=150, y=165)

    def toggle_pw(entry, btn):
        if entry.cget('show') == '':
            entry.config(show='*')
            btn.config(text='👁️‍🗨️')
        else:
            entry.config(show='')
            btn.config(text='👁️')
    eye1 = Button(sgn, text='👁️‍🗨️', relief='flat', command=lambda: toggle_pw(password_entry, eye1))
    eye1.place(x=320, y=128)
    eye2 = Button(sgn, text='👁️‍🗨️', relief='flat', command=lambda: toggle_pw(confirm_password_entry, eye2))
    eye2.place(x=320, y=163)

    def create_acc():
        global error_email_label_2, error_pw_label_2
        user_name = username_entry.get().strip()
        email = email_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if error_email_label_2:
            error_email_label_2.destroy()
            error_email_label_2 = None
        if error_pw_label_2:
            error_pw_label_2.destroy()
            error_pw_label_2 = None

        if not check_email_2(email):
            error_email_label_2 = Label(sgn, text="Email không hợp lệ", fg="red", relief='flat', bd=0)
            error_email_label_2.place(x=150, y=110)
            return

        if not check_password_2(password):
            error_pw_label_2 = Label(sgn, text="Password phải chứa ít nhất kí tự viết hoa, kí đặc biệt và chữ số", fg="red")
            error_pw_label_2.place(x=15, y=148)
            return

        users = load_users()
        if user_name in users:
            Label(sgn, text="Tên người dùng đã tồn tại!", fg="red", relief='flat', bd=0).place(x=100, y=195)
            return
        elif password != confirm_password:
            Label(sgn, text="Mật khẩu không khớp!", fg="red").place(x=100, y=195)
            return
        users[user_name] = {"email": email, "password": password}
        save_users(users)
        Label(sgn, text="✅ Tạo tài khoản thành công", fg="green").place(x=100, y=195)
    create_acc = Button(sgn, text='Create Account', font=('Arial', 13, 'bold'), command=create_acc)
    create_acc.place(x=105 ,y=220)

    def back_to_login():
        username_entry.delete(0, END)
        email_entry.delete(0, END)
        password_entry.delete(0, END)
        confirm_password_entry.delete(0, END)
        sgn.destroy()
        pw_win.deiconify()
    Button(sgn, text="Back", relief='flat', bd=0, command=back_to_login).place(x=10, y=250)
    sgn.protocol("WM_DELETE_WINDOW", lambda: None)

#============================================FORGET PASSWORD=======================================
def open_forget_password(pw_win):
    pw_win.withdraw()
    fpw = Toplevel()
    fpw.title("Forget Password")
    fpw.geometry("350x250+580+140")
    fpw.resizable(False, False)
    
    Label(fpw, text="FORGET PASSWORD", font=('Arial', 16, 'bold')).place(x=70, y=10)

    # Username / Email
    Label(fpw, text="Username/Email:", font=('Arial', 11, 'bold')).place(x=12, y=60)
    username_entry = Entry(fpw, width=30)
    username_entry.place(x=150, y=60)

    # New Password
    Label(fpw, text="New Password:", font=('Arial', 11, 'bold')).place(x=12, y=100)
    new_pw_entry = Entry(fpw, width=30, show="*")
    new_pw_entry.place(x=150, y=100)

    # Confirm Password
    Label(fpw, text="Confirm Password:", font=('Arial', 11, 'bold')).place(x=12, y=140)
    confirm_pw_entry = Entry(fpw, width=30, show="*")
    confirm_pw_entry.place(x=150, y=140)

    msg = Label(fpw, text="", font=('Arial', 10, 'bold'))
    msg.place(x=70, y=170)

    # Hiển thị / ẩn mật khẩu
    def toggle_pw(entry, btn):
        if entry.cget('show') == '':
            entry.config(show='*')
            btn.config(text='👁️‍🗨️')
        else:
            entry.config(show='')
            btn.config(text='👁️')

    eye1 = Button(fpw, text='👁️‍🗨️', relief='flat',
                  command=lambda: toggle_pw(new_pw_entry, eye1))
    eye1.place(x=320, y=98)
    eye2 = Button(fpw, text='👁️‍🗨️', relief='flat',
                  command=lambda: toggle_pw(confirm_pw_entry, eye2))
    eye2.place(x=320, y=138)

    # ==== Reset mật khẩu ====
    def reset_password():
        global error_pw_label_1
        users = load_users()
        name_or_email = username_email_entry.get().strip()
        new_pw = new_pw_entry.get()
        confirm_pw = confirm_pw_entry.get()
        if not name_or_email or not new_pw or not confirm_pw:
            msg.config(text="⚠️ Vui lòng nhập đủ thông tin", fg="red")
            return
        found_user = None
        for username, info in users.items():
            if name_or_email == username or name_or_email == info.get("email", ""):
                found_user = username
                break
        if not found_user:
            msg.config(text="❌ Không tìm thấy tài khoản", fg="red")
            return
        if error_pw_label_1:
            error_pw_label_1.destroy()
            error_pw_label_1 = None
        if not check_password_1(new_pw):
            error_pw_label_1 = Label(fpw, text="Password phải chứa ít nhất kí tự viết hoa, kí đặc biệt và chữ số", fg="red")
            error_pw_label_1.place(x=15, y=120)
            return
        if new_pw != confirm_pw:
            msg.config(text="⚠️ Mật khẩu không khớp", fg="red")
            return
        # Lưu mật khẩu mới
        users[found_user]["password"] = new_pw
        save_users(users)
        msg.config(text="✅ Đổi mật khẩu thành công!", fg="green")
        new_pw_entry.delete(0, END)
        confirm_pw_entry.delete(0, END)
        username_email_entry.delete(0, END)
    Button(fpw, text="Reset", bg="blue", fg="white", font=('Arial', 12, 'bold'),
           command=reset_password).place(x=135, y=200)

    # ==== Quay lại Login ====
    def back():
        fpw.destroy()
        pw_win.deiconify()
        # Xóa hết ô nhập Login để không hiện mật khẩu cũ
        for widget in pw_win.winfo_children():
            if isinstance(widget, Entry):
                widget.delete(0, END)
    Button(fpw, text="Back", relief='flat', command=back).place(x=10, y=220)
    fpw.protocol("WM_DELETE_WINDOW", back)

#============================================LOGIN=======================================
pw_win = Tk()
pw_win.title("Account")
pw_win.geometry("350x250+580+140")
pw_win.resizable(False, False)

login = Label(pw_win, text="LOGIN", font=('Arial', 18, 'bold'))
login.place(x=135, y=10)

username_email = Label(pw_win, text="Username/Email", font=("Arial", 11, 'bold'))
username_email.place(x=20, y=60)
username_email_entry = Entry(pw_win, text="Username/Email", width=28)
username_email_entry.place(x=150, y=60)

password = Label(pw_win, text="Password", font=("Arial", 11, 'bold'))
password.place(x=20, y=95)
password_entry = Entry(pw_win, text="Password", width=28, show="*")
password_entry.place(x=150, y=95)

msg_lbl = Label(pw_win, text="", fg="red", font=('Arial', 9, 'bold'))
msg_lbl.place(x=42, y=140)

def toggle_pw(entry, btn):
        if entry.cget('show') == '':
            entry.config(show='*')
            btn.config(text='👁️‍🗨️')
        else:
            entry.config(show='')
            btn.config(text='👁️')
eye = Button(pw_win, text='👁️‍🗨️', relief='flat', command=lambda: toggle_pw(password_entry, eye))
eye.place(x=320, y=95)

is_checked = tk.BooleanVar(value=False)
check = tk.Checkbutton(pw_win, text="Remember me", variable=is_checked)
check.place(x=0, y=120)

users = load_users()
for username, info in users.items():
    if info.get("remember", False):
        username_email_entry.insert(0, username)
        password_entry.insert(0, info.get("password", ""))
        is_checked.set(True)
        break

def login_acc():
    username_input = username_email_entry.get().strip()
    password_input = password_entry.get().strip()

    users = load_users()
    login_user = None
    for username, info in users.items():
        if ((username_input == username or username_input == info['email']) and (password_input == info['password'])):
            login_user = username
            break
    if login_user:
        msg_lbl.config(text="✅ Login thành công!", fg="green")
        for user in users:
            users[user]["remember"] = False  # reset tất cả
        users[login_user]["remember"] = is_checked.get()
        save_users(users)  # Lưu lại file users.json
        open_main(pw_win, login_user)
    else:
        msg_lbl.config(text="❌ Username/Email hoặc mật khẩu không đúng", fg="red")
def go_to_signup():
    username_email_entry.delete(0, END)
    password_entry.delete(0, END)
    is_checked.set(False)
    msg_lbl.config(text="")
    open_signup(pw_win)

login = Button(pw_win, text="Login", font=('Arial', 13, 'bold'), fg='white', bg='blue', command=login_acc)
login.place(x=145, y=160)

forget_pw = Button(pw_win, text="Forget password", font=('Arial', 9), activeforeground="#6633FF", relief='flat', bd=0, highlightthickness=0, command=lambda: open_forget_password(pw_win))
forget_pw.place(x=0, y=200)

signup_entry = Button(pw_win, text='Have an account? Sign up', font=('Arial', 9), activeforeground="#6633FF", relief='flat', bd=0, highlightthickness=0, command=go_to_signup)
signup_entry.place(x=0, y=220)

pw_win.mainloop()