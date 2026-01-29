# Deployment Guide

This guide provides instructions for deploying the Pneumonia Diagnosis AI model in clinical settings.

## ⚠️ Important Disclaimer

**This model is currently for research and educational purposes only.** 

Before clinical deployment:
- Obtain necessary regulatory approvals (FDA 510(k), CE marking, etc.)
- Conduct prospective clinical validation studies
- Ensure compliance with local healthcare regulations (HIPAA, GDPR, etc.)
- Establish clear protocols for human oversight

## Deployment Checklist

### Pre-Deployment Requirements

- [ ] **Clinical Validation**
  - [ ] Validation by board-certified radiologists
  - [ ] Testing on diverse patient populations
  - [ ] Performance evaluation on prospective data
  - [ ] Inter-rater reliability assessment

- [ ] **Regulatory Compliance**
  - [ ] FDA clearance (US) or equivalent
  - [ ] CE marking (EU) if applicable
  - [ ] Local healthcare authority approval
  - [ ] Medical device classification

- [ ] **Technical Validation**
  - [ ] Model performance metrics documented
  - [ ] Bias and fairness assessment
  - [ ] Robustness testing (various image qualities)
  - [ ] Failure mode analysis

- [ ] **Infrastructure**
  - [ ] PACS system integration tested
  - [ ] DICOM compatibility verified
  - [ ] Network security assessment
  - [ ] Backup and disaster recovery plan

- [ ] **Documentation**
  - [ ] User manual for clinicians
  - [ ] Technical documentation
  - [ ] Standard Operating Procedures (SOPs)
  - [ ] Incident reporting procedures

- [ ] **Training**
  - [ ] Staff training on AI system usage
  - [ ] Understanding of model limitations
  - [ ] Interpretation of Grad-CAM visualizations
  - [ ] Escalation protocols

## Deployment Options

### Option 1: On-Premise Deployment

Deploy the model on hospital servers.

**Pros:**
- Complete data control
- Low latency
- No internet dependency

**Cons:**
- Requires IT infrastructure
- Maintenance overhead
- Higher upfront costs

**Setup:**
1. Install dependencies on server
2. Load model and weights
3. Set up API endpoint
4. Integrate with PACS
5. Configure monitoring

### Option 2: Cloud Deployment

Deploy on AWS, Azure, or Google Cloud.

**Pros:**
- Scalable
- Managed infrastructure
- Automatic updates possible

**Cons:**
- Data privacy concerns
- Ongoing costs
- Internet dependency

**Setup:**
1. Choose cloud provider
2. Set up secure VM or container
3. Configure HIPAA-compliant storage
4. Implement encryption in transit/at rest
5. Set up monitoring and logging

### Option 3: Hybrid Deployment

Edge processing with cloud backup.

**Pros:**
- Balance of control and scalability
- Redundancy
- Flexible architecture

**Cons:**
- More complex setup
- Higher maintenance

## Integration with PACS

### DICOM Integration

```python
import pydicom
from src.predict import load_model_and_metadata, predict_single_image

def process_dicom_study(dicom_path):
    """Process DICOM study for pneumonia detection."""
    # Read DICOM
    ds = pydicom.dcmread(dicom_path)
    
    # Extract pixel data
    pixel_array = ds.pixel_array
    
    # Normalize and preprocess
    # ... preprocessing steps ...
    
    # Run inference
    model, metadata, class_names = load_model_and_metadata(...)
    prediction = predict_single_image(model, img_array, class_names)
    
    # Attach to DICOM as structured report
    # ... DICOM SR creation ...
    
    return prediction
```

### HL7 Integration

For integration with hospital information systems:

```python
def send_hl7_message(patient_id, prediction, confidence):
    """Send prediction via HL7 message."""
    message = f"""
    MSH|^~\\&|AI_SYSTEM|HOSPITAL|HIS|HOSPITAL|{timestamp}||ORU^R01|{msg_id}|P|2.5
    PID|||{patient_id}
    OBR|1||{accession}|CHEST_XRAY
    OBX|1|ST|PNEUMONIA_DETECTION||{prediction}||||||F
    OBX|2|NM|CONFIDENCE||{confidence}||||||F
    """
    # Send via MLLP
    # ... implementation ...
```

## API Deployment

### REST API Example

```python
from flask import Flask, request, jsonify
from src.predict import load_model_and_metadata, predict_single_image

app = Flask(__name__)

# Load model once at startup
model, metadata, class_names = load_model_and_metadata(
    'models/final_model.keras',
    'deployment/model_metadata.json',
    'deployment/class_indices.json'
)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for predictions."""
    try:
        # Get image from request
        file = request.files['image']
        img = Image.open(file.stream)
        
        # Preprocess
        img_array, _ = preprocess_image(img)
        
        # Predict
        prediction = predict_single_image(model, img_array, class_names)
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "api.py"]
```

Build and run:
```bash
docker build -t pneumonia-ai .
docker run -p 5000:5000 pneumonia-ai
```

## Monitoring and Maintenance

### Performance Monitoring

Track these metrics:
- **Prediction latency**: Time per inference
- **Throughput**: Predictions per hour
- **Model accuracy**: On validation set
- **System uptime**: Availability percentage
- **Error rates**: Failed predictions

### Model Drift Detection

```python
import numpy as np
from scipy import stats

def detect_drift(recent_predictions, baseline_predictions, threshold=0.05):
    """Detect if model predictions have drifted."""
    # Kolmogorov-Smirnov test
    statistic, p_value = stats.ks_2samp(
        recent_predictions,
        baseline_predictions
    )
    
    if p_value < threshold:
        return True, f"Drift detected (p={p_value:.4f})"
    return False, "No significant drift"
```

### Logging

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='logs/predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_prediction(patient_id, prediction, confidence):
    """Log each prediction for audit trail."""
    logging.info(f"Patient: {patient_id} | Prediction: {prediction} | Confidence: {confidence:.2%}")
```

## Clinical Workflow Integration

### Triage Workflow

```
1. X-ray acquired → PACS
2. PACS triggers AI analysis
3. AI returns prediction + Grad-CAM
4. Results displayed to radiologist
5. Radiologist reviews and confirms/overrides
6. Final diagnosis recorded
```

### Alert System

```python
def check_urgent_case(prediction, confidence, threshold=0.9):
    """Alert for high-confidence pneumonia cases."""
    if prediction == "PNEUMONIA" and confidence > threshold:
        send_alert(
            priority="HIGH",
            message=f"High-confidence pneumonia detected ({confidence:.1%})",
            recipient="on-call-radiologist"
        )
```

## Security Considerations

### Data Privacy

- Encrypt data in transit (TLS/SSL)
- Encrypt data at rest
- De-identify patient information
- Implement access controls
- Maintain audit logs

### HIPAA Compliance

- Business Associate Agreement (BAA)
- Technical safeguards
- Physical safeguards
- Administrative safeguards
- Regular security assessments

### Model Security

- Protect model weights from extraction
- Implement input validation
- Rate limiting on API
- Monitor for adversarial attacks

## Backup and Recovery

### Model Versioning

```python
# Save with version tag
model.save(f'models/model_v{version}_{timestamp}.keras')

# Keep metadata
metadata = {
    'version': version,
    'timestamp': timestamp,
    'performance': metrics,
    'training_data': data_info
}
```

### Disaster Recovery

1. Regular backups of:
   - Model files
   - Configuration
   - Logs
   - Metadata

2. Recovery plan:
   - Restore from backup
   - Verify model integrity
   - Test predictions
   - Resume service

## User Training

### For Radiologists

- Understanding AI predictions
- Interpreting Grad-CAM visualizations
- When to trust/override AI
- Reporting issues

### For IT Staff

- System monitoring
- Troubleshooting
- Performance optimization
- Security updates

## Regulatory Documentation

Maintain these documents:

1. **Design History File (DHF)**
   - Design requirements
   - Verification and validation
   - Risk analysis

2. **Device Master Record (DMR)**
   - Device specifications
   - Manufacturing process
   - Quality assurance procedures

3. **Device History Record (DHR)**
   - Production records
   - Testing results
   - Release documentation

## Performance Thresholds

Set clinical thresholds based on use case:

| Use Case | Sensitivity | Specificity | PPV | NPV |
|----------|------------|-------------|-----|-----|
| Screening | >95% | >80% | TBD | >99% |
| Triage | >90% | >85% | TBD | >95% |
| Second Opinion | >85% | >90% | TBD | >90% |

## Continuous Improvement

1. **Regular Retraining**
   - Collect new annotated data
   - Retrain every 6-12 months
   - Validate on prospective data

2. **Performance Review**
   - Quarterly performance reports
   - Compare AI vs radiologist agreement
   - Identify failure modes

3. **User Feedback**
   - Collect radiologist feedback
   - Track overrides and reasons
   - Improve model based on feedback

## Support and Maintenance

### Service Level Agreement (SLA)

- **Uptime**: 99.9%
- **Response time**: <100ms per prediction
- **Support response**: <4 hours for critical issues

### Maintenance Schedule

- Daily: Automated health checks
- Weekly: Review logs and metrics
- Monthly: Performance reports
- Quarterly: Security audits
- Annually: Model retraining

## Contact for Deployment Support

For deployment assistance:
- Technical: tech@example.com
- Clinical: clinical@example.com
- Regulatory: regulatory@example.com

---

**Remember**: This is a medical AI system. Patient safety is paramount. Always maintain human oversight and follow established medical protocols.
