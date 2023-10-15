def open_file(path: str):
    try:
        f = open(path, "r", encoding="utf-8")
        content = f.read()
        f.close()
        return content
    except:
        raise ValueError(f'Erro ao tentar abrir o arquivo: {path}.')


def save_file(path: str, content: str):
    try:
        f = open(path, "w", encoding="utf-8")
        f.write(content)
        f.close()
    except:
        raise ValueError(f'Erro ao tentar salvar o arquivo: {path}.')
