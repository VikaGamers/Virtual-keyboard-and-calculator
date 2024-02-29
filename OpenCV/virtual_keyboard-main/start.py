import subprocess

def main():
    print("Що ви хочете обрати?")
    print("1. Клавіатура")
    print("2. Калькулятор")
    
    choice = input("Ваш вибір: ")

    if choice == "1":
        subprocess.run(["python", "C:/Users/Дмитрий/Desktop/OpenCV/virtual_keyboard-main/main.py"])

    elif choice == "2":
        subprocess.run(["python", "C:/Users/Дмитрий/Desktop/OpenCV/virtual_keyboard-main/calc.py"])
    else:
        print("Неправильний вибір. Будь ласка, оберіть знову.")

if __name__ == "__main__":
    main()
