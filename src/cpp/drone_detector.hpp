/**
 * @file drone_detector.hpp
 * @brief Drone detection using OpenCV DNN module in C++
 * @details Optimized for Raspberry Pi 5 counter-UAS system
 */

#ifndef DRONE_DETECTOR_HPP
#define DRONE_DETECTOR_HPP

#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <string>
#include <vector>

namespace csuas {

/**
 * @struct Detection
 * @brief Represents a single drone detection
 */
struct Detection {
    cv::Rect bbox;          ///< Bounding box
    float confidence;       ///< Detection confidence
    int class_id;          ///< Class ID (0 for drone)
    
    Detection(const cv::Rect& box, float conf, int cls = 0)
        : bbox(box), confidence(conf), class_id(cls) {}
};

/**
 * @class DroneDetector
 * @brief Main class for drone detection using YOLO models
 */
class DroneDetector {
public:
    /**
     * @brief Constructor
     * @param model_path Path to the model file (.onnx, .weights, etc.)
     * @param config_path Path to config file (for Darknet models)
     * @param confidence_threshold Minimum confidence for detections
     * @param nms_threshold Non-maximum suppression threshold
     */
    DroneDetector(const std::string& model_path,
                  const std::string& config_path = "",
                  float confidence_threshold = 0.5f,
                  float nms_threshold = 0.4f);
    
    /**
     * @brief Destructor
     */
    ~DroneDetector() = default;
    
    /**
     * @brief Detect drones in an image
     * @param image Input image (BGR format)
     * @return Vector of detections
     */
    std::vector<Detection> detect(const cv::Mat& image);
    
    /**
     * @brief Draw detections on image
     * @param image Input/output image
     * @param detections Vector of detections to draw
     */
    void drawDetections(cv::Mat& image, const std::vector<Detection>& detections);
    
    /**
     * @brief Set confidence threshold
     * @param threshold New confidence threshold
     */
    void setConfidenceThreshold(float threshold);
    
    /**
     * @brief Set NMS threshold
     * @param threshold New NMS threshold
     */
    void setNMSThreshold(float threshold);
    
    /**
     * @brief Check if model is loaded
     * @return True if model is loaded successfully
     */
    bool isModelLoaded() const;

private:
    /**
     * @brief Load the YOLO model
     */
    void loadModel();
    
    /**
     * @brief Post-process network outputs
     * @param outputs Network outputs
     * @param image_size Size of input image
     * @return Vector of detections
     */
    std::vector<Detection> postProcess(const std::vector<cv::Mat>& outputs,
                                       const cv::Size& image_size);

    cv::dnn::Net net_;                  ///< Neural network
    std::string model_path_;            ///< Path to model file
    std::string config_path_;           ///< Path to config file
    float confidence_threshold_;        ///< Confidence threshold
    float nms_threshold_;               ///< NMS threshold
    std::vector<std::string> output_layer_names_;  ///< Output layer names
    bool model_loaded_;                 ///< Model load status
    
    static constexpr int INPUT_WIDTH = 416;   ///< Model input width
    static constexpr int INPUT_HEIGHT = 416;  ///< Model input height
};

} // namespace csuas

#endif // DRONE_DETECTOR_HPP
