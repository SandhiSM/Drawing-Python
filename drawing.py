from PIL import Image


class Draw:
    def __init__(self, title: str, file_format: str, size: tuple):
        self.title: str = title
        self.file_format: str = f".{file_format}"
        self.size: tuple = size
        self.horizontal: int = self.size[0]  # x
        self.vertical: int = self.size[1]  # y
        self.picture: list = list()
        self.image = Image.new("RGB", self.size, (255, 255, 255))
        self.generate()

    def generate(self):
        for y in range(0, self.vertical):
            self.picture.append(list())
            for _ in range(0, self.horizontal):
                self.picture[y].append((255, 255, 255))

    def color(self, scope: list, rgb: tuple):
        for place in scope:
            if len(place) == 2:
                x, y = place
                self.picture[y][x] = rgb
            else:  # len(place) == 4
                x1, y1, x2, y2 = place
                x1 -= 1
                y1 -= 1
                x2 -= 1
                y2 -= 1
        while True:
            if y1 == y2:
                if x1 != x2:
                    self.picture[y1][x1] = rgb
                else:
                    self.picture[y2][x2] = rgb
                    break
            else:
                if x1 <= self.horizontal - 1:
                    self.picture[y1][x1] = rgb
                else:
                    y1 += 1
                    x1 = 0
                    continue
            x1 += 1
        for y, line in enumerate(self.picture, 0):
            for x, color in enumerate(line, 0):
                self.image.putpixel((x, y), color)

    def scaling(self, size: tuple):
        self.image = self.image.resize(size, Image.LANCZOS)

    def show(self):  # not working
        self.image.show(f"{self.title}{self.file_format}")

    def show_list(self):
        print(self.picture)

    def save(self):
        self.image.save(fr".\output\{self.title}{self.file_format}")


def type_checker(check: str) -> bool:
    try:
        _ = int(check)
    except ValueError:
        return False
    else:
        if int(check) < 0:
            return False
        else:
            return True


def type_checker2(check: str) -> bool:
    try:
        _ = int(check)
    except ValueError:
        return False
    else:
        return True


def null_checker(check: str) -> bool:
    if check == '':
        return False
    else:
        return True


def content_checker(check: str) -> bool:
    if check.lower() == "jpeg" or check.lower() == "png":
        return True
    else:
        return False


def mode_branch(image):
    while True:
        mode: str = input(
            "Enter mode (available -> ['color', 'scaling', 'show', 'show_list, 'save', 'exit']) > ")
        match mode:
            case "color":
                scope: list = list()
                while True:
                    x1: str = input(
                        "Position of X from (If there are no more or you want to exit, leave this blank.) > ")
                    if x1 == '':
                        if len(scope) == 0:
                            break
                        else:
                            r: str = input("Enter r of rgb > ")
                            g: str = input("Enter g of rgb > ")
                            b: str = input("Enter b of rgb > ")
                            if type_checker2(r) and type_checker2(g) and type_checker2(b):
                                if int(r) <= 255 and int(g) <= 255 and int(b) <= 255:
                                    rgb: tuple = (int(r), int(g), int(b))
                                    Draw.color(image, scope, rgb)
                                    scope.clear()
                                else:
                                    print("Something is not written or valid.")
                                    break
                            else:
                                print("Something is not written or valid.")
                                break
                    else:
                        y1: str = input("Position of Y from > ")
                        x2: str = input(
                            "Position of X to (If you don't specify a range, leave this blank.) > ")
                        if x2 == '':
                            if type_checker(x1) and type_checker(y1):
                                scope.append((int(x1), int(y1)))
                            else:
                                print("Something is not written or valid.")
                                break
                        else:
                            y2: str = input("Position of Y to > ")
                            if type_checker(x1) and type_checker(x2) and type_checker(y1) and type_checker(y2):
                                if y1 <= y2:
                                    scope.append(
                                        (int(x1), int(y1), int(x2), int(y2)))
                                else:
                                    print("Something is not written or valid.")
                                    break
                            else:
                                print("Something is not written or valid.")
                                break
            case "scaling":
                x: str = input("Enter the x value to resize > ")
                y: str = input("Enter the y value to resize > ")
                if type_checker(x) and type_checker(y):
                    size: tuple = (int(x), int(y))
                    Draw.scaling(image, size)
                else:
                    print("Something is not written or valid.")
            case "show":
                Draw.show(image)
            case "show_list":
                Draw.show_list(image)
            case "save":

                Draw.save(image)
            case "exit":
                break
            case _:
                print("Invalid syntax.")


def main():
    title: str = input("Enter image title > ")
    file_format: str = input(
        "Enter file format (available -> ['PNG', 'JPEG']) > ")
    x: str = input("Enter size of X > ")
    y: str = input("Enter size of Y > ")
    if null_checker(title) and content_checker(file_format):
        if type_checker(x) and type_checker(y):
            size: tuple = (int(x), int(y))
            image = Draw(title, file_format, size)
            mode_branch(image)
        else:
            print("Something is not written or valid.")
    else:
        print("Something is not written or valid.")


if __name__ == "__main__":
    main()
