
def main():

    # بخش اول: گرفتن ورودی از کاربر
    lang_input = input("زبان را وارد کنید (رشته ها را با کاما از هم جدا کنید): ")
    input_string = input("رشته مورد نظر برای بررسی پذیرش را وارد کنید: ")

    # تبدیل ورودی زبان به لیستی از رشته ها و حذف فاصله های اضافی
    language = [item.strip() for item in lang_input.split(',')]

    #   ساختن ماشین متناظر با زبان
    states = {}
    next_state_id = 0
    accept_states = set()

    # حالت شروع
    start_state = "q0"
    states[start_state] = {}

    # تابع کمکی برای ساختن یک حالت جدید
    def make_new_state():
        nonlocal next_state_id
        new_name = f"q{next_state_id}"
        next_state_id += 1
        states[new_name] = {}
        return new_name

    # اضافه کردن هر رشته از زبان به ساختار ماشین
    for word in language:
        current = start_state
        for ch in word:
            # اگر از حالت فعلی با این حرف مسیری نیست، یک حالت جدید بساز
            if ch not in states[current]:
                new_state = make_new_state()
                states[current][ch] = new_state
            # حرکت به حالت بعدی
            current = states[current][ch]
        # بعد از تمام شدن رشته، این حالت را پذیرنده علامت بزن
        accept_states.add(current)

    #  کامل کردن توابع انتقال
    # اول الفبا را از حرف های موجود در زبان و رشته ورودی به دست می آوریم
    alphabet = set()
    for word in language:
        for ch in word:
            alphabet.add(ch)
    for ch in input_string:
        alphabet.add(ch)

    # اگر الفبا خالی نبود، یک حالت مرده می سازیم
    dead_state = None
    if alphabet:
        dead_state = "dead"
        states[dead_state] = {}
        # از حالت مرده با همه حروف به خودش می رویم
        for ch in alphabet:
            states[dead_state][ch] = dead_state

    # برای هر حالتی که به ازای بعضی حروف انتقال نداشت، به حالت مرده وصل می کنیم
    for state in list(states.keys()):
        for ch in alphabet:
            if ch not in states[state]:
                if dead_state is not None:
                    states[state][ch] = dead_state
                else:
                    states[state][ch] = state

    # بخش چهارم: چاپ توابع انتقال کامل شده
    print("\n=== توابع انتقال ماشین (کامل) ===")
    sorted_states = sorted(states.keys())
    sorted_alphabet = sorted(alphabet) if alphabet else []

    for state in sorted_states:
        for ch in sorted_alphabet:
            next_state = states[state].get(ch, state)
            print(f"delta({state}, '{ch}') = {next_state}")

    #   بررسی پذیرش رشته ورودی
    print("\n=== بررسی پذیرش رشته ===")
    current = start_state
    for ch in input_string:
        if ch not in alphabet and alphabet:
            print(f"رشته شامل حرف '{ch}' است که در الفبای زبان نیست.")
            current = None
            break
        if current in states and ch in states[current]:
            current = states[current][ch]
        else:
            current = None
            break

    if current is not None and current in accept_states:
        print(f"رشته '{input_string}' توسط زبان پذیرفته می شود.")
    else:
        print(f"رشته '{input_string}' توسط زبان پذیرفته نمی شود.")

    #  محاسبه پیشوندها، پسوندها و زیررشته ها
    print("\n=== پیشوندها، پسوندها و زیررشته های رشته ورودی ===")

    prefixes = [input_string[:i] for i in range(len(input_string) + 1)]
    print(f"پیشوندها: {prefixes}")

    suffixes = [input_string[i:] for i in range(len(input_string) + 1)]
    print(f"پسوندها: {suffixes}")

    substrings = set()
    for i in range(len(input_string)):
        for j in range(i + 1, len(input_string) + 1):
            substrings.add(input_string[i:j])
    print(f"زیررشته ها: {sorted(substrings)}")

    # بخش هفتم: بررسی منظم بودن زبان
    print("\n=== بررسی منظم بودن زبان ===")
    # طبق نظریه زبان ها، زبان های متناهی همیشه منظم هستند
    # در حالت کلی برای زبان های نامتناهی تشخیص منظم بودن تصمیم ناپذیر است

    if len(language) < 100 and not any('*' in word for word in language):
        print("زبان ورودی متناهی است و بنابراین منظم می باشد.")
    else:
        print("زبان ممکن است نامتناهی باشد.")
        print("تشخیص منظم بودن زبان های نامتناهی در حالت کلی تصمیم ناپذیر است.")
        print("اما اگر این زبان با یک عبارت منظم ساده داده شده باشد، می توان آن را منظم در نظر گرفت.")

    print("\nپایان برنامه.")


if __name__ == "__main__":
    main()