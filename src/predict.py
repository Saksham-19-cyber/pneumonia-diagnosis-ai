"""
Inference script for pneumonia diagnosis from chest X-rays.
"""

import os
import json
import argparse
import numpy as np
from tensorflow import keras
from PIL import Image
import matplotlib.pyplot as plt
from utils.gradcam import generate_gradcam_visualization, find_last_conv_layer


def load_model_and_metadata(model_path, metadata_path, class_indices_path):
    """
    Load the trained model and associated metadata.
    
    Args:
        model_path: Path to the saved model (.keras file)
        metadata_path: Path to model metadata JSON
        class_indices_path: Path to class indices JSON
    
    Returns:
        model: Loaded Keras model
        metadata: Model metadata dictionary
        class_names: Dictionary mapping indices to class names
    """
    print(f"Loading model from {model_path}...")
    model = keras.models.load_model(model_path)
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    with open(class_indices_path, 'r') as f:
        class_indices = json.load(f)
    
    # Reverse mapping: index -> class name
    class_names = {v: k for k, v in class_indices.items()}
    
    return model, metadata, class_names


def preprocess_image(img_path, target_size=(224, 224)):
    """
    Load and preprocess an image for model prediction.
    
    Args:
        img_path: Path to the image file
        target_size: Target size for resizing
    
    Returns:
        img_array: Preprocessed image array for model input
        original_img: Original image for visualization
    """
    # Load image
    img = Image.open(img_path)
    original_img = np.array(img.resize(target_size))
    
    # Preprocess for model
    img = img.resize(target_size)
    img_array = np.array(img)
    
    # Handle grayscale images
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    
    # Normalize
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array, original_img


def predict_single_image(model, img_array, class_names, threshold=0.5):
    """
    Make a prediction on a single image.
    
    Args:
        model: Trained Keras model
        img_array: Preprocessed image array
        class_names: Dictionary mapping indices to class names
        threshold: Decision threshold (default 0.5)
    
    Returns:
        prediction: Dictionary with prediction results
    """
    # Get prediction
    pred_proba = model.predict(img_array, verbose=0)[0][0]
    
    # Determine class
    pred_class_idx = 1 if pred_proba > threshold else 0
    pred_class_name = class_names[pred_class_idx]
    confidence = pred_proba if pred_class_idx == 1 else 1 - pred_proba
    
    prediction = {
        'class': pred_class_name,
        'class_index': pred_class_idx,
        'confidence': float(confidence),
        'probability': {
            'NORMAL': float(1 - pred_proba),
            'PNEUMONIA': float(pred_proba)
        }
    }
    
    return prediction


def visualize_prediction(original_img, overlayed_img, prediction, save_path=None):
    """
    Create a visualization showing the original image, Grad-CAM, and prediction.
    
    Args:
        original_img: Original image
        overlayed_img: Image with Grad-CAM overlay
        prediction: Prediction dictionary
        save_path: Optional path to save the visualization
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Original image
    axes[0].imshow(original_img, cmap='gray' if len(original_img.shape) == 2 else None)
    axes[0].set_title('Original X-Ray', fontsize=14)
    axes[0].axis('off')
    
    # Grad-CAM overlay
    axes[1].imshow(overlayed_img)
    axes[1].set_title('Grad-CAM Heatmap', fontsize=14)
    axes[1].axis('off')
    
    # Add prediction text
    pred_text = f"Prediction: {prediction['class']}\n"
    pred_text += f"Confidence: {prediction['confidence']:.2%}\n"
    pred_text += f"Normal: {prediction['probability']['NORMAL']:.2%}\n"
    pred_text += f"Pneumonia: {prediction['probability']['PNEUMONIA']:.2%}"
    
    fig.suptitle(pred_text, fontsize=12, y=0.05, verticalalignment='bottom')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=150)
        print(f"Visualization saved to {save_path}")
    
    plt.show()


def main(args):
    """
    Main function to run inference on an image.
    """
    # Load model and metadata
    model, metadata, class_names = load_model_and_metadata(
        args.model_path,
        args.metadata_path,
        args.class_indices_path
    )
    
    print(f"\nModel: {metadata['model_name']} v{metadata['version']}")
    print(f"Architecture: {metadata['architecture']}")
    print(f"Classes: {list(class_names.values())}\n")
    
    # Preprocess image
    print(f"Loading image: {args.image_path}")
    img_array, original_img = preprocess_image(args.image_path)
    
    # Make prediction
    print("Making prediction...")
    prediction = predict_single_image(model, img_array, class_names, args.threshold)
    
    # Print results
    print("\n" + "="*50)
    print("PREDICTION RESULTS")
    print("="*50)
    print(f"Class: {prediction['class']}")
    print(f"Confidence: {prediction['confidence']:.2%}")
    print(f"\nProbabilities:")
    print(f"  Normal:    {prediction['probability']['NORMAL']:.2%}")
    print(f"  Pneumonia: {prediction['probability']['PNEUMONIA']:.2%}")
    print("="*50 + "\n")
    
    # Generate Grad-CAM if requested
    if args.show_gradcam:
        print("Generating Grad-CAM visualization...")
        last_conv_layer = args.conv_layer or find_last_conv_layer(model)
        print(f"Using layer: {last_conv_layer}")
        
        overlayed_img, _ = generate_gradcam_visualization(
            model, img_array, original_img, last_conv_layer
        )
        
        # Visualize
        save_path = args.output_path if args.output_path else None
        visualize_prediction(original_img, overlayed_img, prediction, save_path)
    
    # Save prediction to JSON if requested
    if args.save_json:
        json_path = args.image_path.replace(os.path.splitext(args.image_path)[1], '_prediction.json')
        with open(json_path, 'w') as f:
            json.dump(prediction, f, indent=2)
        print(f"Prediction saved to {json_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Predict pneumonia from chest X-ray images'
    )
    
    parser.add_argument(
        'image_path',
        type=str,
        help='Path to the chest X-ray image'
    )
    
    parser.add_argument(
        '--model-path',
        type=str,
        default='models/final_model.keras',
        help='Path to the trained model (default: models/final_model.keras)'
    )
    
    parser.add_argument(
        '--metadata-path',
        type=str,
        default='deployment/model_metadata.json',
        help='Path to model metadata JSON'
    )
    
    parser.add_argument(
        '--class-indices-path',
        type=str,
        default='deployment/class_indices.json',
        help='Path to class indices JSON'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.5,
        help='Decision threshold (default: 0.5)'
    )
    
    parser.add_argument(
        '--show-gradcam',
        action='store_true',
        help='Generate and show Grad-CAM visualization'
    )
    
    parser.add_argument(
        '--conv-layer',
        type=str,
        default=None,
        help='Name of convolutional layer for Grad-CAM (default: auto-detect)'
    )
    
    parser.add_argument(
        '--output-path',
        type=str,
        default=None,
        help='Path to save the visualization'
    )
    
    parser.add_argument(
        '--save-json',
        action='store_true',
        help='Save prediction results to JSON file'
    )
    
    args = parser.parse_args()
    main(args)
