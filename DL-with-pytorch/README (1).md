# 🔢 MNIST Digit Classifier (PyTorch)

> A beginner-friendly neural network that classifies handwritten digits (0–9) using PyTorch.  
> Built as a personal variation of the [official PyTorch Quickstart Tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html).

---

## 📌 What It Does

Trains a simple fully-connected neural network on the **MNIST dataset** — 70,000 grayscale images of handwritten digits — and learns to predict which number (0–9) is in each image.

**Example:**  
Input: image of a handwritten `7`  
Output: `Predicted: 7, Actual: 7` ✅

---

## 🆚 Difference from the Original Tutorial

| | Original Tutorial | This Project |
|---|---|---|
| **Dataset** | FashionMNIST (clothing) | MNIST (digits) |
| **Classes** | T-shirt, Shoe, Bag... | 0, 1, 2 ... 9 |
| **Hidden layers** | 512 → 512 | 256 → 128 |
| **Goal** | Classify clothing type | Classify digit |

Same PyTorch skeleton, different data and a slightly smaller model.

---

## 🗂️ Project Structure

```
mnist-classifier/
│
├── mnist_classifier.py   # Main training script
├── mnist_model.pth       # Saved model weights (generated after training)
├── data/                 # Auto-downloaded MNIST dataset
└── README.md
```

---

## 🧠 Model Architecture

```
Input (28×28 image)
    ↓  Flatten → 784-dim vector
Linear(784 → 256)
    ↓  ReLU
Linear(256 → 128)
    ↓  ReLU
Linear(128 → 10)
    ↓
Output (probabilities for digits 0–9)
```

---

## ⚙️ Requirements

```bash
pip install torch torchvision
```

- Python 3.8+
- PyTorch 2.x
- torchvision

---

## 🚀 How to Run

```bash
python mnist_classifier.py
```

On first run, MNIST dataset will be **automatically downloaded** to `./data/`.

---

## 📊 Training Details

| Hyperparameter | Value |
|---|---|
| Optimizer | SGD |
| Learning rate | 0.001 |
| Loss function | CrossEntropyLoss |
| Batch size | 64 |
| Epochs | 5 |

**Expected results after 5 epochs:**
```
Epoch 5 ─────────────
  Test Accuracy: ~97.0%,  Avg Loss: ~0.10
Done! 🎉
```

---

## 💾 Save & Load Model

The model is saved after training:
```python
torch.save(model.state_dict(), "mnist_model.pth")
```

To load and reuse:
```python
model = MyDigitNet().to(device)
model.load_state_dict(torch.load("mnist_model.pth", weights_only=True))
model.eval()
```

---

## 📚 Key Concepts

| Concept | What it does |
|---|---|
| `Dataset` | Stores images + labels |
| `DataLoader` | Feeds data in batches during training |
| `nn.Flatten` | Converts 2D image (28×28) → 1D vector (784) |
| `nn.Linear` | Fully connected layer — core computation |
| `nn.ReLU` | Activation function: turns negatives to 0 |
| `loss.backward()` | Computes gradients (backpropagation) |
| `optimizer.step()` | Updates weights using computed gradients |
| `model.eval()` | Switches off training-only features during testing |

---

## 🔗 References

- [PyTorch Quickstart Tutorial](https://docs.pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html)
- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

---

*Made as a learning exercise, adapting the official PyTorch tutorial with a different dataset and model size.*
