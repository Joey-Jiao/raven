from pathlib import Path

from tokenizers import Tokenizer


class QwenTokenizer:
    def __init__(self, path: str | Path):
        self._tokenizer = self._load_tokenizer_from_path(path)
        self.eos_id = 151643

    def encode(self, text: str, add_eos: bool = True) -> list[int]:
        token_ids = self._tokenizer.encode(text).ids
        if add_eos:
            token_ids.append(self.eos_id)
        return token_ids

    def decode(self, token_ids: list[int]) -> str:
        return self._tokenizer.decode(token_ids)

    @property
    def get_vocab_size(self) -> int:
        return self._tokenizer.get_vocab_size()

    def get_vocab(self) -> dict[str, int]:
        return self._tokenizer.get_vocab()

    def token2id(self, token: str) -> int:
        return self._tokenizer.token_to_id(token)

    def id2token(self, id: int) -> str:
        return self._tokenizer.id_to_token(id)

    @staticmethod
    def _load_tokenizer_from_path(tokenizer_path: str) -> Tokenizer:
        path = Path(tokenizer_path)
        tokenizer_file = path / "tokenizer.json"

        if not tokenizer_file.exists():
            raise FileNotFoundError(
                f"tokenizer.json not found in '{tokenizer_path}"
            )

        return Tokenizer.from_file(str(tokenizer_file))
