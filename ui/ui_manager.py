# ui/ui_manager.py
import pygame
import json
from ui.label import Label
from ui.image import UIImage
from ui.image_button import ImageButton

class UIManager:
    def __init__(self):
        self.ui_list = []

    def add(self, ui_obj):
        self.ui_list.append(ui_obj)

    def handle_events(self, event):
        # 클릭 이벤트는 보통 위에 있는 UI부터 처리해야 하므로 layer 역순
        for ui in sorted(self.ui_list, key=lambda x: x.layer, reverse=True):
            if ui.visible:
                result = ui.handle_event(event)
                if result:
                    return ui  # 클릭된 UI 객체 반환
        return None

    def update(self, dt):
        for ui in self.ui_list:
            if ui.visible:
                ui.update(dt)

    def draw(self, surface):
        # 레이어 낮은 것부터 높게 순서대로 draw → 위에 있을수록 늦게 그려진다
        for ui in sorted(self.ui_list, key=lambda x: x.layer):
            if ui.visible:
                ui.draw(surface)

    def load_uis(self, path, action_map=None):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for obj in data["objects"]:
            t = obj["type"]

            if t == "label":
                ui = Label(
                    obj.get("x", 0),
                    obj.get("y", 0),
                    obj.get("width", 0),
                    obj.get("text", ""),
                    obj.get("font_size", 24),
                    tuple(obj.get("color", (255,255,255))),
                    obj.get("layer", 0)
                )
                ui.load_ui(obj)

            elif t == "image":
                ui = UIImage(
                    obj.get("x", 0),
                    obj.get("y", 0),
                    obj["width"],
                    obj["height"],
                    obj["image_path"],
                    obj.get("layer", 0)
                )
                ui.load_ui(obj)

            elif t == "button":
                ui = ImageButton(
                    obj.get("x", 0),
                    obj.get("y", 0),
                    obj.get("width", 100),
                    obj.get("height", 50),
                    obj["image_path"],
                    obj.get("text", "Button"),
                    obj.get("font_size", 24),
                    tuple(obj.get("text_color", (255,255,255))),
                    tuple(obj.get("color_idle", (60,60,60))),
                    tuple(obj.get("color_hover", (90,90,90))),
                    None,  # action은 나중에 연결
                    obj.get("layer", 0)
                )
                ui.load_ui(obj)

                # action 연결
                if hasattr(ui, "action_name") and action_map:
                    if ui.action_name in action_map:
                        ui.action = action_map[ui.action_name]
                    else:
                        print(f"[WARN] action '{ui.action_name}' not found in action_map")

            else:
                print(f"[WARN] Unknown UI type: {t}")
                continue

            self.add(ui)
