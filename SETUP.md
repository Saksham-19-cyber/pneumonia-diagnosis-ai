# Setup Guide

This guide will help you set up the Pneumonia Diagnosis AI project on your local machine.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- 8GB+ RAM recommended
- GPU (optional but recommended for training)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pneumonia-diagnosis-ai.git
cd pneumonia-diagnosis-ai
```

### 2. Create a Virtual Environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download the Dataset

You'll need to download chest X-ray images. We recommend:

**Option 1: Kaggle Dataset (Recommended)**
1. Go to [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
2. Download the dataset
3. Extract to `data/` directory

**Option 2: NIH Chest X-rays**
1. Visit [NIH Clinical Center](https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-one-largest-publicly-available-chest-x-ray-datasets-scientific-community)
2. Follow their download instructions
3. Organize into the required structure

### 5. Organize Data Directory

Your data should be structured as:

```
data/
├── train/
│   ├── NORMAL/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── PNEUMONIA/
│       ├── image1.jpg
│       ├── image2.jpg
│       └── ...
├── test/
│   ├── NORMAL/
│   │   └── ...
│   └── PNEUMONIA/
│       └── ...
└── val/  (optional - will be created from train split)
    ├── NORMAL/
    │   └── ...
    └── PNEUMONIA/
        └── ...
```

### 6. Verify Installation

Test your setup:

```bash
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__); print('GPU available:', tf.config.list_physical_devices('GPU'))"
```

Expected output:
```
TensorFlow version: 2.x.x
GPU available: [list of GPUs] or []
```

## Directory Structure Setup

Create the necessary directories:

```bash
mkdir -p data/train/NORMAL data/train/PNEUMONIA
mkdir -p data/test/NORMAL data/test/PNEUMONIA
mkdir -p data/val/NORMAL data/val/PNEUMONIA
mkdir -p models outputs logs
```

## Running the Notebook

### Start Jupyter Notebook

```bash
jupyter notebook
```

Navigate to `notebooks/explainable-ai-for-pneumonia-diagnosis-using-chest.ipynb` and run the cells.

### Or Use Jupyter Lab

```bash
jupyter lab
```

## Quick Start with Pre-trained Model

If you want to skip training and use a pre-trained model:

1. Download the pre-trained model (link to be added)
2. Place it in `models/final_model.keras`
3. Run inference:

```bash
python src/predict.py path/to/xray.jpg --show-gradcam
```

## GPU Setup (Optional)

### For NVIDIA GPUs:

1. Install CUDA Toolkit (11.2 or compatible)
2. Install cuDNN (8.1 or compatible)
3. Install TensorFlow with GPU support:

```bash
pip install tensorflow-gpu
```

Verify GPU:
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

### For Apple Silicon (M1/M2):

```bash
pip install tensorflow-macos
pip install tensorflow-metal
```

## Troubleshooting

### Issue: Import errors

**Solution:**
```bash
pip install --upgrade tensorflow numpy pandas matplotlib
```

### Issue: Out of memory during training

**Solutions:**
- Reduce batch size in the notebook
- Use a machine with more RAM
- Enable mixed precision training
- Use gradient checkpointing

### Issue: Slow training without GPU

**Solutions:**
- Use Google Colab (free GPU)
- Use Kaggle Notebooks (free GPU)
- Reduce image size
- Use fewer training samples initially

### Issue: Data loading errors

**Solutions:**
- Verify data directory structure
- Check file permissions
- Ensure images are in correct format (JPG/JPEG/PNG)

## Development Setup

For contributors:

```bash
# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/
```

## Docker Setup (Advanced)

Coming soon: Dockerfile for containerized deployment

## Cloud Setup

### Google Colab

1. Upload the notebook to Google Drive
2. Open with Google Colab
3. Enable GPU: Runtime > Change runtime type > GPU
4. Install requirements in the first cell:
   ```python
   !pip install -q tensorflow pandas matplotlib seaborn scikit-learn
   ```

### Kaggle Notebooks

1. Create a new notebook on Kaggle
2. Add the dataset
3. Enable GPU accelerator
4. Upload and run the notebook

## Next Steps

After setup:
1. Read the [README.md](README.md) for project overview
2. Run the training notebook
3. Evaluate the model
4. Try inference on new images
5. Explore Grad-CAM visualizations

## Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/pneumonia-diagnosis-ai/issues)
3. Create a new issue with details about your problem

## Resources

- [TensorFlow Installation Guide](https://www.tensorflow.org/install)
- [Keras Documentation](https://keras.io/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
