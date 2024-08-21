import argparse
from rich.console import Console
import random
console = Console()

# Karakter değiştirme kuralları
substitutions = {
    'a': '@', 'o': '0', 'i': '1', 'e': '3', 's': '$'
}

def print_ascii_art():
    with open('mrs_cupp.txt', 'r', encoding='utf-8') as file:
        banners = file.read().strip().split('**********HACK ASCİİ**********')
    art = random.choice(banners)
    console.print(art, style="red")

print_ascii_art()

def get_user_info():
    """Kullanıcı bilgisini toplar ve isteğe bağlı alanları yönetir."""
    user_info = {}
    user_info['first_name'] = input("Adınızı girin: ")
    user_info['last_name'] = input("Soyadınızı girin: ")
    user_info['username'] = input("Kullanıcı adınızı girin: ")  # Yeni kullanıcı adı
    user_info['birth_year'] = input("Doğum yılınızı girin: ")
    user_info['birth_month'] = input("Doğum ayınızı girin (MM): ")
    user_info['birth_day'] = input("Doğum gününüzü girin (DD): ")

    # Evcil hayvan adı isteğe bağlı
    pet_name = input("Evcil hayvanınızın adını girin (boş bırakabilirsiniz): ")
    user_info['pet_name'] = pet_name if pet_name else "unknown"

    # Favori renk isteğe bağlı
    favorite_color = input("Favori renginizi girin (boş bırakabilirsiniz): ")
    user_info['favorite_color'] = favorite_color if favorite_color else "unknown"

    # Favori mekan isteğe bağlı
    favorite_place = input("Favori mekanınızı girin (boş bırakabilirsiniz): ")
    user_info['favorite_place'] = favorite_place if favorite_place else "unknown"
    
    # Ek kelimeler isteğe bağlı
    additional_words = input("Ek kelimeleri virgülle ayırarak girin (boş bırakabilirsiniz): ")
    user_info['additional_words'] = [word.strip() for word in additional_words.split(',')] if additional_words else []

    return user_info

def substitute_chars(word):
    """Leet speak için karakter değiştirme uygular."""
    for key, value in substitutions.items():
        word = word.replace(key, value)
    return word

def generate_passwords(user_info):
    """Kullanıcı bilgilerine dayalı olarak parola listesi oluşturur."""
    passwords = set()
    
    basic_combinations = [
        user_info['first_name'], user_info['last_name'],
        user_info['username'], user_info['birth_year'], 
        user_info['pet_name'], user_info['favorite_color'],
        user_info['favorite_place']
    ]
    
    # Basit kombinasyonlar
    for item in basic_combinations:
        passwords.add(item)
        passwords.add(substitute_chars(item))
    
    # Alanları birleştirerek daha karmaşık parolalar oluşturma
    for item1 in basic_combinations:
        for item2 in basic_combinations:
            if item1 != item2:
                passwords.add(item1 + item2)
                passwords.add(substitute_chars(item1 + item2))
    
    # Yılı kombinasyonlara ekleme
    for password in list(passwords):
        passwords.add(password + user_info['birth_year'])
    
    # Yaygın son ekler ekleme
    common_endings = ['123', '!', '@', '*', '?', '2024']
    for password in list(passwords):
        for ending in common_endings:
            passwords.add(password + ending)
    
    # Ek kelimeleri ekleme
    for word in user_info['additional_words']:
        for password in list(passwords):
            passwords.add(password + word)
    
    return passwords

def generate_advanced_passwords(user_info, min_length=8, max_length=16):
    """Uzunluk kısıtlamaları ve gelişmiş özelliklerle parolalar oluşturur."""
    passwords = generate_passwords(user_info)
    
    # Uzunluk filtreleme
    passwords = {pw for pw in passwords if min_length <= len(pw) <= max_length}
    
    # Özel kurallar uygulama (örneğin, en az bir özel karakter içermeli)
    special_chars = "!@#$%^&* "
    def meets_custom_rules(password):
        return any(char in special_chars for char in password)
    
    passwords = {pw for pw in passwords if meets_custom_rules(pw)}
    
    return passwords

def save_passwords(passwords, filename="password_list.txt"):
    """Oluşturulan parolaları bir dosyaya kaydeder."""
    with open(filename, "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print(f"{len(passwords)} parola '{filename}' dosyasına kaydedildi.")

def main():
    """Komut satırı arayüzünü ve parola oluşturma işlemini yönetir."""
    parser = argparse.ArgumentParser(description="CUPP gibi Gelişmiş Parola Profiler")
    parser.add_argument("-o", "--output", type=str, help="Çıktı dosya adı", default="password_list.txt")
    parser.add_argument("--min-length", type=int, help="Minimum parola uzunluğu", default=8)
    parser.add_argument("--max-length", type=int, help="Maksimum parola uzunluğu", default=16)
    
    args = parser.parse_args()
    
    user_info = get_user_info()
    passwords = generate_advanced_passwords(user_info, min_length=args.min_length, max_length=args.max_length)
    save_passwords(passwords, filename=args.output)

if __name__ == "__main__":
    main()
