from PIL import Image
import pickle
import os


class Draw:
    def __init__(self, title: str, file_format: str, size: tuple) -> None:
        self.title: str = title
        self.file_format: str = f".{file_format}"
        self.size: tuple = size
        self.horizontal, self.vertical = self.size
        self.picture: list = list()
        self.image: Image = Image.new("RGB", self.size, (255, 255, 255))
        self.generate()

    def generate(self) -> None:
        for y in range(0, self.vertical):
            self.picture.append(list())
            for _ in range(0, self.horizontal):
                self.picture[y].append((255, 255, 255))

    def scope_checker(self, scopes: list) -> bool:
        for scope in scopes:
            if len(scope) == 2:
                if scope[0] <= self.horizontal and scope[1] <= self.vertical:
                    pass
                else:
                    return False
            else:
                if scope[0] <= self.horizontal and scope[1] <= self.vertical and scope[2] <= self.horizontal and scope[3] <= self.vertical:
                    pass
                else:
                    return False
        else:
            return True

    def scope_checker2(self, block: tuple, scopes: list) -> bool:
        self.width, self.height = block
        for scope in scopes:
            if len(scope) == 2:
                if scope[0] * self.width <= self.horizontal and scope[1] * self.height <= self.vertical:
                    pass
                else:
                    return False
            else:
                if scope[0] * self.width <= self.horizontal and scope[2] * self.width <= self.horizontal and scope[3] * self.height <= self.vertical:
                    pass
                else:
                    return False
        else:
            return True

    def division_checker(self, block: tuple) -> bool:
        x, y = block
        return self.horizontal % x == 0 and self.vertical % y == 0

    def load(self, name: str, file_format: str) -> None:
        with open(fr".\output\temp\{name}.pickle", "rb") as f:
            self.picture = pickle.load(f)
        self.title: str = name
        self.file_format: str = f".{file_format}"
        self.horizontal: int = len(self.picture[0])
        self.vertical: int = len(self.picture)
        self.size: tuple = (self.horizontal, self.vertical)
        self.image: Image = Image.new("RGB", self.size, (255, 255, 255))
        for y, line in enumerate(self.picture, 0):
            for x, color in enumerate(line, 0):
                self.image.putpixel((x, y), color)

    def pixel_color(self, scope: list, rgb: tuple) -> None:
        for place in scope:
            if len(place) == 2:
                x, y = place
                self.picture[y-1][x-1] = rgb
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

    def block_color(self, scope: list, rgb: tuple) -> None:
        scopes: list = list()
        for place in scope:
            if len(place) == 2:
                x, y = place
                x1: int = self.width * x - self.width + 1
                y1: int = self.height * y - self.height + 1
                x2: int = self.width * x
                y2_: int = self.height * y + 1
                for y2 in range(y1, y2_):
                    scopes.append((x1, y2, x2, y2))
                self.pixel_color(scopes, rgb)
                scopes.clear()
            else:  # len(place) == 4
                x1, y1, x2, y2 = place
                x1: int = self.width * x1 - self.width + 1
                y1: int = self.height * y1 - self.height + 1
                x2: int = self.width * x2
                y2_: int = self.height * y2 + 1
                for y2 in range(y1, y2_):
                    scopes.append((x1, y2, x2, y2))
                self.pixel_color(scopes, rgb)
                scopes.clear()

    def scaling(self, size: tuple) -> None:
        self.image = self.image.resize(size, Image.LANCZOS)

    def show(self) -> None:
        self.scaling(self.size)
        self.image.show(f"{self.title}{self.file_format}")

    def show_list(self) -> None:
        print(self.picture)

    def temporary_save(self) -> None:
        with open(fr".\output\temp\{self.title}.pickle", "wb") as f:
            pickle.dump(self.picture, f)

    def save(self, ediable: bool = False) -> None:
        self.scaling(self.size)
        self.image.save(fr".\output\completed\{self.title}{self.file_format}")
        if ediable:
            self.temporary_save()

    @staticmethod
    def show_color_sample(rgb: tuple):
        color_sample = Image.new("RGB", (512, 512), rgb)
        color_sample.show()


class ValidChecker:
    def type_checker(check: str) -> bool:
        try:
            _ = int(check)
        except ValueError:
            return False
        else:
            return True

    def type_checker2(check: str) -> bool:
        if ValidChecker.type_checker(check):
            return int(check) > 0

    def null_checker(check: str) -> bool:
        return check != ''

    def content_checker(check: str) -> bool:
        return check.lower() == "jpeg" or check.lower() == "png"

    def exist_checker(file_name: str) -> bool:
        return os.path.exists(fr".\output\temp\{file_name}.pickle")


def mode_branch(image) -> None:
    while True:
        mode: str = input(
            "Enter mode (available -> ['load', 'pixelcolor', 'blockcolor', 'scaling', 'show', 'showcolorsample', 'show_list, 'temporarysave', 'save'(Type 'save -e' to set to 'ediable'), 'exit']) > ")
        match mode:
            case "load":
                name: str = input("Input image title to load > ")
                file_format: str = input(
                    "Enter file format (available -> ['PNG', 'JPEG']) > ")
                if ValidChecker.exist_checker(name):
                    if ValidChecker.content_checker(file_format):
                        Draw.load(image, name, file_format)
                    else:
                        print("File Format is inappropriate.")
                else:
                    print("No such file exists.")
            case "pixelcolor":
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
                            if ValidChecker.type_checker(r) and ValidChecker.type_checker(g) and ValidChecker.type_checker(b):
                                if int(r) <= 255 and int(g) <= 255 and int(b) <= 255:
                                    rgb: tuple = (int(r), int(g), int(b))
                                    if Draw.scope_checker(image, scope):
                                        Draw.pixel_color(image, scope, rgb)
                                        scope.clear()
                                    else:
                                        print(
                                            "Something is not written or valid.")
                                        break
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
                            if ValidChecker.type_checker2(x1) and ValidChecker.type_checker2(y1):
                                scope.append((int(x1), int(y1)))
                            else:
                                print("Something is not written or valid.")
                                break
                        else:
                            y2: str = input("Position of Y to > ")
                            if ValidChecker.type_checker2(x1) and ValidChecker.type_checker2(x2) and ValidChecker.type_checker2(y1) and ValidChecker.type_checker2(y2):
                                if int(y1) <= int(y2):
                                    scope.append(
                                        (int(x1), int(y1), int(x2), int(y2)))
                                else:
                                    print("Something is not written or valid.")
                                    break
                            else:
                                print("Something is not written or valid.")
                                break

            case "blockcolor":
                scope: list = list()
                x: str = input("Enter the width of one block > ")
                y: str = input("Enter the height of ont block > ")
                if ValidChecker.type_checker2(x) and ValidChecker.type_checker2(y):
                    block: tuple = (int(x), int(y))
                    if Draw.division_checker(image, block):
                        while True:
                            x1: str = input(
                                "Block position of X from (If there are no more or you want to exit, leave blank.) > ")
                            if x1 == '':
                                if len(scope) == 0:
                                    break
                                else:
                                    r: str = input("Enter r of rgb > ")
                                    g: str = input("Enter g of rgb > ")
                                    b: str = input("Enter b of rgb > ")
                                    if ValidChecker.type_checker(r) and ValidChecker.type_checker(g) and ValidChecker.type_checker(b):
                                        if int(r) <= 255 and int(g) <= 255 and int(b) <= 255:
                                            rgb: tuple = (
                                                int(r), int(g), int(b))
                                            if Draw.scope_checker2(image, block, scope):
                                                Draw.block_color(
                                                    image, scope, rgb)
                                                scope.clear()
                                            else:
                                                print(
                                                    "Something is not written or valid.")
                                                break
                                        else:
                                            print(
                                                "Something is not written or valid.")
                                            break
                                    else:
                                        print(
                                            "Something is not written or valid.")
                                        break
                            else:
                                y1: str = input("Block position of Y from > ")
                                x2: str = input(
                                    "Block position of X to (If you don't specify a range, leave this blank.) > ")
                                if x2 == '':
                                    if ValidChecker.type_checker2(x1) and ValidChecker.type_checker2(y1):
                                        scope.append((int(x1), int(y1)))
                                    else:
                                        print(
                                            "Something is not written or valid.")
                                        break
                                else:
                                    y2: str = input(
                                        "Block position of Y to > ")
                                    if ValidChecker.type_checker2(x1) and ValidChecker.type_checker2(x2) and ValidChecker.type_checker2(y1) and ValidChecker.type_checker2(y2):
                                        if int(y1) <= int(y2):
                                            scope.append(
                                                (int(x1), int(y1), int(x2), int(y2)))
                                        else:
                                            print(
                                                "The y specified after must be greater than or equal to the y specified before.")
                                            break
                                    else:
                                        print(
                                            "Something is not written or valid.")
                                        break
                    else:
                        print(
                            "The width and height of the block must be an integral number of the overall size.")
                else:
                    print("Something is not written or valid.")

            case "scaling":
                x: str = input("Enter the x value to resize > ")
                y: str = input("Enter the y value to resize > ")
                if ValidChecker.type_checker2(x) and ValidChecker.type_checker2(y):
                    size: tuple = (int(x), int(y))
                    Draw.scaling(image, size)
                else:
                    print("Something is not written or valid.")

            case "show":
                Draw.show(image)

            case "showcolorsample":
                r: str = input("Enter r of rgb > ")
                g: str = input("Enter g of rgb > ")
                b: str = input("Enter b of rgb > ")
                if ValidChecker.type_checker(r) and ValidChecker.type_checker(g) and ValidChecker.type_checker(b):
                    if int(r) <= 255 and int(g) <= 255 and int(b) <= 255:
                        rgb: tuple = (int(r), int(g), int(b))
                        Draw.show_color_sample(rgb)
                    else:
                        print("RGB must be 0~255.")
                else:
                    print("Something is not written or valid.")

            case "show_list":
                Draw.show_list(image)

            case "temporarysave":
                Draw.temporary_save(image)

            case "save":
                Draw.save(image)

            case "save -e":
                Draw.save(image, ediable=True)

            case "exit":
                break

            case _:
                print("Invalid syntax.")


def main() -> None:
    print("If you use the 'load' mode, you can use any number you like, but I don't recommend using unnecessarily large numbers, as it will take a long time to process them.")
    title: str = input("Enter image title > ")
    file_format: str = input(
        "Enter file format (available -> ['PNG', 'JPEG']) > ")
    x: str = input("Enter size of X > ")
    y: str = input("Enter size of Y > ")
    if ValidChecker.null_checker(title) and ValidChecker.content_checker(file_format):
        if ValidChecker.type_checker2(x) and ValidChecker.type_checker2(y):
            size: tuple = (int(x), int(y))
            image: Draw = Draw(title, file_format, size)
            mode_branch(image)
        else:
            print("Something is not written or valid.")
    else:
        print("Something is not written or valid.")


if __name__ == "__main__":
    main()
