class Point:
    def __init__(self, x: int, y: int):
        self.col = x
        self.row = y

    def collides_with(self, p: "Point") -> bool:
        return self.col == p.col and self.row == p.row
    
    def __add__(self, p: "Point") -> "Point":
        return Point(self.col + p.col, self.row + p.row)
    
    def __iter__(self):
        return iter((self.col, self.row))
    
    def __str__(self) -> str:
        return f"({self.col}, {self.row})"