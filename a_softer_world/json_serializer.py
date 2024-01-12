from json import JSONEncoder as _JSONEncoder
import dataclasses


class JSONEncoder(_JSONEncoder):
    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        return super().default(obj)

