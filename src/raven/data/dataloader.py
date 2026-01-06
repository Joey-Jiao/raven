from torch.utils.data import DataLoader

from .datasets.pretrain import PretrainDataset
from .tokenizer import QwenTokenizer


def build_dataloader(
    dataset_path: str,
    tokenizer: QwenTokenizer,
    seq_len: int,
    batch_size: int,
    rank: int = 0,
    world_size: int = 1,
) -> DataLoader:
    dataset = PretrainDataset(
        dataset_path=dataset_path,
        tokenizer=tokenizer,
        seq_len=seq_len,
    )

    dataset._dataset = dataset.dataset.shard(num_shards=world_size, index=rank)

    return DataLoader(dataset, batch_size=batch_size)
