from abc import ABC, abstractmethod
from datetime import datetime
import flet as ft

class CustomMap:

    def __init__(self):
        self._keys = []
        self._values = []

    def put(self, key, value):
        if key in self._keys:
            index = self._keys.index(key)
            self._values[index] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key):
        if key in self._keys:
            index = self._keys.index(key)
            return self._values[index]
        return None

    def __str__(self):
        pairs = [f"{self._keys[i]}: {self._values[i]}" for i in range(len(self._keys))]
        return f"CustomMap({', '.join(pairs)})"

class AbstractEntity(ABC):
    @abstractmethod
    def display_info(self):
        pass


class Task(AbstractEntity):
    def __init__(self, title: str, priority: int):
        self._title = title
        self._priority = priority
        self._completed = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) > 0:
            self._title = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if value > 0:
            self._priority = value

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value: bool):
        self._completed = value

    def display_info(self):
        status = "Выполнено" if self._completed else "В процессе"
        return f"Задача: {self._title} (Приоритет: {self._priority}) - {status}"

    def __str__(self):
        return f"[{'X' if self._completed else ' '}] {self._title} (Приоритет: {self._priority})"

    def __repr__(self):
        return f"Task(title='{self._title}', priority={self._priority}, completed={self._completed})"

    def __eq__(self, other):
        if isinstance(other, Task):
            return self._title == other._title and self._priority == other._priority
        return False

    def __lt__(self, other):
        return self._priority < other._priority

    @staticmethod
    def create_default_tasks():
        tasks_list = []
        for i in range(1, 11):
            tasks_list.append(Task(f"Задача №{i}", priority=i))
        return tasks_list

class AppSession:
    def __init__(self, username="UserName"):
        self.username = username
        self.time_in = datetime.now()
        self.time_out = None

    def close_session(self):
        self.time_out = datetime.now()
        time_format = "%d.%m.%Y %H:%M:%S"

        report = (
            "+\n"
            "+\n"
            f"| login | time_in | time_out |\n"
            f"|{self.username} | {self.time_in.strftime(time_format)} | {self.time_out.strftime(time_format)}\n"
            "+\n"
            "+"
        )
        with open("session_report.txt", "w", encoding="utf-8") as f:
            f.write(report)

def main(page: ft.Page):
    page.title = "Менеджер задач (ООП проект)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 500
    page.window.height = 650

    session = AppSession(username="Denis_Savitskiy")

    tasks_collection = Task.create_default_tasks()

    stats_map = CustomMap()
    stats_map.put("total", len(tasks_collection))
    stats_map.put("active", len(tasks_collection))

    title_label = ft.Text("Менеджер задач", size=22, weight=ft.FontWeight.BOLD)

    task_input = ft.TextField(label="Новая задача", width=320)

    task_list_view = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=True)

    def update_list_display():
        task_list_view.controls.clear()
        for t in tasks_collection:
            task_list_view.controls.append(ft.Text(str(t)))
        page.update()

    def add_task_clicked(e):
        if task_input.value.strip():
            new_task = Task(title=task_input.value.strip(), priority=len(tasks_collection) + 1)
            tasks_collection.append(new_task)
            task_input.value = ""
            update_list_display()

    add_button = ft.Container(
        content=ft.Text("Добавить", color=ft.colors.WHITE),
        bgcolor=ft.colors.BLUE,
        padding=10,
        border_radius=6,
        on_click=add_task_clicked,
        alignment=ft.alignment.Alignment(0, 0)
    )
    info_label = ft.Text(f"Всего задач в системе: {len(tasks_collection)}")

    update_list_display()

    def window_event(e):
        if e.data == "close":
            session.close_session()
            page.window.destroy()

    page.window.prevent_close = True
    page.window.on_event = window_event

    page.add(
        ft.Column(
            [
                title_label,
                ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(content=task_list_view, height=350, border_radius=8),
                info_label
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )


if __name__ == "__main__":
    ft.app(target=main)