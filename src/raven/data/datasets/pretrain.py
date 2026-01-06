from typing import Iterator

import torch
from datasets import load_dataset
from torch.utils.data import IterableDataset

from ..tokenizer import QwenTokenizer


class PretrainDataset(IterableDataset):
    def __init__(
        self,
        dataset_path: str,
        tokenizer: QwenTokenizer,
        seq_len: int,
        split: str = "train",
    ):
        self._tokenizer = tokenizer
        self._seq_len = seq_len
        self._dataset = load_dataset(dataset_path, split=split, streaming=True)

    def __iter__(self) -> Iterator[tuple[torch.Tensor, torch.Tensor]]:
        buffer: list[int] = []

        for sample in self._dataset:
            text = sample["text"]
            tokens = self._tokenizer.encode(text, add_eos=True)
            buffer.extend(tokens)

            while len(buffer) >= self._seq_len + 1:
                chunk = buffer[: self._seq_len + 1]
                buffer = buffer[self._seq_len + 1 :]

                input_ids = torch.tensor(chunk[:-1], dtype=torch.long)
                labels = torch.tensor(chunk[1:], dtype=torch.long)
                yield input_ids, labels

