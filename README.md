# Urban remote sensing and land-cover classification

Academic work by **Frederick Abalo**, University of Pennsylvania.

[Portfolio](https://freddie999.github.io/portfolio/) · [Executed classification notebook](Homework4.ipynb)

## Featured project: EuroSAT RGB classification

Classifying satellite image patches into ten land-use and land-cover classes. I compare five convolutional-network configurations, testing deeper features, global average pooling, image augmentation, skip connections, and dropout.

![Held-out confusion matrix](homework4-output/confusion_matrix.png)

### Experiment and results

- Stratified 70/15/15 training, validation, and test split; saved image manifest.
- Training-only normalization and augmentation; shared seed and training budget.
- Model and checkpoint selected by validation performance before test evaluation.
- Selected model: plain CNN with flips and 90-degree rotations, epoch 27.
- **Test accuracy: 97.73%** — 3,958 of 4,050 images classified correctly.
- **Test macro F1: 0.9767.**
- Per-class evaluation, confusion matrix, learning curves, and example errors.

Skip connections and dropout did not improve the selection metric in this run. The notebook discusses those findings rather than assuming additional complexity helps.

### Inspect or reproduce

Open [Homework4.ipynb](Homework4.ipynb) to inspect saved outputs without retraining. [homework4-output/](homework4-output/) contains metrics, predictions, training histories, normalization statistics, figures, and the split manifest. Downloaded imagery and model checkpoints are excluded.

To train in an isolated environment from this repository root:

```sh
uv venv --python 3.14
uv pip install -r requirements-portfolio.txt
uv run jupyter lab Homework4.ipynb
```

The notebook downloads EuroSAT and chooses CUDA, Apple MPS, or CPU according to availability. The saved run used Apple MPS; [environment.json](homework4-output/environment.json) records the core runtime versions. Training all five configurations can take substantial time and replaces experiment files, so preserve existing results before rerunning. Accelerator differences can affect reproducibility.

### Limitations

One seed and one random image split do not establish performance in a new geographic region. Similar or nearby scenes may cross partitions. Architecture comparisons change several components between the starter and deeper baseline; the notebook distinguishes that comparison from the incremental experiments.

### Sources and credit

Developed for a University of Pennsylvania course, adapting Xiaojiang Li's [CNN teaching notebook](https://colab.research.google.com/drive/1S9GDD1vCLVTzVuQsnWO1jyI5rIjx8ktK). Dataset: [EuroSAT](https://github.com/phelber/EuroSAT). Instructor-provided labs elsewhere in this course fork remain credited teaching materials.
