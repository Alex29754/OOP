import json
from abc import ABC, abstractmethod
from typing import Dict, List
from pathlib import Path

# === Настройки ===

OUTPUT_FILE = "output.txt"

def write_to_output(text: str, end: str = "\n"):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(text + end)


# ==== Command Pattern ====

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class PrintCommand(Command):
    def __init__(self, char: str, output: List[str]):
        self.char = char
        self.output = output

    def execute(self):
        self.output.append(self.char)
        print(self.char, end="")
        write_to_output(self.char, end="")

    def undo(self):
        if self.output:
            removed = self.output.pop()
            print("\nundo")
            write_to_output("undo")
            updated = ''.join(self.output)
            print(updated)
            write_to_output(updated)


class VolumeUpCommand(Command):
    def __init__(self):
        self.message = "volume increased +20%"

    def execute(self):
        print(self.message)
        write_to_output(self.message)

    def undo(self):
        msg = "volume decreased -20%"
        print("undo ->", msg)
        write_to_output("undo -> " + msg)


class VolumeDownCommand(Command):
    def __init__(self):
        self.message = "volume decreased -20%"

    def execute(self):
        print(self.message)
        write_to_output(self.message)

    def undo(self):
        msg = "volume increased +20%"
        print("undo ->", msg)
        write_to_output("undo -> " + msg)


class MediaPlayerCommand(Command):
    def __init__(self):
        self.running = False

    def execute(self):
        self.running = True
        msg = "media player launched"
        print(msg)
        write_to_output(msg)

    def undo(self):
        if self.running:
            msg = "media player closed"
            print("undo ->", msg)
            write_to_output("undo -> " + msg)


# ==== Memento ====

class KeyboardStateSaver:
    def __init__(self, filepath="keyboard_state.json"):
        self.filepath = Path(filepath)

    def save(self, associations: Dict[str, str]):
        with self.filepath.open("w", encoding="utf-8") as f:
            json.dump(associations, f)

    def load(self) -> Dict[str, str]:
        if self.filepath.exists():
            with self.filepath.open("r", encoding="utf-8") as f:
                return json.load(f)
        return {}


# ==== Keyboard ====

class Keyboard:
    def __init__(self):
        self.associations: Dict[str, str] = {}
        self.commands: Dict[str, Command] = {}
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
        self.text_output: List[str] = []
        self.state_saver = KeyboardStateSaver()
        self.load_state()

    def associate_key(self, key: str, command: Command):
        self.commands[key] = command
        self.associations[key] = command.__class__.__name__
        self.save_state()

    def press_key(self, key: str):
        command = self.commands.get(key)
        if command:
            command.execute()
            self.history.append(command)
            self.redo_stack.clear()
        else:
            print(f"No command associated with '{key}'")

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            self.redo_stack.append(command)
        else:
            print("Nothing to undo")

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.execute()
            self.history.append(command)
        else:
            print("Nothing to redo")

    def save_state(self):
        save_dict = {k: v.__class__.__name__ for k, v in self.commands.items()}
        self.state_saver.save(save_dict)

    def load_state(self):
        mapping = self.state_saver.load()
        for key, command_name in mapping.items():
            command = self._create_command_by_name(command_name)
            if command:
                self.commands[key] = command

    def _create_command_by_name(self, name: str) -> Command:
        if name == "VolumeUpCommand":
            return VolumeUpCommand()
        elif name == "VolumeDownCommand":
            return VolumeDownCommand()
        elif name == "MediaPlayerCommand":
            return MediaPlayerCommand()
        elif name == "PrintCommand":
            return PrintCommand("*", self.text_output)  # заглушка
        return None


# ==== Пример использования ====

if __name__ == "__main__":
    kb = Keyboard()

    # Привязки
    kb.associate_key("a", PrintCommand("a", kb.text_output))
    kb.associate_key("b", PrintCommand("b", kb.text_output))
    kb.associate_key("c", PrintCommand("c", kb.text_output))
    kb.associate_key("ctrl++", VolumeUpCommand())
    kb.associate_key("ctrl+-", VolumeDownCommand())
    kb.associate_key("ctrl+p", MediaPlayerCommand())

    # Нажатия
    kb.press_key("a")
    kb.press_key("b")
    kb.press_key("c")
    kb.undo()
    kb.undo()
    kb.redo()
    kb.press_key("ctrl++")
    kb.press_key("ctrl+-")
    kb.press_key("ctrl+p")
    kb.press_key("d")  # Команда не задана
    kb.undo()
    kb.undo()
