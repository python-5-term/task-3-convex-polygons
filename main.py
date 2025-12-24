import math
from convex_polygon import ConvexPolygon


def main():
    print("=" * 60)
    print("Тестирование класса ConvexPolygon")
    print("=" * 60)
    
    print("\n1. Простые выпуклые многоугольники:")
    
    print("\n   Квадрат:")
    square = ConvexPolygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    print(f"     Площадь: {square.area()}")
    print(f"     Периметр: {square.perimeter()}")
    print(f"     (0.5, 0.5) внутри: {square.contains_point((0.5, 0.5))}")
    
    print("\n   Треугольник:")
    triangle = ConvexPolygon([(0, 0), (2, 0), (1, 2)])
    print(f"     Площадь: {triangle.area():.2f}")
    print(f"     Периметр: {triangle.perimeter():.2f}")
    print(f"     (1, 0.5) внутри: {triangle.contains_point((1, 0.5))}")
    
    print("\n   Шестиугольник:")
    hexagon = ConvexPolygon([(0, 0), (2, 0), (3, 1), (2, 2), (0, 2), (-1, 1)])
    print(f"     Площадь: {hexagon.area():.2f}")
    print(f"     Периметр: {hexagon.perimeter():.2f}")
    print(f"     (1, 1) внутри: {hexagon.contains_point((1, 1))}")
    
    print("\n2. Невыпуклые многоугольники:")
    
    print("\n   Вогнутый четырехугольник:")
    try:
        concave = ConvexPolygon([(0, 0), (3, 0), (1, 1), (3, 3), (0, 3)])
        print("     ОШИБКА: Принят как выпуклый!")
    except ValueError as e:
        print(f"     {e}")
    
    print("\n   Самопересекающийся (бант):")
    try:
        bowtie = ConvexPolygon([(0, 0), (2, 2), (0, 2), (2, 0)])
        print("     ОШИБКА: Принят как выпуклый!")
    except ValueError as e:
        print(f"     {e}")
    
    print("\n   Спираль (несколько оборотов):")
    try:
        spiral = []
        for i in range(12):
            angle = 2 * 2 * math.pi * i / 12  # 2 оборота
            r = 1 + 0.5 * i / 12
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            spiral.append((x, y))
        
        spiral_poly = ConvexPolygon(spiral)
        print("     ОШИБКА: Принята как выпуклая!")
    except ValueError as e:
        print(f"     {e}")
    
    print("\n3. Операции с многоугольниками:")
    
    print("\n   Триангуляция квадрата:")
    print(f"     {square.triangulate()}")
    
    print("\n   Пересечение двух квадратов:")
    poly1 = ConvexPolygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    poly2 = ConvexPolygon([(1, 1), (3, 1), (3, 3), (1, 3)])
    intersection = poly1.intersect(poly2)
    if intersection:
        print(f"     Пересечение существует")
        print(f"     Площадь пересечения: {intersection.area():.2f}")
    else:
        print("     Пересечения нет")
    
    print("\n4. Особые случаи:")
    
    print("\n   Точка на границе квадрата:")
    print(f"     (0, 0.5) на границе: {square.contains_point((0, 0.5))}")
    print(f"     (0, 0.5) строго внутри: {square.contains_point((0, 0.5), include_boundary=False)}")
    
    print("\n   Недостаточно вершин:")
    try:
        line = ConvexPolygon([(0, 0), (1, 1)])
        print("     ОШИБКА: Принят как многоугольник!")
    except ValueError as e:
        print(f"     {e}")
    
    print("\n   Пятиугольник по часовой стрелке:")
    cw_pentagon = ConvexPolygon([(0, 0), (0, 2), (1, 3), (2, 2), (2, 0)][::-1])
    print(f"     Автоматически исправлен на против часовой стрелки")
    print(f"     Площадь: {cw_pentagon.area():.2f}")
    
    print("\n5. Дополнительные тесты:")
    
    print("\n   Правильный пятиугольник:")
    pentagon = ConvexPolygon([
        (0, 0), (1, 2), (3, 2), (4, 0), (2, -1)
    ])
    print(f"     Площадь: {pentagon.area():.2f}")
    print(f"     (2, 1) внутри: {pentagon.contains_point((2, 1))}")
    
    print("\n   Тест на несколько оборотов:")
    # Создаем фигуру, где все повороты в одну сторону, но делается 2 оборота
    counter_example = []
    for i in range(8):
        angle = 4 * math.pi * i / 8  # 2 полных оборота
        r = 1 + 0.2 * (i % 2)  # Немного меняем радиус
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        counter_example.append((x, y))
    
    try:
        counter_poly = ConvexPolygon(counter_example)
        print("     ОШИБКА: Контрпример принят как выпуклый!")
    except ValueError as e:
        print(f"     {e}")
    
    print("\n" + "=" * 60)
    print("Все тесты завершены!")
    print("=" * 60)


if __name__ == "__main__":
    main()
