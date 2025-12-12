/**
 * @file drone_detector.cpp
 * @brief Implementation of DroneDetector class
 */

#include "drone_detector.hpp"
#include <iostream>
#include <fstream>

namespace csuas {

DroneDetector::DroneDetector(const std::string& model_path,
                             const std::string& config_path,
                             float confidence_threshold,
                             float nms_threshold)
    : model_path_(model_path)
    , config_path_(config_path)
    , confidence_threshold_(confidence_threshold)
    , nms_threshold_(nms_threshold)
    , model_loaded_(false) {
    
    loadModel();
}

void DroneDetector::loadModel() {
    try {
        // Check if model file exists
        std::ifstream model_file(model_path_);
        if (!model_file.good()) {
            std::cerr << "Error: Model file not found at " << model_path_ << std::endl;
            return;
        }
        
        // Determine model type and load accordingly
        if (model_path_.substr(model_path_.find_last_of(".") + 1) == "onnx") {
            net_ = cv::dnn::readNetFromONNX(model_path_);
            std::cout << "Loaded ONNX model from " << model_path_ << std::endl;
        }
        else if (model_path_.substr(model_path_.find_last_of(".") + 1) == "weights") {
            if (config_path_.empty()) {
                std::cerr << "Error: Config file required for Darknet weights" << std::endl;
                return;
            }
            net_ = cv::dnn::readNetFromDarknet(config_path_, model_path_);
            std::cout << "Loaded Darknet model from " << model_path_ << std::endl;
        }
        else {
            std::cerr << "Error: Unsupported model format" << std::endl;
            return;
        }
        
        // Set backend and target for Raspberry Pi
        net_.setPreferableBackend(cv::dnn::DNN_BACKEND_OPENCV);
        net_.setPreferableTarget(cv::dnn::DNN_TARGET_CPU);
        
        // Get output layer names
        std::vector<int> out_layers = net_.getUnconnectedOutLayers();
        std::vector<std::string> layer_names = net_.getLayerNames();
        
        output_layer_names_.resize(out_layers.size());
        for (size_t i = 0; i < out_layers.size(); ++i) {
            output_layer_names_[i] = layer_names[out_layers[i] - 1];
        }
        
        model_loaded_ = true;
        std::cout << "Model loaded successfully" << std::endl;
        
    } catch (const cv::Exception& e) {
        std::cerr << "Error loading model: " << e.what() << std::endl;
        model_loaded_ = false;
    }
}

std::vector<Detection> DroneDetector::detect(const cv::Mat& image) {
    if (!model_loaded_) {
        std::cerr << "Error: Model not loaded" << std::endl;
        return std::vector<Detection>();
    }
    
    // Create blob from image
    cv::Mat blob;
    cv::dnn::blobFromImage(image, blob, 1.0/255.0, 
                          cv::Size(INPUT_WIDTH, INPUT_HEIGHT),
                          cv::Scalar(0, 0, 0), true, false);
    
    // Set input
    net_.setInput(blob);
    
    // Forward pass
    std::vector<cv::Mat> outputs;
    net_.forward(outputs, output_layer_names_);
    
    // Post-process outputs
    return postProcess(outputs, image.size());
}

std::vector<Detection> DroneDetector::postProcess(const std::vector<cv::Mat>& outputs,
                                                  const cv::Size& image_size) {
    std::vector<cv::Rect> boxes;
    std::vector<float> confidences;
    std::vector<int> class_ids;
    
    // Process each output
    for (const auto& output : outputs) {
        for (int i = 0; i < output.rows; ++i) {
            const float* data = output.ptr<float>(i);
            
            // Extract confidence
            float confidence = data[4];
            
            if (confidence > confidence_threshold_) {
                // Get class scores
                cv::Mat scores = output.row(i).colRange(5, output.cols);
                cv::Point class_id_point;
                double max_class_score;
                cv::minMaxLoc(scores, nullptr, &max_class_score, nullptr, &class_id_point);
                
                // Use class score as confidence if available
                if (scores.cols > 0) {
                    confidence = static_cast<float>(max_class_score);
                }
                
                if (confidence > confidence_threshold_) {
                    // Get bounding box
                    int center_x = static_cast<int>(data[0] * image_size.width);
                    int center_y = static_cast<int>(data[1] * image_size.height);
                    int width = static_cast<int>(data[2] * image_size.width);
                    int height = static_cast<int>(data[3] * image_size.height);
                    
                    int left = center_x - width / 2;
                    int top = center_y - height / 2;
                    
                    boxes.push_back(cv::Rect(left, top, width, height));
                    confidences.push_back(confidence);
                    class_ids.push_back(class_id_point.x);
                }
            }
        }
    }
    
    // Apply Non-Maximum Suppression
    std::vector<int> indices;
    cv::dnn::NMSBoxes(boxes, confidences, confidence_threshold_, nms_threshold_, indices);
    
    // Create detection objects
    std::vector<Detection> detections;
    for (int idx : indices) {
        detections.emplace_back(boxes[idx], confidences[idx], class_ids[idx]);
    }
    
    return detections;
}

void DroneDetector::drawDetections(cv::Mat& image, const std::vector<Detection>& detections) {
    for (const auto& det : detections) {
        // Draw bounding box
        cv::rectangle(image, det.bbox, cv::Scalar(0, 255, 0), 2);
        
        // Create label
        std::string label = "Drone: " + std::to_string(static_cast<int>(det.confidence * 100)) + "%";
        
        // Get text size
        int baseline;
        cv::Size text_size = cv::getTextSize(label, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseline);
        
        // Draw label background
        cv::rectangle(image, 
                     cv::Point(det.bbox.x, det.bbox.y - text_size.height - 10),
                     cv::Point(det.bbox.x + text_size.width, det.bbox.y),
                     cv::Scalar(0, 255, 0), -1);
        
        // Draw label text
        cv::putText(image, label, 
                   cv::Point(det.bbox.x, det.bbox.y - 5),
                   cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0), 1);
    }
    
    // Draw detection count
    std::string count_text = "Drones: " + std::to_string(detections.size());
    cv::putText(image, count_text, cv::Point(10, 30),
               cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(0, 0, 255), 2);
}

void DroneDetector::setConfidenceThreshold(float threshold) {
    confidence_threshold_ = threshold;
}

void DroneDetector::setNMSThreshold(float threshold) {
    nms_threshold_ = threshold;
}

bool DroneDetector::isModelLoaded() const {
    return model_loaded_;
}

} // namespace csuas
