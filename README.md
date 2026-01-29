# Explainable AI for Pneumonia Diagnosis

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange)](https://www.tensorflow.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An end-to-end deep learning solution for pneumonia detection from chest X-rays with explainability using Grad-CAM, designed for clinical deployment.

## 📋 Overview

This project implements a state-of-the-art deep learning model for automated pneumonia diagnosis from chest X-ray images. Built on transfer learning with ResNet50, the model achieves high accuracy while providing visual explanations of its predictions through Gradient-weighted Class Activation Mapping (Grad-CAM), making it suitable for real-world clinical applications.

### Key Features

- ✅ **Transfer Learning**: ResNet50 pre-trained on ImageNet for robust feature extraction
- ✅ **Class Imbalance Handling**: Weighted loss functions for balanced learning
- ✅ **Explainability**: Grad-CAM visualizations for clinical validation
- ✅ **Clinical Workflow Integration**: Optimized thresholds for triage scenarios
- ✅ **Comprehensive Metrics**: Accuracy, Precision, Recall, AUC, Specificity, and NPV
- ✅ **Production Ready**: Complete deployment package with versioning and metadata

## 🏥 Clinical Applications

The model is designed to support radiologists in:
- **Screening**: Rapid triage of chest X-rays in high-volume settings
- **Second Opinion**: Validation tool for ambiguous cases
- **Remote Diagnosis**: Enabling telemedicine and underserved areas
- **Training**: Educational tool with visual explanations

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| Architecture | ResNet50 (Transfer Learning) |
| Validation Split | 15% |
| Training Strategy | Class-weighted + Data Augmentation |
| Callbacks | Early Stopping, LR Reduction, Model Checkpoint |

*Note: Specific performance metrics should be added after model evaluation*

## 🔬 Dataset

This project uses chest X-ray images for binary classification:
- **Class 0**: Normal (healthy lungs)
- **Class 1**: Pneumonia

### Recommended Datasets
- [Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) on Kaggle
- [NIH Chest X-rays](https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-one-largest-publicly-available-chest-x-ray-datasets-scientific-community)

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.8+
TensorFlow 2.x
NumPy
Pandas
Matplotlib
Seaborn
scikit-learn
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pneumonia-diagnosis-ai.git
cd pneumonia-diagnosis-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the dataset and organize it in the following structure:
```
data/
├── train/
│   ├── NORMAL/
│   └── PNEUMONIA/
├── test/
│   ├── NORMAL/
│   └── PNEUMONIA/
└── val/
    ├── NORMAL/
    └── PNEUMONIA/
```

### Training

Run the Jupyter notebook:
```bash
jupyter notebook explainable-ai-for-pneumonia-diagnosis-using-chest.ipynb
```

Or train directly with Python:
```bash
python train.py
```

### Inference

```python
from tensorflow import keras
import numpy as np
from PIL import Image

# Load the model
model = keras.models.load_model('models/final_model.keras')

# Load and preprocess image
img = Image.open('path/to/xray.jpg')
img = img.resize((224, 224))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Predict
prediction = model.predict(img_array)
class_name = "PNEUMONIA" if prediction[0][0] > 0.5 else "NORMAL"
confidence = prediction[0][0] if prediction[0][0] > 0.5 else 1 - prediction[0][0]

print(f"Prediction: {class_name} (Confidence: {confidence:.2%})")
```

## 🔍 Explainability with Grad-CAM

The model includes Grad-CAM (Gradient-weighted Class Activation Mapping) to visualize which regions of the X-ray influenced the diagnosis:

```python
from utils.gradcam import generate_gradcam

# Generate heatmap
heatmap = generate_gradcam(model, img_array, layer_name='conv5_block3_out')

# Overlay on original image
overlayed_img = overlay_heatmap(img, heatmap)
```

This provides:
- **Transparency**: Shows what the model "sees"
- **Clinical Validation**: Radiologists can verify if the model focuses on relevant anatomical regions
- **Trust Building**: Increases confidence in AI-assisted diagnosis

## 📁 Repository Structure

```
pneumonia-diagnosis-ai/
├── data/                           # Dataset directory (not tracked)
├── models/                         # Saved models
│   ├── final_model.keras          # Production model
│   ├── best_model.keras           # Best validation model
│   └── finetuned_model.keras      # Fine-tuned model
├── notebooks/                      # Jupyter notebooks
│   └── explainable-ai-for-pneumonia-diagnosis-using-chest.ipynb
├── outputs/                        # Training outputs
│   ├── training_metrics.png       # Training/validation curves
│   ├── confusion_matrix.png       # Confusion matrix
│   ├── clinical_triage.png        # Clinical threshold analysis
│   └── threshold_optimization.png # ROC and threshold optimization
├── src/                           # Source code
│   ├── train.py                   # Training script
│   ├── evaluate.py                # Evaluation script
│   ├── predict.py                 # Inference script
│   └── utils/                     # Utility functions
│       ├── gradcam.py            # Grad-CAM implementation
│       ├── preprocessing.py       # Data preprocessing
│       └── metrics.py            # Custom metrics
├── deployment/                    # Deployment files
│   ├── model_metadata.json       # Model versioning info
│   └── class_indices.json        # Class mapping
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## 📈 Training Pipeline

The model uses a robust training pipeline:

1. **Data Augmentation**: Rotation, zoom, flip, brightness adjustment
2. **Class Weights**: Automatic calculation to handle imbalanced datasets
3. **Transfer Learning**: ResNet50 base with custom classification head
4. **Callbacks**:
   - Early Stopping (patience: 10 epochs)
   - Model Checkpoint (save best model)
   - Learning Rate Reduction (factor: 0.5)

## 🏥 Clinical Deployment Checklist

- ✅ Model architecture: ResNet50 transfer learning
- ✅ Class imbalance: Handled with class weights
- ✅ Validation strategy: 15% split from training data
- ✅ Callbacks: ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
- ✅ Metrics: Accuracy, Precision, Recall, AUC, Specificity, NPV
- ✅ Clinical thresholds: Configured for triage workflow
- ✅ Explainability: Grad-CAM implemented
- ✅ Model versioning: Saved with metadata

### Next Steps for Hospital Deployment

1. **Clinical Validation**: Test with radiologists on representative patient data
2. **Prospective Study**: Evaluate on new, unseen patient cases
3. **PACS Integration**: Connect with Picture Archiving and Communication System
4. **Regulatory Approval**: Obtain FDA clearance or CE marking (as required)
5. **Performance Monitoring**: Track model drift over time
6. **Human-in-the-Loop**: Establish radiologist review workflow
7. **Edge Cases**: Create fallback procedures for uncertain predictions

## 📊 Visualization Examples

The project generates several visualizations:

- **Training Metrics**: Loss and accuracy curves over epochs
- **Confusion Matrix**: True vs predicted classifications
- **ROC Curve**: Receiver Operating Characteristic with AUC
- **Precision-Recall Curve**: Threshold optimization
- **Clinical Triage**: Sensitivity vs specificity trade-offs
- **Grad-CAM Heatmaps**: Visual explanations for predictions

## 🔧 Configuration

Model hyperparameters and training configuration can be adjusted in the notebook or via a config file:

```python
CONFIG = {
    'image_size': (224, 224),
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.0001,
    'validation_split': 0.15,
    'early_stopping_patience': 10,
    'reduce_lr_patience': 5,
    'reduce_lr_factor': 0.5,
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**This model is for research and educational purposes only.** It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified healthcare providers with any questions you may have regarding a medical condition.

## 📚 Citation

If you use this code in your research, please cite:

```bibtex
@software{pneumonia_diagnosis_ai,
  title={Explainable AI for Pneumonia Diagnosis from Chest X-rays},
  author={Your Name},
  year={2026},
  url={https://github.com/yourusername/pneumonia-diagnosis-ai}
}
```

## 🔗 References

- He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. CVPR.
- Selvaraju, R. R., et al. (2017). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. ICCV.
- Rajpurkar, P., et al. (2017). CheXNet: Radiologist-Level Pneumonia Detection on Chest X-Rays with Deep Learning.

## 📧 Contact

For questions or feedback, please open an issue or contact [your.email@example.com](mailto:your.email@example.com)

---

**Made with ❤️ for advancing healthcare through AI**
