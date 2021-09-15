from pathlib import Path
from collections import defaultdict

import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, GappedSquareModuleDrawer, HorizontalBarsDrawer, RoundedModuleDrawer, SquareModuleDrawer, VerticalBarsDrawer
from qrcode.image.styles.colormasks import HorizontalGradiantColorMask, RadialGradiantColorMask, SolidFillColorMask, SquareGradiantColorMask, VerticalGradiantColorMask


DATA_DIR = Path(__file__).parent / "output"


class CustomQrCode(qrcode.QRCode):
    def __init__(self, data="", qr_color="black", bg_color="white",
                 edge_color="", qr_size=1, box_size=10, border=1):
        super().__init__()
        self.color = qr_color
        self.bg_color = bg_color
        self.edge_color = edge_color
        self.version = qr_size
        self.box_size = box_size
        self.border = border
        self.error_correction = qrcode.constants.ERROR_CORRECT_H
        self.add_data(data)
        self.make()

    def create(self, img_path="", mod="", color_mask=""):
              
        mod_dic = defaultdict(lambda: SquareModuleDrawer())
        mod_dic["rounded"] = RoundedModuleDrawer()
        mod_dic["square"] = GappedSquareModuleDrawer()
        mod_dic["Vbar"] = VerticalBarsDrawer()
        mod_dic["Hbar"] = HorizontalBarsDrawer()
        mod_dic["circle"] = CircleModuleDrawer()
        mod = mod_dic[mod]

        mask_dic = defaultdict(lambda: SolidFillColorMask(
            back_color=self.bg_color, front_color=self.color))
        mask_dic["RadialGradiant"] = RadialGradiantColorMask(
            back_color=self.bg_color, edge_color=self.edge_color, center_color=self.color)
        mask_dic["SquareGradiant"] = SquareGradiantColorMask(
            back_color=self.bg_color, edge_color=self.edge_color, center_color=self.color)
        mask_dic["HorizontalGradiant"] = HorizontalGradiantColorMask(
            back_color=self.bg_color, left_color=self.color, right_color=self.edge_color)
        mask_dic["VerticalGradiant"] = VerticalGradiantColorMask(
            back_color=self.bg_color, top_color=self.color, bottom_color=self.edge_color)
        mask = mask_dic[color_mask]

        img = self.make_image(image_factory=StyledPilImage, module_drawer=mod, color_mask=mask,
                              embeded_image_path=img_path)

        img.save(DATA_DIR / "qrcode.png")


if __name__ == "__main__":
    qrcode = CustomQrCode("coucou comment tu va bien?", qr_color=(
        255, 0, 0), bg_color=(0, 255, 0), edge_color=(0, 0, 255))
    qrcode.create(img_path="python.png", mod="square",
                  color_mask="RadialGradiant")
