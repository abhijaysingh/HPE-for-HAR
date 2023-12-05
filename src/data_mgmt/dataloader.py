import torch
from torch.utils.data.dataloader import default_collate
from typing import Any, List, Mapping, Sequence, Tuple

class Collater:
    def __init__(self, dataset):
        self.dataset = dataset

    def __call__(self, batch) -> Any:
        elem = batch[0]

        if isinstance(elem, torch.Tensor):
            return default_collate(batch)
        elif isinstance(elem, float):
            return torch.tensor(batch, dtype=torch.float)
        elif isinstance(elem, int):
            return torch.tensor(batch)
        elif isinstance(elem, str):
            return batch
        elif isinstance(elem, Mapping):
            return {key: self([data[key] for data in batch]) for key in elem}
        elif isinstance(elem, Sequence) and not isinstance(elem, str):
            return [self(s) for s in zip(*batch)]

        raise TypeError(f"DataLoader found invalid type: '{type(elem)}'")

    def collate_fn(self, batch: List[Any]) -> Any:
        view1 = [item["view1"] for item in batch]
        view2 = [item["view2"] for item in batch]
        view3 = [item["view3"] for item in batch]
        labels = [item["label"] for item in batch]

        batched_graphs = []
        for i in range(len(view1)):
            batched_graphs.append([view1[i], view2[i], view3[i]])

        labels = torch.tensor(labels, dtype=torch.long)

        return batched_graphs, labels


class DataLoader(torch.utils.data.DataLoader):
    def __init__(self, dataset, batch_size: int = 1, shuffle: bool = False, **kwargs):
        self.collator = Collater(dataset)

        super().__init__(
            dataset,
            batch_size,
            shuffle,
            collate_fn=self.collator.collate_fn,
            **kwargs,
        )
