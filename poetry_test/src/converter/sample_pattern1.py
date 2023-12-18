from dataclasses import dataclass


@dataclass
class DetailRow:
    key: int
    before: dict
    after: dict

    def validate(self):
        ...

    def transform(self):
        ...

    def diff(self):
        ...

    def load(self):
        ...

# インスタンス生成
detail = DetailRow(1, {'a': 1}, {'b': 2})
print(detail)
