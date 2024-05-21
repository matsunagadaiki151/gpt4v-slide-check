from dataclasses import dataclass
import yaml

@dataclass
class YamlData:
    model: str

def from_dict(data_class: YamlData, data: dict):
    """
    再帰的に辞書からデータクラスのインスタンスを作成するヘルパー関数。
    """
    if not hasattr(data_class, '__dataclass_fields__'):
        return data

    fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
    return data_class(**{f: from_dict(fieldtypes[f], data[f]) for f in data})

def load_model_name():
    # YAMLファイルを読み込む
    with open('config.yml', 'r') as file:
        data = yaml.safe_load(file)
    yml_data = from_dict(YamlData, data)

    return yml_data.model


if __name__ == "__main__":
    print(load_model_name())
