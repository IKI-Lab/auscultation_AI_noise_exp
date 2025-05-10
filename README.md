# Not a Matter of Trust: Increasing Complexity Drives Physician’s Reliance on Artificial Intelligence

This project is designed to conduct experiments for the paper **Not a Matter of Trust: Increasing Complexity Drives Physician’s Reliance on Artificial Intelligence**. It uses PyQt5 for the graphical user interface (GUI) to guide participants through the experiment.

## Project Structure

The project is organized as follows:\
├── app.py # Main entry point for the application\
├── experiment.py # Defines the Experiment class and trial dataset generation\
├── trial.py # Handles trial logic and GUI components\
├── PostTrial.py # Manages post-trial questions and forms\
├── instructions1.py # Contains instructional screens for participants\
├── welcome.py # Welcome screen and initial dialogs\
├── forms/ # Directory containing .ui files for GUI forms\
├── stimuli/ # Directory containing stimuli (audio, video, etc.)\
├── matrix16.csv # Full matrix for trial sequences\
├── seq_matrix.csv # Sequence matrix for trials\
├── trials.csv # Main trial data\
├── trials_test.csv # Test trial data\
├── requirements.txt # Python dependencies\
└── README.md

### Key Files

- **`app.py`**: Initializes the application and manages the main window and navigation between screens.
- **`experiment.py`**: Defines the `Experiment` class, which handles trial data, group assignments, and trial sequences.
- **`trial.py`**: Implements the `Trial` class, which manages the trial flow, including audio/video playback, classification, and confidence measurement.
- **`PostTrial.py`**: Contains classes for post-trial questions and feedback forms.
- **`instructions1.py`**: Provides instructional screens for guiding participants through the experiment.
- **`forms/`**: Contains `.ui` files for GUI components.
- **`stimuli/`**: Stores audio and video stimuli used during the trials.

## Setup

To set up and run the experiment, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd auscultation_AI_noise_exp
   ```
2. **Install dependencies**: Ensure you have Python 3.13 installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Create folder `files`**
4. **Run `app.py`**