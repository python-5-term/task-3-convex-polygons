import math
from itertools import combinations


class ConvexPolygon:
    def __init__(self, vertices):
        """
        vertices: список кортежей (x, y)
        """
        if len(vertices) < 3:
            raise ValueError("Многоугольник должен иметь минимум 3 вершины.")
        self.vertices = vertices #сохраняем вершины
        if not self._is_convex():
            raise ValueError("Переданные вершины не образуют выпуклый многоугольник.")

    # ---------- Проверка выпуклости ----------
    def _is_convex(self):
        """Проверяет, является ли многоугольник выпуклым.
        Выпуклость определяется по знаку векторного произведения соседних рёбер.
        Все знаки должны быть одинаковыми."""
        n = len(self.vertices)
        signs = []
        for i in range(n):
            #три последовательные вершины
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            x3, y3 = self.vertices[(i + 2) % n]
            #векторное произведение
            cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x1)
            signs.append(cross)
        return all(s >= 0 for s in signs) or all(s <= 0 for s in signs)

    # ---------- Площадь ----------
    def area(self):
        """Вычисляет площадь по формуле Гаусса."""
        n = len(self.vertices)
        s = 0
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            s += x1 * y2 - x2 * y1
        return abs(s) / 2

    # ---------- Периметр ----------
    def perimeter(self):
        """Вычисляет периметр."""
        n = len(self.vertices)
        p = 0
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            p += math.hypot(x2 - x1, y2 - y1)
        return p

    # ---------- Проверка нахождения точки внутри ----------
    def contains_point(self, point):
        """Проверяет, находится ли точка внутри выпуклого многоугольника."""
        x, y = point
        n = len(self.vertices)
        prev_sign = None
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
            sign = cross >= 0
            if prev_sign is None:
                prev_sign = sign
            elif sign != prev_sign:
                #если знак отличается - точка снаружи
                return False
        return True

    # ---------- Триангуляция ----------
    def triangulate(self):
        """
        Для выпуклого многоугольника триангуляция тривиальна:
        можно соединять вершину 0 с каждой парой соседних.
        """
        triangles = []
        for i in range(1, len(self.vertices) - 1):
            tri = [self.vertices[0], self.vertices[i], self.vertices[i + 1]]
            triangles.append(tri)
        return triangles

    # ---------- Пересечение двух выпуклых многоугольников ----------
    def intersect(self, other):
        """
        Реализовано через алгоритм отсечения Сазерленда–Ходжмана.
        Возвращает новый ConvexPolygon или None, если нет пересечения.
        """
        # Проверяет, находится ли точка внутри полуплоскости относительно ребра
        def inside(p, edge_start, edge_end):
            return (edge_end[0] - edge_start[0]) * (p[1] - edge_start[1]) - \
                   (edge_end[1] - edge_start[1]) * (p[0] - edge_start[0]) >= 0
         # Находит точку пересечения двух отрезков (p1-p2) и (e1-e2)
        def intersection(p1, p2, e1, e2):
            A1 = p2[1] - p1[1]
            B1 = p1[0] - p2[0]
            C1 = A1 * p1[0] + B1 * p1[1]
            A2 = e2[1] - e1[1]
            B2 = e1[0] - e2[0]
            C2 = A2 * e1[0] + B2 * e1[1]
            det = A1 * B2 - A2 * B1
            if det == 0:
                return None  # параллельные
            x = (B2 * C1 - B1 * C2) / det
            y = (A1 * C2 - A2 * C1) / det
            return (x, y)
        #отсечение каждой стороны другого многоугольника
        output = self.vertices[:]
        for i in range(len(other.vertices)):
            input_list = output
            output = []
            A = other.vertices[i]
            B = other.vertices[(i + 1) % len(other.vertices)]
            if not input_list:
                break
            S = input_list[-1]
            for E in input_list:
                if inside(E, A, B):
                    if not inside(S, A, B):
                        output.append(intersection(S, E, A, B))
                    output.append(E)
                elif inside(S, A, B):
                    output.append(intersection(S, E, A, B))
                S = E
        if len(output) < 3:  # Если меньше 3 вершин — пересечения нет
            return None
        return ConvexPolygon(output)

    def __repr__(self):
        return f"ConvexPolygon({self.vertices})"


def _print_polygon(name, poly: ConvexPolygon):
    print(f"\n{name}:")
    for i, (x, y) in enumerate(poly.vertices, start=1):
        print(f"  Вершина {i}: ({x:.3f}, {y:.3f})")
    print(f"  Кол-во вершин: {len(poly.vertices)}")
    print(f"  Площадь: {poly.area():.3f}")
    print(f"  Периметр: {poly.perimeter():.3f}")


if __name__ == "__main__":
    print("=== Тестовый запуск ConvexPolygon ===")

    # ----- Исходные многоугольники -----
    poly1 = ConvexPolygon([(0, 0), (4, 0), (4, 4), (0, 4)])
    poly2 = ConvexPolygon([(2, 2), (6, 2), (6, 6), (2, 6)])

    print("\n=== Исходные многоугольники ===")
    _print_polygon("poly1", poly1)
    _print_polygon("poly2", poly2)

    # ----- Проверка точек -----
    print("\n=== Проверка точек внутри poly1 ===")
    test_points = [
        (1, 1),   # внутри
        (4, 2),   # на границе
        (5, 5)    # снаружи
    ]
    for i, p in enumerate(test_points, start=1):
        inside = poly1.contains_point(p)
        print(f"  Точка {i}: {p} -> внутри? {inside}")

    # ----- Триангуляция -----
    print("\n=== Триангуляция poly1 ===")
    triangles = poly1.triangulate()
    for i, tri in enumerate(triangles, start=1):
        print(f"  Треугольник {i}:")
        for j, (x, y) in enumerate(tri, start=1):
            print(f"    Вершина {j}: ({x:.3f}, {y:.3f})")

    # ----- Пересечение двух многоугольников -----
    print("\n=== Пересечение poly1 и poly2 ===")
    intersection = poly1.intersect(poly2)

    if intersection is None:
        print("  Пересечения нет (intersection = None)")
    else:
        print("  Пересекаются! Полученный многоугольник пересечения:")
        _print_polygon("intersection", intersection)

        print("\n  Вершины многоугольника пересечения по порядку:")
        for i, (x, y) in enumerate(intersection.vertices, start=1):
            print(f"    Пересечение: вершина {i}: ({x:.3f}, {y:.3f})")

        print(f"\n  Площадь пересечения: {intersection.area():.3f}")
