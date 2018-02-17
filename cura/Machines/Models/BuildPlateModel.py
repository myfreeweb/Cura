from PyQt5.QtCore import Qt

from UM.Application import Application
from UM.Qt.ListModel import ListModel

from cura.Machines.VariantManager import VariantType


class BuildPlateModel(ListModel):
    NameRole = Qt.UserRole + 1
    ContainerNodeRole = Qt.UserRole + 2

    def __init__(self, parent = None):
        super().__init__(parent)

        self.addRoleName(self.NameRole, "name")
        self.addRoleName(self.ContainerNodeRole, "container_node")

        self._application = Application.getInstance()
        self._variant_manager = self._application._variant_manager
        self._machine_manager = self._application.getMachineManager()

        self._machine_manager.globalContainerChanged.connect(self._update)

        self._update()

    def _update(self):
        global_stack = self._machine_manager._global_container_stack
        if not global_stack:
            self.setItems([])
            return

        variant_dict = self._variant_manager.getVariantNodes(global_stack, variant_type = VariantType.BUILD_PLATE)

        item_list = []
        for name, variant_node in variant_dict.items():
            item = {"name": name,
                    "container_node": variant_node}
            item_list.append(item)
        self.setItems(item_list)
