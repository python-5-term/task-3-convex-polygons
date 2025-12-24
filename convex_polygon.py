import math


class ConvexPolygon:
    def __init__(self, vertices):
        """
        vertices: список кортежей (x, y) в порядке обхода
        """
        if len(vertices) < 3:
            raise ValueError("Многоугольник должен иметь минимум 3 вершины.")

        unique_vertices = []
        for v in vertices:
            if not unique_vertices or v != unique_vertices[-1]:
                unique_vertices.append(v)

        if len(unique_vertices) < 3:
            raise ValueError("Вершины образуют отрезок или точку.")
        
        self.vertices = unique_vertices

        if not self._is_convex():
            raise ValueError("Переданные вершины не образуют выпуклый многоугольник.")

        if self._signed_area() < 0:
            self.vertices = list(reversed(self.vertices))
    
    def _signed_area(self):
        """Вычисляет знаковую площадь (отрицательная если по часовой стрелке)."""
        area = 0
        n = len(self.vertices)
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            area += x1 * y2 - x2 * y1
        return area / 2
    
    def _cross_product(self, o, a, b):
        """Векторное произведение OA x OB."""
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    
    def _is_convex(self):
        """
        Проверяет, является ли многоугольник выпуклым.
        
        Алгоритм:
        1. Для каждой вершины вычисляем векторное произведение двух последовательных ребер
        2. Все векторные произведения должны иметь одинаковый знак
        3. Дополнительно проверяем, что нет самопересечений
        """
        n = len(self.vertices)
        if n < 3:
            return False

        for i in range(n):
            for j in range(i + 1, n):
                if self.vertices[i] == self.vertices[j]:
                    return False

        sign = 0  
        
        for i in range(n):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % n]
            c = self.vertices[(i + 2) % n]
            
            # Векторное произведение AB x BC
            cross = self._cross_product(a, b, c)
            
            if abs(cross) < 1e-10:
                continue
            
            if sign == 0:
                sign = 1 if cross > 0 else -1
            else:
                current_sign = 1 if cross > 0 else -1
                if current_sign != sign:
                    return False
        
        if sign == 0:
            return False
        
        # Дополнительная проверка на самопересечение
        # Проверяем пересечение непоследовательных сторон
        for i in range(n):
            for j in range(i + 2, n):
                # Пропускаем соседние стороны (у них общая вершина)
                if (j + 1) % n == i:
                    continue
                
                p1 = self.vertices[i]
                p2 = self.vertices[(i + 1) % n]
                q1 = self.vertices[j]
                q2 = self.vertices[(j + 1) % n]
                
                if self._segments_intersect(p1, p2, q1, q2, include_endpoints=False):
                    return False
        
        return True
    
    def _segments_intersect(self, p1, p2, q1, q2, include_endpoints=False):
        """
        Проверяет, пересекаются ли отрезки p1-p2 и q1-q2.
        """
        def orientation(a, b, c):
            """Ориентация тройки точек (a, b, c)."""
            val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
            if abs(val) < 1e-10:
                return 0
            return 1 if val > 0 else -1
        
        def on_segment(a, b, c):
            """Проверяет, лежит ли точка b на отрезке a-c."""
            return (min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and
                    min(a[1], c[1]) <= b[1] <= max(a[1], c[1]))
        
        o1 = orientation(p1, p2, q1)
        o2 = orientation(p1, p2, q2)
        o3 = orientation(q1, q2, p1)
        o4 = orientation(q1, q2, p2)
        
        if o1 != o2 and o3 != o4:
            return True
        
        if include_endpoints:
            if o1 == 0 and on_segment(p1, q1, p2):
                return True
            if o2 == 0 and on_segment(p1, q2, p2):
                return True
            if o3 == 0 and on_segment(q1, p1, q2):
                return True
            if o4 == 0 and on_segment(q1, p2, q2):
                return True
        
        return False

    def area(self):
        """Вычисляет площадь по формуле шнуровки."""
        return abs(self._signed_area())

    def perimeter(self):
        """Вычисляет периметр."""
        n = len(self.vertices)
        p = 0
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            p += math.hypot(x2 - x1, y2 - y1)
        return p

    def contains_point(self, point, include_boundary=True):
        """
        Проверяет, находится ли точка внутри выпуклого многоугольника.
        """
        x, y = point
        n = len(self.vertices)
        
        # Проверяем, лежит ли точка на границе
        if include_boundary:
            for i in range(n):
                x1, y1 = self.vertices[i]
                x2, y2 = self.vertices[(i + 1) % n]
                
                # Проверяем коллинеарность
                cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
                if abs(cross) > 1e-10:
                    continue
                
                # Проверяем, что точка между вершинами
                if (min(x1, x2) <= x <= max(x1, x2) and
                    min(y1, y2) <= y <= max(y1, y2)):
                    return True
        
        # Для выпуклого многоугольника достаточно проверить, что точка находится с одной стороны от всех ребер
        for i in range(n):
            x1, y1 = self.vertices[i]
            x2, y2 = self.vertices[(i + 1) % n]
            
            cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
            
            if cross < 0:  # Точка справа от ребра (снаружи)
                return False
        
        return True
    
    def triangulate(self):
        """
        Триангуляция выпуклого многоугольника методом веера.
        """
        n = len(self.vertices)
        if n < 3:
            return []
        
        triangles = []
        for i in range(1, n - 1):
            triangle = [self.vertices[0], self.vertices[i], self.vertices[i + 1]]
            triangles.append(triangle)
        
        return triangles
    
    def intersect(self, other):
        """
        Алгоритм отсечения Сазерленда-Ходжмана.
        """
        def inside(p, edge_start, edge_end):
            return (edge_end[0] - edge_start[0]) * (p[1] - edge_start[1]) - \
                   (edge_end[1] - edge_start[1]) * (p[0] - edge_start[0]) >= 0
        
        def line_intersection(p1, p2, e1, e2):
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = e1
            x4, y4 = e2
            
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denom) < 1e-10:
                return None
            
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            
            if 0 <= t <= 1:
                x = x1 + t * (x2 - x1)
                y = y1 + t * (y2 - y1)
                return (x, y)
            
            return None
        
        output_poly = self.vertices[:]
        
        for i in range(len(other.vertices)):
            if not output_poly:
                break
                
            input_poly = output_poly
            output_poly = []
            
            edge_start = other.vertices[i]
            edge_end = other.vertices[(i + 1) % len(other.vertices)]
            
            if not input_poly:
                continue
                
            S = input_poly[-1]
            
            for E in input_poly:
                if inside(E, edge_start, edge_end):
                    if not inside(S, edge_start, edge_end):
                        intersect_pt = line_intersection(S, E, edge_start, edge_end)
                        if intersect_pt:
                            output_poly.append(intersect_pt)
                    output_poly.append(E)
                elif inside(S, edge_start, edge_end):
                    intersect_pt = line_intersection(S, E, edge_start, edge_end)
                    if intersect_pt:
                        output_poly.append(intersect_pt)
                
                S = E
        
        if len(output_poly) < 3:
            return None
        
        # Удаление дубликатов
        unique_points = []
        for p in output_poly:
            if not unique_points or p != unique_points[-1]:
                unique_points.append(p)
        
        if len(unique_points) > 1 and unique_points[0] == unique_points[-1]:
            unique_points.pop()
        
        if len(unique_points) < 3:
            return None
        
        try:
            return ConvexPolygon(unique_points)
        except ValueError:
            return None
    
    def __repr__(self):
        return f"ConvexPolygon({self.vertices})"
    
    def __str__(self):
        return f"Выпуклый многоугольник с {len(self.vertices)} вершинами, площадь={self.area():.2f}"
