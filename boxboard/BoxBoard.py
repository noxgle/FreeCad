import os
import FreeCAD as App
import FreeCADGui as Gui


class GuiBoxBoard:

    def __init__(self):
        self.path_to_ui = os.path.join(App.getUserMacroDir(True), "boxboard/BoxBoard.ui")
        self.f = Gui.PySideUic.loadUi(self.path_to_ui)
        self.f.b_ok.clicked.connect(self.action)
        self.f.show()

    def action(self):
        b_width = self.f.i_width.text()
        b_height = self.f.i_height.text()
        b_depth = self.f.i_depth.text()
        b_thickness = self.f.i_thickness.text()
        b_front = self.f.i_front.isChecked()
        b_back = self.f.i_back.isChecked()
        external_dim = self.f.i_external.isChecked()
        if b_front is True:
            b_front = '1'
        else:
            b_front = '0'

        if b_back is True:
            b_back = '1'
        else:
            b_back = '0'

        if external_dim is True:
            external_dim = '1'
        else:
            external_dim = '0'

        BoxBoard(b_width=b_width, b_height=b_height, b_depth=b_depth, b_thickness=b_thickness, b_front=b_front,
                 b_back=b_back, external_dim=external_dim)


class BoxBoard:

    def __init__(self, b_width, b_height, b_depth, b_thickness, b_front='0', b_back='0', external_dim='1'):
        self.box_data = {}
        try:
            self.b_width = float(b_width)
            self.b_height = float(b_height)
            self.b_depth = float(b_depth)
            self.b_thickness = float(b_thickness)
            self.b_front = int(b_front)
            self.b_back = int(b_back)
            self.external_dim = int(external_dim)
        except Exception as e:
            App.Console.PrintError('Error! Only numbers without 0!')
            return
        if self.b_width == 0 or self.b_height == 0 or self.b_depth == 0 or self.b_thickness == 0:
            App.Console.PrintError('Error! Only numbers without 0!')
            return
        if self.external_dim == 1 and self.b_depth / self.b_thickness < self.b_front+self.b_back+1:
            App.Console.PrintError('Error! depth is to small! ')
            return
        self.create()
        self.draw()

    def create(self):

        if self.external_dim == 1:

            b1 = (self.b_height - (self.b_thickness * 2),
                  self.b_depth - (self.b_back * self.b_thickness) - (self.b_front * self.b_thickness),
                  self.b_thickness)
            b2 = (
                self.b_width,
                self.b_depth - (self.b_back * self.b_thickness) - (self.b_front * self.b_thickness),
                self.b_thickness)
            self.box_data = {'b1': b1, 'b2': b1, 'b3': b2, 'b4': b2}

            if self.b_back == 1:
                b_back = (self.b_width, self.b_height, self.b_thickness)
                self.box_data['b5'] = b_back

            if self.b_front == 1:
                b_front = (self.b_width, self.b_height, self.b_thickness)
                self.box_data['b6'] = b_front

        elif self.external_dim == 0:
            b1 = (self.b_height,
                  self.b_depth,
                  self.b_thickness)
            b2 = (
                self.b_width + (self.b_thickness * 2),
                self.b_depth,
                self.b_thickness)
            self.box_data = {'b1': b1, 'b2': b1, 'b3': b2, 'b4': b2}

            if self.b_back == 1:
                b_back = (self.b_width + 2 * self.b_thickness, self.b_height + 2 * self.b_thickness, self.b_thickness)
                self.box_data['b5'] = b_back

            if self.b_front == 1:
                b_front = (self.b_width + 2 * self.b_thickness, self.b_height + 2 * self.b_thickness, self.b_thickness)
                self.box_data['b6'] = b_front

    def draw(self):
        print(self.box_data)
        App.newDocument('Unnamed')

        part = 'b1'
        z = self.box_data[part][0]
        y = self.box_data[part][1]
        x = self.box_data[part][2]
        move_x = 0
        move_y = 0
        move_z = self.box_data[part][2]
        App.ActiveDocument.addObject("Part::Box", part)
        App.ActiveDocument.getObject(part).Width = y
        App.ActiveDocument.getObject(part).Height = z
        App.ActiveDocument.getObject(part).Length = x
        App.ActiveDocument.getObject(part).Placement = App.Placement(App.Vector(move_x, move_y, move_z),
                                                                     App.Rotation(App.Vector(0, 0, 1), 0))
        App.ActiveDocument.recompute()

        part = 'b2'
        z = self.box_data[part][0]
        y = self.box_data[part][1]
        x = self.box_data[part][2]
        move_x = self.box_data['b3'][0] - self.box_data[part][2]
        move_y = 0
        move_z = self.box_data[part][2]
        App.ActiveDocument.addObject("Part::Box", part)
        App.ActiveDocument.getObject(part).Width = y
        App.ActiveDocument.getObject(part).Height = z
        App.ActiveDocument.getObject(part).Length = x
        App.ActiveDocument.getObject(part).Placement = App.Placement(App.Vector(move_x, move_y, move_z),
                                                                     App.Rotation(App.Vector(0, 0, 1), 0))
        App.ActiveDocument.recompute()

        part = 'b3'
        x = self.box_data[part][0]
        y = self.box_data[part][1]
        z = self.box_data[part][2]
        move_x = 0
        move_y = 0
        move_z = 0
        App.ActiveDocument.addObject("Part::Box", part)
        App.ActiveDocument.getObject(part).Width = y
        App.ActiveDocument.getObject(part).Height = z
        App.ActiveDocument.getObject(part).Length = x
        App.ActiveDocument.getObject(part).Placement = App.Placement(App.Vector(move_x, move_y, move_z),
                                                                     App.Rotation(App.Vector(0, 0, 1), 0))
        App.ActiveDocument.recompute()

        part = 'b4'
        move_x = 0
        move_y = 0
        move_z = self.box_data[part][2] + self.box_data['b1'][0]
        App.ActiveDocument.addObject("Part::Box", part)
        App.ActiveDocument.getObject(part).Width = y
        App.ActiveDocument.getObject(part).Height = z
        App.ActiveDocument.getObject(part).Length = x
        App.ActiveDocument.getObject(part).Placement = App.Placement(App.Vector(move_x, move_y, move_z),
                                                                     App.Rotation(App.Vector(0, 0, 1), 0))
        App.ActiveDocument.recompute()

        if 'b5' in self.box_data:
            part = 'b5'

            y = self.box_data[part][0]
            z = self.box_data[part][1]
            x = self.box_data[part][2]

            move_x = 0
            move_y = -self.b_thickness
            move_z = 0
            App.ActiveDocument.addObject("Part::Box", part)
            App.ActiveDocument.getObject(part).Width = x
            App.ActiveDocument.getObject(part).Height = z
            App.ActiveDocument.getObject(part).Length = y
            App.ActiveDocument.getObject(part).Placement = App.Placement(App.Vector(move_x, move_y, move_z),
                                                                         App.Rotation(App.Vector(0, 0, 1), 0))
            App.ActiveDocument.recompute()

        if 'b6' in self.box_data:
            part = 'b6'

            y = self.box_data[part][0]
            z = self.box_data[part][1]
            x = self.box_data[part][2]

            move_x = 0
            move_y = self.box_data['b2'][1]
            move_z = 0
            App.ActiveDocument.addObject("Part::Box", part)
            App.ActiveDocument.getObject(part).Width = x
            App.ActiveDocument.getObject(part).Height = z
            App.ActiveDocument.getObject(part).Length = y
            App.ActiveDocument.getObject(part).Placement = App.Placement(App.Vector(move_x, move_y, move_z),
                                                                         App.Rotation(App.Vector(0, 0, 1), 0))
            App.ActiveDocument.recompute()

        # __objs__ = []
        # __objs__.append(App.getDocument('Unnamed').getObject("b1"))
        # __objs__.append(App.getDocument('Unnamed').getObject("b2"))
        # __objs__.append(App.getDocument('Unnamed').getObject("b3"))
        # __objs__.append(App.getDocument('Unnamed').getObject("b4"))


if __name__ == '__main__':
    G = GuiBoxBoard()
