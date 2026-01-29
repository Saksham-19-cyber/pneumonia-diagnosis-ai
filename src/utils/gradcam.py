"""
Grad-CAM (Gradient-weighted Class Activation Mapping) implementation
for visualizing which parts of the image influenced the model's prediction.

Reference: Selvaraju et al., 2017 - "Grad-CAM: Visual Explanations from Deep Networks"
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2


def get_gradcam_heatmap(model, img_array, last_conv_layer_name, pred_index=None):
    """
    Generate Grad-CAM heatmap for a given image and model.
    
    Args:
        model: Trained Keras model
        img_array: Preprocessed image array (batch size of 1)
        last_conv_layer_name: Name of the last convolutional layer
        pred_index: Index of the class to visualize (None for predicted class)
    
    Returns:
        heatmap: Grad-CAM heatmap as numpy array
    """
    # Create a model that maps the input image to the activations
    # of the last conv layer and the output predictions
    grad_model = keras.models.Model(
        inputs=[model.inputs],
        outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )
    
    # Compute the gradient of the predicted class with respect to
    # the feature map
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]
    
    # Gradient of the output neuron with respect to the feature map
    grads = tape.gradient(class_channel, last_conv_layer_output)
    
    # Global average pooling of gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    # Multiply each channel by its importance
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    
    # Normalize the heatmap
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def overlay_heatmap_on_image(img, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
    """
    Overlay Grad-CAM heatmap on the original image.
    
    Args:
        img: Original image as numpy array (RGB)
        heatmap: Grad-CAM heatmap
        alpha: Transparency of the heatmap overlay (0-1)
        colormap: OpenCV colormap to use
    
    Returns:
        superimposed_img: Image with heatmap overlay
    """
    # Resize heatmap to match image size
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # Convert heatmap to RGB
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, colormap)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    # Superimpose heatmap on image
    superimposed_img = heatmap * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)
    
    return superimposed_img


def generate_gradcam_visualization(model, img_array, original_img, 
                                   last_conv_layer_name='conv5_block3_out',
                                   pred_index=None):
    """
    Complete pipeline to generate and overlay Grad-CAM visualization.
    
    Args:
        model: Trained Keras model
        img_array: Preprocessed image array for model input
        original_img: Original image for visualization (0-255 range)
        last_conv_layer_name: Name of the last conv layer
        pred_index: Class index to visualize
    
    Returns:
        overlayed_img: Original image with Grad-CAM heatmap overlay
        heatmap: Raw heatmap array
    """
    # Generate heatmap
    heatmap = get_gradcam_heatmap(model, img_array, last_conv_layer_name, pred_index)
    
    # Overlay on original image
    overlayed_img = overlay_heatmap_on_image(original_img, heatmap)
    
    return overlayed_img, heatmap


def find_last_conv_layer(model):
    """
    Automatically find the last convolutional layer in the model.
    
    Args:
        model: Keras model
    
    Returns:
        layer_name: Name of the last convolutional layer
    """
    for layer in reversed(model.layers):
        if len(layer.output_shape) == 4:  # Conv layers have 4D output
            return layer.name
    raise ValueError("Could not find a convolutional layer in the model")


# Example usage
if __name__ == "__main__":
    # Load model
    model = keras.models.load_model('models/final_model.keras')
    
    # Load and preprocess image
    from tensorflow.keras.preprocessing import image
    img_path = 'path/to/xray.jpg'
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    # Generate Grad-CAM
    last_conv_layer = find_last_conv_layer(model)
    overlayed, heatmap = generate_gradcam_visualization(
        model, img_array, np.array(img), last_conv_layer
    )
    
    # Save or display
    import matplotlib.pyplot as plt
    plt.imshow(overlayed)
    plt.axis('off')
    plt.title('Grad-CAM Visualization')
    plt.savefig('gradcam_output.png', bbox_inches='tight', dpi=150)
    plt.show()
