import hashlib

from MD5 import MD5

if __name__ == "__main__":

    message = "abc"

    print(f"Входная строка: {message}\n")

    # Использование библиотеки hashlib
    lib_result = hashlib.md5(message.encode()).hexdigest()
    print("MD5 хэш (библиотека hashlib):", lib_result)

    # Использование собственной реализации MD5
    md5 = MD5()

    result = md5.md5(message=message)
    print("MD5 хэш (самостоятельная реализация):", result)

    if result == lib_result:
        print(f"\nХэши равны:\n{lib_result}\n{result}")
    else:
        print(f"\nХэши не равны:\n{lib_result}\n{result}")
