import random
from database import async_session
from models import Card
from sqlalchemy import select, func


REAL_PLAYERS = [
    {"name": "Сидни Кросби", "pos": "ЦН", "age": 39, "ovr": 93, "country": "Канада", "league": "NHL", "club": "Питтсбург"},
    {"name": "Александр Овечкин", "pos": "ЛП", "age": 40, "ovr": 92, "country": "Россия", "league": "NHL", "club": "Вашингтон"},
    {"name": "Евгений Малкин", "pos": "ЦН", "age": 39, "ovr": 91, "country": "Россия", "league": "NHL", "club": "Питтсбург"},
    {"name": "Коннор Макдэвид", "pos": "ЦН", "age": 28, "ovr": 97, "country": "Канада", "league": "NHL", "club": "Эдмонтон"},
    {"name": "Никита Кучеров", "pos": "ПП", "age": 32, "ovr": 95, "country": "Россия", "league": "NHL", "club": "Тампа-Бэй"},
    {"name": "Виктор Хедман", "pos": "З", "age": 35, "ovr": 92, "country": "Швеция", "league": "NHL", "club": "Тампа-Бэй"},
    {"name": "Андрей Василевский", "pos": "В", "age": 31, "ovr": 94, "country": "Россия", "league": "NHL", "club": "Тампа-Бэй"},
    {"name": "Джейми Бенн", "pos": "ЛП", "age": 36, "ovr": 88, "country": "Канада", "league": "NHL", "club": "Даллас"},
    {"name": "Миро Хейсканен", "pos": "З", "age": 31, "ovr": 91, "country": "Финляндия", "league": "NHL", "club": "Даллас"},
    {"name": "Микко Рантанен", "pos": "ПП", "age": 29, "ovr": 93, "country": "Финляндия", "league": "NHL", "club": "Даллас"},
    {"name": "Джон Таварес", "pos": "ЦН", "age": 34, "ovr": 87, "country": "Канада", "league": "NHL", "club": "Торонто"},
    {"name": "Остон Мэттьюс", "pos": "ЦН", "age": 28, "ovr": 94, "country": "США", "league": "NHL", "club": "Торонто"},
    {"name": "Митч Марнер", "pos": "ПП", "age": 28, "ovr": 90, "country": "Канада", "league": "NHL", "club": "Торонто"},
    {"name": "Артемий Панарин", "pos": "ЛП", "age": 34, "ovr": 91, "country": "Россия", "league": "NHL", "club": "Рейнджерс"},
    {"name": "Игорь Шестёркин", "pos": "В", "age": 30, "ovr": 93, "country": "Россия", "league": "NHL", "club": "Рейнджерс"},
    {"name": "Джек Айкел", "pos": "ЦН", "age": 29, "ovr": 88, "country": "США", "league": "NHL", "club": "Вегас"},
    {"name": "Марк Стоун", "pos": "ПП", "age": 33, "ovr": 89, "country": "Канада", "league": "NHL", "club": "Вегас"},
    {"name": "Ши Теодор", "pos": "З", "age": 30, "ovr": 86, "country": "Канада", "league": "NHL", "club": "Вегас"},
    {"name": "Александр Никишин", "pos": "З", "age": 24, "ovr": 87, "country": "Россия", "league": "KHL", "club": "СКА"},
    {"name": "Иван Демидов", "pos": "ЛП", "age": 19, "ovr": 82, "country": "Россия", "league": "KHL", "club": "СКА"},
    {"name": "Арсений Грицюк", "pos": "ПП", "age": 24, "ovr": 84, "country": "Россия", "league": "KHL", "club": "СКА"},
    {"name": "Марат Хайруллин", "pos": "ЦН", "age": 28, "ovr": 83, "country": "Россия", "league": "KHL", "club": "СКА"},
    {"name": "Дамир Шарипзянов", "pos": "З", "age": 29, "ovr": 86, "country": "Россия", "league": "KHL", "club": "Авангард"},
    {"name": "Иван Игумнов", "pos": "ЦН", "age": 24, "ovr": 82, "country": "Россия", "league": "KHL", "club": "Авангард"},
    {"name": "Михаил Гуляев", "pos": "З", "age": 25, "ovr": 83, "country": "Россия", "league": "KHL", "club": "Авангард"},
    {"name": "Дмитрий Вишневский", "pos": "З", "age": 35, "ovr": 84, "country": "Россия", "league": "KHL", "club": "Спартак"},
    {"name": "Иван Морозов", "pos": "ЦН", "age": 24, "ovr": 84, "country": "Россия", "league": "KHL", "club": "Спартак"},
    {"name": "Павел Порядин", "pos": "ПП", "age": 28, "ovr": 85, "country": "Россия", "league": "KHL", "club": "Спартак"},
    {"name": "Никита Сусуев", "pos": "ЛП", "age": 24, "ovr": 82, "country": "Россия", "league": "KHL", "club": "Спартак"},
    {"name": "Егор Яковлев", "pos": "З", "age": 35, "ovr": 85, "country": "Россия", "league": "KHL", "club": "Металлург"},
    {"name": "Михаил Фёдоров", "pos": "ЦН", "age": 19, "ovr": 80, "country": "Россия", "league": "KHL", "club": "Металлург"},
    {"name": "Александр Сиряцкий", "pos": "З", "age": 19, "ovr": 78, "country": "Россия", "league": "KHL", "club": "Металлург"},
    {"name": "Игорь Нечаев", "pos": "ЛП", "age": 20, "ovr": 79, "country": "Россия", "league": "KHL", "club": "Металлург"},
    {"name": "Игорь Ожиганов", "pos": "З", "age": 32, "ovr": 84, "country": "Россия", "league": "KHL", "club": "Динамо Москва"},
    {"name": "Тимур Кол", "pos": "З", "age": 19, "ovr": 78, "country": "Россия", "league": "KHL", "club": "Динамо Москва"},
    {"name": "Владимир Селиванов", "pos": "В", "age": 17, "ovr": 75, "country": "Россия", "league": "KHL", "club": "Динамо Москва"},
    {"name": "Иван Рябкин", "pos": "ЦН", "age": 19, "ovr": 79, "country": "Россия", "league": "KHL", "club": "Динамо Москва"},
    {"name": "Данис Зарипов", "pos": "ЛП", "age": 43, "ovr": 82, "country": "Россия", "league": "KHL", "club": "Ак Барс"},
    {"name": "Александр Радулов", "pos": "ПП", "age": 39, "ovr": 85, "country": "Россия", "league": "KHL", "club": "Ак Барс"},
    {"name": "Сергей Морозов", "pos": "ЦН", "age": 44, "ovr": 80, "country": "Россия", "league": "VHL", "club": "Торос"},
    {"name": "Алексей Кузнецов", "pos": "ЦН", "age": 30, "ovr": 78, "country": "Россия", "league": "VHL", "club": "Торос"},
    {"name": "Андрей Орлов", "pos": "З", "age": 28, "ovr": 77, "country": "Россия", "league": "VHL", "club": "Торос"},
    {"name": "Владимир Соколов", "pos": "В", "age": 26, "ovr": 76, "country": "Россия", "league": "VHL", "club": "Торос"},
    {"name": "Иван Петров", "pos": "ЦН", "age": 24, "ovr": 74, "country": "Россия", "league": "VHL", "club": "Буран"},
    {"name": "Александр Смирнов", "pos": "ЛП", "age": 25, "ovr": 75, "country": "Россия", "league": "VHL", "club": "Буран"},
    {"name": "Дмитрий Волков", "pos": "З", "age": 27, "ovr": 74, "country": "Россия", "league": "VHL", "club": "Буран"},
    {"name": "Пётр Соловьёв", "pos": "В", "age": 29, "ovr": 73, "country": "Россия", "league": "VHL", "club": "Буран"},
    {"name": "Никита Соколов", "pos": "ЦН", "age": 22, "ovr": 73, "country": "Россия", "league": "VHL", "club": "АКМ"},
    {"name": "Артём Кузнецов", "pos": "ПП", "age": 23, "ovr": 74, "country": "Россия", "league": "VHL", "club": "АКМ"},
    {"name": "Максим Орлов", "pos": "З", "age": 26, "ovr": 73, "country": "Россия", "league": "VHL", "club": "АКМ"},
    {"name": "Егор Зайцев", "pos": "В", "age": 24, "ovr": 72, "country": "Россия", "league": "VHL", "club": "АКМ"},
]

FIRST_NAMES = ["Александр", "Сергей", "Дмитрий", "Андрей", "Алексей", "Николай", "Владимир", "Игорь", "Роман", "Павел", "Максим", "Артём", "Денис", "Егор", "Илья", "Кирилл", "Матвей", "Тимофей", "Глеб", "Савелий", "Ярослав", "Михаил", "Иван", "Пётр", "Фёдор"]
LAST_NAMES = ["Петров", "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", "Соколов", "Михайлов", "Новиков", "Фёдоров", "Морозов", "Волков", "Лебедев", "Семёнов", "Егоров", "Павлов", "Козлов", "Степанов", "Николаев", "Орлов", "Зайцев", "Соловьёв", "Борисов", "Яковлев", "Григорьев"]
COUNTRIES = ["Россия", "Россия", "Россия", "Канада", "США", "Швеция", "Финляндия", "Чехия", "Словакия"]
POSITIONS = ["ЦН", "ЛП", "ПП", "З", "З", "В"]
LEAGUES = ["VHL", "KHL", "NHL"]
CLUBS = {
    "VHL": ["Торос", "Буран", "АКМ", "Югра", "Динамо-Алтай"],
    "KHL": ["ЦСКА", "СКА", "Динамо Москва", "Спартак", "Ак Барс", "Авангард", "Металлург", "Трактор"],
    "NHL": ["Питтсбург", "Вашингтон", "Тампа-Бэй", "Торонто", "Рейнджерс", "Вегас", "Даллас", "Эдмонтон"],
}


def calculate_stats(ovr: int, position: str) -> dict:
    base = ovr - 10
    stats = {
        "speed": base + random.randint(-8, 8),
        "shot": base + random.randint(-8, 8),
        "pass_": base + random.randint(-8, 8),
        "defense": base + random.randint(-8, 8),
        "physical": base + random.randint(-8, 8),
        "goalie": 0,
    }
    if position == "В":
        stats["goalie"] = ovr
        stats["speed"] = max(40, ovr - 15)
        stats["shot"] = 0
        stats["pass_"] = max(30, ovr - 20)
    for k in stats:
        stats[k] = max(30, min(99, stats[k]))
    return stats


def determine_rarity(ovr: int) -> str:
    if ovr >= 93: return "legend"
    if ovr >= 87: return "elite"
    if ovr >= 80: return "gold"
    if ovr >= 72: return "silver"
    return "bronze"


def determine_role(stats: dict, position: str) -> str:
    if position == "В":
        return "wall" if stats["goalie"] >= 85 else "flexible"
    if stats["shot"] >= 80 and stats["pass_"] < 70:
        return "sniper"
    if stats["pass_"] >= 80 and stats["shot"] < 70:
        return "playmaker"
    if stats["speed"] >= 85:
        return "speedster"
    if stats["defense"] >= 80 and stats["speed"] < 70:
        return "defender"
    return "universal"


def build_all_cards() -> list:
    """Собирает все карточки (в памяти)."""
    cards_data = []

    for p in REAL_PLAYERS:
        stats = calculate_stats(p["ovr"], p["pos"])
        cards_data.append({
            "name": p["name"], "position": p["pos"], "age": p["age"], "ovr": p["ovr"],
            "speed": stats["speed"], "shot": stats["shot"], "pass_": stats["pass_"],
            "defense": stats["defense"], "physical": stats["physical"], "goalie": stats["goalie"],
            "rarity": determine_rarity(p["ovr"]), "role": determine_role(stats, p["pos"]),
            "country": p["country"], "league": p["league"], "club": p["club"],
            "potential": min(99, p["ovr"] + random.randint(0, 5)),
        })

    for i in range(260):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        ovr = random.randint(55, 88)
        pos = random.choice(POSITIONS)
        league = random.choice(LEAGUES)
        country = random.choice(COUNTRIES)
        stats = calculate_stats(ovr, pos)
        cards_data.append({
            "name": f"{first} {last}", "position": pos, "age": random.randint(18, 36), "ovr": ovr,
            "speed": stats["speed"], "shot": stats["shot"], "pass_": stats["pass_"],
            "defense": stats["defense"], "physical": stats["physical"], "goalie": stats["goalie"],
            "rarity": determine_rarity(ovr), "role": determine_role(stats, pos),
            "country": country, "league": league, "club": random.choice(CLUBS[league]),
            "potential": min(99, ovr + random.randint(0, 10)),
        })

    return cards_data


async def generate_cards_if_empty():
    """Генерирует карточки батчами по 50 штук."""
    async with async_session() as session:
        count = await session.scalar(select(func.count(Card.id)))
        if count and count > 0:
            return

    all_cards = build_all_cards()
    batch_size = 50

    for i in range(0, len(all_cards), batch_size):
        batch = all_cards[i:i + batch_size]
        async with async_session() as session:
            for data in batch:
                session.add(Card(**data))
            await session.commit()

    return len(all_cards)
