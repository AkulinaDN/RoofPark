from PIL import Image
from collections import Counter

def calculate_color_areas_sorted(image_path):
    # Открываем изображение
    img = Image.open(image_path)
    
    # Преобразуем в RGB, если изображение имеет прозрачность
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGBA')
    
    # Получаем данные пикселей
    pixels = list(img.getdata())
    
    # Считаем количество каждого цвета
    color_counter = Counter(pixels)
    
    # Общее количество пикселей
    total_pixels = img.width * img.height
    
    # Сортируем цвета по количеству пикселей (площади) по убыванию
    sorted_colors = sorted(color_counter.items(), key=lambda x: x[1], reverse=True)
    
    # Выводим результаты
    print(f"Размер изображения: {img.width}x{img.height}")
    print(f"Всего пикселей: {total_pixels}")
    print("\nЦвета отсортированы по площади (по убыванию):")
    print("=" * 60)
    
    for rank, (color, count) in enumerate(sorted_colors, 1):
        area_percent = (count / total_pixels) * 100
        
        if len(color) == 4:  # RGBA
            r, g, b, a = color
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            alpha_info = f", Alpha: {a}"
            color_info = f"RGBA({r}, {g}, {b}, {a})"
        else:  # RGB
            r, g, b = color
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            alpha_info = ""
            color_info = f"RGB({r}, {g}, {b})"
        
        print(f"{rank:2}. {color_info}")
        print(f"    HEX: {color_hex}")
        print(f"    Пикселей: {count:8,d} ({area_percent:6.2f}%)")
        print(f"    Площадь: {count:,d} px²")
        print()

# Версия с визуализацией и сортировкой
def analyze_image_colors_sorted(image_path):
    from PIL import Image
    import matplotlib.pyplot as plt
    from collections import Counter
    
    # Открываем и анализируем изображение
    img = Image.open(image_path)
    
    if img.mode in ('RGBA', 'LA', 'P'):
        img_rgba = img.convert('RGBA')
    else:
        img_rgba = img.convert('RGB')
    
    pixels = list(img_rgba.getdata())
    color_counter = Counter(pixels)
    total_pixels = len(pixels)
    
    # Сортируем по убыванию количества пикселей
    sorted_colors = sorted(color_counter.items(), key=lambda x: x[1], reverse=True)
    
    # Подготовка данных для визуализации (в отсортированном порядке)
    colors = []
    counts = []
    labels = []
    color_infos = []
    
    for rank, (color, count) in enumerate(sorted_colors, 1):
        area_percent = count / total_pixels * 100
        
        if len(color) == 4:
            r, g, b, a = color
            if a == 0:  # Прозрачный пиксель
                color_display = (0.9, 0.9, 0.9, 0.5)  # Светло-серый для прозрачности
                label = f"{rank}. Прозрачный\n{count:,d}px ({area_percent:.1f}%)"
                color_info = f"RGBA({r},{g},{b},{a})"
            else:
                color_display = (r/255, g/255, b/255, 1)
                label = f"{rank}. #{r:02x}{g:02x}{b:02x}\n{count:,d}px ({area_percent:.1f}%)"
                color_info = f"RGBA({r},{g},{b},{a})"
        else:
            r, g, b = color
            color_display = (r/255, g/255, b/255, 1)
            label = f"{rank}. #{r:02x}{g:02x}{b:02x}\n{count:,d}px ({area_percent:.1f}%)"
            color_info = f"RGB({r},{g},{b})"
        
        colors.append(color_display)
        counts.append(count)
        labels.append(label)
        color_infos.append((color_info, count, area_percent))
    
    # Создаем график
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. Исходное изображение
    ax1.imshow(img)
    ax1.set_title('Исходное изображение')
    ax1.axis('off')
    
    # 2. Диаграмма площадей (отсортированная)
    ax2.pie(counts, labels=labels, colors=colors, startangle=90)
    ax2.set_title('Распределение цветов по площади (отсортировано)')
    
    plt.tight_layout()
    plt.show()
    
    # Вывод текстовой информации (отсортированной)
    print("=" * 70)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА (ОТСОРТИРОВАНО ПО ПЛОЩАДИ)")
    print("=" * 70)
    print(f"Размер: {img.width} × {img.height} пикселей")
    print(f"Всего пикселей: {total_pixels:,d}")
    print(f"Уникальных цветов: {len(color_counter)}")
    print("\nЦвета отсортированы по убыванию площади:")
    print("-" * 70)
    
    print(f"{'№':>2} | {'Цвет':25} | {'Пикселей':>12} | {'Площадь, %':>10} | {'Доля':10}")
    print("-" * 70)
    
    cumulative_percent = 0
    for rank, (color_info, count, area_percent) in enumerate(color_infos, 1):
        cumulative_percent += area_percent
        # Создаем строку для визуализации доли
        bar_length = int(area_percent / 2)  # Масштабируем для отображения
        bar = "█" * bar_length
        
        print(f"{rank:2} | {color_info:25} | {count:12,d} | {area_percent:10.2f}% | {bar}")
    
    print("-" * 70)
    print(f"Суммарная площадь: {total_pixels:,d} px² (100.00%)")
    
    # Дополнительная статистика
    print("\nДополнительная статистика:")
    print(f"• Самый частый цвет занимает {color_infos[0][2]:.1f}% площади")
    print(f"• Топ-3 цвета занимают {sum([c[2] for c in color_infos[:3]]):.1f}% площади")
    print(f"• Топ-5 цветов занимают {sum([c[2] for c in color_infos[:5]]):.1f}% площади")

# Упрощенная версия для быстрого использования
def quick_color_analysis(image_path):
    """Быстрый анализ с сортировкой по площади"""
    img = Image.open(image_path)
    
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGBA')
    
    pixels = list(img.getdata())
    color_counter = Counter(pixels)
    total_pixels = len(pixels)
    
    # Сортируем по убыванию
    sorted_colors = sorted(color_counter.items(), key=lambda x: x[1], reverse=True)
    
    print(f"Анализ: {image_path}")
    print(f"Всего пикселей: {total_pixels:,d}")
    print("\nТоп цветов по площади:")
    print("-" * 55)
    
    for rank, (color, count) in enumerate(sorted_colors, 1):
        percent = (count / total_pixels) * 100
        
        if len(color) == 4:
            r, g, b, a = color
            color_str = f"RGBA({r:3d},{g:3d},{b:3d},{a:3d})"
            hex_str = f"#{r:02x}{g:02x}{b:02x}"
        else:
            r, g, b = color
            color_str = f"RGB({r:3d},{g:3d},{b:3d})"
            hex_str = f"#{r:02x}{g:02x}{b:02x}"
        
        # Отображаем только топ-10 или все, если меньше 10
        if rank <= 10 or len(sorted_colors) <= 10:
            print(f"{rank:2}. {color_str} {hex_str:10} - {count:8,d} px ({percent:6.2f}%)")
    
    if len(sorted_colors) > 10:
        other_count = sum(count for _, count in sorted_colors[10:])
        other_percent = (other_count / total_pixels) * 100
        print(f"   ... и еще {len(sorted_colors)-10} цветов: {other_count:,d} px ({other_percent:.2f}%)")

# Пример использования
if __name__ == "__main__":
    # Укажите путь к вашему изображению
    image_path = "C:/Users/Akulina/Documents/10б Неумойчева/РасчетПроцента крыш/Наш район разметка зон2.png"
    
    print("Выберите вариант анализа:")
    print("1. Подробный анализ с сортировкой")
    print("2. Быстрый анализ (только топ-10)")
    print("3. Анализ с визуализацией")
    
    choice = input("Введите номер (1-3): ").strip()
    
    if choice == "1":
        calculate_color_areas_sorted(image_path)
    elif choice == "2":
        quick_color_analysis(image_path)
    elif choice == "3":
        analyze_image_colors_sorted(image_path)
    else:
        # По умолчанию используем подробный анализ
        calculate_color_areas_sorted(image_path)