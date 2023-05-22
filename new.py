import re
import sqlite3
from datetime import date
import time
import tkinter

def main():  # sourcery skip: extract-duplicate-method, low-code-quality, merge-comparisons, remove-unnecessary-else, remove-unreachable-code, use-fstring-for-concatenation, use-getitem-for-re-match-groups
    conn = sqlite3.connect('userdata.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                    name TEXT,
                    idcard TEXT,
                    gender TEXT,
                    birthday TEXT,
                    age INTEGER,
                    address TEXT,
                    phone TEXT
                    )''')

    def search_info():
        search_name = input("请输入您要查询的姓名：")
        if check_chinese_name(search_name): # 此处需要判断用户输入的是否为汉语，否则会报错
            result = cursor.execute(f"SELECT * FROM user WHERE name='{search_name}';").fetchall()
            if len(result) == 0:  
                print("未查询到相关信息")

            else:
                for row in result:
                    time.sleep(1)
                    print(f"姓名：{row[0]}，性别：{row[2]}，年龄：{row[4]}，身份证号码：{row[1]}，地址：{row[5]}，手机号码：{row[6]}")
                return result


    def check_chinese_name(name):
        if re.match(r'^[\u4e00-\u9fa5]+$', name):
            return True
        else:
            print("姓名必须为中文")
            return False

    def get_chinese_name():
        while True:
            name = input("请输入您的姓名：")
            if check_chinese_name(name):
                return name

    def check_chinese_idcard(idcard):
        if validate_idcard(idcard):
            return idcard
        else:
            print("身份证号码无效，请重新输入")

    def get_chinese_idcard():
        while True:
            idcard = input("请输入18位的中国大陆身份证号码(末尾的字母X请使用大写):")
            if check_chinese_idcard(idcard):
                return idcard

    def check_chinese_address(address):           
        if re.match(r'^[\u4e00-\u9fa5]+$', address):
            return address
        else:
            print("地址必须为中文")

    def get_chinese_address():           
        while True:
            address = input("请输入您的地址：")
            if check_chinese_address(address):
                return address

    def check_chinese_phone(phone):            
        if phone.isdigit() and len(phone) == 11:
                # 如果是，跳出循环
            return phone
        else:
                # 如果不是，提示用户重新输入
            print("无效的手机号码号码,请使用11位数字输入。")

    def get_chinese_phone():            
        while True:
            phone = input("请输入手机号码号码：")
            # 检查手机号码号码是否只包含数字，并且长度为11位
            if check_chinese_phone(phone):
                # 如果是，跳出循环
                return phone

    def delete_info():
        while True:
            name = input("请输入要删除的记录的姓名：")
            idcard = input("请输入要删除的记录的身份证号码：")
            if check_chinese_name(name) and check_chinese_idcard(idcard):
                break

        cursor.execute(f"SELECT * FROM user WHERE name='{name}' AND idcard='{idcard}'")
        result = cursor.fetchall()
        if not result:
            print("未找到匹配的记录")
            return

        # 输出匹配的记录并确认是否删除
        for i, row in enumerate(result):
            print(f"{i + 1}. 姓名：{row[0]} 身份证号码：{row[1]} 地址：{row[5]} 手机号码：{row[6]}")
        while True:
            confirm = input("是否确认删除？(y/n)")
            if confirm.lower() in ["y", "n"]:
                break

        if confirm.lower() == "y":
            cursor.execute(f"DELETE FROM user WHERE name='{name}' AND idcard='{idcard}'")
            conn.commit()

            print("删除成功")

    def query_data():
        result = cursor.execute("SELECT * FROM user;").fetchall()
        for row in result:
            if len(row[0]) < 3:
                name1 = row[0][0]
                name2 = row[0][1] + '  ' # 在第二个汉字后面添加两个空格
                print(f"姓名：{name1:<3}{name2.strip()}，身份证号码：{row[1]}，性别：{row[2]}，生日：{row[3]}，年龄：{row[4]}，地址：{row[5]}，电话：{row[6]}")
            else:
                print(f"姓名：{row[0]:<3}，身份证号码：{row[1]}，性别：{row[2]}，生日：{row[3]}，年龄：{row[4]}，地址：{row[5]}，电话：{row[6]}")

    while True:
        option = input("请选择您要进行的操作:1.查询 2.登记 3.修改 4.删除 5.列表\n")
        if option == "1":
            search_info()

        elif option == "4":
            # 让用户选择要删除的记录
            delete_info()

        elif option == "5":
            #查询所有数据列表
            query_data()

        elif option == "3":
            while True:
                result = search_info()
                if result:
                    #根据查询结果，获取姓名和身份证号码
                    name = result[0][0]
                    idcard = result[0][1]

                # 输出匹配的记录并提示用户选择要修改的记录
                for i, row in enumerate(result):
                    print(f"{i + 1}. 姓名：{row[0]} 身份证号码：{row[1]} 地址：{row[5]} 手机号码：{row[6]}")
                while True:
                    index = input("请选择您要修改的记录：")
                    if index.isdigit():
                        index = int(index)
                        if 1 <= index <= len(result):
                            break

                # 用户输入新的信息
                while True:
                    new_name = input("请输入您的新姓名：")
                    if check_chinese_name(new_name):
                        break
                while True:
                    new_idcard = input("请输入您新的身份证号码:")
                    if check_chinese_idcard(new_idcard):
                        break
                while True:
                    new_address = input("请输入您新的地址:")
                    if check_chinese_address(new_address):
                        break
                while True:    
                    new_phone = input("请输入新的手机号码:")
                    if check_chinese_phone(new_phone):
                        break

                # 更新数据库中的记录
                cursor.execute(f"UPDATE user SET name='{new_name}', idcard='{new_idcard}', address='{new_address}', phone='{new_phone}' WHERE name='{name}' AND idcard='{idcard}'")
                conn.commit()

                print("更新成功") 
                return


        elif option == "2":
            count = 0  # 初始化用户输入身份证信息错误的次数
            while True:
                name = get_chinese_name()

                idcard = get_chinese_idcard()
                        #查询数据库中是否存在相同身份证的记录
                result = cursor.execute(f"SELECT * FROM user WHERE idcard='{idcard}';").fetchall()
                if len(result) > 0:
                    count += 1
                    if count >= 2:  # 判断是否输错了两次以上，是则退出程序
                        print("已连续两次输入错误，程序已退出。")
                        return
                    for row in result:
                        print("您输入的身份证号码已存在，请稍后正在为您显示结果：")
                        time.sleep(1)  #延迟1秒显示结果
                        print(f"姓名：{row[0]}，性别：{row[2]}，年龄：{row[4]}，身份证号码：{row[1]}，地址：{row[5]}, 手机号码：{row[6]}")
                    continue

                address = get_chinese_address()

                phone = get_chinese_phone()

                gender, birthday, age = get_user_info(idcard)
                cursor.execute(f"INSERT INTO user (name, idcard, gender, birthday, age, address, phone) VALUES ('{name}', '{idcard}', '{gender}', '{birthday}', {age}, '{address}','{phone}')")
                conn.commit()
                time.sleep(1)
                print("登记成功")
                time.sleep(1)
                print(f"姓名：{name}，性别：{gender}，年龄：{age}，身份证号码：{idcard}，地址：{address}, 手机号码: {phone}")    
                return

        else:
            print("您输入的选项不存在，请重新输入！")


def validate_idcard(idcard):
#     # 判断身份证号码是否合法（仅限中国身份证）
    if not isinstance(idcard, str) or len(idcard) != 18:
        return False
    factors = [int(idcard[i]) * (2 ** (17 - i)) for i in range(17)]
    check_code = str((12 - sum(factors) % 11) % 11)
    if check_code == '10':
        check_code = 'X'
    return check_code == idcard[-1].upper()

def get_user_info(idcard):
    # 根据身份证号码获取用户性别、出生日期和年龄
    if not validate_idcard(idcard):
        return "", "", -1

    birth_year = int(idcard[6:10])
    birth_month = int(idcard[10:12])
    birth_day = int(idcard[12:14])

    today = date.today()
    age = today.year - birth_year - ((today.month, today.day) < (birth_month, birth_day))

    gender_code = int(idcard[-2])
    gender = "男" if gender_code % 2 == 1 else "女"

    birthday = f"{birth_year}-{birth_month}-{birth_day}"

    return gender, birthday, age

if __name__ == '__main__':
    main()