def generate_passwords():
    prefixes = ["068", "096", "097", "063"]
    ranges = [
        ("0660000000", "0669999999"),
        ("0970000000", "0979999999")
    ]

    with open("passwords.txt", "w") as file:
        for prefix in prefixes:
            for start, end in ranges:
                start_num = int(start)
                end_num = int(end)
                for number in range(start_num, end_num + 1):
                    password = f"{prefix}{str(number)[3:]}\n"
                    file.write(password)

if __name__ == "__main__":
    generate_passwords()
    print("Файл passwords.txt успешно создан.")