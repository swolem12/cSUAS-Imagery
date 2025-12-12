/**
 * @file main.cpp
 * @brief Main application for drone detection
 */

#include "drone_detector.hpp"
#include <iostream>
#include <string>

void printUsage(const char* program_name) {
    std::cout << "Usage: " << program_name << " [options]\n"
              << "Options:\n"
              << "  --model PATH        Path to model file (required)\n"
              << "  --config PATH       Path to config file (for Darknet models)\n"
              << "  --source PATH       Video source (0 for webcam, or path to video)\n"
              << "  --confidence FLOAT  Confidence threshold (default: 0.5)\n"
              << "  --nms FLOAT         NMS threshold (default: 0.4)\n"
              << "  --output PATH       Output video path (optional)\n"
              << "  --help              Show this help message\n";
}

int main(int argc, char** argv) {
    std::string model_path;
    std::string config_path;
    std::string source = "0";
    std::string output_path;
    float confidence = 0.5f;
    float nms = 0.4f;
    
    // Parse command line arguments
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        
        if (arg == "--help") {
            printUsage(argv[0]);
            return 0;
        }
        else if (arg == "--model" && i + 1 < argc) {
            model_path = argv[++i];
        }
        else if (arg == "--config" && i + 1 < argc) {
            config_path = argv[++i];
        }
        else if (arg == "--source" && i + 1 < argc) {
            source = argv[++i];
        }
        else if (arg == "--confidence" && i + 1 < argc) {
            confidence = std::stof(argv[++i]);
        }
        else if (arg == "--nms" && i + 1 < argc) {
            nms = std::stof(argv[++i]);
        }
        else if (arg == "--output" && i + 1 < argc) {
            output_path = argv[++i];
        }
    }
    
    // Validate required arguments
    if (model_path.empty()) {
        std::cerr << "Error: Model path is required\n";
        printUsage(argv[0]);
        return 1;
    }
    
    // Initialize detector
    std::cout << "Initializing drone detector...\n";
    csuas::DroneDetector detector(model_path, config_path, confidence, nms);
    
    if (!detector.isModelLoaded()) {
        std::cerr << "Error: Failed to load model\n";
        return 1;
    }
    
    // Open video source
    cv::VideoCapture cap;
    if (source == "0") {
        cap.open(0);
    } else {
        cap.open(source);
    }
    
    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open video source: " << source << "\n";
        return 1;
    }
    
    // Setup video writer if output specified
    cv::VideoWriter writer;
    if (!output_path.empty()) {
        int fourcc = cv::VideoWriter::fourcc('m', 'p', '4', 'v');
        double fps = cap.get(cv::CAP_PROP_FPS);
        int width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
        int height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
        writer.open(output_path, fourcc, fps, cv::Size(width, height));
        
        if (!writer.isOpened()) {
            std::cerr << "Warning: Could not open output video file\n";
        }
    }
    
    std::cout << "Starting detection... Press 'q' to quit\n";
    
    cv::Mat frame;
    while (true) {
        cap >> frame;
        if (frame.empty()) {
            break;
        }
        
        // Detect drones
        std::vector<csuas::Detection> detections = detector.detect(frame);
        
        // Draw detections
        detector.drawDetections(frame, detections);
        
        // Write to output if specified
        if (writer.isOpened()) {
            writer.write(frame);
        }
        
        // Display frame
        cv::imshow("Drone Detection", frame);
        
        // Check for quit
        if (cv::waitKey(1) == 'q') {
            break;
        }
    }
    
    // Cleanup
    cap.release();
    if (writer.isOpened()) {
        writer.release();
    }
    cv::destroyAllWindows();
    
    std::cout << "Detection stopped\n";
    return 0;
}
